import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger=setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection=mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='expense_manager'
    )

    cursor=connection.cursor(dictionary=True)
    yield cursor
    if commit:
            connection.commit()
    
    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"Fetching_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        query="SELECT * FROM expenses WHERE expense_date = %s"
        cursor.execute(query, (expense_date,))
        expenses=cursor.fetchall()
    return expenses

def delete_expenses_for_date(expense_date):
    logger.info(f"Delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        query="DELETE FROM expenses WHERE expense_date = %s"
        cursor.execute(query, (expense_date,))

def insert_expenses(expense_date, amount, category, notes):
    logger.info(f"Insert_expenses called with {expense_date}, {amount}, {category}, {notes}")
    with get_db_cursor(commit=True) as cursor:
        query="""
        INSERT INTO expenses (expense_date, amount, category, notes)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (expense_date, amount, category, notes))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"Fetching_expense_summary called with start:{start_date} to end:{end_date}") 
    with get_db_cursor() as cursor:
        query="""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE expense_date BETWEEN %s AND %s
        GROUP BY category
        """
        cursor.execute(query, (start_date, end_date))
        summary=cursor.fetchall()
    return summary

def fetch_monthly_expense_summary():
    logger.info(f"fetch_expense_summary_by_months")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT month(expense_date) as expense_month, 
               monthname(expense_date) as month_name,
               sum(amount) as total FROM expenses
               GROUP BY expense_month, month_name;
            '''
        )
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    expenses=fetch_expenses_for_date('2024-08-01')
    print(expenses)
    