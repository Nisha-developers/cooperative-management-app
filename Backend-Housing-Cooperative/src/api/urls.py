from django.urls import path, include

urlpatterns = [
   path('users/', include('api.users.urls')),
   path('wallet/', include('api.wallet.urls'))
]
