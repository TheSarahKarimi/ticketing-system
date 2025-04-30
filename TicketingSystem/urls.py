from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

admin.site.site_header = 'Ticketing System'
admin.site.site_title = "Admin"
admin.site.index_title = "Welcome to the Ticketing System Admin"

urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path('auth/',include('Users.urls')),
    path('',include('Tickets.urls')),
] + debug_toolbar_urls()
