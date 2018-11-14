"""
HTTP REST API URI definition.
"""
from django.urls import path

from . import views

app_name = 'autotest'
urlpatterns = [
    path('suites', views.SuiteCollectionView.as_view(), name='suites'),
    path('suites/<int:id>', views.SuiteView.as_view(), name='suite'),
    path('jobs', views.JobCollectionView.as_view(), name='jobs'),
    path('jobs/<int:id>', views.JobView.as_view(), name='job'),
]
