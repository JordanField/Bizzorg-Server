from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class AllReadSuperuserWriteAuthorization(Authorization):
    '''
    This is used on Employee objects. Everyone can read employee
    details, but only VIP staff can change or delete them.
    '''
    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        if bundle.request.user.is_staff:
            return object_list
        else:
            raise Unauthorized('Only superusers can create users.')

    def create_detail(self, object_list, bundle):
        if bundle.request.user.is_staff:
            return True
        else:
            raise Unauthorized('superusers only')

    def update_list(self, object_list, bundle):
        if bundle.request.user.is_staff:
            return object_list
        else:
            raise Unauthorized('superusers only')

    def update_detail(self, object_list, bundle):
        return bundle.request.user.is_staff

    def delete_list(self, object_list, bundle):
        raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        raise Unauthorized()

class GroupAuthorization(Authorization):
    '''
    In order to keep users for seeing groups that they are not members 
    of, the authorization for employee groups allows group info to be
    read by all members and changed by group administrators. this means 
    that group administrators can add or remove employees, or change the 
    name of the group. People who are designated as VIP staff have all 
    priviliges however, and can also delete groups.
    '''

    def read_list(self, object_list, bundle):
        '''
        If the user is a VIP staff member, return all groups. If they are
        not, return only the groups that the user is a member of.
        '''
        request_user = bundle.request.user
        if request_user.is_staff:
            return object_list
        else:
            return object_list.filter(members = request_user.employee_profile)

    def read_detail(self, object_list, bundle):
        '''
        Return true if the user is either a member of the VIP staff list OR
        they are a member of the group requested.
        '''
        request_user = bundle.request.user
        return (request_user.employee_profile in bundle.obj.members.all() or
               request_user.is_staff)

    def create_list(self, object_list, bundle):
        '''
        If the user is a VIP staff member, allow all. if the user has groups
        they are an administator of, only allow groups which are sub-groups
        of the groups they admin.
        '''
        if bundle.request.user.is_staff:
            return object_list

        allowed = []
        for obj in object_list:
            # If the parent group is in the set of groups the user admins.
            if obj.parent_group in bundle.request.user.admin_of:
                # Allow the group.
                allowed.append(obj)
        return allowed


    def create_detail(self, object_list, bundle):
        '''
        Return true if the user is in the VIP staff list OR if the groups
        parents is one of the groups the user admins.
        '''
        return (bundle.request.user.is_staff or 
        bundle.obj.parent_group in bundle.obj.user.employee_profile.admin_of)
            

    def update_list(self, object_list, bundle):
        '''
        If the user is a VIP staff member, allow all. if the user has groups
        they are an administator of, only allow the groups they admin.
        '''
        if bundle.request.user.is_staff:
            return object_list
        else:
            return (
                object_list.filter(members = bundle.request.user)
                           .filter(groupmembership__admin_privileges = True)
            )

    def update_detail(self, object_list, bundle):
        '''
        Return true if the user is in the VIP staff list OR if the user
        is in the group's admins.
        '''
        return (bundle.request.user.is_staff
                or bundle.request.user in obj.admins.all())

    def delete_list(self, object_list, bundle):
        '''
        Only allow if the user is a member of the VIP staff.
        '''
        if bundle.request.user.is_staff:    
            return object_list
        else:
            raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        '''
        Only allow if the user is a member of the VIP staff.
        '''
        return bundle.request.user.is_staff