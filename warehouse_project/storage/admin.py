from django.contrib import admin
from .models import Tariffs, Cells, Clients, Orders

admin.site.register(Tariffs)
admin.site.register(Cells)
admin.site.register(Clients)
admin.site.register(Orders)
