import json
import os
import random
from datetime import datetime, timedelta

PARTICIPANTS = ["Rahul", "Priya", "Aman", "Neha", "Arjun", "Simran", "Karan", "Riya"]

NOISE_TEMPLATES = [
    "ha bilkul", "sahi hai", "ok done", "bhai sun", "kya chal raha hai", 
    "chalo badiya", "kal milte hain", "hahaha true", "bc cool", "lol nice",
    "<Media omitted>", "https://meet.google.com/abc-xyz-123", "call kare kya?",
    "thik hai", "send code snippet", "refer to documentation", "let's test this tomorrow",
    "kya scene?", "batao jaldi", "sure thing", "+1", "cool", "great", "nice",
    "wait checking...", "already done bro", "kaise ho sab?", "koi update?"
]

PLANTED_MESSAGES = [
    # Decision Thread A - Trip
    {
        "id": "msg_trip_decide",
        "timestamp": "2026-04-17T21:34:00",
        "sender": "Priya",
        "text": "haan bhai Manali decision final kar dete hain",
        "thread_id": "thread_trip",
        "reply_to": "msg_trip_prev1",
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_trip_prev1",
        "timestamp": "2026-04-17T21:30:00",
        "sender": "Aman",
        "text": "budget 8k max rakhna",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_trip_prev2",
        "timestamp": "2026-04-17T21:28:00",
        "sender": "Rahul",
        "text": "Manali chalna hai sabko?",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_trip_next1",
        "timestamp": "2026-04-17T21:35:00",
        "sender": "Rahul",
        "text": "sahi hai dates check kar lo",
        "thread_id": "thread_trip",
        "reply_to": "msg_trip_decide",
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_trip_next2",
        "timestamp": "2026-04-17T21:36:00",
        "sender": "Simran",
        "text": "perfect, fast nikalte hain",
        "thread_id": "thread_trip",
        "reply_to": "msg_trip_next1",
        "has_media": False,
        "is_forwarded": False
    },

    # Decision Thread B - Project Database
    {
        "id": "msg_proj_decide",
        "timestamp": "2026-05-12T16:20:00",
        "sender": "Aman",
        "text": "Done, PostgreSQL rakhte hain",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },

    # Decision Thread C - Event Venue
    {
        "id": "msg_event_decide",
        "timestamp": "2026-06-25T14:15:00",
        "sender": "Arjun",
        "text": "Auditorium final ho gaya",
        "thread_id": "thread_event",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },

    # Other Hard Queries
    {
        "id": "msg_budget_decide",
        "timestamp": "2026-04-17T21:30:00",
        "sender": "Aman",
        "text": "8k max rakhna",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_meet_decide",
        "timestamp": "2026-04-18T10:00:00",
        "sender": "Simran",
        "text": "CCD ke paas ikattha hote hain",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_travel_decide",
        "timestamp": "2026-04-18T11:10:00",
        "sender": "Karan",
        "text": "overnight bus book kar li hai",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_deadline_decide",
        "timestamp": "2026-05-20T19:00:00",
        "sender": "Rahul",
        "text": "Sunday raat 12 baje tak submit karna hai",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_snacks_decide",
        "timestamp": "2026-06-25T15:00:00",
        "sender": "Riya",
        "text": "Riya chips and drinks le aayegi",
        "thread_id": "thread_event",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },

    # Semantic & Person & Time Planted Messages
    {
        "id": "msg_airport_leave",
        "timestamp": "2026-04-20T06:00:00",
        "sender": "Rahul",
        "text": "kal subah 5 baje nikalna padega",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_hotel_book",
        "timestamp": "2026-04-19T14:00:00",
        "sender": "Neha",
        "text": "resort stay ready ho gaya hai",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_frontend_framework",
        "timestamp": "2026-05-10T11:00:00",
        "sender": "Neha",
        "text": "React and Vite setup kar diya hai",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_dinner_schedule",
        "timestamp": "2026-06-20T20:00:00",
        "sender": "Karan",
        "text": "Friday 8 PM ko Barbeque Nation me dinner hai",
        "thread_id": "thread_event",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_slides_present",
        "timestamp": "2026-05-25T18:00:00",
        "sender": "Arjun",
        "text": "Arjun presentation handle karega",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_design_files",
        "timestamp": "2026-05-08T15:30:00",
        "sender": "Neha",
        "text": "Figma link pin kar diya hai description me",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_backend_api",
        "timestamp": "2026-05-15T17:00:00",
        "sender": "Aman",
        "text": "FastAPI endpoints ready hain search ke liye",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_wifi_pass",
        "timestamp": "2026-03-10T09:30:00",
        "sender": "Rahul",
        "text": "Office guest network password: guest@2026",
        "thread_id": "thread_general",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_priya_budget",
        "timestamp": "2026-04-17T21:28:00",
        "sender": "Priya",
        "text": "Priya: budget thoda tight hai 8k me try karte hain",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_rahul_trip",
        "timestamp": "2026-04-16T20:00:00",
        "sender": "Rahul",
        "text": "Rahul: Himachal side chalte hain bohot achha mausam hai",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_neha_design",
        "timestamp": "2026-05-09T14:00:00",
        "sender": "Neha",
        "text": "Neha: dark mode look standard lagega interface me",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_aman_perf",
        "timestamp": "2026-05-16T10:00:00",
        "sender": "Aman",
        "text": "Aman: FAISS vector search 10ms me respond kar raha hai",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_simran_sched",
        "timestamp": "2026-06-15T11:00:00",
        "sender": "Simran",
        "text": "Simran: meeting kya 3 baje reschedule ho sakti hai?",
        "thread_id": "thread_event",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_karan_test",
        "timestamp": "2026-05-28T16:00:00",
        "sender": "Karan",
        "text": "Karan: pytest coverage 90% plus exceed kar gaya hai",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_riya_logistics",
        "timestamp": "2026-06-22T12:00:00",
        "sender": "Riya",
        "text": "Riya: cab booking confirmation number email pe bhej diya hai",
        "thread_id": "thread_event",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_arjun_db",
        "timestamp": "2026-05-11T15:00:00",
        "sender": "Arjun",
        "text": "Arjun: SQL relational queries easy rahengay baseline ke liye",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_priya_food",
        "timestamp": "2026-06-21T13:00:00",
        "sender": "Priya",
        "text": "Priya: veg and non-veg dono options available hone chahiye",
        "thread_id": "thread_event",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_rahul_transport",
        "timestamp": "2026-04-18T09:00:00",
        "sender": "Rahul",
        "text": "Rahul: Volvo sleeper bus best rahega overnight journey ke liye",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_march_discuss",
        "timestamp": "2026-03-15T14:00:00",
        "sender": "Aman",
        "text": "March me initial team kickoff meeting set hui thi",
        "thread_id": "thread_general",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_last_week",
        "timestamp": "2026-08-25T11:00:00",
        "sender": "Karan",
        "text": "last week benchmark testing overall complete ho gaya tha",
        "thread_id": "thread_general",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_june_discuss",
        "timestamp": "2026-06-10T16:00:00",
        "sender": "Neha",
        "text": "June me core retrieval pipeline implementation finish hua tha",
        "thread_id": "thread_general",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_april_discuss",
        "timestamp": "2026-04-15T12:00:00",
        "sender": "Priya",
        "text": "April me Himachal dates fixed hue the",
        "thread_id": "thread_trip",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_july_discuss",
        "timestamp": "2026-07-20T15:00:00",
        "sender": "Simran",
        "text": "July me UI design clean baseline deploy kar diya tha",
        "thread_id": "thread_general",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_may_discuss",
        "timestamp": "2026-05-18T10:00:00",
        "sender": "Arjun",
        "text": "May me synthetic dataset schema finalise kia gaya tha",
        "thread_id": "thread_proj",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_yesterday_decide",
        "timestamp": "2026-08-31T18:00:00",
        "sender": "Riya",
        "text": "kal meeting me README docs final approve ho gaya",
        "thread_id": "thread_general",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_august_discuss",
        "timestamp": "2026-08-10T14:00:00",
        "sender": "Aman",
        "text": "August me zero-overlap evaluation metrics compile kar liye",
        "thread_id": "thread_general",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    },
    {
        "id": "msg_recent_update",
        "timestamp": "2026-08-31T20:00:00",
        "sender": "Karan",
        "text": "latest build push kar diya hai GitHub repository pe",
        "thread_id": "thread_general",
        "reply_to": None,
        "has_media": False,
        "is_forwarded": False
    }
]

