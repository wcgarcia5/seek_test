from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.books import Book
from ..serializers.books import BookSerializer


class BookView(APIView):
    """
    endpoint for getting and creating books.

    requires authentication
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        get list of books
        Args:
            request: The incoming HTTP request object (page, page_size and filter).
        Returns:
            Response:
                A Response object containing a list of serialized Book objects
        """
        try:
            books = Book.get_all(request.GET)
            return Response(books, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """
        Creates a new book.

        Args:
            request: The request object.

        Returns:
            Response:
                - A Response object containing the newly created serialized Book object
                  and an HTTP status code of 201 (CREATED) if the creation is successful.
                - A Response object containing the serializer errors
                  and an HTTP status code of 400 (BAD REQUEST) if the data is invalid.
        """
        try:
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                book_id = Book.create(serializer.validated_data)
                created_book = Book.get_by_id(book_id)
                return Response(created_book, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BookDetailView(APIView):
    """
    end point to get, edit and delete books

    requires authentication
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, book_id: str):
        """
        query book by its mongoId
        Args:
            request: The request object
            book_id: MongoID

        Returns:
            Response:
            Object with book response
        """
        try:
            book = Book.get_by_id(book_id)
            if not book:
                return Response(
                    {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return Response(book, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, book_id: str):
        """
        Update book according to data sent in the request.
        Args:
            request: The request object
            book_id: MongoID

        Returns:
            Response:
            Object with updated book
        """
        try:
            serializer = BookSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                success = Book.update(book_id, serializer.validated_data)
                if not success:
                    return Response(
                        {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
                    )
                updated_book = Book.get_by_id(book_id)
                return Response(updated_book, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, book_id):
        """
        Delete book by its mongoID
        Args:
            request: The request object
            book_id: MongoID

        Returns:
            Response:
            object with an HTTP status code of 204 (NO CONTENT).
            if the deletion was successful.
        """
        try:
            success = Book.delete(book_id)
            if not success:
                return Response(
                    {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BookAveragePriceView(APIView):
    """
    Calculates the average price of books published in a specific year.

    requires authentication
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        """
        The average price of books published in the given year.

        Args:
            request: request object.
            year: The year for which to calculate the average price.

        Returns:
            Response:
                Object containing a dictionary with the year
        """
        try:
            average_price = Book.average_price_by_year(year)
            return Response(
                {"year": year, "average_price": average_price},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BulkBookCreateView(APIView):
    """
    Endpoint for creating multiple books in bulk.
    """

    def post(self, request):
        """
        Creates multiple books in bulk.

        Args:
            request: The request object containing a list of book data.

        Returns:
            Response:
                - A Response object containing a list of created books
                  and an HTTP status code of 201 (CREATED) if successful
        """
        try:
            if not isinstance(request.data, list):
                return Response(
                    {"error": "Expected a list of book objects."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = BookSerializer(data=request.data, many=True)
            if serializer.is_valid():
                created_ids = Book.create_many(serializer.validated_data)
                created_books = Book.get_by_ids(created_ids)
                return Response(created_books, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
