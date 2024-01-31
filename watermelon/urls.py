"""
URL configuration for watermelon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path


"""
    last review : 01/09/2024 - by eliso morazara
    
    ENDPOINTS:
        - __debug__/ : Endpoint for the debug tool
        - auth/ : Endpoint for all djoser and jwt related requests (anything User Authentication)
        - admin/ : Endpoint for all admin pages
        - projects : Endpoint for anything in the project app
        - 

    ADDITIONAL INFORMATION:
        AUTH:
            SUB-ENDPOINTS:
                    - auth/jwt/create : to login
                    - auth/users/me : to GET one's User data (must be logged in)
            
            NOTICE: 1 - resource : https://djoser.readthedocs.io/en/latest/getting_started.html

            TO DO:  1 - make sure the log in process also accepts email adresses
        
        PROJECTS:
            SUB-ENDPOINTS:
                    - Defined in project.urls

            NOTICE: 1 - 

            TO DO:  1 - 
            
            
"""

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("admin/", admin.site.urls),
    path('projects/', include('project.urls')),
    path('posts/', include('post.urls')),
    path('collections/', include('collection.urls')),
    path('playground/', include('playground.urls')),
]
