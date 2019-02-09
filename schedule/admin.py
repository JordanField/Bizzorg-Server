from django.contrib import admin
from .models import ScheduleItem

class ScheduleItemInline(admin.StackedInline):
    """
    An admin object that allows an administrator to assign
    Schedule events in the employee-group page of the 
    admin site.
    """
    model = ScheduleItem
    # Denotes that only one extra section should be displayed.
    extra = 1
    # Defines the layout of the inline object.
    fieldsets = (
        (None, {
            'fields': ('title', 'priority', 'start', 'end')
        }),
        ('Extra options', {
            'classes': ('collapse',),
            'fields': ('description', 'employees',)
        })
    )