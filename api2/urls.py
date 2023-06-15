# from django.urls import path, include
# from rest_framework import routers
#
# from api2.views import UserViewSet, PostViewSet, CommentViewSet
#
# # Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'posts', PostViewSet)
# router.register(r'comments', CommentViewSet)
#
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path
from api2 import views

urlpatterns = [
    # posts
    path('posts/', views.PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-detail'),

    # comments
    path('comments/', views.CommentCreateAPIView.as_view(), name='comments-list'),
]
