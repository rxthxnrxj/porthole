from django.urls import path
from . import views





urlpatterns=[
    # path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('getpothole/', views.getConclusion, name='get-conclusion'),
    path('updatepothole/', views.updator, name='update-data'),
    path('image/', views.uploadImage, name='upload-data'),
]


