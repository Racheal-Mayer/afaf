from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('adduser', views.adduser),
    path('login', views.login),
    path('success', views.success),
    path('destroy', views.destroy),	 
    path('addquote', views.addquote),
    path('edit/<int:quote_id>', views.edit),
    path('process_edit/<int:quote_id>', views.process_edit),
    path('delete/<int:quoteId>', views.deletequote),
    path('show/<int:uploaderId>', views.show),
    path('addtofav/<int:quoteId>', views.addToFav),
    path('removefromFav/<int:quoteId>', views.removefromFav),
]