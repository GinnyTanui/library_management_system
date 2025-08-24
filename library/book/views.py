from datetime import timedelta
from django.db import transaction as db_tx
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer
from accounts.permissions import IsLibrarianOrAdmin, isAdmin, IsMember
from rest_framework.views import APIView


LOAN_PERIOD_DAYS = 14 

class BookListView(generics.ListAPIView):    
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    permission_classes = [AllowAny]

class BookCreateAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    permission_classes = [IsLibrarianOrAdmin]  

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

class BookUpdateView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrAdmin] 

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class= BookSerializer
    permission_classes = [isAdmin]

class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated, IsMember]

    def post(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk) 

        with db_tx.atomic():
            ##db_tx.atmoic is used to start a database transaction, this means all the processes nside must succeed or nothing will be saved
            book = Book.objects.select_for_update().get(pk=book.pk)
            ##select_for_update() is a method that locks the rows
            ##it preents two transactions from simulatenously happening at the same time 
            if book.copies_available < 0:
                return Response({"detail": "No copies available for this book"}, status=status.HTTP_404_NOT_FOUND)
            
            exists_active = Transaction.objects.select_for_update().filter(
                user = request.user,
                book=book,
                is_returned=False
            ).exists()
            ##exists is a shortcut.Checks if the user already has a transaction for this book already
            ##if yes, it blocks borrowing for the books, prevents a user for cheking out two books at the same time 
            if exists_active:
                return Response({"detail: You already borrowed this book.Return it first"}, status=status.HTTP_400_BAD_REQUEST)
            due = timezone.now() + timedelta(days=LOAN_PERIOD_DAYS) 

            ##here we are now creating a transactionafter no transaction exists 
            transaction_made = Transaction.objects.create(
                user = request.user,
                book = book,
                due_date = due,
                is_returned = False
            )
            
            book.copies_available -= 1 
            book.save(update_fields=["copies_available"]) 

            return Response(TransactionSerializer(transaction_made).data, status=status.HTTP_201_CREATED)
        
class ReturnBookView(APIView):
    def post(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk) 

        with db_tx.atomic():
            book = Book.objects.select_for_update().get(pk=book.pk)
            transaction_made = Transaction.objects.select_for_update().filter(
                user = request.user,
                book=book, 
                is_returned=False
            ).first() 

            if not transaction_made: 
                return Response({"detail": "No active borrowing found for this book."},
                                status=status.HTTP_404_NOT_FOUND)
            
            transaction_made.is_returned=True 
            transaction_made.returned_at = timezone.now() 

            transaction_made.save(update_fields=["is_returned", "returned_at"])

            book.copies_available += 1
            book.save(update_fields=["copies_available"])

        return Response(TransactionSerializer(transaction_made).data, status=status.HTTP_200_OK)



class MyTransactionsView(generics.ListAPIView):
  
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return (
            Transaction.objects
            .filter(user=self.request.user)
            .select_related("book")
            .order_by("-borrowed_at")
        )