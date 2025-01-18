from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .src.views.books import BookView, BookDetailView, BookAveragePriceView

urlpatterns = [
    path('books/', BookView.as_view(), name='books-list'),
    path('books/<str:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/average-price/<int:year>/', BookAveragePriceView.as_view(), name='book-average-price'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
