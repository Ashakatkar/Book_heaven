from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from books.models import BooksTable,CartTable,PaymentHistory,OrderHistory
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib import messages









# Create your views here.
books=BooksTable.objects.none()
def home(request):
   data={}
   cart_count=find_cart_value(request)
   data['cartvalue']=cart_count
   global books
   books=BooksTable.objects.filter(is_available=True)
   global filtered_books
   filtered_books=books
   data['books']=books
   return render(request,'home/index.html',context=data)


def filter_by_category(request,category_value):
   data={}
   cart_count=find_cart_value(request)
   data['cartvalue']=cart_count
   q1 = Q(is_available=True)
   q2 = Q(category=category_value)
   global books
   global filtered_books
   filtered_books=books.filter(q1 & q2)
   data['books']=filtered_books
   return render(request,'home/index.html',context=data)

def search_by_price_range(request):
   data={}
   cart_count=find_cart_value(request)
   data['cartvalue']=cart_count
   min=request.POST['min']
   max=request.POST['max']
   q1 = Q(is_available=True)
   q2 = Q(price__gte=min)
   q3 = Q(price__lte=max)
   searched_books = filtered_books.filter(q1 & q2 & q3)
   data['books']=searched_books
   return render(request,'home/index.html',context=data)

def sort_by_price(request,sort_value):
   data={}
   cart_count=find_cart_value(request)
   data['cartvalue']=cart_count
   global filtered_books
   if(sort_value=='asc'):
      sorted_books=filtered_books.filter(is_available=True).order_by('price')
   else:
      sorted_books=filtered_books.filter(is_available=True).order_by('-price')
   data['books']=sorted_books
   return render(request,'home/index.html',context=data)


def user_register(request):
    data={}
    if request.user.is_authenticated:
        return redirect('')
    if request.method=='POST':
        uname=request.POST['username']
        upass=request.POST['password']
        uconf_pass=request.POST['password2']
        
        if(uname=='' or upass=='' or uconf_pass==''):
            data['error_msg']="fields cant be empty"
            return render(request,'user/register.html',context=data)
        elif(upass!=uconf_pass):
            data['error_msg']="passwords does not matched"
            return render(request,'user/register.html',context=data)
        elif(User.objects.filter(username=uname).exists()):
            data['error_msg']=uname + " already exist"
            return render(request,'user/register.html',context=data)
        else:  
            new_user=User.objects.create(username=uname)
            new_user.set_password(upass)
            new_user.save()
            return redirect('/login')
    return render(request,'user/register.html',context=data)



def user_login(request):
    data={}
    if request.user.is_authenticated:
       def user_login(request):
          data ={}
          if request.user.is_authenticated:
             if request.user.is_superuser:
              return redirect("/adminpanel")
          else:
            return redirect("/")  
    if request.method=="POST":
      uname=request.POST['username']
      upass=request.POST['password']
      
      if (uname=="" or upass==""):
         data['error_msg']="Fields cant be empty"
      elif(not User.objects.filter(username=uname).exists()):
         data['error_msg']=uname + " user does not exist"
      else:
         user=authenticate(username=uname,password=upass)
         if user is None:
            data['error_msg']="Wrong password"
         else:
            login(request,user)
            if user.is_superuser:
               return redirect("/adminpanel")
            else:
               return redirect("/")
    return render(request,'user/login.html',context=data)


def user_logout(request):
    logout(request)
    return redirect('/')

# creating admin panel

def admin_panel(request):
   data={}
   if not request.user.is_superuser:
      return redirect("/")
   books=BooksTable.objects.all()
   data['books']=books
   return render(request,'admin/books/view_books.html',context=data)

def not_available(request):
   data={}
   books=BooksTable.objects.filter(is_available=False)
   data['books']=books
   return render(request,'admin/books/view_books.html',context=data)

def edit_book(request,int):
   data = {}
   book = BooksTable.objects.get(id=int)
   data['book'] = book
   if request.method=='POST':
      book.name = request.POST.get('name')
      book.price = request.POST.get('price')
      book.description=request.POST.get('description')
      book.quantity=request.POST.get('quantity')
      book.category=request.POST.get('category')
      if 'image' in request.FILES:
         book.images = request.FILES['image']
      book.is_available=(request.POST.get('is_available',False)) and ('is_available' in request.POST)
      book.save()
      return redirect('/adminpanel/')
   return render(request, 'admin/books/edit_book.html',context=data)

def add_to_cart(request,book_id):
   if not request.user.is_authenticated:
      return redirect ("/login")
   book=BooksTable.objects.get(id=book_id)
   if CartTable.objects.filter(uid=request.user.id,bid=book_id).exists():
      messages.error(request, "Product is already in the cart")   
      return redirect("/")
   else:
      cart=CartTable.objects.create(uid=request.user,bid=book)
      cart.save()
      messages.success(request,"Product is added to the cart")
      return redirect("/")
   
def find_cart_value(request):
   user_id = request.user.id
   cart=CartTable.objects.filter(uid=user_id)
   cart_count=cart.count()
   return cart_count

def update_quantity(request,flag,cartid):
   cart=CartTable.objects.get(id=cartid)
   if flag == "inc":
      cart.quantity+=1
      cart.save()
   else:
      if cart.quantity == 1:
         cart.delete()
      else:
         cart.quantity-=1
         cart.save()
   return redirect ("/cart")
   


import razorpay
def cart(request):
   data1={}
   total_price = 0
   data1["total_books"]=0
   books_in_cart=CartTable.objects.filter(uid=request.user.id)
   data1['carts']=books_in_cart
   for book in books_in_cart :
      total_price += book.bid.price*book.quantity
      data1['total_books']+=book.quantity
   data1['total_price'] = total_price
   if total_price>1 :
      client = razorpay.Client(auth=("rzp_test_zGa1u6UMdGpjQT", "wwe08RL8jeD8T4Y4KaOz1SDP"))
      data = { "amount": int((total_price)*100), "currency": "INR", "receipt": "order_rcptid_11" }
      payment = client.order.create(data=data)
   return render(request,'user/cart.html',context=data1)



def cart_delete(request,cart_id):
   cart=CartTable.objects.get(id=cart_id)
   cart.delete()
   return redirect("/cart")
  
def order(request,payment_id,amount):
   payment=PaymentHistory.objects.create(id=payment_id,user=request.user,amount=int(amount)/100)
   cart=CartTable.objects.filter(uid=request.user.id)
   for book in cart:
      orders=OrderHistory.objects.create(paymentid=payment,userid=request.user,bookid=book.bid)
      orders.save()
   cart.delete()
   return redirect("/")

def my_books(request):
    data={}
    books=OrderHistory.objects.filter(userid=request.user.id)
    data['order']=books
    return render(request,'user/my_books.html',context=data)




