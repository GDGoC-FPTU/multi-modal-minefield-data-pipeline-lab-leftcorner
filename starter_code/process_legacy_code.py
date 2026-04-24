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
                    "document_id": f"function_{node.name}",
                    "content": docstring,
                    "source_type": "Code",
                    "author": "Unknown",
                    "timestamp": None,
                    "source_metadata": {"function_name": node.name}
                })
    return logic_info

