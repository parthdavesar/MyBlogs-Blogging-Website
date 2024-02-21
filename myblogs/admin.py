from django.contrib import admin
from .models import blog_category, blog_post, Comment, contact_info, subscription_info, likes

# Register your models here.

admin.site.register(blog_category)
admin.site.register(blog_post)
admin.site.register(Comment)
admin.site.register(contact_info)
admin.site .register(subscription_info)
admin.site .register(likes)