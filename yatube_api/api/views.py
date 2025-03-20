from django.shortcuts import get_object_or_404
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        if post.author != self.request.user:
            raise PermissionDenied()
        serializer.save(author=self.request.user)

    def perform_destroy(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        if post.author.username != self.request.user.username:
            raise PermissionDenied()
        post.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user,
                        post=post)

    def perform_update(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        if comment.author.username != self.request.user.username:
            raise PermissionDenied()
        serializer.save(author=self.request.user,
                        post=post)

    def perform_destroy(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        if comment.author.username != self.request.user.username:
            raise PermissionDenied()
        comment.delete()
