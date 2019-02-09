from django.db import models
from django.core.exceptions import FieldError

class ToDoListItem(models.Model):
    """
    A single to-do list item.

    Fields:
    group           -- A foreign key relationship to a specific group.
    
    title           -- The title of the item, will be used as the __str__ and in 
                    the list view of the app.
    
    description     -- An optional description of the task at hand, this will be
                    shown if an item in the to-do list is expanded to its own 
                    screen.
    
    completed       -- A Boolean value that denotes whether the to-do list item
                    has been completed.
    
    date_created    -- The day the to-do list item was created.
    
    deadline_date   -- The day the item should be completed by.

    priority        -- How important the task it, can be low, regular,
                    significant, urgent or severe.
    
    employees       -- An optional many-to-many relationship relating the item 
                    to one or more employees, shows who this task is for.
    """

    PRIORITY_LOW = 'low'
    PRIORITY_REGULAR = 'reg'
    PRIORITY_SIGNIFICANT = 'sig'
    PRIORITY_URGENT = 'urg'
    PRIORITY_SEVERE = 'sev'

    PRIORITY_CHOICES = (
        (PRIORITY_LOW, 'Low priority'),
        (PRIORITY_REGULAR, 'Regular'),
        (PRIORITY_SIGNIFICANT, 'Significant'),
        (PRIORITY_URGENT, 'Urgent'),
        (PRIORITY_SEVERE, 'Severe')
    )

    group = models.ForeignKey('groups.EmployeeGroup', related_name='to_do_list_items',
    	on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    deadline_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=3, 
                                choices=PRIORITY_CHOICES, 
                                default=PRIORITY_REGULAR)
    employees = models.ManyToManyField('groups.EmployeeProfile', related_name="delegated_tasks", blank=True)

    def __str__(self):
        return 'Group: ' + self.group.name + ' | item: ' + self.title
