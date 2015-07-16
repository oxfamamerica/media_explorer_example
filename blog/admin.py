from django.contrib import admin
from blog.models import Blog
from blog.forms import BlogAdminForm

class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm


admin.site.register(Blog , BlogAdmin)

