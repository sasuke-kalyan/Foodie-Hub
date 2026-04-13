from django.contrib import admin
from .models import ChatRoom, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['sender', 'sender_type', 'message', 'created_at']

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['customer', 'restaurant', 'is_active', 'created_at']
    inlines = [ChatMessageInline]
