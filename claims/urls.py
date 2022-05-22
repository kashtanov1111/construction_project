from django.urls import path

from . import views

app_name = 'claims'
urlpatterns = [
    path('', views.ClaimListView.as_view(), name='claim_list'),
    path('<slug:slug>/delete/', views.ClaimDeleteView.as_view(), name='claim_delete'),
    path('<slug:slug>/update/', views.ClaimUpdateView.as_view(), name='claim_update'),
]
