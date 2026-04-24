import ast

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # TODO: Use the 'ast' module to find docstrings for functions
    # TODO: (Optional/Advanced) Use regex to find business rules in comments like "# Business Logic Rule 001"
    # TODO: Return a dictionary for the UnifiedDocument schema.
    tree = ast.parse(source_code)
    logic_info = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            if docstring:
                logic_info.append({
                    "document_id": f"legacy-code-doc-{node.name}",
                    "content": docstring.strip(),
                    "source_type": "Code",
                    "author": "Unknown",
                    "timestamp": None,
                    "source_metadata": {"function_name": node.name, "type": "docstring"}
                })
    
    import re
    # Extract inline comments that contain important logic or warnings
    comments = re.findall(r'#(.*)', source_code)
    for i, comment in enumerate(comments):
        comment = comment.strip()
        if "Business Logic Rule" in comment or "WARNING" in comment or "discrepancy" in comment:
            logic_info.append({
                "document_id": f"legacy-code-comment-{i}",
                "content": comment,
                "source_type": "Code",
                "author": "Unknown",
                "timestamp": None,
                "source_metadata": {"type": "inline_comment"}
            })

    return logic_info

