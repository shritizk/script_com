from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt

# get model from  dashboard
from dashboard.models import ScriptInfo

def explore_page(request):
    
    scripts = ScriptInfo.objects.filter(public=True)
    
    if not scripts : 
        
        return render(request, "explore.html")
    
    script_data = []
    
    for i in scripts:
    
        script_data.append({
            "title": i.title,
            "date" : i.created_at , 
            "id" : i.script_id
        })
    
    print(script_data)
    
    return render(request, "explore.html", {"scripts": script_data})


# explore the id page 
@csrf_exempt
def script_explore(req, id):
    
    try :     
        script_id = str(id)
        
        script_data = ScriptInfo.objects.get(script_id=script_id)
            
        '''
        script_id = models.UUIDField(primary_key=True)  
        title = models.CharField(max_length=255)
        created_at = models.DateTimeField(auto_now_add=True)
        upvotes = models.PositiveIntegerField(default=0)
        public = models.BooleanField(default=False)
        text = models.TextField(default="", blank=True)
        '''
            
        script = {
                'title': script_data.title,
                'uploaded_at': script_data.created_at,
                'likes': script_data.upvotes,
                'description': script_data.text,
                'id': script_data.script_id
            }
            
        return render(req,'explorebyid.html',{'script': script })
    
    except Exception as e:
        
        print(e)
        
        return render(req,'error.html')
        
@csrf_exempt
def upvote(req, id):
    
    try : 
        
        script_id = str(id)
        
        script_data = ScriptInfo.objects.get(script_id=script_id)
        
        script_data.upvotes += 1
        
        script_data.save()
        
        return redirect(f'/explore/{script_id}')
        
    except Exception as e:
        
        print(e)
        
        return render(req,'error.html')