from django.urls import path
from services.views import (
    home, viewComp, viewFeedbacks
)

app_name = 'services'

urlpatterns = [
    path('home/<str:type>/', home, name='homepage'),
    path('complaint/<str:pk>/', viewComp, name='complaint'),
    path('feedbacks/<str:pk>/', viewFeedbacks, name='feedbacks'),
]