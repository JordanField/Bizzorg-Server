from django.db import models
from django.contrib.auth.models import Group, User
from django.core.exceptions import FieldError
from django.utils import timezone

def user_directory_path(instance, filename):
    """
    Profile pictures are stored in a folder that is denoted by
    the user's ID, this function takes in an instance of a saved
    profile picture, renames the file and puts it in the right place.

    - parameter instance: The instance of a user saving a profile picture.
    - parameter filename: The name of the file sent to the server.
    """
    # Find the filetype by splitting the filename into a list of
    # strings, with the separator being '.'
    split_file_name = filename.split(sep='.')

    # Retrieve the second to last string, which will be the file
    # extension. 
    filetype = split_file_name[len(split_file_name) - 1]

    # Find the current date.
    now = timezone.now()

    # File will be uploaded to 
    # MEDIA_ROOT/employee_profile/pictures/user_<id>/<filename>

    # File name will be
    # <current_year>_<current_month>_<current_day>.<file_format>
    return 'employee_profile/pictures/user_{0}/{1}_{2}_{3}.'.format(
        instance.user.id, now.year, now.month, now.day) + filetype

class EmployeeProfile(models.Model):
    """
    An extension of the User class, adding a profile picture and job position.

    Fields:
    user            -- A one-to-one relationship with the Django User class,
                    giving every user one employee profile.
    job_position -- A string detailing the job of the user.
    profile_picture -- A user-submitted (or pre-defined) photo assigned to a 
                    user.
    """
    user = models.OneToOneField(User, related_name='employee_profile', on_delete=models.CASCADE)
    job_position = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, 
                                        blank=True)

    def __str__(self):
        return "%s %s | %s" % (self.user.first_name, self.user.last_name, 
                               self.job_position)
        """
        Used in the admin portal in the employee group list page.
        """
        # Example __str__: "Joe Bloggs | Research and development"
        return "%s %s | %s" % (self.user.first_name, self.user.last_name, 
                               self.job_position)

    @property
    def admin_of(self):
        # An empty list that will be populated with the correct groups.
        groups = []
        # Find every membership object for this user where they are an admin.
        admin_memberships = self.memberships.filter(admin_privileges=True)
        # For each membership object
        for membership in admin_memberships:
            # Add the corresponding group to the group list.
            groups.append(membership.group)
        # Return the group list.
        return groups

#Ref: 1.2
class EmployeeGroup(models.Model):
    """
    Creates groups of Employees and gives them a to-do list and schedule 
    via the todolist and schedule apps.
    
    Fields:
    name            -- The name of the group.
    members         -- Many-to-many field going through membership linking 
                       users to their respective groups.
    parent_group    -- Optional foreign key relationship linking a group to 
                    another group as its parent.

    Methods:
    group_traceback -- Returns a full trace of the group's parents to the 
                       root group and returns as an array of EmployeeGroup 
                       objects.

    Properties:
    admins          -- Returns a QuerySet of the group's administrators.
    root_group      -- If the group has a parent, this will return the first 
                    level group.
    """
    name = models.CharField(max_length=100)
    members = models.ManyToManyField('groups.EmployeeProfile', 
                                    related_name='employee_groups', 
                                    through='GroupMembership')
    parent_group = models.ForeignKey('self', 
                                    related_name='children', 
                                    blank=True, null=True, on_delete=models.CASCADE) 

    #Ref: 1.2.A
    def group_traceback(self):
        # Create an empty list that the group_traceback list will 
        # be built from
        traceback_list = []                            
        # Set the current group to the group that called this method.
        current_group = self
        # Code will stop looping when the top of the group heirarchy 
        # is reached                            
        while current_group != None:
            # Add group to the traceback list.          
            traceback_list.insert(0, current_group)
            # Move one group up the group heirarchy.
            current_group = current_group.parent_group  
        # Once the root group has been reached, return the traceback list.
        return traceback_list 

    def __str__(self):
        return self.name

    @property 
    def admins(self):
        """returns a QuerySet of the admins of the group"""
        return self.members.filter(memberships__admin_privileges=True)

    @property
    def root_group(self):
        # The first check that needs to be done is that this group is not a
        # root group itself.
        p = self.parent_group 
        # If the group has no parent, return None to show there isn't a root
        # group.
        if p == None:
            return None

        #Keep running until told to stop.
        while True:
            # If the group has a parent group
            if p.parent_group != None:
                # Set the current group to the parent group.
                p = p.parent_group
            else:
                # Stop the loop if there is no more parents.
                break
        # Return the root group.
        return p

    def save(self, *args, **kwargs):
        """
        Saving a group requires some checking before it can be done, to ensure
        that an infinite parent group relationship has been created, in order 
        to prevent this, this algorithm moves its way up the group heirarchy 
        tree checking that a circular relationship is not present.
        """
        # An empty list that will track whether there is a non-tree like
        # relationship created.
        tracker_list = []
        # Start searching at the saved group.
        current_group = self 
        # While there is a parent group present
        while current_group != None:
            # If a group is referenced already in the heirarchy tree:
            if tracker_list.count(current_group) > 0:
                # This is not a validated group relationship, so raise an error.
                raise FieldError('Infinite parent_group relationship detected.')
            else:
                # Now that this group has been validated, move one group up the
                # tree and start the loop over again.
                tracker_list.append(current_group)
                current_group = current_group.parent_group

        # If this loop completes without raising an error. The group
        # relationship is validated, so it is safe to save it to the database.
        super(EmployeeGroup, self).save(*args, **kwargs)

class GroupMembership(models.Model):
    """
    The intermediary table that links Users with Groups, and determines whether 
    they can edit the group.

    Fields:
    user                -- The user the membership is for.
    group               -- What group the user is to be a member of.
    admin_privileges    -- A boolean value determining whether the user is an 
                        administrator of the group. 
    """
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, 
        related_name="memberships")
    group = models.ForeignKey(EmployeeGroup, on_delete=models.CASCADE)
    admin_privileges = models.BooleanField()

    def __str__(self):
        return self.employee.user.first_name + " > " + self.group.name
