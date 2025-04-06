from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail

# db
from dashboard.models import ScriptInfo
from .models import emailCode

# import 
import uuid 

# Create your views here.
# non authed as its just render main page 
def main(req):
    
    # this will show them main page where they will search for the associated email they once used to create and get code for the script
    return render(req,'mainProf.html')


def profile(req):
    
    # get id that is a code btw
    data_id = req.GET.get('key')
    
    if not data_id:
        
        messages.error(req, ' no key provided , please check your email for the key !! ')
                
        response =  render(req,'myscripts.html')
        
        return response
    
    else : 
        
        try : 
        
            codeEmail = emailCode.objects.get(code=data_id)
            
            # now get data based on email 
            user_email = codeEmail.email
            
            #search for this email inside the ScriptInfo
            scripts = ScriptInfo.objects.filter(email = user_email)
            
            script_list = []
                
            for i in scripts : 
                
                script_list.append({
                    'title' : i.title , 
                    'date' : i.created_at , 
                    'id' : i.script_id
                })
                
            return render(req,'myscripts.html',{'script_list' : script_list})
        
        except Exception as e :
            
            print(e)
            
            messages.error(req, ' please try again , something went wrong . Also check key provided is correct  !! ')
                
            response =  redirect('/myprofile')
            
            return response

# backend 
@csrf_exempt
def prof_email(req):
    try: 
        email = req.POST.get('email')
        
        # Check if the email is associated with any script
        script_owner = ScriptInfo.objects.filter(email=email).first()
        
        if not script_owner:
            messages.error(req, 'The email provided does not exist in our records!')
            return redirect('/myprofile')
        
        # Check if the email already has a code
        emailcode = emailCode.objects.filter(email=email).first()
        
        if not emailcode:
            # Generate a new code if no code exists
            uu_id = str(uuid.uuid4())
            emailCode.objects.create(email=email, code=uu_id)
        else:
            # Use the existing code if available
            uu_id = emailcode.code
        
        # Send the email with the code
        send_mail(
            subject="Script_Com!",
            message=f"Your permanent key to access your profile for this email {email} is {uu_id}",
            from_email="shritizk@gmail.com",
            recipient_list=[email]
        )
        
        return redirect('/myprofile/profile')
    
    except Exception as e:
        print(e)
        messages.error(req, 'Something went wrong! Please try again.')
        return redirect('/myprofile')
        
        
def delete_script(req,id) :
    
    try : 
        
        # delete script using this id 
        
        if id : 
            
            script = ScriptInfo.objects.get(script_id=id)
            print(script)
            script.delete()
            print(script)
            
            messages.success(req, 'Script deleted successfully.')
            return redirect('/myprofile/profile')
        else :     
            
            messages.success(req, 'something went wrong at time of deleting this script !!')
            return redirect('/myprofile/profile')
        
    except Exception as e :
        
        print(e)
        
        return redirect('/myprofile/profile')
        