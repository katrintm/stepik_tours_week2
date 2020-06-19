from django.urls import path

from tours.views import DepartureView
from tours.views import MainView
from tours.views import TourView
from tours.views import custom_handler404

urlpatterns = [
    path('', MainView.as_view()),
    path('departure/<str:departure>', DepartureView.as_view()),
    path('tour/<int:id>/', TourView.as_view()),
]

handler404 = custom_handler404
