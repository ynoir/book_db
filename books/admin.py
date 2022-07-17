from django.contrib import admin

from .models import Author
from .models import Book
from .models import Status
from .models import Series
from .models import Tag

admin.site.register(Author)
admin.site.register(Status)
admin.site.register(Book)
admin.site.register(Series)
admin.site.register(Tag)
