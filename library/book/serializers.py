from .models import Book, Transaction
from rest_framework import serializers 

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book 
        fields = "__all__"

# books/serializers.py
from rest_framework import serializers
from .models import Book, Transaction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "total_copies", "copies_available"]


class TransactionSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    book_author = serializers.CharField(source="book.author", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "book",          # user provides this when borrowing
            "book_title",
            "book_author",
            "borrowed_at",
            "due_date",
            "returned_at",
            "is_returned",
        ]
        read_only_fields = [
            "id",
            "book_title",
            "book_author",
            "borrowed_at",
            "due_date",
            "returned_at",
            "is_returned",
        ]


