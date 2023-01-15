"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path, include

from announcement.views import ListCandidatesView, ListAnnouncements, CreateAnnouncementView, UpdateAnnouncementView, \
    CreateCandidateView, UpdateCandidateView

urlpatterns = [

    path('annoucements/', ListAnnouncements.as_view(), name='announcement_list'),
    path('annoucements/new/', CreateAnnouncementView.as_view(), name='announcement_create'),
    path('annoucements/<pk>/edit', UpdateAnnouncementView.as_view(), name='announcement_update'),

    path('api/announcements/', include('announcement.api.urls')),

    path('candidates/', ListCandidatesView.as_view(), name='candidate_list'),
    path('candidates/new/', CreateCandidateView.as_view(), name='candidate_create'),
    path('candidates/<pk>/edit/', UpdateCandidateView.as_view(), name='candidate_update'),

]
