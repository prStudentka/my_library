from django.contrib import admin
from .models import Book, Category, Cart, Comment
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','exist')
    list_display_links = ('id','title')
    search_fields = ('title',)
    list_filter = ('id',)

admin.site.register(Book, BookAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', )
    search_fields = ('name',)
admin.site.register(Category, CategoryAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','date', 'status')
admin.site.register(Cart, CartAdmin)

class CommAdmin(admin.ModelAdmin):
    list_display = ('theme',)
    readonly_fields = ('date_update',"date")
admin.site.register(Comment, CommAdmin)