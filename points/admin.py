from django.contrib import admin
from .models import Point, Message

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id','owner','latitude','longitude','created_at')
    list_filter = ('owner','created_at')
    search_fields = ['owner__username',]
    ordering = ('-created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','point','author','content','created_at')
    list_filter = ('point','author','created_at')
    search_fields = ['author__username','content']
    ordering = ('-created_at',)


