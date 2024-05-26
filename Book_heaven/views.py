from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from books.models import BooksTable
from django.contrib.auth import authenticate,login,logout







# Create your views here.

def home(request):
   data={}
   books=BooksTable.objects.all()
   data['books']=books
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
            return redirect('/')
    return render(request,'user/register.html',context=data)



def user_login(request):
    data={}
    if request.user.is_authenticated:
       def user_login(request):
          data ={}
          if request.user.is_authenticated:
             if request.user.is_superuser:
              return redirect("/admin")
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
               return redirect("/admin")
            else:
               return redirect("/")
    return render(request,'user/login.html',context=data)


def user_logout(request):
    logout(request)
    return redirect('/')

def admin_panel(request):
   if request.user.is_authenticated:
      if not request.user.is_superuser:
         return redirect("/")

   return render(request,'admin/admin.html')
   

