from django.urls import path
from . import views

urlpatterns = [
    path('',views.search_flight, name='public-page'),
    path('find-trains/', views.find_trains, name='find-trains'),
    path('search_result/', views.search_results, name='search_results'),
    path('search_result/<int:fromA>/<int:toA>/<str:departure>',views.search_results),
    path('airport',views.list_airport,name='airport-page'),
    path('home/', views.home, name='home-page'),
    path('airport/add-airport/', views.add_train_stop, name='add_trainstop'),

    path('manage_airport',views.manage_airport,name='manage-airport'),
    path('manage_airport/<int:pk>',views.manage_airport,name='manage-airport-pk'),
    path('save_airport',views.save_airport,name='save-airport'),

    path('delete_airport/<int:pk>',views.delete_train_stop,name='delete_train_stop'),
    path('edit_airport/<int:pk>',views.edit_train_stop,name='edit_train_stop'),

    path('delete_flight/<int:pk>',views.delete_trip,name='delete_trip'),
    path('edit_flight/<int:pk>',views.edit_trip,name='edit_trip'),

    path('flight',views.list_flight,name='flight-page'),

    path('flight/add-flight/', views.add_flight, name='add_flight'),

    path('reservation',views.list_reservation,name='reservation'),
    path('reserve_ticket/<int:flight_id>/', views.reserve_ticket, name='reserve_ticket'),
    path('submit_reservation/<int:flight_id>/', views.reserve_ticket, name='submit_reservation'),
    path('reservation_details/<int:reservation_id>/', views.reservation_details, name='reservation_details'),
    path('update_reservation_status/<int:reservation_id>/', views.update_reservation_status, name='update_reservation_status'),
    path('delete_reservation/<int:pk>', views.delete_reservation, name='delete_reservation'),

    path('share_trip/', views.share_trip, name='share_trip'),
    path('shared_trips/', views.shared_trips, name='shared_trips'),
    path('share_reserved_trip/<int:reservation_id>/', views.share_reserved_trip, name='share_reserved_trip'),
    path('delete_shared_trip/<int:pk>', views.delete_shared_trip, name='delete_shared_trip'),
]