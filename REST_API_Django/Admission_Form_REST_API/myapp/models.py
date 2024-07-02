from django.db import models

# Create your models here.

class Admission(models.Model):

	fname = models.CharField(max_length = 100,blank = True)
	lname = models.CharField(max_length = 100,blank = True)
	email = models.EmailField(max_length=100)
	mobile = models.CharField(max_length = 100,blank = True)
	address = models.CharField(max_length = 100,blank = True)
	course = models.CharField(max_length = 100,blank = True)
	fees = models.DecimalField(max_digits=10, decimal_places=2,blank = True)

	def __str__(self):
		return self.fname + " " + self.lname