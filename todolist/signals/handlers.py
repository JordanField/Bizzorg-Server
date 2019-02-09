from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from groups.models import EmployeeProfile
<<<<<<< Updated upstream
from todolist.models import ToDoList, ToDoListItem
=======
from todolist.models import ToDoListItem
>>>>>>> Stashed changes
from django.contrib.auth.models import User
import logging
from django.core.exceptions import FieldError

# This runs whember a user is assigned to a To-Do list item and ensures that 
# assigned employees must be in the group of the to-do item.
@receiver(m2m_changed, sender = ToDoListItem.employees.through)
def to_do_list_employee_m2m_relationship_changed_handler(sender, **kwargs):
<<<<<<< Updated upstream
	if kwargs['action'] == 'pre_add':
		for employee_primary_key in kwargs['pk_set']:
			employee = EmployeeProfile.objects.get(pk=employee_primary_key)
			if employee not in kwargs['instance'].to_do_list.group.members.all():
				raise FieldError('Delegated users must be in the group of the to-do list')
=======
    if kwargs['action'] == 'pre_add':
    	# For each employee that has been assigned:
        for employee_primary_key in kwargs['pk_set']:
        	# Get the assigned employee
            employee = EmployeeProfile.objects.get(pk=employee_primary_key)
            # Check that the user us a member of the group, if not, raise an
            # error.
            if employee not in kwargs['instance'].group.members.all():
                raise FieldError(
                	'Delegated users must be in the group of the to-do list')
>>>>>>> Stashed changes
