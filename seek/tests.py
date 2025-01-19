from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class BooksAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.access_token = str(AccessToken.for_user(self.user))
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.access_token}"}

        self.mock_books = {
            "total": 2,
            "pages": 1,
            "current_page": 1,
            "books": [
                {
                    "_id": "678af286c3dc45b17b69cb12",
                    "title": "test",
                    "author": "test",
                    "published_date": "2024-01-03T00:00:00",
                    "genre": "test",
                    "price": 30.2
                },
                {
                    "_id": "678b034021687367972a742f",
                    "title": "test",
                    "author": "test",
                    "published_date": "2024-01-03T00:00:00",
                    "genre": "test",
                    "price": 30.2
                }
            ]
        }

        self.new_book_data = {"title": "Book Four", "author": "Author D", "price": 25.99,
                              "published_date": "2022-03-04",
                              "genre": "test"}

    @patch("seek.src.models.books.Book.get_all")
    def test_get_books(self, mock_get_all):
        mock_get_all.return_value = self.mock_books
        response = self.client.get("/api/books/", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("total" in response.data)
        self.assertTrue("pages" in response.data)
        self.assertEqual(len(response.data.get("books")), 2)
        self.assertTrue(type(response))

    @patch("seek.src.models.books.Book.create")
    @patch("seek.src.models.books.Book.get_by_id")
    def test_create_book(self, mock_get_by_id, mock_create):
        mock_create.return_value = "4"
        mock_get_by_id.return_value = {**self.new_book_data, "id": "4"}

        response = self.client.post("/api/books/", data=self.new_book_data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.new_book_data["title"])

    def test_create_book_not_values(self):
        response = self.client.post("/api/books/", data={}, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("seek.src.models.books.Book.get_by_id")
    def test_get_book_detail(self, mock_get_by_id):
        mock_get_by_id.return_value = self.mock_books.get("books", [{}])[0]

        response = self.client.get(f"/api/books/{self.mock_books.get("books", [{}])[0].get("_id", "")}/",
                                   **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "test")

    @patch("seek.src.models.books.Book.update")
    @patch("seek.src.models.books.Book.get_by_id")
    def test_update_book(self, mock_get_by_id, mock_update):
        updated_data = {"title": "Updated Book One"}
        mock_update.return_value = True
        mock_get_by_id.return_value = {**self.mock_books.get("books", [{}])[0],
                                       **updated_data}

        response = self.client.put(f"/api/books/{self.mock_books.get("books", [{}])[0].get("_id", "")}/",
                                   data=updated_data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book One")

    @patch("seek.src.models.books.Book.delete")
    def test_delete_book(self, mock_delete):
        mock_delete.return_value = True

        response = self.client.delete(f"/api/books/{self.mock_books.get("books", [{}])[0].get("_id", "")}/",
                                      **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch("seek.src.models.books.Book.average_price_by_year")
    def test_average_price(self, mock_average_price_by_year):
        mock_average_price_by_year.return_value = 13.49
        response = self.client.get("/api/books/average-price/2020/", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["average_price"], 13.49)
