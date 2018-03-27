import json

x = []
for i in range(10):
    a = ["asd asd"]
    for j in range(15):
        a.append(0)
    x.append(a)
       



data = {}
data['prisutni'] = x




json_data = json.dumps(data)

print(json_data)
