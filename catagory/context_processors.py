from .models import Catagory

def menu_link(request):
    cat_links = Catagory.objects.all()
    return dict(cat_links=cat_links)
    