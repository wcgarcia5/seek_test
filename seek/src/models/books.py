import json
from datetime import datetime
from typing import Dict

from bson import ObjectId

from ..databases.mongo import db
from ..utils import utils


class Book:
    """
        Represents a book in the system.
    """

    def __init__(self, title, author, published_date, genre, price):
        self.title = title
        self.author = author
        self.published_date = published_date
        self.genre = genre
        self.price = price

    @staticmethod
    def create(book_data: Dict) -> str:
        """
        Creates a new book in the database.

        Args:
            book_data (Dict): dictionary with the data of the book to be created.

        Returns:
            str: ID of the book created in the database.
        """
        book_data = utils.convert_dates(book_data)
        result = db.books.insert_one(book_data)
        return str(result.inserted_id)

    @staticmethod
    def get_all(data: Dict) -> Dict:
        """
        Gets all paginated database books.
        Args:
            data (Dict): optional dictionary with filtering and pagination parameters.
                - page (int, optional): Page number (default 1).
                - page_size (int, optional): Number of books per page (default 10).
                - filter (str, optional): JSON filter to search for specific books.

        Returns:
            dict: Dictionary with books and pagination information
        """

        page = int(data.get("page", 1))
        page_size = int(data.get("page_size", 10))
        skip = (page - 1) * page_size
        limit = page_size

        where = json.loads(data.get("filter", "{}")) if "filter" in data else {}
        books = db.books.find(where).skip(skip).limit(limit)
        total_books = db.books.count_documents(where)
        total_pages = (total_books + page_size - 1) // page_size

        return {
            "total": total_books,
            "pages": total_pages,
            "current_page": page,
            "books": [
                {**book, '_id': str(book['_id'])}
                for book in books
            ]
        }

    @staticmethod
    def get_by_id(book_id: str) -> Dict:
        """
        Gets a book by its ID.
        Args:
           book_id: bookID of the book to search for.
        Returns:
            dict: Dictionary with book information
        """
        book = db.books.find_one({'_id': ObjectId(book_id)})
        if book:
            book['_id'] = str(book['_id'])
        return book

    @staticmethod
    def update(book_id: str, updated_data: Dict) -> bool:
        """
        Updates the data of an existing book in the database.

        Args:
            book_id (str): ID of the book to be updated.
            updated_data (Dict): Dictionary with updated book data.

        Returns:
            bool: True the book was updated successfully, False otherwise.
        """
        result = db.books.update_one({'_id': ObjectId(book_id)}, {'$set': updated_data})
        return result.matched_count > 0

    @staticmethod
    def delete(book_id: str) -> bool:
        """
        Deletes a book from the database by its ID.
        Args:
            book_id: The ID of the book to delete.

        Returns:
            True if the book was successfully deleted, False otherwise.
        """
        result = db.books.delete_one({'_id': ObjectId(book_id)})
        return result.deleted_count > 0

    @staticmethod
    def average_price_by_year(year: int) -> int:
        """
        Calculates the average price of books published in a given year.
        Args:
            year: The year for which to calculate the average price.

        Returns:
            The average price of books published in the specified year,
            or 0 if no books were found for that year.
        """
        pipeline = [
            {
                "$match": {
                    "published_date": {
                        "$gte": datetime(year, 1, 1),
                        "$lt": datetime(year + 1, 1, 1)
                    }
                }
            },
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}}
        ]
        result = list(db.books.aggregate(pipeline))
        return result[0]['average_price'] if result else 0

    @staticmethod
    def create_many(book_data_list):
        """
        Bulk create books.

        Args:
            book_data_list: List of validated book data.

        Returns:
            List of created book IDs.
        """
        # Insert many documents into the database
        book_data_list = utils.convert_dates(book_data_list)
        result = db.books.insert_many(book_data_list)
        return result.inserted_ids

    @staticmethod
    def get_by_ids(ids):
        """
        Fetch multiple books by their IDs.

        Args:
            ids: List of MongoDB IDs.

        Returns:
            List of book documents.
        """

        return [
            str(book['_id'])
            for book in list(db.books.find({"_id": {"$in": ids}}))
        ]
