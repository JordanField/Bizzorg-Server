from django.conf.urls import url, include
from . import views

"""
This small file contains the instructions to what view in the views.py
file to redirect to when a request comes in with a specific URL.
"""

urlpatterns = [
    # '/groups/login/'
    url(r'login/', views.login),

    # '/groups/logout/'
    url(r'logout/', views.logout),

	# '/groups/csrf/'
	url(r'csrf/', views.csrf),

	# '/groups/update_profile_picture/'
	url(r'update_profile_picture/', views.update_profile_picture)
]