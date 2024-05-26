from django.shortcuts import render,redirect
from books.models import BooksTable



# Create your views here.

books = BooksTable.objects.filter()
def books(request):
    data = {}
    books = BooksTable.objects.filter()
    data['books'] = books
    return render(request,'books/books.html',context=data)

def publish(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.method=='POST':
        name=request.POST.get('name')
        price=request.POST.get('price')
        description=request.POST.get('description')
        quantity=request.POST.get('quantity')
        category=request.POST.get('category')
        image = request.FILES.get('image')
        

        book=BooksTable.objects.create(name=name,price=price,description=description,quantity=quantity,category=category,image=image,author=request.user)
        book.save()
        return redirect("/")
    return render(request,'author/publish.html')