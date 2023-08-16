from aiogram import Bot, executor, Dispatcher
import requests
import time
import schedule
import pymongo
limit_request=1
from var import token
from var import groupid


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['SeriesDB']
series_collection = db['series']

seconds = time.time()
t = time.ctime(seconds)
day = t[0:3]
catday = {'Mon': 'sibe', 'Tue': 'aege', 'Wed': 'beng', 'Thu': 'java', 'Fri': 'kora', 'Sat': 'kuri', 'Sun': 'manx'}
breed = catday[day]



bot = Bot(token)
dp = Dispatcher(bot=bot)



def adding_to_collection():
    request = f'https://api.thecatapi.com/v1/images/search?limit={limit_request}&breed_ids={breed}&api_key=live_NSO4T9haPU0a9yrI3913IfghtcXGcqlTn7FeMmPDQ72nYMC5fAq5x6pmg9IymUAD'
    response = requests.get(request)
    resp = response.json()
    for i in resp:
        options = {}
        options['_id'] = i['id']
        options['url']=i['url']
        options['breed']=breed
        options['message_status']='not_sent'
        series_collection.insert_one(options)

async def send_a_message():
    adding_to_collection()
    for i in list(series_collection.find()):
        if i['message_status']=='not_sent':
            await bot.send_photo(groupid,photo=i['url'])
        series_collection.update_one({'_id': i['_id']}, {'$set': {'message_status': 'sent'}})



def xt():
    executor.start(dp,send_a_message())


def x():
    schedule.every(150).seconds.do(xt)#могу написать at и любое время
    while True:
        schedule.run_pending()
x()

