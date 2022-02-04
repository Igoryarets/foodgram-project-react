from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (GetTokenAPI, RegisterGetUserAPI, SubscriptionApi,
                    SubscriptionList, logout, set_password)

router = SimpleRouter()

router.register('users', RegisterGetUserAPI)

urlpatterns = [

    path('users/subscriptions/', SubscriptionList.as_view({'get': 'list'}),
         name='subscriptions'),
    path('users/set_password/', set_password, name='set_password'),
    path('auth/token/logout/', logout, name='logout'),
    path('auth/token/login/', GetTokenAPI.as_view(), name='get_token'),
    path('users/<int:user_id>/subscribe/', SubscriptionApi.as_view(),
         name='subscribe'),
    path('', include(router.urls)),
]
