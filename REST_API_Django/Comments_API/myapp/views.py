from django.shortcuts import render
from rest_framework import generics
from .models import Comments
from .serializers import CommentSerializer

class CommentList(generics.ListCreateAPIView):
	queryset = Comments.objects.all()
	serializer_class = CommentSerializer

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Comments
	serializer_class = CommentSerializer