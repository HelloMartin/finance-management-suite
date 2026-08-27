import sqlite3
from contextlib import closing
from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from finance_suite.account import Account
from finance_suite.transaction import Transaction


def _connect(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def _setup_accounts_table(cursor) -> None:
    """Responsible ONLY for the accounts schema."""
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY NOT NULL,
                account_name TEXT NOT NULL,
                account_currency TEXT NOT NULL
            );
        """)


def _setup_transactions_table(cursor) -> None:
    """Responsible ONLY for the transactions schema."""
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY NOT NULL,
                account_id TEXT NOT NULL,
                amount TEXT NOT NULL,
                description TEXT,
                transaction_date DATE NOT NULL,
                
                FOREIGN KEY (account_id)
                    REFERENCES accounts (account_id)
                    ON DELETE CASCADE
            );
        """)


def setup_database(db_path: str = "db.sqlite3") -> None:
    """
    Connects to the database and creates the required table.
    """

    with closing(_connect(db_path=db_path)) as conn, conn:
        cursor = conn.cursor()

        _setup_accounts_table(cursor=cursor)
        _setup_transactions_table(cursor=cursor)


def _row_to_account(row) -> Account:
    account_id = UUID(row[0])
    name = row[1]
    currency = row[2]

    return Account(id=account_id, name=name, currency=currency)


def add_account(account: Account, db_path: str = "db.sqlite3") -> None:
    """
    Writes the account object to the database.
    """

    with closing(_connect(db_path=db_path)) as conn, conn:

        sql = """
                INSERT INTO accounts (
                    account_id,
                    account_name,
                    account_currency
                )
                VALUES(?,?,?)
            """

        params = (str(account.id), account.name, account.currency)

        conn.execute(sql, params)


def get_account_by_id(uuid_str: str, db_path: str = "db.sqlite3") -> Account | None:
    """
    Retrieves a single Account object by its UUID string.
    """

    with closing(_connect(db_path=db_path)) as conn, conn:

        sql = """
                SELECT account_id, account_name, account_currency
                FROM accounts
                WHERE account_id = ?
            """

        row = conn.execute(sql, (uuid_str,)).fetchone()

        if row:
            return _row_to_account(row=row)
        else:
            return None


def get_all_accounts(db_path: str = "db.sqlite3") -> list[Account]:
    """
    Retrieves all Account objects stored in the database.
    """

    with closing(_connect(db_path=db_path)) as conn, conn:

        sql = """
                SELECT account_id, account_name, account_currency
                FROM accounts
            """

        rows = conn.execute(sql).fetchall()

        accounts: list[Account] = []

        for row in rows:
            accounts.append(_row_to_account(row=row))

        return accounts


def _row_to_transaction(row) -> Transaction:
    transaction_id = UUID(row[0])
    account_id = UUID(row[1])
    amount = Decimal(row[2])
    description = row[3]
    transaction_date = date.fromisoformat(row[4])

    return Transaction(
        id=transaction_id,
        account_id=account_id,
        amount=amount,
        description=description,
        date=transaction_date,
    )


def add_transaction(transaction: Transaction, db_path: str = "db.sqlite3") -> None:
    """
    Writes the transaction object to the database.
    """

    with closing(_connect(db_path=db_path)) as conn, conn:

        sql = """
                INSERT INTO transactions (
                    transaction_id,
                    account_id,
                    amount,
                    description,
                    transaction_date
                )
                VALUES(?,?,?,?,?)
            """

        params = (
            str(transaction.id),
            str(transaction.account_id),
            str(transaction.amount),
            transaction.description,
            str(transaction.transaction_date),
        )

        conn.execute(sql, params)


def get_transaction_by_id(
    uuid_str: str, db_path: str = "db.sqlite3"
) -> Transaction | None:
    """
    Retrieves a single Transaction object by its UUID string.
    """

    with closing(_connect(db_path=db_path)) as conn, conn:

        sql = """
                SELECT transaction_id, account_id, amount, description, transaction_date
                FROM transactions
                WHERE transaction_id = ?
            """

        row = conn.execute(sql, (uuid_str,)).fetchone()

        if row:
            return _row_to_transaction(row=row)
        else:
            return None


def get_all_transactions(db_path: str = "db.sqlite3") -> list[Transaction]:
    """
    Retrieves all Transaction objects stored in the database.
    """

    with closing(_connect(db_path=db_path)) as conn, conn:

        sql = """
                SELECT transaction_id, account_id, amount, description, transaction_date
                FROM transactions
            """

        rows = conn.execute(sql).fetchall()

        transactions: list[Transaction] = []

        for row in rows:
            transactions.append(_row_to_transaction(row=row))

        return transactions


def get_all_transactions_by_account_id(
    uuid_str: str, db_path: str = "db.sqlite3"
) -> list[Transaction]:
    """
    Retrieves all Transaction objects of given Account stored in the database.
    """

    with closing(_connect(db_path=db_path)) as conn, conn:

        sql = """
                SELECT transaction_id, account_id, amount, description, transaction_date
                FROM transactions
                WHERE account_id = ?
            """

        rows = conn.execute(sql, (uuid_str,)).fetchall()

        transactions: list[Transaction] = []

        for row in rows:
            transactions.append(_row_to_transaction(row=row))

        return transactions
