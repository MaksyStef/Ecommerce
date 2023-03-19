from .models import Product
def global_context(request):
    catalogue = {}
    for subclass in Product.__subclasses__():
        catalogue[subclass.__name__] = subclass
    return {
        'supercategories' : catalogue,
    }
