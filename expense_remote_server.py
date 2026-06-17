from fastmcp import FastMCP
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP("Expense Tracker")

pool = None


async def get_conn():
    global pool

    if pool is None:
        pool = await asyncpg.create_pool(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            ssl="require"
        )

    return pool


@mcp.tool()
async def add_expense(
    date: str,
    amount: float,
    category: str,
    subcategory: str = "",
    note: str = ""
):
    """Add a new expense"""

    db = await get_conn()

    async with db.acquire() as conn:

        expense_id = await conn.fetchval(
            """
            INSERT INTO expenses
            (expense_date, amount, category, subcategory, note)
            VALUES ($1,$2,$3,$4,$5)
            RETURNING id
            """,
            date,
            amount,
            category,
            subcategory,
            note
        )

    return {
        "status": "ok",
        "id": expense_id
    }


@mcp.tool()
async def list_expenses(start_date: str, end_date: str):

    db = await get_conn()

    async with db.acquire() as conn:

        rows = await conn.fetch(
            """
            SELECT id,
                   expense_date,
                   amount,
                   category,
                   subcategory,
                   note
            FROM expenses
            WHERE expense_date BETWEEN $1 AND $2
            ORDER BY expense_date, id
            """,
            start_date,
            end_date
        )

    return [
        tuple(row.values())
        for row in rows
    ]


@mcp.tool()
async def summarize_expenses(
    start_date: str,
    end_date: str,
    category: str = None
):

    db = await get_conn()

    async with db.acquire() as conn:

        query = """
            SELECT category,
                   SUM(amount) AS total_amount
            FROM expenses
            WHERE expense_date BETWEEN $1 AND $2
        """

        if category:

            query += """
                AND LOWER(category) = LOWER($3)
                GROUP BY category
                ORDER BY category
            """

            rows = await conn.fetch(
                query,
                start_date,
                end_date,
                category
            )

        else:

            query += """
                GROUP BY category
                ORDER BY category
            """

            rows = await conn.fetch(
                query,
                start_date,
                end_date
            )

    return [
        tuple(row.values())
        for row in rows
    ]


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
    mcp.run(transport="http", host="0.0.0.0", port=8000)