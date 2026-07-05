import json
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("logs.jsonl")

def log_query(query: str, answer: str, sources: list, success: bool, chunks_found: bool):
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "chunks_found": chunks_found,
        "answer_length": len(answer),
        "success": success,
        "sources": [doc.metadata.get("source", "unknown") for doc in sources]
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")