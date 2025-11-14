import unittest
from app import app, db, Product


class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        # Use in-memory DB for tests
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True

        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_product(self):
        response = self.client.post(
            "/api/products",
            json={"name": "Ball", "price": 9.99}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Ball", response.data)

    def test_get_products(self):
        # First add a product
        self.client.post(
            "/api/products",
            json={"name": "Bat", "price": 49.99}
        )

        # Then get all products
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bat", response.data)


if __name__ == "__main__":
    unittest.main()
