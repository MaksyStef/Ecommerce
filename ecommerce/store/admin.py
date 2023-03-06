from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Knife)
class KnifeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Melee)
class MeleeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Souvenir)
class SouvenirAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Flashlight)
class FlashlightAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Accompanying)
class AccompanyingAdmin(admin.ModelAdmin):
    pass



@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    pass