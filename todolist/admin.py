from django.contrib import admin
from .models import ToDoListItem

class ToDoListItemInline(admin.StackedInline):
    '''
    An inline object that allows To-Do list items to be create in the same
    page as employee groups.
    '''
    model = ToDoListItem
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('title', 'priority', 'completed')
        }),
        ('Extra options', {
            'classes': ('collapse',),
            'fields': ('description', 'deadline_date', 'employees',)
        })
    )