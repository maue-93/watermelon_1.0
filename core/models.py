from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

"""
    last review : 01/05/2024 - by eliso morazara
    
    MODEL = User : basic user information

    USES :  1 - Authentication, basic information

    WHY :   1 - This is how anyone would get access to the app

    HOW IT WORKS :
            1 - One can create an account and use it to access the app by logging in

    NOTICE: 1 - This class is the default for AUTH_USER_MODEL in the main project's setting,
            and used in other apps

    TO DO : 1 - 

    RELATED FIELDS :
        - profile : model = Profile : the profile of this user
        - project_accesses : model = UserAccess : set of all accesses to projects this user has
        - access_requests : model = AccessRequest : set of all invites and requests to join projects
        - topics : model = Topic : set of task topics authored by this user in this project
"""
class User (AbstractUser):
    email = models.EmailField(unique=True)
# end of User model


"""
    last review : 01/05/2024 - by eliso morazara
    
    MODEL = Profile : more information about the user

    USES :  1 - A way to store more personal information of the user

    WHY :   1 - It is important for a user to present themself the way they want

    HOW IT WORKS :
            1 - Add profile picture, bio, etc

    NOTICE: 1 - 

    TO DO : 1 - Add profile_picture field

    RELATED FIELDS :
        - 
"""
class Profile (models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField()
# end of Profile model
