from django.contrib import admin
from .models import Ticket,Comment
from django.utils.html import format_html, urlencode
from django.urls import reverse


class CommentInLine (admin.TabularInline):
    autocomplete_fields = ['user']
    model = Comment
    extra = 0

@admin.register(Ticket)
class TicketAdmin (admin.ModelAdmin):
    autocomplete_fields = ['user']
    inlines = [CommentInLine]
    prepopulated_fields = {
        'slug':['title']
    }
    list_display = ['title','name','priority','status']
    list_editable = ['status']
    list_per_page = 10
    date_hierarchy = 'created_at'
    empty_value_display = '-empty-'
    search_fields = ['title', 'user__first_name', 'user__last_name']
    list_filter = ['priority','status']

@admin.register(Comment)
class CommentAdmin (admin.ModelAdmin):
    list_display= ['user','title_link','content']
    list_per_page = 10
    date_hierarchy = 'published_at'
    empty_value_display = '-empty-'
    search_fields = ['user__first_name', 'user__last_name','ticket__title','content']
    list_display_links = ['user','title_link']

    def title_link(self, obj):
        url = reverse('admin:Tickets_ticket_change', args=[obj.ticket.id])
        return format_html('<a href="{}">{}</a>', url, obj.ticket.title)
    
    title_link.short_description = 'Title'

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new and obj.ticket.status == Ticket.STATUS_OPEN and obj.user.is_staff:
            obj.ticket.status = Ticket.STATUS_IN_PROGRESS
            obj.ticket.save()