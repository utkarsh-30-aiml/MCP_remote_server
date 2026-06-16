from fastmcp import FastMCP
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
mcp = FastMCP("Expense Tracker")

def get_conn():
    return psycopg2.connect(
       host=os.getenv("DB_HOST"),
       port=os.getenv("DB_PORT"),
       dbname=os.getenv("DB_NAME"),
       user=os.getenv("DB_USER"),
       password=os.getenv("DB_PASSWORD")
    )


@mcp.tool()
def add_expense(
    date: str,
    amount: float,
    category: str,
    subcategory: str = "",
    note: str = ""
):
    """Add a new expense"""

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO expenses
                (expense_date, amount, category, subcategory, note)
                VALUES (%s,%s,%s,%s,%s)
                RETURNING id
                """,
                (date, amount, category, subcategory, note)
            )

            expense_id = cur.fetchone()[0]

    return {
        "status": "ok",
        "id": expense_id
    }




@mcp.tool()
def list_expenses(start_date: str, end_date: str):

    conn = get_conn()

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id,
                   expense_date,
                   amount,
                   category,
                   subcategory,
                   note
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
            ORDER BY expense_date, id
            """,
            (start_date, end_date)
        )

        rows = cur.fetchall()

        cur.close()

        return rows

    finally:
        conn.close()


@mcp.tool()
def summarize_expenses(start_date: str,
                       end_date: str,
                       category: str = None):

    conn = get_conn()

    try:
        cur = conn.cursor()

        query = """
            SELECT category,
                   SUM(amount) AS total_amount
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
        """

        params = [start_date, end_date]

        if category:
            query += " AND LOWER(category) = LOWER(%s)"
            params.append(category)

        query += """
            GROUP BY category
            ORDER BY category
        """

        cur.execute(query, params)

        rows = cur.fetchall()

        cur.close()

        return rows

    finally:
        conn.close()

CATEGORIES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "categories.json"
)

@mcp.resource("expense://categories")
def categories():
    """Valid expense categories and subcategories."""
    
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()
    
if __name__ == "__main__":
    mcp.run()