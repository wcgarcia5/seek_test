from django.urls import path

from .src.views.books import (
    BookView,
    BookDetailView,
    BookAveragePriceView,
    BulkBookCreateView,
)
from .src.views.users import UserCreateView,CustomTokenObtainPairView,CustomTokenRefreshView

urlpatterns = [
    # API Endpoints
    path("books/", BookView.as_view(), name="books-list"),
    path("books/migrate/", BulkBookCreateView.as_view(), name="books-migrate"),
    path("books/<str:book_id>/", BookDetailView.as_view(), name="book-detail"),
    path(
        "books/average-price/<int:year>/",
        BookAveragePriceView.as_view(),
        name="book-average-price",
    ),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateView.as_view(), name="user-register"),
]
