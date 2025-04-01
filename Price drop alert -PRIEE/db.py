import mysql.connector

class EcomDB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pricetracker"
        )
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            site VARCHAR(50) NOT NULL,
                            product_name TEXT NOT NULL,
                            price VARCHAR(50) NOT NULL,
                            image_url TEXT,
                            product_url TEXT NOT NULL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE KEY (product_url)
                        ''')
        self.connection.commit()

    def insert_product(self, site, product_name, price, image_url, product_url):
        cursor = self.connection.cursor()
        try:
            cursor.execute('''INSERT INTO products 
                            (site, product_name, price, image_url, product_url) 
                            VALUES (%s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                            price = VALUES(price),
                            timestamp = CURRENT_TIMESTAMP''',
                         (site, product_name, price, image_url, product_url))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            cursor.close()