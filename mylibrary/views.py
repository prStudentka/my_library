from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth import logout, login

from basket.forms import BasketAddProductForm
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from .serializers import BookSerializer
from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    user = request.user
    if user.is_anonymous:
        user = 'Пользователь'
    return render(request, 'index.html', context={'user': user})

def listOfBooks(request):
    context = {'title': 'Список книг'}
    books = Book.objects.all()
    context['list'] = books
    return render(request, 'books.html', context=context)

def books_paginator(request):
    context = {'title': 'Книги'}
    books = Book.objects.all()
    context['list'] = books

    paginator = Paginator(books, 2)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context['page_obj'] = page_obj
    return render(request, 'book_list.html', context=context)

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    basket_form = BasketAddProductForm()
    return render(request, 'book-info.html', context={'bookInfo': book, 'basket_form': basket_form})

class CommentListView(ListView):
    model = Comment
    template_name = 'comment-list.html'
    context_object_name = 'list_comment'

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comment-info.html'
    context_object_name = 'detail'
    pk_url_kwarg = 'comment_id'

class CommentCreatView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment-add.html'
    context_object_name = 'form'

class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment-edit.html'
    context_object_name = 'form'

class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('list_com_view')


class BookCreatView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book-add.html'
    context_object_name = 'form'
    success_url = reverse_lazy('list')

    @method_decorator(permission_required('mylibrary.view_Book'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book-edit.html'
    context_object_name = 'form'

    @method_decorator(permission_required('mylibrary.view_Book'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('list')

    @method_decorator(permission_required('mylibrary.view_Book'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
        return redirect('log in')
    else:
        form = LoginForm()
    return render(request, 'login.html', context={'form': form})

def user_logout(request):
    logout(request)
    return redirect('log in')

def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('list')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

class API_BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class API_Book_get_put_delete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

def contact_email(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            msg = form.cleaned_data.get("sender") +' ' +form.cleaned_data['content']
            mail=send_mail(
                form.cleaned_data['subject'],
                msg,
                settings.EMAIL_HOST_USER,
                ['oper@mail.ru'],
                fail_silently=False,
            )

            if mail:
                success_message = 'Успешно'
                messages.success(request, success_message)
                return redirect('main')
    else:
        form = ContactUsForm()
    return render(request, 'email.html', {'form': form})

def listOfCategory(request):
    context = {'title': 'Категория книг'}
    category = Category.objects.all()
    context['list'] = category
    context['book'] = Book.objects.all()

    return render(request, 'category.html', context=context)

@login_required
def order(request):
    user = request.session['_auth_user_id']
    book = request.session['basket']
    books = Book.objects.all()
    tmp=[]
    for i in book.keys():
        tmp.append(books.get(id=i))

    instanse = Cart.objects.create(
        user_id=User.objects.get(pk=int(user)).pk
    )
    for item in tmp:
        instanse.books.add(item)

    context = {'title': 'Заказ'}
    context['list'] = Cart.objects.filter(pk=instanse.pk)
    context['books'] = tmp

    return render(request, 'order.html', context=context)
