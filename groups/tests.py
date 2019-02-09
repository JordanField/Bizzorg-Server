from django.test import TestCase
from .models import EmployeeGroup
from django.core.exceptions import FieldError

# Create your tests here.

class EmployeeGroupTestCase(TestCase):

    def test_group_creation(self):
        """Tests the creation and saving of an employee group."""
        testGroup = EmployeeGroup(name='test_group')
        self.assertEqual(testGroup.name, 'test_group')
        testGroup.save()
        testGroupFromDatabase = EmployeeGroup.objects.get(name='test_group')
        self.assertEqual(testGroup, testGroupFromDatabase)

    def test_root_group_property(self):
        """Tests that the root group property works as expected"""
        testGroup1 = EmployeeGroup(name='test_group_1')
        testGroup2 = EmployeeGroup(name='test_group_2', parent_group=testGroup1)
        self.assertEqual(testGroup2.root_group, testGroup1)

        testGroup3 = EmployeeGroup(name='test_group_3', parent_group=testGroup2)
        self.assertEqual(testGroup3.root_group, testGroup1)

        testGroup4 = EmployeeGroup(name='test_group_4')
        testGroup1.parent_group = testGroup4
        self.assertEqual(testGroup3.root_group, testGroup4)

    def test_group_cannot_be_parent_of_itself(self):
        """Tests that a group cannot be a parent of itself, causing a recursive 
        relationship that breaks everything."""
        testGroup = EmployeeGroup(name='test_group')
        testGroup.parent_group = testGroup
        with self.assertRaises(FieldError):
            testGroup.save()

    def test_group_infinite_recursion(self):
        """Tests a parent group relationship that is cyclical cannot be saved 
        into the database."""
        testGroup1 = EmployeeGroup(name='test_group')
        testGroup2 = EmployeeGroup(name='test_group_2')
        testGroup3 = EmployeeGroup(name='test_group_3')

        testGroup1.parent_group = testGroup2
        testGroup2.parent_group = testGroup3
        testGroup3.parent_group = testGroup1

        with self.assertRaises(FieldError):
            testGroup1.save()
            testGroup2.save()
            testGroup3.save()