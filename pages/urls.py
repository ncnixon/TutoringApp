from django.urls import path
from .views import HomePageView, TAProfileDetailView
from .views import HomePageView, TAProfileDetailView, TutoringHourCreateView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),

    #ta/ -> identify profile selection. <int:pk> -> what TA proile to retrieve. 
    #TAProfileDetailView -> retrieve TA info. name="ta_detail" -> reusable url name
    path("ta/<int:pk>/", TAProfileDetailView.as_view(), name="ta_detail"),

    path(
        "hours/add/",
        TutoringHourCreateView.as_view(),
        name="add_tutoring_hour"
    ),
]