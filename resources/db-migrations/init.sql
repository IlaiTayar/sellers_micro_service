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
(1, 'Laptop', 999.99, 'https://picsum.photos/seed/laptop/400/300'),
(2, 'Smartphone', 599.99, 'https://picsum.photos/seed/smartphone/400/300'),
(3, 'Tablet', 399.99, 'https://picsum.photos/seed/tablet/400/300'),
(4, 'Monitor', 199.99, 'https://picsum.photos/seed/monitor/400/300'),
(5, 'Keyboard', 49.99, 'https://picsum.photos/seed/keyboard/400/300'),
(6, 'Mouse', 29.99, 'https://picsum.photos/seed/computer-mouse/400/300'),
(7, 'Desk', 129.99, 'https://picsum.photos/seed/desk/400/300'),
(8, 'Chair', 89.99, 'https://picsum.photos/seed/office-chair/400/300'),
(9, 'Headphones', 79.99, 'https://picsum.photos/seed/headphones/400/300'),
(10, 'Webcam', 39.99, 'https://picsum.photos/seed/webcam/400/300'),
(1, 'Laptop Sleeve', 19.99, 'https://picsum.photos/seed/laptop-bag/400/300'),
(2, 'Charger', 25.99, 'https://picsum.photos/seed/charger/400/300'),
(3, 'USB Cable', 9.99, 'https://picsum.photos/seed/usb-cable/400/300'),
(4, 'HDMI Cable', 14.99, 'https://picsum.photos/seed/hdmi-cable/400/300'),
(5, 'Mouse Pad', 5.99, 'https://picsum.photos/seed/mouse-pad/400/300'),
(6, 'External HDD', 79.99, 'https://picsum.photos/seed/hard-drive/400/300'),
(7, 'Desk Lamp', 34.99, 'https://picsum.photos/seed/desk-lamp/400/300'),
(8, 'Office Chair Mat', 49.99, 'https://picsum.photos/seed/floor-mat/400/300'),
(9, 'Bluetooth Speaker', 49.99, 'https://picsum.photos/seed/speaker/400/300'),
(10, 'Docking Station', 74.99, 'https://picsum.photos/seed/docking-station/400/300'),
(2, 'Laptop', 1099.99, 'https://picsum.photos/seed/laptop,gaming/400/300');
