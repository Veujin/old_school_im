from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('profile/', RedirectView.as_view(pattern_name='im:chat-list', permanent=False)),
    path('', include('django.contrib.auth.urls'))
]