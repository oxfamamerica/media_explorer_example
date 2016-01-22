from django.contrib import admin
from blog.models import Blog

class BlogAdmin(admin.ModelAdmin):
    '''
    Blog Admin  
    '''

    search_fields = ('title','entry',)
    list_display = ('id','title','published')
    list_filter = ('published',)

admin.site.register(Blog, BlogAdmin)
