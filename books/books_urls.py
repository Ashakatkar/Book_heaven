from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.urls import path
from . import views 

urlpatterns = [
    path('',views.books),
    path('publish',views.publish),
]















urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)