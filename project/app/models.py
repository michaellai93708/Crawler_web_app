from django.db import models

# Create your models here.
class result_a(models.Model):
    Title = models.CharField(max_length = 1000)
    Link = models.CharField(max_length = 1000, unique = True)
    Author = models.CharField(max_length = 1000)
    Tag = models.CharField(max_length = 1000)
    Time = models.CharField(max_length = 1000)

class result_b(models.Model):
    Title = models.CharField(max_length = 1000)
    Link = models.CharField(max_length = 1000, unique = True)
    Author = models.CharField(max_length = 1000)
    Tag = models.CharField(max_length = 1000)
    Time = models.CharField(max_length = 1000)


class Trie(models.Model):
    parent_id = models.IntegerField(null = True)
    name = models.CharField(max_length = 100)

class article(models.Model):
    Title = models.CharField(max_length = 1000)
    Link = models.CharField(max_length = 1000, unique = True, null = True)
    Author = models.CharField(max_length = 1000, null = True)
    Tag = models.CharField(max_length = 1000, null = True)
    Date = models.CharField(max_length = 100)

