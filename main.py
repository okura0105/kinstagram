import tweepy
import random
import account
import os

KEYFILE = 'api.txt'
'''
TARGET_LIST = ['筋肉','筋トレ','パンプアップ','腹筋','腕立て','スクワット']
TEXT_LIST = ['ちゃんとプロテイン飲めよ']
'''

keys = {}
for index,key in enumerate(open(KEYFILE)):
    keys[index]=key.strip().split(":")[1] #remove \n by strip


CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET=os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN_KEY=os.environ["ACCESS_TOKEN_KEY"]
ACCESS_TOKEN_SECRET=os.environ["ACCESS_TOKEN_SECRET"]


class Listener(tweepy.StreamListener):
    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)        
        #auth = tweepy.OAuthHandler(keys[0],keys[1])
        #auth.set_access_token(keys[2],keys[3])
        self.api = tweepy.API(auth)
        self.twitter_id = account.id()
        self.reply_flag = 0

    def classify(self):
        print("\n-----------------------reply start------------------------")
        since = None
        classify_list = ['筋肉','筋トレ','パンプアップ','腹筋','腕立て','スクワット']
        exclusion_list = ["bot","ビジネス","副業","公式"]
        
        break_flag = 0

        public_tweets = self.api.home_timeline(count=50)
        #public_tweets = self.api.home_timeline(count=50,since_id=since)

        for tweet in public_tweets:
            user_name = tweet.user.name.split("@")#HN
            screen_name = tweet.user.screen_name

            for i in range(len(exclusion_list)):
                if break_flag == 1:
                    break
                elif exclusion_list[i] in user_name:
                    print("not reply")
                    break_flag = 1
                else:
                    for i in range(len(classify_list)):
                        if classify_list[i] in tweet.text:
                            #debug code
                            '''
                            self.testreply(user_name[0],screen_name,tweet.id,tweet.text)
                            break_flag = 1
                            break
                            '''
                            if tweet.favorited == False:
                                #do reply
                                self.reply(user_name[0],screen_name,tweet.id,tweet.text)
                                #press like for avoid repling twice
                                self.api.create_favorite(tweet.id)
                                
                            else:
                                print("you already replyed it!")
                                break_flag = 1
                            break
                            

    def reply(self,user_name,screen_name,tweet_id,tweet_text):
        text_list = ['、ちゃんとプロテイン飲めよ','、キレてるよ！','、そこまで精進するには眠れない夜もあったろう']
        #num = random.randint(1,tweet.max_num())
        #num_padded = '{0:03d}'.format(num) #ゼロパディング:0で３桁左詰する。 example 1→001

        reply = "@"+screen_name+"\n "+user_name+ random.randrange(len(text_list))
        #reply = "@"+screen_name+"\n "+user_name+tweet.manus(num-1)
        self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)#status
        print("{0}のツイート:{1} に{2}と応援しました!".format(user_name,tweet_text,reply))

    def testreply(self,user_name,screen_name,tweet_id,tweet_text):
        text_list = ['、ちゃんとプロテイン飲めよ','、キレてるよ！','、そこまで精進するには眠れない夜もあったろう']
        #num = random.randint(1,tweet.max_num())
        #num_padded = '{0:03d}'.format(num) #ゼロパディング:0で３桁左詰する。 example 1→001

        reply = "@"+screen_name+"\n "+ 'DEBUG : ' + user_name+ text_list[random.randrange(len(text_list))]
        #reply = "@"+screen_name+"\n "+user_name+tweet.manus(num-1)
        self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)#status
        print("{0}のツイート:{1} に{2}と応援しました!".format(user_name,tweet_text,reply))

    def followback(self):
        print("\n-----------------------followback start------------------------")
        followers = self.api.followers_ids(self.twitter_id)
        ff = self.api.friends_ids(self.twitter_id)
        
        follow_back = list(set(followers)-set(ff))
        print("length of followback_list : {}".format(len(follow_back)))

        for i in range(min(len(follow_back),10)):
            try:
                self.api.create_friendship(follow_back[i])
                print("success follow! "+str(follow_back[i]))
            except tweepy.error.Tweeperror:
                print("error")


def main():
    listener = Listener()
    listener.classify()
    listener.followback()
    

if __name__ == "__main__":
    main()


#api.update_status("テストツイートfrom python")
