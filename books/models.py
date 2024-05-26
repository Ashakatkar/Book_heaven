from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BooksTable(models.Model):
   id=models.AutoField(primary_key=True)
   name=models.CharField(max_length=100)
   price=models.IntegerField()
   description=models.CharField(max_length=100,null=True)
   quantity=models.IntegerField(default=1)
   category=models.CharField(max_length=100)
   image=models.ImageField(upload_to='image')
   author=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
   is_availabe=models.BooleanField(default=False)

class UserTable(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    book_id= models.ForeignKey(BooksTable,on_delete=models.CASCADE,db_column='pid')
    address=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=10)
    is_author=models.BooleanField(default=False)

