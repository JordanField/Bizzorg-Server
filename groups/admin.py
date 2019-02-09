from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import EmployeeGroup, GroupMembership, EmployeeProfile
from django.contrib.auth.models import User
from todolist.models import ToDoListItem
from todolist.admin import ToDoListItemInline
from schedule.models import ScheduleItem
from schedule.admin import ScheduleItemInline

'''
The admin.py module controls what the automatically generated 
admin site looks like. A programmer can create custom admin 
"views" from the base classes, this allows related objects to 
be placed inline with the related objects, making things easier 
for VIP Staff to manage.
'''

class EmployeeGroupInline(admin.StackedInline):
    '''
    Adds a list of members to the group edit page.
    '''
    model = GroupMembership
    extra = 1
    verbose_name = 'membership'

class SubGroupInline(admin.StackedInline):
    '''
    Adds a list of subgroups to the group edit page.
    '''
    model = EmployeeGroup
    extra = 1
    verbose_name = 'Sub-group'
    verbose_name_plural = 'Sub-groups'

class EmployeeProfileInline(admin.TabularInline):
    '''
    Adds the EmployeeProfile model as an inline to the user 
    model in the admin console so they can be easily added 
    together.
    '''
    model = EmployeeProfile
    can_delete = False
    verbose_name_plural = 'employee profile'

def full_name(user):
    '''
    a small function that takes in a user model and returns
    the user's full name.
    '''
    return ("%s, %s" % (user.last_name, user.first_name))

# A string which denotes the name of the corresponding column
# on the admin site.
full_name.short_description = 'Name'

# Denotes that the full name column should be dealt with by
# the 'full_name' function
User.full_name = full_name

# Denotes that, when ordering by name, the last name should
# be used for ordering.
User.full_name.admin_order_field = 'last_name'

# Create a new User Admin page with the added profile inline.
class UserAdmin(BaseUserAdmin):
    list_display = (full_name, 'employee_profile', 'email', 'username')
    inlines = [
        EmployeeProfileInline,
    ]

# Create a new group admin page with the new inlines
class EmployeeGroupAdmin(admin.ModelAdmin):
    list_display = ('name', str, 'parent_group')
    inlines = [
        SubGroupInline,
        EmployeeGroupInline,
        ToDoListItemInline,
        ScheduleItemInline
    ]
    exclude = ('members',)

# Reregister the new User admin page
admin.site.site_header = 'Bizzorg Administration'
admin.site.site_title = 'Bizzorg admin'
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(EmployeeGroup, EmployeeGroupAdmin)
