from django.shortcuts import render

# Create your views here.

# front end 
def home_page(req):
    return render(req,'home_page.html')


    
