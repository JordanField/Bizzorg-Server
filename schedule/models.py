from django.db import models

# Create your models here.

class ScheduleItem(models.Model):
    """
    A single schedule item.

    Fields:
    group           -- A foreign key relationship to a specific group.

    title           -- The title of the item, will be used as the __str__ and 
                    in the list view of the app.

    description     -- An optional description of the item at hand, this will be
                    shown if an item in the to-do list is expanded to its own 
                    screen.

    start           -- The date & time of the beginning schedule item.

    end             -- The date & time of the end of the schedule item

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

    group = models.ForeignKey('groups.EmployeeGroup', 
        related_name='Schedule_items', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    priority = models.CharField(max_length=3, 
                                choices=PRIORITY_CHOICES)
    employees = models.ManyToManyField('groups.EmployeeProfile', 
        related_name="scheduled_events", blank=True)

    def __str__(self):
        return 'Group: ' + self.group.name + ' | item: ' + self.title

