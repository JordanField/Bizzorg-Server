from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from groups.api.resources import (
    EmployeeGroupResource, 
    EmployeeProfileResource, 
    UserResource, 
    GroupMembershipResource
)
from todolist.api.resources import ToDoListItemResource
from schedule.api.resources import ScheduleItemResource
from tastypie.api import Api

'''
Tastypie requires model resources to be linked to a central 'Api' object in 
order to connect to the webserver and serve JSON objects.
'''
bizzorg_api_v1 = Api(api_name='v1')
bizzorg_api_v1.register(UserResource())
bizzorg_api_v1.register(EmployeeGroupResource())
bizzorg_api_v1.register(EmployeeProfileResource())
bizzorg_api_v1.register(ToDoListItemResource())
bizzorg_api_v1.register(GroupMembershipResource())
bizzorg_api_v1.register(ScheduleItemResource())

urlpatterns = [
    #'bizzorg.uk/admin/'
    # Redirects the user to the Admin site.
    url(r'^admin/' , admin.site.urls), 

    #'bizzorg.uk/groups/'
    # Redirects the user to the groups section of the site, used for logging
    # in and out and changing profile picture.
    url(r'^groups/', include('groups.urls')),

    #'bizzorg.uk/api/v1/'
    # Allows access to the Tastypie-generated API.
    url(r'api/', include(bizzorg_api_v1.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)