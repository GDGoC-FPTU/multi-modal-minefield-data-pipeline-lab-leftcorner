import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # TODO: Remove duplicate rows based on 'id'
    # TODO: Clean 'price' column: convert "$1200", "250000", "five dollars" to floats
    # TODO: Normalize 'date_of_sale' into a single format (YYYY-MM-DD)
    # TODO: Return a list of dictionaries for the UnifiedDocument schema.
    df.drop_duplicates(subset='id', inplace=True)
    df['price'] = df['price'].astype(str).replace(r'[\$,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    # Handle multiple date formats safely
    df['date_of_sale'] = pd.to_datetime(df['date_of_sale'], errors='coerce')

    docs = []
    for _, row in df.iterrows():
        # Ensure timestamp is string in ISO format or None if NaT
        timestamp = row['date_of_sale'].isoformat() if pd.notnull(row['date_of_sale']) else None
        
        doc = {
            "document_id": f"csv-sales-{row['id']}",
            "content": f"Sale of {row['product_name']} in category {row['category']}",
            "source_type": "CSV",
            "author": str(row.get('seller_id', 'Unknown')),
            "timestamp": timestamp,
            "source_metadata": {
                "price": row['price'] if pd.notnull(row['price']) else None,
                "currency": row.get('currency'),
                "stock_quantity": row.get('stock_quantity') if pd.notnull(row.get('stock_quantity')) else None
            }
        }
        docs.append(doc)
    
    return docs
