from django.db import models
from django.urls import reverse #generates urls by reversing url patterns
import uuid # needed for instances of books (specific copies)
from django.contrib.auth.models import User # allows use of info of user
from django.conf import settings

# Create your models here.

class Genre(models.Model):
  name = models.CharField(max_length=200, help_text="Enter a genre")

  def __str__(self):
    return self.name

class Author(models.Model):
  first_name = models.CharField(max_length=25)
  last_name = models.CharField(max_length=35)
  date_of_birth = models.DateField(null=True, blank=True)
  date_of_death = models.DateField('Died', null=True, blank=True)
  
  # possibly scrape to add info from wikipedia
  
  def get_absolute_url(self):
    return reverse('author-detail', args=[str(self.id)])
  
  def __str__(self):
    return '%s, %s' % (self.last_name, self.first_name)  

class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
  summary = models.TextField(max_length=1000, help_text="Enter brief description of the book") # add scraper to pull summaries from another source like amazon or barnes and noble
  # isbn = models.CharField('ISBN', max_length=13, help_text="ISBN #") # is this necessary?
  genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="UUID for this particular copy of the book")
  book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
  due_date = models.DateField(null=True, blank=True)
  book_owner = models.ForeignKey(settings.AUTH_USER_MODEL)  # add code to indicate which user owns this book

  LOAN_STATUS = (
    ('m', 'Maintenance'),
    ('o', 'On loan'),
    ('a', 'Available'),
    ('r', 'Reserved'),
  )
  
  status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='Book availability')

  class Meta:
    ordering = ["due_date"]

  def __str__(self):
    return '%s (%s)' % (self.id, self.book.title)
