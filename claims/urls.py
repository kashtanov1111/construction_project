from django.urls import path

from . import views

app_name = 'claims'
urlpatterns = [
    path('', views.ClaimListView.as_view(), name='claim_list'),
    path('expired/', 
        views.ClaimExpiredListView.as_view(), name='claim_expired_list'),
    path('create/', 
        views.ClaimCreateView.as_view(), name='claim_create'),
    path('<slug:slug>/delete/', 
        views.ClaimDeleteView.as_view(), name='claim_delete'),
    path('<slug:slug>/update/', 
        views.ClaimUpdateView.as_view(), name='claim_update'),
    path('<slug:slug>/', 
        views.ClaimDetailView.as_view(), name='claim_detail'),
]
