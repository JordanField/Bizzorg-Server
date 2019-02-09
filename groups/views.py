from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .forms import UpdateProfilePictureForm
import pdb

"""
This file contains the logic for logging users in and out of the
Bizzorg server, as well as updating profile pictures. Requests are made
by the client and are then sent to views, where the request is processed and
the appropriate response is made.
"""

@csrf_exempt
def login(request):
    """
    In order to ensure that I don't have to send the password with each
    request but can ensure all users are authenticated I used Django's
    Session system to send the client a unique session cookie, allowing
    persistent login sessions.
    """

    # Validate that the request was sent through POST
    if request.method != 'POST':
        return HttpResponse('fail', status=401)
    
    # Validate that the request contains a username and password
    try:
        pdb.set_trace()
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        print("no userpass")
        return HttpResponse('fail', status=401)

    # Now the request, username and password have been validated, try and
    # assign the credentials to a user.
    user = authenticate(username = username, password = password)

    # Validate that the credentials correspond to an actual active user.
    if user is None or not user.is_active:
        return HttpResponse('fail', status=403)

    # All validation has now passed, so log the user in and redirect them
    # to their employee object for the client to use.
    auth.login(request, user)
    employeeId = user.employee_profile.id
    return redirect('/api/v1/employees/' + str(employeeId) + '/')

@csrf_exempt
def logout(request):
    """
    Since logging out is a non-vunerable action, no validation needs to be
    performed.
    """
    auth.logout(request)
    return HttpResponse('pass')

@csrf_exempt
def csrf(request):
	"""
	To protect users from cross site request forgery attacks, Django 
	sends a cookie unique to each user of the service, this needs to be
	retrieved before a user can log in, so this view sends the CSRF 
	cookie.
	"""
	return HttpResponse('cookie delivered')

@ensure_csrf_cookie
def update_profile_picture(request):

    # Validate that the request came from an authenticated user.
    if not request.user.is_authenticated:
        return HttpResponse('fail', status=401)

    # Validate the request has been made via POST.
    if request.method != 'POST':
        # If the request was not POST, show the form used to update the
        # profile picture.
        form = UpdateProfilePictureForm()
        return render(request, 'updateprofilepicture.html', {'form': form}) 
        
    # Request has been validated, so build the form from the POST
    # and FILES objects.
    form = UpdateProfilePictureForm(request.POST, request.FILES)

    # Validate the form is correct.
    if not form.is_valid():
        return HttpResponse('fail', status=400)
    
    # Retrieve the user to change the profile picture of.
    employee_to_change = form.cleaned_data['user']

    # Validate that the user can change this profile picture. The
    # user must be either the same as the employee whose profile
    # picture is changing OR the user is in the "VIP Staff" list.
    if not (request.user.employee_profile == employee_to_change or 
        request.user.is_staff):
        return HttpResponse('fail', status=403)

    # Everything is in order, so set the users profile picture to
    # be the new image.
    employee_to_change.profile_picture = request.FILES['new_profile_picture']

    # Save the changes to the database.
    employee_to_change.save()

    # Retrieve the cleaned profile picture url and return it to the
    # client.
    new_image_url = employee_to_change.profile_picture.url
    return HttpResponse(new_image_url)
