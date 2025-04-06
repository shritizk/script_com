from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render , redirect 
from django.contrib import messages
from django.core.mail import send_mail

# utils 
from .utils import *
from dashboard.models import ScriptInfo 

# db 
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#import 
import uuid 
from datetime import datetime


# Create your views here.
def dashboard_page(req):
    
    return render(req,"dashboard.html")


# this  is combination of backend and front end as it performs logic within it self     
def myscript_page(req):
    
    # get input from user 
    search_query = req.GET.get('search')
    
    
    if not search_query:
        
        # concidering that this route might be a redirected one 
        return render(req, 'myscript.html')
        
    else : 
        
        # get data based on the search_query
        try :
            
            script = ScriptInfo.objects.get(script_id=search_query)
            
            # formating this 
            script_data = {
                'script_id': str(script.script_id),  
                'title': script.title,
                'text' : script.text,
                'created_at': script.created_at.isoformat(), 
                'upvotes': script.upvotes,
                'public': script.public
            }
            
            print(script_data)
            
            return render(req, 'myscript.html', {'script_data': script_data})
            
        except Exception as e:
            
            print(e)
            
            messages.error(req, 'Please enter a valid script ID')
    
            return render(req, 'myscript.html')
            
        
    # script_data
    #script_data = {title , date , text}
    
    
    return render(req,"myscript.html")
    

# backend 
@csrf_exempt
def new_script(req):
    
    try:
        
        title = req.POST.get('scriptTitle')
        email = req.POST.get('email')
        
        if title and email : 

            # create a id for the script to give access to the user 
            uu_id = str(uuid.uuid4())
            
            try :
                    
                    send_mail(
                        subject="script_com!",
                        message=f"Your Key for the script {title} is {uu_id}",
                        from_email="shritizk@gmail.com",
                        recipient_list=[email]
                    )
                
            except Exception as e:
                    
                    messages.error(req, 'email entered is wrong !! ')
            
                    response =  redirect('/dashboard/')
        
                    return response 
            
            try : 
                
                ScriptInfo.objects.create(
                    script_id =  uu_id,
                    title = title , 
                    created_at = datetime.utcnow().isoformat(),
                    email = email
                    )
            
                # once done return data this data with a email to the user telling them that what is the uuid / token for the script they just created 
                return redirect('/dashboard/myscript')
                    
            except Exception as e:
        
                print(e)
                
                send_mail(
                        subject="script_com!",
                        message="Token generated wont work as for now due to some issue , please generate new one !!",
                        from_email="shritizk@gmail.com",
                        recipient_list=[email]
                    )
                    
                return render(req,'error.html')
                
        else : 
            
            messages.error(req, 'Please enter a valid script name ')
            
            response =  redirect('/dashboard/')
        
            return response 
            
    except Exception as e:
        
        print(e)
        
        return render(req,'error.html')
        

@csrf_exempt
def edit_req(req):
    if req.method != "POST":
        return render(req, 'error.html', {'error': 'Invalid request method'})

    script_id = req.POST.get('id')
    title = req.POST.get('title')
    text = req.POST.get('text')
    privacy = req.POST.get('privacy')

    try:
        script = ScriptInfo.objects.get(script_id=script_id)
        script.title = title

        if privacy == 'public':
            script.public = True
        else:
            script.public = False

        script.text = text  # Always update text
        script.save()

        return redirect('/dashboard/myscript/')

    except ScriptInfo.DoesNotExist:
        messages.error(req, 'This script does not exist to be updated!')
        return render(req, 'myscript.html')

    except Exception as e:
        print("Unexpected error:", e)
        return render(req, 'error.html', {'error': str(e)})