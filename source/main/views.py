from django.shortcuts import render

# Create your views here.


def HomePageView(request):
    return render(request, "index.html")


def WorksView(request, work_type: str = '', work_name: str = ''):
    if isinstance(work_type, str) and len(work_type) >= 2:
      work_type = work_type.lower()
      if work_type == 'podcasts': 
        if not work_name:
          return render(request, 'inspect_work.html', {'work': 'Podcast'})    
        work_name = work_name.lower()
        
        return render(request, 'inspect_post.html')    
    return render(request, "works.html")
