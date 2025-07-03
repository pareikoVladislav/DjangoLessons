from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include('src.routes')),
    # path('hello/', lambda request: HttpResponse("<h1>HOME PAGE</h1>")),
]
