import random
from datetime import datetime, timedelta, date
import numpy as np
from faker import Faker

from analytics.db import get_conn

fake = Faker()

SEGMENTS = ["SMB", "MidMarket", "Enterprise"]
REGIONS = ["West", "Southwest", "Midwest", "South", "Northeast"]
CHANNELS = ["Organic", "Paid Search", "Social", "Referral", "Email"]
ORDER_STATUSES = ["completed", "cancelled", "returned"]
PLANS = ["Basic", "Pro", "Enterprise"]
TICKET_CATS = ["Billing", "Technical", "Account", "Shipping", "Refund"]
PRIORITIES = ["low", "medium", "high"]
TICKET_STATUSES = ["open", "in_progress", "resolved"]


def rand_dt(days_back: int = 730) -> datetime:
    end = datetime.now()
    start = end - timedelta(days=days_back)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def rand_date(days_back: int = 730) -> date:
    return rand_dt(days_back).date()

def chunked(rows, size):
    for i in range(0, len(rows), size):
        yield rows[i:i+size]

def insert_many(cur, sql, rows, chunk_size=5000):
    for part in chunked(rows, chunk_size):
        cur.executemany(sql, part)


def main(
    n_customers=5000,
    n_products=200,
    n_orders=60000,
    n_order_items=120000,
    n_subscriptions=5500,
    n_tickets=15000,
    seed=42
):
    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)

    conn = get_conn()
    cur = conn.cursor()

    # ✅ Fast + safe reset
    cur.execute("SET FOREIGN_KEY_CHECKS=0;")
    for t in ["support_tickets", "subscriptions", "order_items", "orders", "products", "customers"]:
        cur.execute(f"TRUNCATE TABLE {t};")
    cur.execute("SET FOREIGN_KEY_CHECKS=1;")
    conn.commit()

    # Customers
    customers = []
    for cid in range(1, n_customers + 1):
        seg = random.choices(SEGMENTS, weights=[0.65, 0.25, 0.10])[0]
        region = random.choice(REGIONS)
        channel = random.choices(CHANNELS, weights=[0.35, 0.20, 0.25, 0.10, 0.10])[0]
        created_at = rand_dt(900)
        customers.append((cid, created_at, seg, region, channel))

    insert_many(
        cur,
        "INSERT INTO customers (customer_id, created_at, segment, region, acquisition_channel) VALUES (%s,%s,%s,%s,%s)",
        customers
    )
    conn.commit()

    # Products
    categories = ["Electronics", "Home", "Beauty", "Grocery", "Sports", "Fashion", "Books", "Toys"]
    products = []
    for pid in range(1, n_products + 1):
        cat = random.choice(categories)
        pname = f"{fake.word().title()} {fake.word().title()} {pid}"
        products.append((pid, cat, pname))

    insert_many(
        cur,
        "INSERT INTO products (product_id, category, product_name) VALUES (%s,%s,%s)",
        products
    )
    conn.commit()

    # Orders
    orders = []
    for oid in range(1, n_orders + 1):
        cid = random.randint(1, n_customers)

        cust_created = customers[cid - 1][1]
        min_dt = cust_created
        max_dt = datetime.now()
        if min_dt > max_dt:
            min_dt = max_dt - timedelta(days=30)
        span = max(1, int((max_dt - min_dt).total_seconds()))
        order_date = min_dt + timedelta(seconds=random.randint(0, span))

        status = random.choices(ORDER_STATUSES, weights=[0.90, 0.06, 0.04])[0]
        orders.append((oid, cid, order_date, status))

    insert_many(
        cur,
        "INSERT INTO orders (order_id, customer_id, order_date, order_status) VALUES (%s,%s,%s,%s)",
        orders
    )
    conn.commit()

    # Order items
    order_items = []
    for item_id in range(1, n_order_items + 1):
        oid = random.randint(1, n_orders)
        pid = random.randint(1, n_products)
        qty = random.choices([1, 2, 3, 4], weights=[0.65, 0.20, 0.10, 0.05])[0]
        base_price = random.choice([9.99, 14.99, 19.99, 29.99, 49.99, 79.99, 99.99, 149.99])
        unit_price = float(base_price * random.uniform(0.9, 1.2))
        order_items.append((item_id, oid, pid, qty, round(unit_price, 2)))

    insert_many(
        cur,
        "INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES (%s,%s,%s,%s,%s)",
        order_items
    )
    conn.commit()

    # Subscriptions
    subs = []
    for sid in range(1, n_subscriptions + 1):
        cid = random.randint(1, n_customers)
        plan = random.choices(PLANS, weights=[0.70, 0.25, 0.05])[0]
        start = rand_date(900)

        status = random.choices(["active", "cancelled"], weights=[0.78, 0.22])[0]
        end = None
        if status == "cancelled":
            end_dt = start + timedelta(days=random.randint(30, 360))
            end = min(end_dt, date.today())

        subs.append((sid, cid, plan, start, end, status))

    insert_many(
        cur,
        "INSERT INTO subscriptions (subscription_id, customer_id, plan, start_date, end_date, status) VALUES (%s,%s,%s,%s,%s,%s)",
        subs
    )
    conn.commit()

    # Support tickets
    tickets = []
    for tid in range(1, n_tickets + 1):
        cid = random.randint(1, n_customers)
        created = rand_dt(365)
        cat = random.choice(TICKET_CATS)
        pr = random.choices(PRIORITIES, weights=[0.60, 0.30, 0.10])[0]
        st = random.choices(TICKET_STATUSES, weights=[0.20, 0.20, 0.60])[0]
        tickets.append((tid, cid, created, cat, pr, st))

    insert_many(
        cur,
        "INSERT INTO support_tickets (ticket_id, customer_id, created_at, category, priority, status) VALUES (%s,%s,%s,%s,%s,%s)",
        tickets
    )
    conn.commit()

    cur.close()
    conn.close()

    print("✅ Data generation complete:")
    print(f"customers={n_customers}, products={n_products}, orders={n_orders}, items={n_order_items}, subs={n_subscriptions}, tickets={n_tickets}")


if __name__ == "__main__":
    main()


