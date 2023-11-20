#Stack Over Flow website Data Scrapping Code 
#Using This Code we scrapped 1 million Data

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service

service = Service(
    executable_path=r'E:\DSA Lab Work\Lab4\chromedriver-win64\chromedriver.exe')      #Driver Path
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
page = 1

#Attributes
question_titleList = []
answerList = []
votesList = []
answerNumberList = []
viewsList = []
userList = []
reputationList = []
timeList = []
statusList = []
tagsList = []

url = 'https://stackoverflow.com/questions?tab=active&pagesize=50&page=15000'

while url:
    try:
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")

        for a in soup.findAll('div', attrs={'class', 's-post-summary'}):
            questionTitle = a.find('h3', class_='s-post-summary--content-title')
            answer = a.find('div',class_='s-post-summary--content-excerpt')
            votes = a.select_one('.s-post-summary--stats-item-number')
            views = a.select_one('.s-post-summary--stats-item:contains("views") .s-post-summary--stats-item-number')
            answerNumber = a.select_one('.s-post-summary--stats-item:contains("answers") .s-post-summary--stats-item-number')
            user = a.select_one('.s-user-card--link a')
            reputation = a.select_one('.s-user-card--rep span')
            time = a.find('span', class_='relativetime')
            status = a.select_one('.s-user-card--time a').text.strip()
            li_tags = a.select('.s-post-summary--meta-tags ul li')
            tags = [li.text.strip() for li in li_tags]
            tags = ', '.join(tags)
            
            if questionTitle is not None:
                 question_titleList.append(questionTitle.text.strip())
            else:
                question_titleList.append('none')
            if answer is not None:
                answerList.append(answer.text.strip())
            else:
                answerList.append('none')
            if votes is not None:
                votesList.append(votes.text.strip())
            else:
                votesList.append('0')
            if views is not None:
                viewsList.append(views.text.strip())
            else:
                viewsList.append('0')
            if answerNumber:
                answerNumberList.append(answerNumber.text.strip())
            else:
                answerNumberList.append("0")
                        
            if user:
                userList.append(user.text.strip())
            else:
                userList.append('No User')
            if reputation is not None:
                reputationList.append(reputation.text.strip())
            else:
                reputationList.append('None')
            if time: 
               timeList.append(time.text.strip())
            else:
               timeList.append('None')
            if status: 
               statusList.append(status.split()[0])
            else:
               statusList.append('None')   
            if tags:
                tagsList.append(tags)
            else:
                tagsList.append('None')       


        base_url = "https://stackoverflow.com/questions?tab=active&pagesize=50&page="
        page = page + 1
        url = base_url + str(page)
        

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        break
with open('PageIndex.txt', 'w') as file:
    file.write(str(page))

df = pd.DataFrame({'Title Name': question_titleList, 'Answer' : answerList,'Votes' : votesList, 'Veiws' : viewsList,
                   'Answer Number':answerNumberList, 'User' : userList,'Reputation of User' : reputationList, 'Time' : timeList,
                    'Status': statusList,'Tags': tagsList })
df.to_csv('StackOverflow.csv', index=False, encoding='utf-8', mode='a')
