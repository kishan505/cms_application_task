from django.contrib import admin
from CMS_app.models import Post, Like, Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'profile_id',
        'user',
        'mobile_no',
        'country'
    ]

class PostAdmin(admin.ModelAdmin):
    list_display = [
        'post_id',
        'title',
        'creation_date',
        'author'
    ]

class LikeAdmin(admin.ModelAdmin):
    list_display = [
        'like_id',
        'post',
        'user'
    ]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)

