from django.contrib import admin
from node.models import NodeName, Connection

# Register your models here.

admin.site.register(NodeName)
admin.site.register(Connection)