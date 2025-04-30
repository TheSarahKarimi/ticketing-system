from django.contrib import admin
from .models import CustomUser
from Tickets.models import Ticket
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['fullname','id','email','Total_Tickets']
    search_fields = ['fullname']

    def Total_Tickets (self, Ticket):
        url = (reverse('admin:Tickets_ticket_changelist') 
               + '?' 
               + urlencode({
                   'user__id__exact':str(Ticket.id)
               }))
        return  format_html ('<a href="{}">{}</a>', url, Ticket.Total_Tickets) 
    
    Total_Tickets.short_description = 'Tickets'
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            Total_Tickets= Count ('ticket')
        )
