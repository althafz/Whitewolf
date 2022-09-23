
from django.db import models
from catagory.models import Catagory
from django.urls import reverse

# Create your models here.

class Products(models.Model):
    product_name    = models.CharField(max_length=150, unique=True)
    slug            = models.SlugField(max_length=150, unique=True)
    description     = models.TextField(max_length=300, blank= True)
    price           = models.IntegerField()
    image           = models.ImageField(upload_to='pictory/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True) 
    catagory        = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    
    
    def get_url(self):
        return reverse('product_detail', args=[self.catagory.slug, self.slug])
    
    def __str__(self):
        return self.product_name
    
    