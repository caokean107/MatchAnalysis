import json
import math

#数据标准化
def Zscore(data):
    average = float(sum(data)) / len(data)
    # 方差
    total = 0
    for value in data:
        total += (value - average) ** 2
    stddev = math.sqrt(total / len(data))
    # 标准化方法
    data1 = [(float)(x - average) / stddev for x in data]
    return data1

#获取累计提交数
def coun(a):
    count=0
    for i in a:
        count=count+1
    return count

#读取json文件
FileScore = open('test_data.json', encoding='utf-8')
TestData = json.loads(FileScore.read())

Filetime = open('testTime.json', encoding='utf-8')
Testtime = json.loads(Filetime.read())

#获取运行时间数据，并将其标准化后重新存入
Ztime=[]
for i in Testtime:
    for case in Testtime[i]:
        b=case['time']
        c=0 if b==0 else 1/b
        Ztime.append(c)
Ztime = Zscore(Ztime) #注意，这里的参数是array
count=0
for i in Testtime:
    for case in Testtime[i]:
        case['time']=Ztime[count]
        count=count+1

#构建自己需要的score.json文件
Usuerscore = {}
for key in TestData:
    cases = TestData[key]['cases']
    user_id = str(TestData[key]['user_id'])
    if key not in Testtime:
        tt={}
    else:
        tt=Testtime[key]
    Cases = []
    print(user_id)
    print(cases)
    for case in cases:
        judge=True
        for i in tt:
            if i['case_id']==case['case_id']:
                judge=False
                Case = {"case_id": case["case_id"],
                        "case_type": str(case["case_type"]),
                        "score": case["final_score"],
                        "UploadNum": coun(case["upload_records"]),
                        "Testtime":i['time']}
                Cases.append(Case)
                break
        if judge:
            Case = {"case_id": case["case_id"],
                    "case_type": str(case["case_type"]),
                    "score": case["final_score"],
                    "UploadNum": coun(case["upload_records"]),
                    "Testtime": 0}
            Cases.append(Case)

    if len(Cases) != 0:
        Usuerscore[user_id] = {"cases": Cases}
#标准化score文件里的分数和提交次数两项指标
ZScore=[]
Znum=[]
for i in Usuerscore:
    for case in Usuerscore[i]['cases']:
        bb=case['score']
        bbb=case['UploadNum']
        ZScore.append(bb)
        Znum.append(bbb)
ZScore= Zscore(ZScore) #注意，这里的参数是array
Znum=Zscore(Znum)
count=0
for i in Usuerscore:
    for case in Usuerscore[i]['cases']:
        case['score']=ZScore[count]
        case['UploadNum']=Znum[count]
        count=count+1

NewjsonFile = json.dumps(Usuerscore, indent=4, ensure_ascii=False)

with open("JsonSet"+"/"+"score.json", 'w', encoding='utf-8') as json_file:
    json_file.write(NewjsonFile)
