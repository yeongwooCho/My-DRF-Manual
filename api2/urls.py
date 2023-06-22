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
    path('posts/', views.PostViewSet.as_view(actions={
        'get': 'list'
    }), name='post-list'),
    path('posts/<int:pk>/', views.PostViewSet.as_view(actions={
        'get': 'retrieve'
    }), name='post-detail'),
    # like
    # path('posts/<int:pk>/like/', views.PostLikeUpdateAPIView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', views.PostViewSet.as_view(actions={
        'get': 'like'
    }), name='post-like'),

    # comments
    path('comments/', views.CommentViewSet.as_view(actions={
        'post': 'create'
    }), name='comments-list'),

    # cate tag
    path('catetag/', views.CateTagAPIView.as_view(), name='catetag'),
]
