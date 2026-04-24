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
    
    # Remove specific noise tokens and timestamps
    text = re.sub(r'\[(?:Music(?: starts| ends)?|inaudible|Laughter)\]', '', text)
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # Find price in Vietnamese words
    price_match = re.search(r'năm trăm nghìn', text, re.IGNORECASE)
    price = price_match.group(0) if price_match else None

    return {
        "document_id": "transcript-1",
        "content": text.strip(),
        "source_type": "Transcript",
        "author": "Unknown",
        "timestamp": None,
        "source_metadata": {"price_mentioned": price}
    }

