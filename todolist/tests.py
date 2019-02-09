from django.test import TestCase
from .models import ToDoList, ToDoListItem
from groups.models import EmployeeGroup, GroupMembership
from django.contrib.auth.models import User
from django.core.exceptions import FieldError

class ToDoListTestCase(TestCase):

    def test_that_delegated_employee_must_be_member_of_to_do_list_group(self):
        testGroup = EmployeeGroup(name='test_group')
        testGroup.save()
        
        testUserInGroup = User(username='test_user_in_group')
        testUserInGroup.save()
        
        testMembership = GroupMembership(group=testGroup, user=testUserInGroup, admin_privileges=False)
        testMembership.save()
        
        testUserNotInGroup = User(username='test_user_not_in_group')
        testUserNotInGroup.save()

        testToDoList = testGroup.to_do_list
        testToDoListItem = ToDoListItem(to_do_list=testToDoList, title='test_item')
        testToDoListItem.save()

        testToDoListItem.employees.add(testUserInGroup)

        with self.assertRaises(FieldError):
            testToDoListItem.employees.add(testUserNotInGroup)