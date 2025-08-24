# books/urls.py
from django.urls import path
from .views import (
    BookListView, BookCreateAPIView, BookUpdateView, BookDeleteView,
    BorrowBookView, ReturnBookView, MyTransactionsView, BookDetailView
)

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/create/", BookCreateAPIView.as_view(), name="book-create"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
    path("books/<int:pk>/borrow/", BorrowBookView.as_view(), name="book-borrow"),
    path("books/<int:pk>/return/", ReturnBookView.as_view(), name="book-return"),
    path("transactions/mine/", MyTransactionsView.as_view(), name="my-transactions"),
]
