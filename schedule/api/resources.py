from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from schedule.models import ScheduleItem
from todolist.api.authorization import GroupItemAuthorization

class ScheduleItemResource(ModelResource):
    '''
    The Tastypie resource class for schedule events
    '''
    # Connects schedule event resources to their groups in the API
    group = fields.ForeignKey(
        'groups.api.resources.EmployeeGroupResource', 'group')

    # Connects schedule event resources to the employees they are assigned to.
    employees = fields.ToManyField(
        'groups.api.resources.EmployeeProfileResource', 
        'employees', full=True, null=True)

    class Meta:
        # Denoets this class to all ScheduleItem objects.
        queryset = ScheduleItem.objects.all()

        #e.g. /api/v1/schedule-items/
        resource_name = 'schedule-items'

        
        authorization = GroupItemAuthorization()
        filtering = {
        'employees': ALL_WITH_RELATIONS,
        'group': ALL_WITH_RELATIONS
        }
        ordering = {
        'start': ALL_WITH_RELATIONS
        }