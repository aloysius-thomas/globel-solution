"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from accounts.views import about
from accounts.views import contact_us_page_view
from accounts.views import dashboard
from accounts.views import digital_marketing_page_view
from accounts.views import home
from accounts.views import login_view
from accounts.views import logout_view
from accounts.views import mobile_development_page_view
from accounts.views import project_support_page_view
from accounts.views import software_development_page_view

urlpatterns = [
    path('database/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('about/', about, name='about'),
    path('dashboard/', include('solutions.urls')),
    path('services/software-development/', software_development_page_view, name='software-development-page'),
    path('services/digital-marketing/', digital_marketing_page_view, name='digital-marketing-page'),
    path('services/mobile-development/', mobile_development_page_view, name='mobile-development-page'),
    path('services/project-support/', project_support_page_view, name='project-support-page'),
    path('contact-us/', contact_us_page_view, name='contact-us-page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
