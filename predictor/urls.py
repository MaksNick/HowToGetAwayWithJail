from django.urls import path
from . import views

urlpatterns = [
    path("", views.predict_legal_outcome, name="predict_legal_outcome"),
    path("query/<int:query_id>/", views.query_detail, name="query_detail"),
]
