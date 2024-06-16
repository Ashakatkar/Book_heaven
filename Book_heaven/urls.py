"""
URL configuration for Book_heaven project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from books import views as bookviews
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('logout/', views.user_logout),
    path('login/', views.user_login),
    path('register/', views.user_register),
    path('publish', bookviews.publish),
    path('category/<category_value>', views.filter_by_category),
    path('sort/<sort_value>', views.sort_by_price),
    path('search/', views.search_by_price_range),
    # creating admin urls 
    path('adminpanel/', views.admin_panel),
    path('adminpanel/authorize/', views.not_available),
    path('adminpanel/edit_book/<int>', views.edit_book),
    # add to cart url
    path('addtocart/<book_id>', views.add_to_cart),
    path('cart/', views.cart),
    path('cartupdate/<cartid>/<flag>', views.update_quantity),
    path('deletecart/<cart_id>', views.cart_delete),
    path('order/<payment_id>/<amount>', views.order),
    path('mybooks/', views.my_books )


    


    

    
    
]


urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
