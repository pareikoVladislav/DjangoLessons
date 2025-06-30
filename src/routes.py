from django.urls import path, include

urlpatterns = [
    path('first_app/', include('src.first_app.urls')),
]
