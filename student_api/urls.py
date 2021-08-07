from django.urls import path
from .views import home, manual_api, student_list_api, student_list_api2, student_add_api, student_api, student_api_get_update_delete

urlpatterns = [
    path('', home),
    path('manual/', manual_api),
    path('list/', student_list_api2),
    path('add/', student_add_api),
    path('student/', student_api),
    path('student/<int:id>/', student_api_get_update_delete)

]
