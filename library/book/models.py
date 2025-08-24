from django.db import models
from django.conf import settings

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200) 
    isbn = models.CharField(max_length=16, unique=True, db_index=True) 
    total_copies = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False) 

    def __str__(self):
        status = "Returned" if self.is_returned else "Borrowed"
        return f"{self.user} → {self.book} ({status})"