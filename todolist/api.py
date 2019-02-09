from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from .models import ToDoListItem

class ToDoListItemResource(ModelResource):
	todolist = fields.ForeignKey('todolist.api.ToDoListResource', 'to_do_list')
	employees = fields.ToManyField('groups.api.resources.EmployeeProfileResource', 'employees')

	class Meta:
		queryset = ToDoListItem.objects.all()
		resource_name = 'todolist/todolist_item'
		filtering = {
		'employees': ALL_WITH_RELATIONS
		}
		ordering = {
		'completed': ALL_WITH_RELATIONS
		}