import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

from .models import Book, Author, Series, Status, Tag


def index(request):
    first_books_list = Book.objects.order_by('name')[:5]
    context = {'first_books_list': first_books_list}
    return render(request, 'books/index.html', context)

def books(request):
    books = Book.objects.order_by('name')
    context = {'books': books}
    return render(request, 'books/books.html', context)

def authors(request):
    authors = Author.objects.order_by('name')
    context = {'authors': authors}
    return render(request, 'books/authors.html', context)

def author(request, author_id):
    books = Book.objects.filter(author_id = author_id).order_by('name')
    context = {'books': books}
    return render(request, 'books/books.html', context)

def tags(request):
    tags = Tag.objects.order_by('name')
    context = {'tags': tags}
    return render(request, 'books/tags.html', context)

def tag(request, tag_id):
    books = Book.objects.filter(tags__id__exact=tag_id).order_by('name')
    context = {'books': books}
    return render(request, 'books/books.html', context)

def statuss(request):
    statuss = Status.objects.order_by('name')
    context = {'statuss': statuss}
    return render(request, 'books/statuss.html', context)

def status(request, status_id):
    books = Book.objects.filter(status_id = status_id).order_by('name')
    context = {'books': books}
    return render(request, 'books/books.html', context)




# def series(request):
#     return JsonResponse({
#         'data': json.loads(
#             serialize('json', Series.objects.order_by('name')))})
