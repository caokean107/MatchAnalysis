import json

import os


json_path = os.path.dirname(os.path.abspath("JsonSet/score.json"))
json_file = open(os.path.join(json_path, "score.json"),encoding='utf-8')
ScoreData = json.load(json_file)

json_path = os.path.dirname(os.path.abspath("JsonSet/sample.json"))
json_file = open(os.path.join(json_path, "sample.json"),encoding='utf-8')
FileTem = json.load(json_file)
TemplateKey = FileTem.keys()

Res= {}

for key in ScoreData:
    user_id = str(key)
    cases = ScoreData[key]['cases']
    res = []
    for i in TemplateKey:
        judge=True
        for case in cases:
            if case['case_id']==i:
                judge=False
                temp=case['score']
                temp1=case['UploadNum']
                temp2=case['Testtime']
                res.append(3*temp+temp1+temp2)
                break
        if judge:
            res.append(0)

    Res[user_id] = res

NewjsonFile = json.dumps(Res, indent=4, ensure_ascii=False)

with open("JsonSet"+"\\"+"grade.json", 'w', encoding='utf-8') as json_file:
    json_file.write(NewjsonFile)