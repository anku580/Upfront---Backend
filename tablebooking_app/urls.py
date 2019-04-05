# django imports
from django.urls import path

# project imports
from tablebooking_app.views.table_view import TableView
from tablebooking_app.views.table_detail_view import TableDetailView
from tablebooking_app.views.tablebooking_view import TableBookingView
from tablebooking_app.views.tablebooking_detail_view import TableBookingDetailView

urlpatterns = [
    path('restaurants/<int:resid>/tables',TableView.as_view()),
    path('restaurants/<int:resid>/tables/<int:tableid>',TableDetailView.as_view()),
    path('restaurants/<int:resid>/tables/<int:tableid>/date/<int:dd>/<int:mm>/<int:yyyy>/bookings',TableBookingView.as_view()),
    path('restaurants/<int:resid>/tables/<int:tableid>/date/<int:dd>/<int:mm>/<int:yyyy>/bookings/<int:bookingid>',
         TableBookingDetailView.as_view()),

]