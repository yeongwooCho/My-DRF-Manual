# from django.contrib.auth.models import User
# from blog.models import Post, Comment
# from rest_framework import viewsets
#
# from api2.serializers import UserSerializer, PostSerializer, CommentSerializer
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
# -----------------------------------------------
from collections import OrderedDict

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import obj_to_post, prev_next_post, obj_to_comment
from api2.serializers import CommentSerializer, PostListSerializer, PostRetrieveSerializer, CateTagSerializer, \
    PostSerializerDetail
from blog.models import Post, Comment, Category, Tag


# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     # serializer many=True
#     serializer_class = PostListSerializer


# class PostRetrieveAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     # serializer many=False
#     serializer_class = PostRetrieveSerializer


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# class PostLikeAPIView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostLikeSerializer
#
#     # PATCH
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#
#         data = {'like': instance.like + 1}  # 코드 추가
#
#         serializer = self.get_serializer(instance, data=data, partial=partial)  # 해당 데이터 삽입
#         serializer.is_valid(raise_exception=True)  # partial 이 true 여서 유효성 체크 통과함
#         self.perform_update(serializer)
#
#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}
#
#         # return Response(serializer.data)
#         return Response(data['like'])

class PostLikeAPIView(GenericAPIView):
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()
        return Response(instance.like)


class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()

        data = {
            'cateList': cateList,
            'tagList': tagList,
        }

        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)


class PostPageNumberPagination(PageNumberPagination):
    page_size = 3  # 하나의 페이지 단위
    # page_size_query_param = 'page_size'
    # max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
        ]))


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    # serializer many=True
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }


def get_previous_next(instance):
    try:
        prev = instance.get_previous_by_update_dt()
    except instance.DoesNotExist:
        prev = None

    try:
        # next는 예약어이기에 이름충돌을 막기위해 nextt 사용
        next_ = instance.get_next_by_update_dt()
    except instance.DoesNotExist:
        next_ = None

    return prev, next_


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    # serializer many=False
    serializer_class = PostSerializerDetail

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        prevInstance, nextInstance = get_previous_next(instance)
        commentList = instance.comment_set.all()
        # commentList = Comment.objects.filter(post_id=instance.id)

        data = {
            'post': instance,
            'prevPost': prevInstance,
            'nextPost': nextInstance,
            'commentList': commentList,
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }


class PostRetrieveAPIViewWithoutSerializer(RetrieveAPIView):
    # queryset = Post.objects.all()
    # serializer many=False
    # serializer_class = PostSerializerDetail

    def get_queryset(self):
        return Post.objects.all().select_related('category').prefetch_related('tags', 'comment_set')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # prevInstance, nextInstance = get_previous_next(instance)
        commentList = instance.comment_set.all()
        # commentList = Comment.objects.filter(post_id=instance.id)

        # data = {
        #     'post': instance,
        #     'prevPost': prevInstance,
        #     'nextPost': nextInstance,
        #     'commentList': commentList,
        # }
        #
        # serializer = self.get_serializer(data)

        postDict = obj_to_post(instance)
        prevDict, nextDict = prev_next_post(instance)
        commentDict = [obj_to_comment(c) for c in commentList]

        dataDict = {
            'post': postDict,
            'prevPost': prevDict,
            'nextPost': nextDict,
            'commentList': commentDict,
        }

        return Response(dataDict)

    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #     return {
    #         'request': None,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }
