from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='booking-home'),
	path('booking-room-detail/<int:room_id>/', views.room_details, name='room_details'),
	path('booking-room-detail/<int:room_id>/update/', views.room_update, name='room_update'),
	path('booking-room-detail/<int:room_id>/delete/', views.room_delete, name='room_delete'),
]