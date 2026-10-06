DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS seller;

CREATE TABLE seller (
    seller_id int(11) NOT NULL AUTO_INCREMENT,
    seller_name varchar(300) NOT NULL DEFAULT '',
    email varchar(300) NOT NULL DEFAULT '',
    status varchar(300) NOT NULL DEFAULT 'active',
    PRIMARY KEY (seller_id)
);

CREATE TABLE item (
    item_id int(11) NOT NULL AUTO_INCREMENT,
    seller_id int(11) NOT NULL,
    item_name varchar(300) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    image_url varchar(500) NULL,
    PRIMARY KEY (item_id),
    FOREIGN KEY (seller_id) REFERENCES seller(seller_id)
);

INSERT INTO seller (seller_name, email, status) VALUES
('Alice Smith', 'alice@example.com', 'active'),
('Bob Johnson', 'bob@example.com', 'inactive'),
('Charlie Brown', 'charlie@example.com', 'active'),
('Dana White', 'dana@example.com', 'inactive'),
('Eve Black', 'eve@example.com', 'active'),
('Frank Green', 'frank@example.com', 'active'),
('Grace Blue', 'grace@example.com', 'inactive'),
('Hank Purple', 'hank@example.com', 'active'),
('Ivy Orange', 'ivy@example.com', 'inactive'),
('Jack Gray', 'jack@example.com', 'active');

INSERT INTO seller (seller_id, seller_name, email, status)
VALUES
(100, 'Admin', 'admin@admin', 'active');

INSERT INTO item (seller_id, item_name, price, image_url) VALUES
(1, 'Laptop', 999.99, 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80'),
(2, 'Smartphone', 599.99, 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80'),
(3, 'Tablet', 399.99, 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=80'),
(4, 'Monitor', 199.99, 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=80'),
(5, 'Keyboard', 49.99, 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80'),
(6, 'Mouse', 29.99, 'https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=800&q=80'),
(7, 'Desk', 129.99, 'https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=800&q=80'),
(8, 'Chair', 89.99, 'https://images.unsplash.com/photo-1505843490701-5be5d3e5b6c0?auto=format&fit=crop&w=800&q=80'),
(9, 'Headphones', 79.99, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80'),
(10, 'Webcam', 39.99, 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80'),
(1, 'Laptop Sleeve', 19.99, 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80'),
(2, 'Charger', 25.99, 'https://images.unsplash.com/photo-1609592424257-7a0f5d7f2b0f?auto=format&fit=crop&w=800&q=80'),
(3, 'USB Cable', 9.99, 'https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=800&q=80'),
(4, 'HDMI Cable', 14.99, 'https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=800&q=80'),
(5, 'Mouse Pad', 5.99, 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=800&q=80'),
(6, 'External HDD', 79.99, 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=800&q=80'),
(7, 'Desk Lamp', 34.99, 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80'),
(8, 'Office Chair Mat', 49.99, 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=800&q=80'),
(9, 'Bluetooth Speaker', 49.99, 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=80'),
(10, 'Docking Station', 74.99, 'https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=800&q=80'),
(2, 'Laptop', 1099.99, 'https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?auto=format&fit=crop&w=800&q=80');
