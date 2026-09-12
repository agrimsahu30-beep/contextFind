import json
import os
from backend.search import SearchEngine

def run_evaluation():
    base_dir = os.path.dirname(__file__)
    queries_path = os.path.join(base_dir, "data", "queries.json")
    
    if not os.path.exists(queries_path):
        raise FileNotFoundError(f"Queries file missing at {queries_path}")
        
    with open(queries_path, "r", encoding="utf-8") as f:
        queries = json.load(f)
        
    engine = SearchEngine()
    
    modes = ["keyword", "semantic", "hybrid"]
    summary = {}
    evaluation_details = {}
    
    for mode in modes:
        correct_top1 = 0
        correct_top5 = 0
        mrr_sum = 0.0
        
        hard_top1 = 0
        hard_total = 0
        
        details = []
        
        for q in queries:
            expected_id = q["expected_message_id"]
            is_hard = q.get("hard", False)
            if is_hard:
                hard_total += 1
                
            res = engine.search(q["query"], mode=mode, top_k=5)
            retrieved_ids = [r["message_id"] for r in res["results"]]
            
            rank = None
            if expected_id in retrieved_ids:
                rank = retrieved_ids.index(expected_id) + 1
                
            if rank == 1:
                correct_top1 += 1
                if is_hard:
                    hard_top1 += 1
                    
            if rank is not None and rank <= 5:
                correct_top5 += 1
                mrr_sum += 1.0 / rank
                
            details.append({
                "id": q["id"],
                "query": q["query"],
                "expected": expected_id,
                "rank": rank,
                "retrieved": retrieved_ids
            })
            
        total = len(queries)
        overall_acc = (correct_top1 / total) * 100.0
        hard_acc = (hard_top1 / hard_total) * 100.0 if hard_total > 0 else 0.0
        recall_5 = (correct_top5 / total) * 100.0
        mrr = (mrr_sum / total)
        
        summary[mode] = {
            "overall_accuracy": round(overall_acc, 2),
            "hard_accuracy": round(hard_acc, 2),
            "recall_at_5": round(recall_5, 2),
            "mrr": round(mrr, 4),
            "total_queries": total,
            "hard_queries": hard_total
        }
        evaluation_details[mode] = details
        
    print("\n================ EVALUATION BENCHMARK RESULTS ================")
    print(f"{'Method':<12} | {'Overall Acc':<12} | {'Hard 8 Acc':<12} | {'Recall@5':<10} | {'MRR':<8}")
    print("-" * 65)
    for mode in modes:
        s = summary[mode]
        print(f"{mode.capitalize():<12} | {s['overall_accuracy']:>11}% | {s['hard_accuracy']:>11}% | {s['recall_at_5']:>9}% | {s['mrr']:>8.4f}")
    print("=============================================================\n")
    
    out_path = os.path.join(base_dir, "data", "eval_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    details_path = os.path.join(base_dir, "data", "evaluation_details.json")
    with open(details_path, "w", encoding="utf-8") as f:
        json.dump(evaluation_details, f, indent=2)
        
    return summary

if __name__ == "__main__":
    run_evaluation()
