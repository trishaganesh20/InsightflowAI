USE ba_assistant;

DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
  customer_id BIGINT PRIMARY KEY,
  created_at DATETIME NOT NULL,
  segment VARCHAR(20) NOT NULL,
  region VARCHAR(30) NOT NULL,
  acquisition_channel VARCHAR(30) NOT NULL,
  INDEX idx_customers_created_at (created_at),
  INDEX idx_customers_segment (segment),
  INDEX idx_customers_region (region)
);

CREATE TABLE products (
  product_id BIGINT PRIMARY KEY,
  category VARCHAR(50) NOT NULL,
  product_name VARCHAR(100) NOT NULL,
  INDEX idx_products_category (category)
);

CREATE TABLE orders (
  order_id BIGINT PRIMARY KEY,
  customer_id BIGINT NOT NULL,
  order_date DATETIME NOT NULL,
  order_status VARCHAR(20) NOT NULL,
  INDEX idx_orders_customer_date (customer_id, order_date),
  INDEX idx_orders_status (order_status),
  CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
  order_item_id BIGINT PRIMARY KEY,
  order_id BIGINT NOT NULL,
  product_id BIGINT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  INDEX idx_items_order (order_id),
  INDEX idx_items_product (product_id),
  CONSTRAINT fk_items_order
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
  CONSTRAINT fk_items_product
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE subscriptions (
  subscription_id BIGINT PRIMARY KEY,
  customer_id BIGINT NOT NULL,
  plan VARCHAR(30) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NULL,
  status VARCHAR(20) NOT NULL,
  INDEX idx_sub_customer (customer_id),
  INDEX idx_sub_status (status),
  CONSTRAINT fk_sub_customer
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE support_tickets (
  ticket_id BIGINT PRIMARY KEY,
  customer_id BIGINT NOT NULL,
  created_at DATETIME NOT NULL,
  category VARCHAR(50) NOT NULL,
  priority VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL,
  INDEX idx_tickets_customer_time (customer_id, created_at),
  INDEX idx_tickets_priority (priority),
  CONSTRAINT fk_tickets_customer
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
