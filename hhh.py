from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import vk_api
from bs4 import BeautifulSoup
import requests
import lxml
import time, random, asyncio
from apscheduler.schedulers.background import BackgroundScheduler

from vk_api.longpoll import VkLongPoll, VkEventType
"""
1) Создать список пользоватлей
2) Сначало провеить каждого пользователя на наличие сторисов (storyes:list)
4) Cмотрим сторис. время 1 сториса 12 секунд

"""


class Bot():
    def __init__(self, login:str, password:str, token: str, usertoken:str):
        try:
            self.vk_session = vk_api.VkApi(token=token)
            user_session = vk_api.VkApi(token=usertoken)
            self.api = user_session.get_api()
        except Exception as e:
            print(e)

        self.login = login
        self.password = password
        self.count = 0
        self.longpoll = VkLongPoll(self.vk_session)
        
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler.add_job(self.posers, trigger='interval', seconds=10, id='1')
        self.scheduler.add_job(self.rebot_posts, trigger='interval', dayes=1, id='2')
        self.storyes=[]

    def rebot_posts(self):
        self.count = 0
        self.scheduler.add_job(self.posers, trigger='interval', seconds=10, id='1')
    def SelectUserLink(self, user_id:str):
        if "\n" in user_id:
            user_id = user_id.removesuffix("\n")
        id = self.vk_session.method('utils.resolveScreenName', {'screen_name':user_id})['object_id']
        return id
    

    def AddUser(self, profile:str):
        try:
            with open('user.text', 'a') as f:
                f.write(profile+'\n')
        except Exception as e:
            print(e)
            self.vk_session.method('messages.send',{
                'user_id':self.api.users.get(user_ids=profile)['id'],
                'random_id':0,
                'message':"Ошибка добавления пользователя!"})


    def SelectStory(self ,user_id):
        """Получаем количество активных сторисов пользователя
        
        """
        stories = self.api.stories.get(
            owner_id=user_id
        )
        return stories['count']
    

    def WatchStory(self, id:list):
        self.count += 1
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.driver.get("https://vk.com/login")
            time.sleep(2)

            email_input = self.driver.find_element(By.ID, 'index_email')
            email_input.clear()
            email_input.send_keys("89826638353")
            email_input.send_keys(Keys.ENTER)
            time.sleep(4)

            password = self.driver.find_element(By.NAME, 'password')
            password.clear()
            password.send_keys(self.password)
            password.send_keys(Keys.ENTER)
            time.sleep(2)

            story = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Новости').click()
            time.sleep(5)

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            for user in id:
                elements = soup.find('div',{'class':'stories_feed_items'}).find('a',{'href':f'/{user}'})
           
                storys = self.driver.find_element(By.ID, elements['id']).click()
                time.sleep(15)
                element = self.driver.find_element(By.CLASS_NAME, 'stories_layer_close').click()
            self.driver.close()
        except Exception as e:
            print(e)

    def posers(self):
        if self.count != 1000:
            users = []
            with open('user.text','r') as f:
                users.append(f.readlines())
            id_user = [self.SelectUserLink(x) for x in users[0]]
            user_with_story = [[x, self.SelectStory(x)] for x in id_user]
            users = []
            for i in range(len(user_with_story)):
                if user_with_story[i][1] != 0:
                    user = self.vk_session.method('users.get',{
                                                'user_ids':user_with_story[i][0],
                                                'fields':'screen_name'
                                                })[0]['screen_name']
                    users.append(user)

            if len(users) == 1:
                self.WatchStory(users)
        else:
             self.scheduler.remove_job(id="1")
    
            
    def main(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message = event.text
                if message == "!Добавить":
                               self.vk_session.method('messages.send',{
                                                'user_id':event.peer_id,
                                                'random_id':0,
                                                'message':"Отправьте id пользователя со /"})
                
                elif "/" in message:
                    id = message.removeprefix("/")
                    try:
                        self.AddUser(id)
                        self.vk_session.method('messages.send',{
                                                'user_id':event.peer_id,
                                                'random_id':0,
                                                'message':"Пользователь успешно добавлен"})
                    except Exception as e:
                        print(e)
                        self.vk_session.method('messages.send',{
                                                'user_id':event.peer_id,
                                                'random_id':0,
                                                'message':"Ошибка добавления. Смотрите логи"})
                        
                    
                    
    async def start_schedule():
        while True:
            await asyncio.sleep(10)

if __name__=="__main__":
    c = Bot("+79826338353",
            "89122625502L",
            "vk1.a.PQVopLTsap_YfRXIbRXBzXOxYeyWaijULawkUphDYFBjJmoTsQGEi9RKL1jl-ykBmXXBesJEnWIFExVYlfOg6YqvzqmhA0L_kNb49ksZay2qW-T7oW-7YX6n0DXG-t9yGnKdluXGJkPTVc05qt0JNGQ8bYzNFFCBgEYhWGRVW685SkQWgXkps6gpAlkEy2hOX_2fT9y01RKUdMjuXoclvw",
            "vk1.a.Gvf8uabMziuEPb8CNMUxrSJbuK7o3ae0NbggoDDstpPbvIOMzaFmyuZoWe8GIH5Zu6seg0298Je8toeLDc3wlp0GfzvmTENwQpT6jNwf5HGAnYYVbq6ImLKfH2O4Ib-W8bOGLG2SkOT2iyX3wNnFBXWSEdV2z2tzj4YX-zT7jdSQjG7TKxYFDfUDkEIIS9KnfY8BYXQzldtz9z1B9HSY_A")

    c.main()
