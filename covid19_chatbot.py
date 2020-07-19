from flask import Flask, make_response, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

url = "http://www.seoul.go.kr/coronaV/coronaStatus.do"
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data,'html.parser')

@app.route ('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))

def results():
    req = request.get_json(force=True)
    print(req)
    print('--------------------------------------------')

    # 크롤링
    regions = soup.find_all('em', class_='sr-only')     # 25개 자치구
    nums = soup.find_all('span', class_='num')      # 25개 자치구 확진자 수
    date = soup.find('p', class_='txt-status')
    target = 0

    ary = req.get("queryResult")["outputContexts"]
    print(ary)
    print('======================================')

    goal = ""
    for dic in ary:
        if "parameters" in dic:
            print(dic['parameters']['region'])
            goal = dic['parameters']['region']
            break

    for index in range(len(regions)):
        if(regions[index].string == goal):
                target = index
                break

    region = regions[target].string
    num = nums[target].string
    ans = date.string[2:-1] + "\n" + region + " 확진자 " + num + "명 입니다." + '\n' + "도움이 되셨나요?"

    response =\
    {
        'fulfillmentMessages' : [{
            'text' : {'text':
                [ans]
            }
        }]
    }

    return response

if __name__ == '__main__':
    app.run(debug=True)