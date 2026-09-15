import time
import psycopg2
from decimal import Decimal, ROUND_DOWN
from faker import Faker
import random
import argparse
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Project configuration (safe to hardcode here)
# -----------------------------
NUM_CUSTOMERS = 10
ACCOUNTS_PER_CUSTOMER = 2
NUM_TRANSACTIONS = 50
MAX_TXN_AMOUNT = 1000.00
CURRENCY = "USD"

# Non-zero initial balances
INITIAL_BALANCE_MIN = Decimal("10.00")
INITIAL_BALANCE_MAX = Decimal("1000.00")

# Loop config
DEFAULT_LOOP = True
SLEEP_SECONDS = 2

# CLI override (run once mode)
parser = argparse.ArgumentParser(description="Run fake data generator")
parser.add_argument("--once", action="store_true", help="Run a single iteration and exit")
args = parser.parse_args()
LOOP = not args.once and DEFAULT_LOOP


fake = Faker()


def random_money(min_val: Decimal, max_val: Decimal) -> Decimal:
    val = Decimal(str(random.uniform(float(min_val), float(max_val))))
    return val.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


def generate_account_number() -> str:
    return f"ACC-{random.randint(1000000000, 9999999999)}"


conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)
print("connexion est correct")
time.sleep(0.5)
conn.autocommit = True
cur = conn.cursor()


def run_iteration():
    customers = []
    # 1. Generate customers
    for _ in range(NUM_CUSTOMERS):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()

        cur.execute(
            "INSERT INTO customers (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id",
            (first_name, last_name, email),
        )
        customer_id = cur.fetchone()[0]
        customers.append(customer_id)

    accounts = []
    for customer_id in customers:
        for _ in range(ACCOUNTS_PER_CUSTOMER):
            initial_balance = random_money(INITIAL_BALANCE_MIN, INITIAL_BALANCE_MAX)
            account_number = generate_account_number()
            cur.execute(
                "INSERT INTO accounts (customer_id, account_number, balance) VALUES (%s, %s, %s) RETURNING id",
                (customer_id, account_number, initial_balance),
            )
            account_id = cur.fetchone()[0]
            accounts.append(account_id)

    txn_types = ["DEPOSIT", "WITHDRAWAL", "TRANSFER"]
    for _ in range(NUM_TRANSACTIONS):
        account_id = random.choice(accounts)
        txn_type = random.choice(txn_types)
        amount = round(random.uniform(1, MAX_TXN_AMOUNT), 2)

        if txn_type == "TRANSFER" and len(accounts) > 1:
            related_account = random.choice([a for a in accounts if a != account_id])
        else:
            related_account = account_id

        cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM transactions")
        next_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO transactions (id, account_id, amount, tx_type, related_account, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (next_id, account_id, amount, txn_type, related_account, "COMPLETED"),
        )

    print(f" Generated {len(customers)} customers, {len(accounts)} accounts, {NUM_TRANSACTIONS} transactions.")

try:
    iteration = 0
    while True:
        iteration += 1
        print(f"\n--- Iteration {iteration} started ---")
        run_iteration()
        print(f"--- Iteration {iteration} finished ---")
        if not LOOP:
            break
        time.sleep(SLEEP_SECONDS)

except KeyboardInterrupt:
    print("\nInterrupted by user. Exiting gracefully...")

finally:
    cur.close()
    conn.close()
    sys.exit(0)