import requests
import json

# url="https://pclub-cp.herokuapp.com/AxYYzz786_rj"
url = "https://pclub-cp-competecode.herokuapp.com/AxYYzz786_rj"

response = requests.get(url)

if 'response' not in response.json():
    exit(0)

userlist = response.json()["response"]
quedict = response.json()["questionlist"]

print(quedict)

user_score = []
user_handle = []


question_solved_user_count = {}

for user in userlist:
    came = {}
    score = 0
    handle = user
    status_code = 429
    while status_code != 200:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
        status_code = response.status_code
        if status_code == 400:
            break
        if status_code == 429:
            time.sleep(1)
    if status_code == 400:
        continue
    stat = response.json()['result']
    for submission in stat:
        if(submission["problem"].get("contestId")):
            iid = str(submission["problem"]["contestId"]) + submission["problem"]["index"]
            if quedict.get(iid) and submission["verdict"]=="OK":
                if iid not in question_solved_user_count:
                    question_solved_user_count[iid]=1
                else:
                    question_solved_user_count[iid]+=1
                if(came.get(iid)):
                    score = score
                else:
                    score += 1
                came[iid]=1
    # print(handle, score)
    user_score.append(score)
    user_handle.append(handle)

# response = requests.post('https://pclub-cp.herokuapp.com/AxYYzz786_rj_leaderboard_overcome_502', data={'score':user_score, 'handle':user_handle, 'question_user_count':question_solved_user_count})
response = requests.post('https://pclub-cp-competecode.herokuapp.com/AxYYzz786_rj_leaderboard_overcome_502', data={'score':user_score, 'handle':user_handle, 'question_user_count':json.dumps(question_solved_user_count)})

print(response.text)
