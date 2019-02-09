from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import Authentication, SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.http import HttpBadRequest
from groups.models import EmployeeGroup, EmployeeProfile, GroupMembership
from django.contrib.auth.models import User
from .authorization import AllReadSuperuserWriteAuthorization, GroupAuthorization

class EmployeeProfileResource(ModelResource):
    '''
    The TastyPie resource for an Employee profile.
    '''

    # Link the user object to its corresponding employee profile object,
    # 'full=True' means that instead of showing a link to a user API object
    # it will present all the JSON as an internal dictionary.
    user = fields.ToOneField(
        'groups.api.resources.UserResource', 'user', full=True)

    # Link the user API object to the groups that user is an administrator of.
    administrating = fields.ToManyField(
        'groups.api.resources.EmployeeGroupResource', 'admin_of', null=True)
    
    class Meta:
        # Users are only allowed to add and change objects via the API, not
        # delete them. the allowed_methods attribute achieves this.
        allowed_methods = ['get', 'patch', 'put', ]

        # Sets the objects to be all employee profiles.
        queryset = EmployeeProfile.objects.all()

        # Sets the resource name, which is used as the URL.
        # e.g. '/api/v1/employees/''
        resource_name = 'employees'

        # the Authentication attribute tells Tastypie that only logged-in
        # users are able to view this object in the API.
        authentication = SessionAuthentication()

        # Links to a custom-written authorization object that allows all users
        # to see the data, but only VIP staff to change it.
        authorization = AllReadSuperuserWriteAuthorization()

        # Determines which fields a user is able to filter data with.
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'employee': ALL_WITH_RELATIONS
        }

class UserResource(ModelResource):
    '''
    The Tastypie resource object for a core Django user model.
    '''
    class Meta:
        # Since the user api object will never actually be seen directly (it
        # is linked to the API via the EmployeeProfileResource class) the
        # only method that should be allowed is to change an existing user,
        # all other tasks should be done via the admin site.
        allowed_methods = ['patch',]

        # Sets the selection to all users.
        queryset = User.objects.all()

        # (Unused) '/api/v1/users/'
        resource_name = 'users'

        # Excludes sensitive and irrelevant data like password and user ID.
        excludes = ['password', 'is_active', 'is_superuser', 
                    'date_joined', 'last_login', 'id', 'resource_uri']

        #See authentication property in EmployeeProfileResource above.
        authentication = SessionAuthentication()

        #See authorization property in EmployeeProfileResource above.
        authorization = AllReadSuperuserWriteAuthorization()
        
        filtering = {
            'username': ALL,
            'employee': ALL_WITH_RELATIONS
        }

        
class GroupMembershipResource(ModelResource):
    '''
    Tastypie resource object for a group membership (including admin rights)
    '''

    # Connects the employee profile object to the membership class.
    employee = fields.ToOneField(
        'groups.api.resources.EmployeeProfileResource', 'employee', full=True)

    # Connects the group object to the membership class.
    group = fields.ToOneField(
        'groups.api.resources.EmployeeGroupResource', 'group')

    def save_m2m(self, bundle):
        pass

    class Meta:
        # Sets the selection to all group memberships
        queryset = GroupMembership.objects.all()

        # Sets the available fields. 
        fields = ['admin_privileges', 'employee']

        #See authenticaction property in EmployeeProfileResource above.
        authentication = SessionAuthentication()

        # Sets the authorization to the custom group authentication, which is
        # described in authorization.py.
        authorization = GroupAuthorization()
        
        filtering = {
            'admin_privileges': ALL_WITH_RELATIONS,
            'employee': ALL_WITH_RELATIONS
        }

class EmployeeGroupResource(ModelResource):
    '''
    Tastypie resource object for an employee group.
    '''
    # Connects the parent group attribute to the tastypie resource
    # class.
    parent_group = fields.ForeignKey('self', 'parent_group', null=True)
    '''
    Since I am using an extra "groupmembership" object to link employees
    to employee groups only providing a many-to-many connection without
    the through link omits data from the API resource class, breaking some
    functionality in the client. As such, there are two different fields
    for the members of a group, members_full is a read-only field that
    shows all data (e.g. admin privileges) whereas members is a writable,
    filterable field that only shows the data URIs for the members.
    When adding members to a group that also have admin privileges, the
    API uses two seperate lists, 'members' and 'admins', which are used
    once sent to create the appropriate groupmembership objects.
    '''
    members_full = fields.ToManyField(GroupMembershipResource, 
        attribute = lambda bundle: bundle.obj.members.through.objects.filter(group=bundle.obj) or bundle.obj.members, 
        readonly=True, full=True)
    members = fields.ToManyField(EmployeeProfileResource, 'members', null=True)
    admins = fields.ToManyField(EmployeeProfileResource, 'admins', null=True)

    class Meta:
        # Denotes this API resource class is for all EmployeeGroup objects.
        queryset = EmployeeGroup.objects.all()

        # e.g. 'api/v1/employee-groups/'
        resource_name = 'employee-groups'

        #See authenticaction property in EmployeeProfileResource above.
        authentication = SessionAuthentication()

        # Sets the authorization to the custom group authentication, which is
        # described in authorization.py.
        authorization = GroupAuthorization()

        filtering = {
            'members': ALL_WITH_RELATIONS,
            'parent_group': ALL_WITH_RELATIONS,
            'name': ALL,
            'employee': ALL_WITH_RELATIONS,
            'members_full': ALL_WITH_RELATIONS,
        }

    def hydrate_name(self, bundle):
        '''
        When newly-created objects in the client are sent to the server
        the name of the new group is converted to all lowercase before it
        is created, to ensure consistency across all group names.
        '''
        bundle.data['name'] = bundle.data['name'].lower()
        return bundle

    def save_m2m(self, bundle):
        '''
        group member lists work differently in the API than in the native
        django model format, consisting of two seperate 'members' and
        'admins' lists instead of an intermediary model with an admin
        flag. As such, when objects are sent from the client to the server
        they must be converted into this format. 
        '''

        # Find the sent group.
        group = bundle.obj

        # If the sent object has no members assigned
        if bundle.data['members'] == None:
            # Bubble this error up to the server console.
            print("no_member_bundles")
            return

        # Set the member list to each employee object in the list of members
        # sent by the client.
        members = [member.obj for member in bundle.data['members']]

        # Set the member list to each employee object in the list of admins
        # sent by the client.   
        admins = [admin.obj for admin in bundle.data['admins']]
        
        # clear the current members of the group to prevent duplicates
        group.members.clear()

        for member in members:
            is_admin = member in admins
            # create a new group membership object with the 
            # member, group, and is_admin fields.
            group_membership = GroupMembership(
                employee=member, group=group, admin_privileges=is_admin)
            #Save the new membership to the database.
            group_membership.save()
