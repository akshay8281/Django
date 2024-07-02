from django.shortcuts import render	
import requests
# Create your views here.

def index(request):
	if request.method == "POST":
		title = request.POST['title']
		author = request.POST['author']
		isbn = request.POST['isbn']
		publisher = request.POST['publisher']

		url = "http://localhost:8000/api/books"
		querystring = {"title":title,"author":author,"isbn":isbn,"publisher":publisher}
		response = requests.post(url,json=querystring)
		print(response)
		msg = "Data Inserted Successfully"
		return render(request,'index.html',{'msg':msg})
	else:
		return render(request,'index.html')