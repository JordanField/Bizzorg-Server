from django import forms
from groups.models import EmployeeProfile

class UpdateProfilePictureForm(forms.Form):
    """
    This form allows the client to send a profile picture to the server and 
    have it applied to a user.
    
    Fields:
    user -- The user to which the profile picture will be assigned
    new_profile_picture -- The image file of the new profile picture.
    """
    user = forms.ModelChoiceField(queryset=EmployeeProfile.objects.all())
    new_profile_picture = forms.ImageField()