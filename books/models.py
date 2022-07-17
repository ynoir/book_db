from django.db import models


class Author(models.Model):    
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField(default=0)
    series = models.ForeignKey(Series, on_delete=models.DO_NOTHING, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.name
