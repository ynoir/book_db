import json
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.core.management.commands.dumpdata import Command as DumpDataCommand
from django.core.files.base import ContentFile

from .models import Book, Author, Series, Status, Tag

def fetch_cover_url(book):
    """
    Tries to find a cover URL using Open Library API.
    """
    if book.isbn:
        # Try by ISBN first
        isbn_clean = book.isbn.replace('-', '').replace(' ', '')
        url = f"https://covers.openlibrary.org/b/isbn/{isbn_clean}-M.jpg?default=false"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return url
        except requests.exceptions.RequestException:
            pass

    # Fallback to searching by title and author
    search_url = "https://openlibrary.org/search.json"
    params = {'title': book.name, 'author': book.author.name, 'limit': 1}
    try:
        response = requests.get(search_url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('docs'):
                cover_i = data['docs'][0].get('cover_i')
                if cover_i:
                    return f"https://covers.openlibrary.org/b/id/{cover_i}-M.jpg"
    except requests.exceptions.RequestException:
        pass
    
    return None

def index(request):
    return render(request, 'books/index.html')

def books(request):
    books = Book.objects.order_by('name')
    context = {'books': books}
    return render(request, 'books/books.html', context)

def fetch_book_cover(request, book_id):
    """
    AJAX view to fetch a single book cover, download it, and return the local URL.
    """
    try:
        book = Book.objects.get(id=book_id)
        
        # If we already have a local image, return it
        if book.cover_image:
            return JsonResponse({'image_url': book.cover_image.url})
            
        # If we marked it as 'none' before, don't try again
        if book.image_url == 'none':
            return JsonResponse({'image_url': None})

        # Find the external URL if we don't have it
        if not book.image_url:
            new_url = fetch_cover_url(book)
            if new_url:
                book.image_url = new_url
                book.save()
            else:
                book.image_url = 'none'
                book.save()
                return JsonResponse({'image_url': None})

        # Download the image and save it locally
        if book.image_url and book.image_url != 'none':
            try:
                response = requests.get(book.image_url, timeout=10)
                if response.status_code == 200:
                    file_name = f"cover_{book.id}.jpg"
                    book.cover_image.save(file_name, ContentFile(response.content), save=True)
                    return JsonResponse({'image_url': book.cover_image.url})
            except Exception as e:
                print(f"Error downloading image: {e}")
        
        return JsonResponse({'image_url': None})
        
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

def authors(request):
    authors = Author.objects.order_by('name')
    context = {'authors': authors}
    return render(request, 'books/authors.html', context)

def author(request, author_id):
    books = Book.objects.filter(author_id = author_id).order_by('name')
    context = {'books': books}
    return render(request, 'books/books.html', context)

def seriess(request):
    seriess = Series.objects.order_by('name')
    context = {'seriess': seriess}
    return render(request, 'books/seriess.html', context)

def series(request, series_id):
    books = Book.objects.filter(series_id = series_id).order_by('name')
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

def export(request):
    ddc = DumpDataCommand()
    return HttpResponse(ddc.handle(format = 'JSON', indent = 1, database = 'default'))
