from django.shortcuts import render
from rest_framework import generics
from .models import Admission
from .serializers import AdmissionSerializer

class AdmissionList(generics.ListCreateAPIView):
	queryset = Admission.objects.all()
	serializer_class = AdmissionSerializer

class AdmissionDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Admission
	serializer_class = AdmissionSerializer