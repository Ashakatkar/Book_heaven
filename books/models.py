from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BooksTable(models.Model):
   id=models.AutoField(primary_key=True)
   name=models.CharField(max_length=100)
   price=models.IntegerField()
   description=models.CharField(max_length=100,null=True)
   quantity=models.IntegerField(default=1)
   choices=(("novel","Novel"),
            ("story","Story"),
            ("comic","Comics"),
            ("historical","Historical"))
   category=models.CharField(max_length=100,choices=choices)
   image=models.ImageField(upload_to='image')
   author=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
   is_available=models.BooleanField(default=False)

class UserTable(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    is_author=models.BooleanField(default=False)


class CartTable(models.Model):
   #uid_id
   uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
   bid = models.ForeignKey(BooksTable,on_delete=models.CASCADE,db_column='bid')
   quantity=models.IntegerField(default=1)

class PaymentHistory(models.Model):
   id=models.CharField(max_length=20,primary_key=True)
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   amount=models.IntegerField()

class OrderHistory(models.Model):
   id=models.AutoField(primary_key=True)
   paymentid=models.ForeignKey(PaymentHistory,on_delete=models.CASCADE)
   userid=models.ForeignKey(User,on_delete=models.CASCADE)
   bookid=models.ForeignKey(BooksTable,on_delete=models.CASCADE)
   date=models.DateField(auto_now=True)


