from django.contrib import admin
from maiagogo.models import  Post, Comment, Category, Page, UserProfile

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(UserProfile)

