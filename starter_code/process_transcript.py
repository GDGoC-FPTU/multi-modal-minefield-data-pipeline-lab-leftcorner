import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # TODO: Remove noise tokens like [Music], [inaudible], [Laughter]
    # TODO: Strip timestamps [00:00:00]
    # TODO: Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    # TODO: Return a cleaned dictionary for the UnifiedDocument schema.
    text = re.sub(r'\[.*?\]', '', text)  # Remove [Music], [inaudible], etc.
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)  # Remove timestamps
    price_match = re.search(r'(\w+\s)?(nghìn|triệu|tỷ)', text)
    price = None
    if price_match:
        price = price_match.group(0)

    return {
        "document_id": "transcript_1",
        "content": text.strip(),
        "source_type": "Transcript",
        "author": "Unknown",
        "timestamp": None,
        "source_metadata": {"price": price}
    }

