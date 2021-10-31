from django.contrib import admin
from .models import Tree, Link
# Register your models here.

class TreeAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Tree, TreeAdmin)
admin.site.register(Link)