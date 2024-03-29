from django.contrib import admin

from .models import Comment, Follow, Group, Like, Post, Profile_id


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    empty_value_display = '-пусто-'
    search_fields = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post', 'author', 'text', 'created')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text_profile', 'author')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Profile_id, ProfileAdmin)
admin.site.register(Like, LikeAdmin)
