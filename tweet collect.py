import pandas as pd
import json as js
import psycopg2 as p2
import tweepy as ty
import time
api_key='uF0DOC3pQoNjgNnQOK1Wi088v'

api_key_secret='7lOS2UZ5F7XuFQielKpwEMf16Jij6mlZU6FZaGVR9uaNEbPZ8w'



access_token='2682699414-Si4SU72snug3AgKaAlMTXA9eoDAUoYUW4rAdvPs'

access_token_secret= 'tb2NbDAvMUybh1xhBH9J8sr4pJw370lPyQESdUKf29dEi'
auth = ty.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = ty.API(auth)
print('Define the necessary parmeters: ')
user = (input('Please enter your target\'s Twitter Username:' ))
print('\n')
print('If you want to get the maximum, just click "Enter/Return" only: ')
page = (input('Please enter the number of pages you want to crawl:'))
user1 =  api.get_user (screen_name= user)
  
ID = user1.id_str
Tweetuser = api.lookup_users(user_id=[ID])

for i in range(len(Tweetuser)):
    print ('Name - ' + Tweetuser[i].name)
    print ('Bio - ' + Tweetuser[i].description)
    print ('Location - ' + Tweetuser[i].location)
    print ('Joined at - ' + str(Tweetuser[i].created_at))
    print ('User ID - '+ Tweetuser[i].id_str)
    
    followers_count = user1.followers_count

    print("Number of Followers - " + str(followers_count))
    print ('')


auth = ty.OAuthHandler(api_key,api_key_secret)

auth.set_access_token(access_token,access_token_secret)
 
api = ty.API(auth)

n=0
conn = p2.connect(database = 'twitter project',user = 'postgres', password = '75321596548', host = 'localhost',port='5432')
data=[]
cursor = conn.cursor()
for user_info in ty.Cursor(api.user_timeline,
                              screen_name = user,
                              tweet_mode = 'extended').pages():
    for search_info in user_info:        
        id = search_info.id
        Twitter = search_info.full_text.replace('\'',' ''('')')
        created_at = search_info.created_at
        like_count = search_info.favorite_count
        retweet_count = search_info.retweet_count
       
        sql_command = """insert into twitter values ({},'{}','{}',{},{});""" \
            .format(id,str(Twitter),str(created_at),like_count,retweet_count)
        n+=1
        print(sql_command)
        cursor.execute(sql_command)
        data.append([search_info.id,
                     search_info.full_text,
                     search_info.created_at,
                     search_info.favorite_count,
                     search_info.retweet_count])
print('total insert: ' + str(n) + 'rows record.')
'''
n=0
columns= ['ID', 'tweet', 'created_at', 'like_count', 'retweet_count']

data= []


conn = p2.connect(database = 'twitter project',user = 'postgres', password = '75321596548', host = 'localhost',port='5432')
cursor = conn.cursor()


for user_type in ty.Cursor(api.user_timeline, screen_name = user, tweet_mode='extended').pages(100):
 
    for search_info in user_type:
        id= search_info.id
        tweet= search_info.full_text.replace('\'',' ')
        created_at=search_info.created_at
        like_count= search_info.favorite_count
        retweet_count=search_info.retweet_count
      
        sql_command = """insert into twitter values({},'{}','{}',{},{});""".format(str(id), str(tweet), str(created_at),str(like_count), str(retweet_count))
        n+=1
        print (sql_command)
        cursor.execute(sql_command)
        data.append([search_info.id,
                     search_info.full_text,
                     search_info.created_at,
                     search_info.favorite_count,
                     search_info.retweet_count])    
print(str(n)+'tweet found')

'''
conn.commit()
cursor.close()
conn.close


conn = p2.connect(database = 'twitter project',user = 'postgres', password = '75321596548', host = 'localhost',port='5432')
cursor = conn.cursor()

columns = ['ID','tweet','created_at','like_count','retweet_count']
df = pd.DataFrame(data,columns = columns)
df2= df[df['tweet'].str.contains('covid|virus|vaccin',case=False)] 

x=0


user_key = str(user)
cursor.execute("""CREATE TABLE IF NOT EXISTS public."{}" (id bigint);""".format(user))

for i in df2.iloc[:,0]:
    cursor.execute("""insert into "{}" values({});""".format(user,i))
    x+=1
print ('Result:'+str(x)+'rows')
conn.commit()
cursor.close()
conn.close