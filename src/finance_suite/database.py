import sqlite3
from uuid import UUID

from finance_suite.account import Account


def setup_database(db_path: str = "db.sqlite3") -> None:
    """
    Connects to the database and creates the required table.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # The actual SQL command using the defined schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY NOT NULL,
            account_name TEXT NOT NULL,
            account_currency TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def add_account(account: Account, db_path: str = "db.sqlite3") -> None:
    """
    Writes the account object to the database.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """
        INSERT INTO accounts (
            account_id,
            account_name,
            account_currency
        )
        VALUES(?,?,?)
    """

    params = (str(account.id), account.name, account.currency)

    try:
        cursor.execute(sql, params)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error occurred while saving: {e}")
    finally:
        conn.close()


def get_account_by_id(uuid_str: str, db_path: str = "db.sqlite3") -> Account | None:
    """
    Retrieves a single Account object by its UUID string.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """
        SELECT account_id, account_name, account_currency
        FROM accounts
        WHERE account_id = ?
    """

    try:
        cursor.execute(sql, (uuid_str,))
        row = cursor.fetchone()

        if row:
            account_id = UUID(row[0])
            name = row[1]
            currency = row[2]

            return Account(id=account_id, name=name, currency=currency)
        else:
            return None

    except sqlite3.Error as e:
        print(f"Database error occurred while saving: {e}")
    finally:
        conn.close()


def get_all_accounts(db_path: str = "db.sqlite3") -> list[Account]:
    """
    Retrieves all Account objects stored in the database.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """
        SELECT account_id, account_name, account_currency
        FROM accounts
    """

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()

        accounts: list[Account] = []

        if rows:
            for row in rows:
                account_id = UUID(row[0])
                name = row[1]
                currency = row[2]

                accounts.append(Account(id=account_id, name=name, currency=currency))

        return accounts

    except sqlite3.Error as e:
        print(f"Database error occurred while saving: {e}")
        return []
    finally:
        conn.close()
