import json
import time
import os

# Robust path handling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "raw_data")


# Import role-specific modules
from schema import UnifiedDocument
from process_pdf import extract_pdf_data
from process_transcript import clean_transcript
from process_html import parse_html_catalog
from process_csv import process_sales_csv
from process_legacy_code import extract_logic_from_code
from quality_check import run_quality_gate

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================
# Task: Orchestrate the ingestion pipeline and handle errors/SLA.

def main():
    start_time = time.time()
    final_kb = []
    
    # --- FILE PATH SETUP ---
    tasks = [
        {"name": "PDF Lecture", "func": extract_pdf_data, "path": os.path.join(RAW_DATA_DIR, "lecture_notes.pdf")},
        {"name": "Transcript", "func": clean_transcript, "path": os.path.join(RAW_DATA_DIR, "demo_transcript.txt")},
        {"name": "HTML Catalog", "func": parse_html_catalog, "path": os.path.join(RAW_DATA_DIR, "product_catalog.html")},
        {"name": "Sales CSV", "func": process_sales_csv, "path": os.path.join(RAW_DATA_DIR, "sales_records.csv")},
        {"name": "Legacy Code", "func": extract_logic_from_code, "path": os.path.join(RAW_DATA_DIR, "legacy_pipeline.py")},
    ]
    
    output_path = os.path.join(os.path.dirname(SCRIPT_DIR), "processed_knowledge_base.json")
    # -----------------------

    print("--- Starting Ingestion Pipeline ---")
    
    for task in tasks:
        try:
            print(f"Processing {task['name']}...")
            if not os.path.exists(task['path']):
                print(f"  [Error] File not found: {task['path']}")
                continue

            result = task['func'](task['path'])
            
            if not result:
                print(f"  [Skip] {task['name']} returned empty extraction.")
                continue
                
            docs = result if isinstance(result, list) else [result]
            
            for doc in docs:
                if doc and run_quality_gate(doc):
                    doc_dict = doc.dict() if hasattr(doc, 'dict') else doc
                    final_kb.append(doc_dict)

        except Exception as e:
            print(f"  [Critical Error] Failed to process {task['name']}: {str(e)}")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(final_kb, f, indent=4, ensure_ascii=False)
        print(f"\n--- Knowledge Base saved to: {output_path} ---")
    except Exception as e:
        print(f"  [Error] Could not save KB: {e}")

    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*30)
    print(f"PIPELINE SUMMARY (SLA Report)")
    print(f"Total Time: {duration:.2f} seconds")
    print(f"Valid Documents Stored: {len(final_kb)}")
    print(f"Success Rate: {(len(final_kb)/len(tasks))*100:.1f}%")
    print("="*30)


if __name__ == "__main__":
    main()