def generate_synthetic_corpus(total_messages=4200, seed=42):
    random.seed(seed)
    planted_ids = {m["id"] for m in PLANTED_MESSAGES}
    messages = list(PLANTED_MESSAGES)
    
    start_date = datetime(2026, 3, 1, 9, 0, 0)
    time_span_seconds = int((datetime(2026, 8, 31, 23, 59, 59) - start_date).total_seconds())
    
    for i in range(1, total_messages - len(PLANTED_MESSAGES) + 1):
        msg_id = f"msg_{i:04d}"
        if msg_id in planted_ids:
            msg_id = f"msg_gen_{i:04d}"
            
        offset_sec = random.randint(0, time_span_seconds)
        ts = start_date + timedelta(seconds=offset_sec)
        sender = random.choice(PARTICIPANTS)
        text = random.choice(NOISE_TEMPLATES)
        
        has_media = (text == "<Media omitted>")
        is_forwarded = (random.random() < 0.05)
        
        messages.append({
            "id": msg_id,
            "timestamp": ts.isoformat(),
            "sender": sender,
            "text": text,
            "thread_id": f"thread_{random.randint(1, 50)}",
            "reply_to": None,
            "has_media": has_media,
            "is_forwarded": is_forwarded
        })
        
    messages.sort(key=lambda x: x["timestamp"])
    
    out_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "messages.json")
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
        
    print(f"Generated {len(messages)} messages at {out_path}")

if __name__ == "__main__":
    generate_synthetic_corpus()
