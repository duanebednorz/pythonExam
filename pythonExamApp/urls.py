from django.urls import path, include
from . import views

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('viewQuotes', views.viewQuotes),
    path('addQuote', views.addQuote),
    path('oneQuote/<int:oneQuoteID>', views.oneQuote),
    path('newLike/<int:oneQuoteID>', views.newLike),
    path('unLike/<int:oneUserID>',views.unLike),
    path('oneQuote/<int:oneQuoteID>/delete', views.deleteQuote),
    path('oneQuote/<int:oneQuoteID>/update', views.updateQuote),
    path('viewAccount/<int:oneUserID>', views.viewAccount),
    path('editAccount/<int:oneUserID>', views.editAccount),
    path('user/<int:userID>', views.userQuotes)
]