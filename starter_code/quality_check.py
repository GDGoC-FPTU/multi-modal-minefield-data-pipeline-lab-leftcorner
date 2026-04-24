import re

# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    # Return True if pass, False if fail.
    content = document_dict.get("content", "")
    doc_id = document_dict.get("document_id", "Unknown")
    source_type = document_dict.get("source_type", "Unknown")

    if content is None or len(content.strip()) < 20:
        print(f"[QA Gate] REJECTED: {doc_id} - Content too short.")
        return False
    
    toxic_words = ["null pointer exception", "segmentation fault", "access denied"]
    if any(word in content.lower() for word in toxic_words):
        print(f"[QA Gate] REJECTED: {doc_id} - Found toxic/error string.")
        return False

    if source_type == "Code":
        comment_rules = re.findall(r'#.*(\d+)\s*%', content)

        code_only = re.sub(r'#.*', '', content)
        
        for pct in comment_rules:
            decimal_val = str(float(pct) / 100) 
            if decimal_val not in code_only and pct not in code_only:
                print(f"[QA Gate] REJECTED: {doc_id} - Potential logic discrepancy: '{pct}%' mentioned in comment but not found in execution logic.")
                return False

    print(f"[QA Gate] PASSED: {doc_id}")
    return True
