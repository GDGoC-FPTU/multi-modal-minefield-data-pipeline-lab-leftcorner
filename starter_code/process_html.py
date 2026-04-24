from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        # pass
    # ------------------------------------------
    
    # TODO: Use BeautifulSoup to find the table with id 'main-catalog'
    # TODO: Extract rows, handling 'N/A' or 'Liên hệ' in the price column.
    # TODO: Return a list of dictionaries for the UnifiedDocument schema.
    table = soup.find('table', id='main-catalog')
    if not table:
        print("Error: No table with id 'main-catalog' found.")
        return []
    products = []
    for row in table.find_all('tr')[1:]:  # Skip header row
        cols = row.find_all('td')
        if len(cols) < 4:
            continue  # Skip malformed rows
        product_id = cols[0].text.strip()
        name = cols[1].text.strip()
        price_text = cols[2].text.strip()
        price = None
        if price_text not in ['N/A', 'Liên hệ']:
            try:
                price = float(price_text.replace('$', '').replace(',', ''))
            except ValueError:
                pass  # Keep price as None if conversion fails
        category = cols[3].text.strip()
        
        products.append({
            "document_id": product_id,
            "content": f"{name} - {category}",
            "source_type": "HTML",
            "author": "Unknown",
            "timestamp": None,
            "source_metadata": {"price": price}
        })
    return products

