from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import *


class CategoryAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin,
                    list_display=(
                        'tree_actions',
                        'indented_title',
                    ),
                    list_display_links=(
                        'indented_title',
                    ))

admin.site.register(Item, list_display=('name', 'description', 'isArchived'))
admin.site.register(File, exclude=['itemId'])
admin.site.register(Photo, exclude=['itemId'])
admin.site.register(Fond)