from django.contrib import admin
from .models import BooksTable,UserTable,PaymentHistory,OrderHistory

# Register your models here.
admin.site.register(BooksTable)
admin.site.register(UserTable)
admin.site.register(PaymentHistory)
admin.site.register(OrderHistory)


