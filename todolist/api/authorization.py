from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
import pdb

class GroupItemAuthorization(Authorization):
    '''
    The group item Authorization class denotes how auxilliary group objects
    (To-do list items, schedule events) can be viewed and who can view and
    edit them. The main procedure is to allow all members of the group to view
    items for that group, but only group admins should be allowed to create
    and edit items. Only VIP staff are able to delete items.
    '''

    def read_list(self, object_list, bundle):
        # Determine that user is logged in
        if not bundle.request.user.is_authenticated:
            raise Unauthorized()
       
        # Allow any items where the employee is part of the group the item
        # is assigned to.
        return object_list.filter(
            group__members=bundle.request.user.employee_profile
        )

    def read_detail(self, object_list, bundle):
        b = bundle
        # Return true if the item requested is assigned to a group the user
        # is in.
        return b.request.user.employee_profile in b.obj.group.members.all()

    def create_list(self, object_list, bundle):
        # Create a list of all the group the user is an admin of.
        admin_groups = bundle.request.user.employee_profile.admin_of

        # This is a rather complicated list comprehension, but all it is
        # saying is to add the group requested to an array only if that
        # group is being adminitrated by the user that requested this data.
        return [group for group in object_list if group in admin_groups]

    def create_detail(self, object_list, bundle):
        b = bundle
        # return true if the item's group is in the list of groups the user
        # is an admin of.
        return b.obj.group in b.request.user.employee_profile.admin_of

    # Updating data is the same as creating data.
    update_list = create_list
    update_detail = create_detail

    # Deleting data is not allowed.
    delete_list = lambda self, object_list, bundle: []
    delete_detail = lambda self, object_list, bundle: False
