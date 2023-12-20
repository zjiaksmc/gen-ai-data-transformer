from django.urls import path
from . import views

urlpatterns = [
    ## Autoclean job
    path('job/', views.JobList.as_view(), name='job_list'),
    path('job/<str:id>', views.JobDetail.as_view(), name='job_detail')
]