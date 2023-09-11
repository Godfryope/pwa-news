from django.contrib import admin
from .models import *

# Register your models here

admin.site.register(Category)
# admin.site.register(News)
class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(News, NewsAdmin)

