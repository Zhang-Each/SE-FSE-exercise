import requests
import json
from bs4 import BeautifulSoup

all_problem_set = {}
for num in range(1, 37):
    base_url = "http://121.42.201.251/se/?switch=7&sub="
    url = base_url + str(num)
    fse = requests.get(url)
    html = fse.text
    parse_html = BeautifulSoup(html, 'html.parser')
    content = parse_html.find('div', id="content")
    
    # 获得了content下面所有的文本，根据文本内容再进行筛选
    test_set = [x.strip() for x in content.get_text().split('\n') if x.strip()]
    test_set.pop(0)
    
    # 通过获取所有的正确答案的下标来定位题目的位置
    answer_set = [-1]
    for i in range(len(test_set)):
        if test_set[i][0: 4] == "正确答案":
            answer_set.append(i)
    
    problem_list = []
    for i in range(len(answer_set)):
        if i == 0:
            continue
        else:
            problem = test_set[answer_set[i - 1] + 1: answer_set[i] + 1]
            topic = problem[0]
            answer = problem[-1][-1]
            options = problem[1: -1]
            dict_problem = {'topic': topic, 'answer': answer, 'options': options}
            problem_list.append(dict_problem)
    all_problem_set[num] = problem_list
file = "软工基客观题库.json"
with open(file, 'w') as json_file:
    json.dump(all_problem_set, json_file)
