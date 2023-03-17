from .models import Product
def global_context(request):
    catalogue = {}
    for subclass in Product.__subclasses__():
        catalogue[subclass.__name__] = subclass.get_absolute_url_to_type()
    return {
        'supercategories' : catalogue,
    }
