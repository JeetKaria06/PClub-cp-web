from django.shortcuts import render,HttpResponse
from .models import Questions, Users, Leaderboard
import requests
import time
import datetime
# Create your views here.
def Home(request):
    return render(request,'Home.html')

def Ques(request):
    questions = Questions.objects.all()
    return render(request,'Questions.html', {'questions':questions})


def Leaderbord(request):
    
    questions = Questions.objects.all()
    
    leaders = Leaderboard.objects.order_by('-score')
    # print(leaders)
    return render(request,'Leaderbord.html', {'leaders':leaders, 'totalPros':len(questions)})

def AxYYzz786_rj(request):
    quedict = {}
    Leaderboard.objects.all().delete()

    questions = Questions.objects.all()
    for question in questions:
        quedict[question.rcid()] = 1

    users = Users.objects.all()
    for user in users:
        came = {}
        score = 0
        handle = user.usr_name
        status_code = 429
        while status_code != 200:
            response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
            status_code = response.status_code
            if status_code == 429:
                time.sleep(1)
        print(response.status_code)
        stat = response.json()['result']
        for submission in stat:
            if(submission["problem"].get("contestId")):
                iid = str(submission["problem"]["contestId"]) + submission["problem"]["index"]
                if quedict.get(iid) and submission["verdict"]=="OK":
                    if(came.get(iid)):
                        score = score
                    else:
                        score += 1
                    came[iid]=1

        # print(score, handle)
        l = Leaderboard(usr_name=handle, score=score, profile_pic=user.profile_pic)
        l.save()
    return HttpResponse("Done.")

def Register(request):
    u = Users(usr_name=request.GET.get('cf_id'), usr_mail=request.GET.get('email'))
    u.register()
    u.getPic()
    u.save()
    return render(request,'Home.html')