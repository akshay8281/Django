from rest_framework import serializers
from .models import Admission

class AdmissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Admission
		fields = ('id','fname','lname','email','mobile','address','course','fees')


