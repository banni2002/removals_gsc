import sqlite3
import logging
from datetime import datetime

# Constants
DB_PATH = "path_to_your_database.db"
SUBMITTED_STATE = "submitted"
NOT_INDEXED_STATE = "NOT"
NULL_STATE = None

def get_db_connection(db_path):
    return sqlite3.connect(db_path)

def get_products_to_index(cursor):
    query = "SELECT * FROM products WHERE is_index=? AND state IS NULL ORDER BY total_order DESC"
    cursor.execute(query, (NOT_INDEXED_STATE,))
    columns = [description[0] for description in cursor.description]
    return [{columns[index]: value for index, value in enumerate(row)} for row in cursor.fetchall()]

def update_product_state(cursor, product_id, state=SUBMITTED_STATE):
    query = "UPDATE products SET state = ?, submitted_at = ? WHERE product_id = ?"
    cursor.execute(query, (state, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id))

def count_products_by_state(cursor, state):
    query = "SELECT COUNT(*) FROM products WHERE state = ?"
    cursor.execute(query, (state,))
    return cursor.fetchone()[0]

def submit_product_and_update_state(cursor, product):
    print("INDEX", product['product_id'], product['product_url'])
    submitted = index_url(http=http, url=product['product_url'])
    if submitted:
        update_product_state(cursor, product['product_id'])

def main(db_path=DB_PATH):
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        products_to_index = get_products_to_index(cursor)
        for product in products_to_index:
            if product['product_url']:
                submit_product_and_update_state(cursor, product)
                conn.commit()
                # Check for position_api_json_file and google_api_json_files logic here
        submitted_count = count_products_by_state(cursor, SUBMITTED_STATE)
        logging.info(f"Number of products submitted: {submitted_count}")
        # Wait for 24 hours before repeating the process
        logging.info(f"*** Waiting for {interval_hours} hours before submitting the next set of products ***")
        time.sleep(interval_hours * 60 * 60)

if __name__ == "__main__":
    main()