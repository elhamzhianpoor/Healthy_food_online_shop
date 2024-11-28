from django.contrib import admin
from home.models import *
import admin_thumbnails


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1


@admin_thumbnails.thumbnail('image')
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_price', 'modified', 'available_products','likes_count','stock','status','average')
    search_fields = ('name',)
    list_filter = ('available_products',)
    prepopulated_fields = {
        'slug': ('name',)
    }
    raw_id_fields = ('diet_category','main_menu' ,'menu_item')
    inlines = [VariantInline,ImageInline]
    list_editable = ('unit_price', 'stock')


@admin.register(DietCategory)
class DietCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'created', 'modified')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created','rate','is_reply','body')


@admin.register(PriceChange)
class PriceChangeAdmin(admin.ModelAdmin):
    list_display = ('product','variant', 'unit_price', 'date')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'created', 'modified')
    prepopulated_fields = {
        'slug': ('name',)
    }


admin.site.register(Size)
admin.site.register(CookedSteak)
admin.site.register(MainMenu)



