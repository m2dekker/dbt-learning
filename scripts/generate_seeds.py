"""Generate deterministic sample shop data as dbt seeds.

Run from the project root:  python scripts/generate_seeds.py

The data deliberately contains data-quality issues (duplicates, nulls,
inconsistent casing, orphan keys, mismatched payments) so dbt tests have
something to catch. A fixed random seed makes the output reproducible.
"""

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

random.seed(42)
SEEDS_DIR = Path(__file__).resolve().parent.parent / "seeds"

FIRST_NAMES = ["Emma", "Liam", "Olivia", "Noah", "Sophie", "Lucas", "Mila", "Daan",
               "Julia", "Sem", "Anna", "Finn", "Sara", "Levi", "Eva", "Max",
               "Lotte", "Jesse", "Tess", "Thijs", "Nora", "Bram", "Lisa", "Ruben"]
LAST_NAMES = ["de Jong", "Jansen", "de Vries", "van Dijk", "Bakker", "Visser",
              "Smit", "Meijer", "Mulder", "Bos", "Peters", "Hendriks", "Smith",
              "Müller", "Dubois", "Garcia", "Rossi", "Nowak"]
COUNTRIES = ["NL", "NL", "NL", "BE", "DE", "FR", "GB"]

PRODUCTS = [  # (name, category, price_cents)
    ("Wireless Mouse", "Electronics", 2499), ("Mechanical Keyboard", "Electronics", 8999),
    ("USB-C Hub", "Electronics", 3999), ("27in Monitor", "Electronics", 24999),
    ("Noise Cancelling Headphones", "Electronics", 19999), ("Webcam HD", "Electronics", 5999),
    ("Desk Lamp", "Home Office", 3499), ("Ergonomic Chair", "Home Office", 29999),
    ("Standing Desk", "Home Office", 44999), ("Monitor Arm", "Home Office", 7999),
    ("Notebook A5", "Stationery", 799), ("Gel Pens (10 pack)", "Stationery", 1299),
    ("Sticky Notes", "Stationery", 499), ("Desk Organizer", "Stationery", 1999),
    ("Coffee Beans 1kg", "Pantry", 2299), ("Green Tea (50 bags)", "Pantry", 899),
    ("Protein Bars (12)", "Pantry", 2499), ("Water Bottle", "Lifestyle", 1799),
    ("Backpack", "Lifestyle", 6999), ("Laptop Sleeve", "Lifestyle", 2999),
]

STATUSES = ["completed"] * 6 + ["shipped"] * 2 + ["placed", "returned"]
PAYMENT_METHODS = ["credit_card"] * 4 + ["paypal"] * 2 + ["bank_transfer", "gift_card"]


def write_csv(name, header, rows):
    path = SEEDS_DIR / f"{name}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    print(f"{path.name}: {len(rows)} rows")


def random_ts(start: date, end: date) -> datetime:
    span = (end - start).days
    return datetime.combine(start, datetime.min.time()) + timedelta(
        days=random.randint(0, span), seconds=random.randint(0, 86399))


def main():
    # ---- customers -------------------------------------------------------
    customers = []
    for cid in range(1, 101):
        first, last = random.choice(FIRST_NAMES), random.choice(LAST_NAMES)
        email = f"{first}.{last}".lower().replace(" ", "").replace("ü", "u") + f"{cid}@example.com"
        country = random.choice(COUNTRIES)
        created = random_ts(date(2023, 1, 1), date(2024, 6, 30))
        if cid % 9 == 0:
            email = email.upper()                       # ISSUE: inconsistent casing
        if cid % 7 == 0:
            country = country.lower()                   # ISSUE: inconsistent casing
        if cid in (13, 42, 77):
            email = ""                                  # ISSUE: null email
        if cid in (21, 58):
            first = first + "  "                        # ISSUE: trailing whitespace
        customers.append([cid, first, last, email, country,
                          created.isoformat(sep=" "), created.isoformat(sep=" ")])
    customers += [list(customers[4]), list(customers[33])]  # ISSUE: exact duplicate rows
    write_csv("raw_customers",
              ["id", "first_name", "last_name", "email", "country_code", "created_at", "updated_at"],
              customers)

    # ---- products --------------------------------------------------------
    products = []
    for pid, (name, category, price) in enumerate(PRODUCTS, start=1):
        if pid in (3, 12, 19):
            category = category.lower()                 # ISSUE: inconsistent casing
        products.append([pid, name, category, price])
    write_csv("raw_products", ["id", "name", "category", "price_cents"], products)

    # ---- orders, order_items, payments -----------------------------------
    orders, items, payments = [], [], []
    item_id = payment_id = 0
    for oid in range(1, 301):
        customer_id = random.randint(1, 100)
        if oid == 150:
            customer_id = 999                           # ISSUE: orphan foreign key
        created = random_ts(date(2024, 1, 1), date(2025, 6, 30))
        status = random.choice(STATUSES)
        if oid % 23 == 0:
            status = status.capitalize()                # ISSUE: inconsistent casing
        orders.append([oid, customer_id, created.isoformat(sep=" "), status])

        order_total = 0
        for _ in range(random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10])[0]):
            item_id += 1
            pid = random.randint(1, len(PRODUCTS))
            qty = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
            price = PRODUCTS[pid - 1][2]
            product_ref = pid
            if item_id == 77:
                product_ref = ""                        # ISSUE: null product_id
            if item_id == 200:
                qty = 0                                 # ISSUE: zero quantity
            order_total += qty * price
            items.append([item_id, oid, product_ref, qty, price])

        if status.lower() == "placed":
            continue                                    # not paid yet
        amount_left = order_total
        if oid in (37, 111, 222):
            amount_left -= 500                          # ISSUE: payment != order total
        n_payments = 2 if (random.random() < 0.08 and amount_left > 2000) else 1
        for i in range(n_payments):
            payment_id += 1
            amount = amount_left if i == n_payments - 1 else amount_left // 2
            amount_left -= amount
            method = random.choice(PAYMENT_METHODS)
            if method == "paypal" and payment_id % 5 == 0:
                method = "PayPal"                       # ISSUE: inconsistent casing
            amount_out = "" if payment_id in (60, 180) else amount  # ISSUE: null amount
            paid_at = created + timedelta(minutes=random.randint(1, 120))
            payments.append([payment_id, oid, method, amount_out, paid_at.isoformat(sep=" ")])

    orders += [list(orders[9]), list(orders[199])]      # ISSUE: duplicate order rows
    write_csv("raw_orders", ["id", "customer_id", "ordered_at", "status"], orders)
    write_csv("raw_order_items",
              ["id", "order_id", "product_id", "quantity", "unit_price_cents"], items)
    write_csv("raw_payments",
              ["id", "order_id", "payment_method", "amount_cents", "created_at"], payments)


if __name__ == "__main__":
    main()
