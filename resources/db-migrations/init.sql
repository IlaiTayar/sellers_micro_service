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
(1, 'Laptop', 999.99, 'https://loremflickr.com/400/300/laptop?lock=1'),
(2, 'Smartphone', 599.99, 'https://loremflickr.com/400/300/smartphone?lock=2'),
(3, 'Tablet', 399.99, 'https://loremflickr.com/400/300/tablet?lock=3'),
(4, 'Monitor', 199.99, 'https://loremflickr.com/400/300/computer,monitor?lock=4'),
(5, 'Keyboard', 49.99, 'https://loremflickr.com/400/300/keyboard?lock=5'),
(6, 'Mouse', 29.99, 'https://loremflickr.com/400/300/computer,mouse?lock=6'),
(7, 'Desk', 129.99, 'https://loremflickr.com/400/300/desk?lock=7'),
(8, 'Chair', 89.99, 'https://loremflickr.com/400/300/office,chair?lock=8'),
(9, 'Headphones', 79.99, 'https://loremflickr.com/400/300/headphones?lock=9'),
(10, 'Webcam', 39.99, 'https://loremflickr.com/400/300/webcam?lock=10'),
(1, 'Laptop Sleeve', 19.99, 'https://loremflickr.com/400/300/laptop,sleeve?lock=11'),
(2, 'Charger', 25.99, 'https://loremflickr.com/400/300/phone,charger?lock=12'),
(3, 'USB Cable', 9.99, 'https://loremflickr.com/400/300/usb,cable?lock=13'),
(4, 'HDMI Cable', 14.99, 'https://loremflickr.com/400/300/hdmi,cable?lock=14'),
(5, 'Mouse Pad', 5.99, 'https://loremflickr.com/400/300/mouse,pad?lock=15'),
(6, 'External HDD', 79.99, 'https://loremflickr.com/400/300/hard,drive?lock=16'),
(7, 'Desk Lamp', 34.99, 'https://loremflickr.com/400/300/desk,lamp?lock=17'),
(8, 'Office Chair Mat', 49.99, 'https://loremflickr.com/400/300/floor,mat?lock=18'),
(9, 'Bluetooth Speaker', 49.99, 'https://loremflickr.com/400/300/bluetooth,speaker?lock=19'),
(10, 'Docking Station', 74.99, 'https://loremflickr.com/400/300/docking,station?lock=20'),
(2, 'Laptop', 1099.99, 'https://loremflickr.com/400/300/gaming,laptop?lock=21');
