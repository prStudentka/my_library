from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='main'),

    path('books/', listOfBooks, name='list'),
    path('book-list/', books_paginator, name='paginator'),
    path('book-info/<int:book_id>/', book_detail, name='detail'),
    path('page/book-add/', BookCreatView.as_view(), name='add_book_view'),
    path('page/book-edit/<int:pk>/', BookUpdateView.as_view(), name='edit_book_view'),
    path('page/add/', CommentCreatView.as_view(), name= 'add_com_view'),
    path('view/edit/<int:pk>/', CommentUpdateView.as_view(), name='edit_com_view'),
    path('view/<int:comment_id>/', CommentDetailView.as_view(), name='info_com_view'),
    path('page/list/', CommentListView.as_view(), name='list_com_view'),

    path('book/del/<int:pk>/', BookDeleteView.as_view(), name='del_book_view'),
    path('page/del/<int:pk>/', CommentDeleteView.as_view(), name='del_com_view'),

    path('registration/', user_registration, name='regis'),
    path('login/', user_login, name='log in'),
    path('logout/', user_logout, name='log out'),

    path('api/book/', API_BookList.as_view(), name='api_list'),
    path('api/detail/<int:pk>/', API_Book_get_put_delete.as_view(), name='api_detail'),

    path('email/', contact_email, name='email'),

    path('category/', listOfCategory, name='list_category'),
    path('order/', order, name='client'),
]
