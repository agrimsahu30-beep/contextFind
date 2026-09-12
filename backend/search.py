import json
import math
import os
import re

# pyrefly: ignore [missing-import]
import faiss

# pyrefly: ignore [missing-import]
import numpy as np

# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer

from backend.query_parser import (
    parse_query,
    DECISION_KEYWORDS,
)


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
TOKEN_PATTERN = re.compile(r"\b\w+\b", re.UNICODE)
STOPWORDS = {
    "a", "an", "and", "are", "at", "did", "do", "for", "how", "i",
    "in", "is", "it", "of", "on", "the", "to", "was", "we", "what",
    "when", "where", "who", "with", "you",
}


class SearchEngine:

    def __init__(self, data_dir=None, index_dir=None):

        base_dir = os.path.dirname(__file__)

        self.data_dir = data_dir or os.path.join(base_dir, "data")
        self.index_dir = index_dir or os.path.join(base_dir, "index")

        messages_path = os.path.join(
            self.data_dir,
            "messages.json"
        )

        faiss_path = os.path.join(
            self.index_dir,
            "messages.faiss"
        )

        id_map_path = os.path.join(
            self.index_dir,
            "id_map.json"
        )

        if not (
            os.path.exists(messages_path)
            and os.path.exists(faiss_path)
            and os.path.exists(id_map_path)
        ):
            raise FileNotFoundError(
                "Index or dataset files missing. "
                "Please run generator.py and indexer.py first."
            )

        # -----------------------------
        # Load messages
        # -----------------------------

        with open(
            messages_path,
            "r",
            encoding="utf-8"
        ) as f:

            self.messages = json.load(f)

        self.msg_dict = {
            m["id"]: m
            for m in self.messages
        }

        self.msg_index_map = {
            m["id"]: i
            for i, m in enumerate(self.messages)
        }

        # -----------------------------
        # Load FAISS
        # -----------------------------

        self.faiss_index = faiss.read_index(
            faiss_path
        )

        with open(
            id_map_path,
            "r",
            encoding="utf-8"
        ) as f:

            self.id_map = {
                int(k): v
                for k, v in json.load(f).items()
            }

        self.row_by_message_id = {
            message_id: row
            for row, message_id in self.id_map.items()
        }
        self.thread_messages = {}
        for message in self.messages:
            self.thread_messages.setdefault(message["thread_id"], []).append(message)
        for messages in self.thread_messages.values():
            messages.sort(key=lambda message: message["timestamp"])

        thread_index_path = os.path.join(self.index_dir, "threads.faiss")
        thread_map_path = os.path.join(self.index_dir, "thread_map.json")
        self.thread_index = None
        self.thread_id_map = {}
        if os.path.exists(thread_index_path) and os.path.exists(thread_map_path):
            self.thread_index = faiss.read_index(thread_index_path)
            with open(thread_map_path, "r", encoding="utf-8") as f:
                self.thread_id_map = {
                    int(row): thread_id
                    for row, thread_id in json.load(f).items()
                }

        self._message_tokens = {
            message["id"]: self._tokenize(message["text"])
            for message in self.messages
        }
        self._document_frequency = {}
        for tokens in self._message_tokens.values():
            for token in set(tokens):
                self._document_frequency[token] = (
                    self._document_frequency.get(token, 0) + 1
                )
        self._average_document_length = sum(
            len(tokens) for tokens in self._message_tokens.values()
        ) / len(self.messages)

        # -----------------------------
        # Load embedding model
        # -----------------------------

        self.model = SentenceTransformer(
            MODEL_NAME
        )

    # ============================================================
    # KEYWORD SCORE
    # ============================================================

    @staticmethod
    def _tokenize(text: str):
        return [
            token
            for token in TOKEN_PATTERN.findall(text.lower())
            if token not in STOPWORDS
        ]

    def _compute_keyword_score(
        self,
        query: str,
        text: str
    ) -> float:

        q_tokens = set(self._tokenize(query))
        t_tokens = self._tokenize(text)

        if not q_tokens or not t_tokens:
            return 0.0

        document_length = len(t_tokens)
        score = 0.0
        for token in q_tokens:
            frequency = t_tokens.count(token)
            if not frequency:
                continue
            document_frequency = self._document_frequency.get(token, 0)
            idf = math.log(
                1 + (len(self.messages) - document_frequency + 0.5)
                / (document_frequency + 0.5)
            )
            denominator = frequency + 1.5 * (
                1 - 0.75 + 0.75 * document_length / self._average_document_length
            )
            score += idf * frequency * 2.5 / denominator

        return score / (score + 1.5) if score else 0.0

    # ============================================================
    # DECISION SCORE
    # ============================================================

    def _compute_decision_score(
        self,
        text: str
    ) -> float:

        text_lower = text.lower()

        matches = [
            keyword
            for keyword in DECISION_KEYWORDS
            if keyword in text_lower
        ]

        if not matches:
            return 0.0

        # Saturating score.
        return min(
            1.0,
            0.4 + (0.2 * len(matches))
        )

    @staticmethod
    def _reciprocal_rank_fusion(*rankings, constant=60):
        scores = {}
        for ranking in rankings:
            for rank, row in enumerate(ranking, start=1):
                scores[row] = scores.get(row, 0.0) + 1.0 / (constant + rank)
        max_score = max(scores.values(), default=1.0)
        return {row: score / max_score for row, score in scores.items()}

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        query: str,
        mode: str = "hybrid",
        top_k: int = 10
    ):

        query_analysis = parse_query(
            query
        )

        q_intent = query_analysis[
            "intent"
        ]

        q_person = query_analysis[
            "person"
        ]

        q_time = query_analysis[
            "time_range"
        ]

        # ========================================================
        # KEYWORD MODE
        # ========================================================

        if mode == "keyword":

            scored_candidates = []

            for message in self.messages:

                score = self._compute_keyword_score(
                    query,
                    message["text"]
                )

                if score > 0:

                    scored_candidates.append(
                        (
                            score,
                            message["id"],
                            score,
                            0.0,
                            0.0,
                            0.0,
                            0.0
                        )
                    )

            scored_candidates.sort(
                key=lambda x: x[0],
                reverse=True
            )

            top_candidates = (
                scored_candidates[:top_k]
            )

        # ========================================================
        # SEMANTIC / HYBRID
        # ========================================================

        else:

            # ---------------------------------------------
            # Encode query
            # ---------------------------------------------

            query_vec = self.model.encode(
                [query],
                normalize_embeddings=True
            )

            query_vec = np.asarray(
                query_vec,
                dtype=np.float32
            )

            # ---------------------------------------------
            # Retrieve larger candidate pool
            # ---------------------------------------------

            candidate_k = min(
                500,
                len(self.messages)
            )

            similarities, faiss_indices = (
                self.faiss_index.search(
                    query_vec,
                    candidate_k
                )
            )

            similarity_by_row = {
                int(row): float(similarity)
                for similarity, row in zip(similarities[0], faiss_indices[0])
                if row >= 0
            }
            semantic_ranking = [int(row) for row in faiss_indices[0] if row >= 0]
            candidate_rows = set(similarity_by_row)
            thread_semantic_scores = {}
            for row, similarity in similarity_by_row.items():
                message = self.msg_dict[self.id_map[row]]
                thread_id = message["thread_id"]
                thread_semantic_scores[thread_id] = max(
                    thread_semantic_scores.get(thread_id, 0.0),
                    max(0.0, similarity),
                )

            # Semantic retrieval alone can be crowded out by repeated short
            # messages. Add lexical, temporal, and decision candidates before
            # reranking; this does not encode any query-to-answer mapping.
            keyword_rows = sorted(
                (
                    (self._compute_keyword_score(query, message["text"]), message["id"])
                    for message in self.messages
                ),
                reverse=True,
            )[:candidate_k]
            keyword_ranking = [
                self.row_by_message_id[message_id]
                for score, message_id in keyword_rows
                if score > 0
            ]
            rrf_scores = self._reciprocal_rank_fusion(
                semantic_ranking,
                keyword_ranking,
            )
            candidate_rows.update(
                self.row_by_message_id[message_id]
                for score, message_id in keyword_rows
                if score > 0
            )

            thread_query_scores = {}
            if self.thread_index is not None:
                thread_similarities, thread_rows = self.thread_index.search(
                    query_vec,
                    min(10, self.thread_index.ntotal),
                )
                thread_query_scores = {
                    self.thread_id_map[int(row)]: max(0.0, float(similarity))
                    for similarity, row in zip(thread_similarities[0], thread_rows[0])
                    if row >= 0
                }
                for thread_id in thread_query_scores:
                    candidate_rows.update(
                        self.row_by_message_id[message["id"]]
                        for message in self.thread_messages[thread_id]
                    )

            if q_time:
                candidate_rows.update(
                    self.row_by_message_id[message["id"]]
                    for message in self.messages
                    if q_time["start"] <= message["timestamp"] <= q_time["end"]
                )

            if q_intent == "decision":
                candidate_rows.update(
                    self.row_by_message_id[message["id"]]
                    for message in self.messages
                    if self._compute_decision_score(message["text"]) > 0
                )

            scored_candidates = []

            # =================================================
            # Candidate processing
            # =================================================

            for faiss_row in candidate_rows:

                if faiss_row not in self.id_map:
                    continue

                message_id = self.id_map[
                    faiss_row
                ]

                message = self.msg_dict[
                    message_id
                ]

                similarity = similarity_by_row.get(faiss_row)
                if similarity is None:
                    vector = self.faiss_index.reconstruct(faiss_row)
                    similarity = float(np.dot(query_vec[0], vector))

                semantic_score = max(0.0, similarity)
                lexical_score = self._compute_keyword_score(query, message["text"])
                fusion_score = rrf_scores.get(faiss_row, 0.0)

                # =============================================
                # Semantic-only mode
                # =============================================

                if mode == "semantic":

                    scored_candidates.append(
                        (
                            semantic_score,
                            message_id,
                            semantic_score,
                            0.0,
                            0.0,
                            0.0,
                            0.0
                        )
                    )

                    continue

                # =============================================
                # TEMPORAL FILTER
                # =============================================

                temporal_score = 0.0

                if q_time:

                    timestamp = message[
                        "timestamp"
                    ]

                    inside_range = (
                        q_time["start"]
                        <= timestamp
                        <= q_time["end"]
                    )

                    if not inside_range:
                        # Explicit dates are constraints even when the query
                        # also contains a person or decision signal.
                        continue

                    else:

                        temporal_score = 1.0

                # =============================================
                # PERSON SCORE
                # =============================================

                person_score = 0.0

                if q_person:

                    if (
                        message["sender"].lower()
                        == q_person.lower()
                    ):

                        person_score = 1.0

                # =============================================
                # DECISION SCORE
                # =============================================

                decision_score = 0.0

                # IMPORTANT:
                # Decision language only matters when
                # the user is actually asking a decision query.

                if q_intent == "decision":

                    decision_score = (
                        self._compute_decision_score(
                            message["text"]
                        )
                    )

                thread_support_score = 0.0
                if q_intent == "decision" and decision_score > 0:
                    thread_support_score = thread_semantic_scores.get(
                        message["thread_id"],
                        0.0,
                    )

                # =============================================
                # CONTEXT SCORE
                # =============================================

                # Keep this small for now.
                #
                # A thread existing by itself is not evidence
                # of relevance.

                context_score = max(
                    thread_support_score,
                    thread_query_scores.get(message["thread_id"], 0.0),
                )

                # =============================================
                # FINAL SCORE
                # =============================================

                final_score = (
                    0.50 * max(
                        semantic_score,
                        lexical_score,
                        0.95 * thread_support_score,
                    )
                    + 0.15 * fusion_score
                    + 0.15 * person_score
                    + 0.10 * temporal_score
                    + 0.10 * decision_score
                    + 0.10 * context_score
                )

                scored_candidates.append(
                    (
                        final_score,
                        message_id,
                        max(
                            semantic_score,
                            lexical_score,
                            0.95 * thread_support_score,
                        ),
                        person_score,
                        temporal_score,
                        decision_score,
                        context_score
                    )
                )

            # =============================================
            # Sort
            # =============================================

            scored_candidates.sort(
                key=lambda x: x[0],
                reverse=True
            )

            top_candidates = (
                scored_candidates[:top_k]
            )

        # ========================================================
        # BUILD RESULTS
        # ========================================================

        results = []

        for rank, item in enumerate(
            top_candidates,
            start=1
        ):

            (
                final_score,
                message_id,
                semantic_score,
                person_score,
                temporal_score,
                decision_score,
                context_score
            ) = item

            message = self.msg_dict[
                message_id
            ]

            # =============================================
            # WHY THIS MATCHED
            # =============================================

            reasons = []

            if semantic_score >= 0.40:

                reasons.append(
                    "High semantic similarity"
                )

            if person_score > 0:

                reasons.append(
                    f"Sender matches {q_person}"
                )

            if temporal_score > 0:

                reasons.append(
                    "Within requested date range"
                )

            if decision_score > 0:

                reasons.append(
                    "Decision language detected"
                )

            if not reasons:

                reasons.append(
                    "Candidate match"
                )

            # =============================================
            # CONTEXT
            # =============================================

            index = self.msg_index_map[
                message_id
            ]

            thread_messages = self.thread_messages[message["thread_id"]]
            thread_index = next(
                i for i, context_message in enumerate(thread_messages)
                if context_message["id"] == message_id
            )
            raw_context = thread_messages[
                max(0, thread_index - 2):thread_index + 3
            ]

            context = []

            for context_message in raw_context:

                context.append(
                    {
                        "id": context_message["id"],
                        "sender": context_message["sender"],
                        "text": context_message["text"],
                        "timestamp": context_message["timestamp"],
                        "thread_id": context_message["thread_id"],
                        "is_target": (
                            context_message["id"]
                            == message_id
                        )
                    }
                )

            # =============================================
            # RESULT
            # =============================================

            results.append(
                {
                    "rank": rank,

                    "message_id": message["id"],

                    "sender": message["sender"],

                    "timestamp": message["timestamp"],

                    "text": message["text"],

                    "score": round(
                        final_score,
                        4
                    ),

                    "score_breakdown": {
                        "semantic": round(
                            semantic_score,
                            4
                        ),

                        "person": round(
                            person_score,
                            4
                        ),

                        "temporal": round(
                            temporal_score,
                            4
                        ),

                        "decision": round(
                            decision_score,
                            4
                        ),

                        "context": round(
                            context_score,
                            4
                        )
                    },

                    "reasons": reasons,

                    "context": context
                }
            )

        return {
            "query": query,

            "mode": mode,

            "query_analysis": query_analysis,

            "results": results
        }
