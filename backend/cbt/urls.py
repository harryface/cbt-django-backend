from django.urls import path, include

urlpatterns = [
    path('api/examiner/', include('core.examiner.urls')),
    path('api/taker/', include('core.taker.urls')),
]
