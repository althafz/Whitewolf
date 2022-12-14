from django import forms
from store.models import Products, Variation
from catagory.models import Catagory

class CatagoryForm(forms.ModelForm):
  
  class Meta:
     model = Catagory
     fields = ['catagory_name', 'slug', 'description', 'cat_image']
  
  def __init__(self, *args, **kwargs):
    super(CatagoryForm, self).__init__(*args, **kwargs)
    
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'form-control'
  
class ProductForm(forms.ModelForm):
  
  class Meta:
     model = Products
     fields = ['product_name', 'slug', 'description', 'price', 'image', 'catagory', 'stock', 'is_available']
  
  def __init__(self, *args, **kwargs):
    super(ProductForm, self).__init__(*args, **kwargs)
    
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'form-control'
    
    self.fields['is_available'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'
    
    
class VariationForm(forms.ModelForm):
  
  class Meta:
    model = Variation
    fields = ['product', 'variation_catagory', 'variation_value', 'is_active']
  
  def __init__(self, *args, **kwargs):
    super(VariationForm, self).__init__(*args, **kwargs)
    
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'form-control'
      
    self.fields['is_active'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'