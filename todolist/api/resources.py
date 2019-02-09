from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from todolist.models import ToDoListItem
from .authorization import GroupItemAuthorization
import pdb

class ToDoListItemResource(ModelResource):
    '''
    The TastyPie resource object for a To-do list item.
    '''

    # Link the employee group resource to the To-Do list item resource in
    # order to show the assigned group for a specific to-do item.
    group = fields.ForeignKey(
        'groups.api.resources.EmployeeGroupResource', 'group')

    # Link the employee profile resource to the To-Do list item resource in
    # order to display the assigned employees for specific to-do items
    employees = fields.ToManyField(
        'groups.api.resources.EmployeeProfileResource', 'employees', 
        full = True)

    class Meta:
        queryset = ToDoListItem.objects.all()

        # See details for the ToDoListItemAuthorization at 
        # todolist/api/authorization.
        authorization = GroupItemAuthorization()
        resource_name = 'todolist-items'
        filtering = {
        'employees': ALL_WITH_RELATIONS,
        'group': ALL_WITH_RELATIONS
        }
        ordering = {
        'completed': ALL_WITH_RELATIONS
        }

    def save_m2m(self, bundle):
        '''
        Saving an many-to-many object often causes problems, as multiple
        links to the same person can be applied, causing the employee to 
        assigned more than once. Also, if a PATCH request is made and assigned
        members are ommited so as to say they shouldn't be changed this 
        caused the assigned employees to be deleted, so I had to create a fix
        for that.
        '''
        # Retrieve the object the request is making changes to.
        obj = bundle.obj

        # Retrieve the employees before changes are made.
        original_employees = obj.employees.all()

        # Retrieve the new bundle containing the (possible) new assigned
        # employees.
        new_bundle = bundle.data['employees']

        # Find the server model representation for each employee and create
        # a list of them.
        new_employees = [employee_raw.obj for employee_raw in new_bundle]

        # If the list of new employees is empty, assume this means that the
        # user did not want to change the assigned employees and save the
        # originals back into the database. If there are assigned employees,
        # save them into the database instead.
        if len(new_employees) == 0:
            obj.employees.set(original_employees)
        else:
            obj.employees.set(new_employees)
        obj.save()

