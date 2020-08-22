import os
import django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyPclub2.settings")
django.setup()

from app1.models import Users, Questions, Leaderboard
import requests
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
        # print("while + "+str(response.status_code))
        if status_code == 429:
            # print("hey it is this")
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

