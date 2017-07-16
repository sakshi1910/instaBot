import requests, urllib                     # Importing Libraries..
from termcolor import colored
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt



APP_ACCESS_TOKEN = '5715338192.ed958cb.a30cdc9365704aa38a702754d7743083'  # Token of sakshi....

#Sandbox Users :

BASE_URL = 'https://api.instagram.com/v1/'

avg_sentiment=[0.0,0.0]

#                           Function declaration to get your own info ........



def self_info():                 # defining Function to ascess users information...
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print colored('GET request url : %s','blue') % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print colored('Username: %s','grey') % (user_info['data']['username'])
            print colored('No. of followers: %s','grey') % (user_info['data']['counts']['followed_by'])
            print colored('No. of people you are following: %s','grey') % (user_info['data']['counts']['follows'])
            print colored('No. of posts: %s','grey') % (user_info['data']['counts']['media'])
        else:
            print colored('User does not exist!!','red')
    else:
        print colored('Status code other than 200 received!','red')



#    Function declaration to get the ID of a user by username


def get_user_id(insta_username):                  # Defining function to get User_ID by passing username ..
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print colored('GET request url : %s','blue') % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print colored('Status code other than 200 received!','red')
        exit()



#                Function declaration to get the info of a user by username.............................




def get_user_info(insta_username):            #     Defining function to Get user information by passing username ...
    user_id = get_user_id(insta_username)     #     Calling Function of get user_Id  to further proceed..
    if user_id == None:
        print colored('Insta user Of This Username does not exist!','red')
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print colored('GET request url : %s','blue') % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print colored('Username: %s','grey') % (user_info['data']['username'])
            print colored('No. of followers: %s','grey') % (user_info['data']['counts']['followed_by'])
            print colored('No. of people you are following: %s','grey') % (user_info['data']['counts']['follows'])
            print colored('No. of posts: %s','grey') % (user_info['data']['counts']['media'])
        else:
            print colored('No data exists for this user!','red')
    else:
        print colored('Status code other than 200 received!','red')



#                       Function declaration to get your recent post...................



def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print colored('GET request url : %s','blue') % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)    # using urllib library to download the post by passing link of recent media to it ..
            print colored('Your image From Your Recent Posts has been downloaded Successfully!','cyan')
        else:
            print colored('Post does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')



#                    Function declaration to get the recent post of a user by username.................



def get_user_post(insta_username):   # Defining function to get recent posts of a user by passing username to function..
    user_id = get_user_id(insta_username)    # Calling get user id function to get user id by passing username ..
    if user_id == None:
        print colored('Insta user Of This Username does not exist!', 'red')
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print colored('GET request url : %s','blue') % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)  # Fetching users recent post by passing link to the function as parameter..
            print colored('The Image From users Recent Posts has been downloaded!','cyan')
        else:
            print colored('Post does not exist!', 'red')
    else:
        print colored('Status code other than 200 received!','red')


#                 Function declaration to get the ID of the recent post of a user by username........


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)               #         Capturing the user id ......
    if user_id == None:                                 #         checking in case post exists or not .......
        print colored('Insta User of this Username does not exist!','red')
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print colored('GET request url : %s','blue') % (request_url)
    user_media = requests.get(request_url).json()            #      Fetching json data ........

    if user_media['meta']['code'] == 200:                    #    checking the status code .......
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print colored('No recent post of the user!','red')
            exit()
    else:
        print colored('Status code other than 200 received!','red')
        exit()



#                        Function declaration to like the recent post of a user.........



def like_a_post(insta_username):                              #     Defining the Function ............
    media_id = get_post_id(insta_username)                     # Getting post id by passing the username .......
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}                 #    passing the payloads ........
    print colored('POST request url : %s','blue') % (request_url)         #    post request method  to posting the like ......
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:                        #    checking the status code .....
        print colored('Like was successful!','cyan')
    else:
        print colored('Your like was unsuccessful.Please Try again!','red')



#                 Function declaration to Get the like lists on the recent post of a user.........


def get_like_list(insta_username):            # Defining the Function ............
    media_id = get_post_id(insta_username)  # Getting post id by passing the username .......
    request_url = BASE_URL + 'media/%s/likes?access_token=%s' % (media_id, APP_ACCESS_TOKEN)    #    passing the end points and media id along with access token ..
    print colored('GET request url : %s', 'blue') % (request_url)
    like_list = requests.get(request_url).json()

    if like_list['meta']['code'] == 200:  # checking the status code .....
        if len(like_list['data']):
            position = 1
            print colored("List of people who Liked Your Recent post", 'grey')
            for users in like_list['data']:
                if users['username']!= None:
                    print position, colored(users['username'],'green')
                    position = position + 1
                else:
                    print colored('No one had liked Your post!', 'magenta')
        else:
            print colored("User Does not have any post",'red')
    else:
        print colored('Status code other than 200 recieved', 'red')


#        Function declaration to Get the lists of comments on  the recent post of a user.........


def get_comment_list(insta_username):  # Defining the Function ............
    media_id = get_post_id(insta_username)  # Getting post id by passing the username .......
    request_url = BASE_URL + 'media/%s/comments?access_token=%s' % (media_id, APP_ACCESS_TOKEN)   #    passing the end points and media id along with access token ..
    print colored('GET request url : %s', 'blue') % (request_url)
    comment_list = requests.get(request_url).json()

    if comment_list['meta']['code'] == 200:  # checking the status code .....
        if len(comment_list['data']):
            position = 1
            print colored("List of people who commented Your Recent post", 'blue')
            for users in comment_list['data']:
                if users['username'] != None:
                    print position, colored(users['username'], 'green')
                    position = position + 1
                else:
                    print colored('No one had commented on Your post!', 'magenta')
        else:
            print colored("User Does not have any post", 'red')
    else:
        print colored('Status code other than 200 recieved', 'red')

def get_comment_list(insta_username):  # Defining the Function ............
    media_id = get_post_id(insta_username)  # Getting post id by passing the username .......
    request_url = BASE_URL + 'media/%s/comments?access_token=%s' % (
    media_id, APP_ACCESS_TOKEN)  # passing the end points and media id along with access token ..
    print colored('GET request url : %s\n', 'blue') % (request_url)
    comment_list = requests.get(request_url).json()

    if comment_list['meta']['code'] == 200:  # checking the status code .....
        if len(comment_list['data']):
            position = 1
            print colored("List of people who commented on Your Recent post", 'blue')
            for _ in range(len(comment_list['data'])):
                if comment_list['data'][position - 1]['text']:
                    print colored(comment_list['data'][position - 1]['from']['username'], 'yellow') + colored(' said: ', 'yellow') + colored(comment_list['data'][position - 1]['text'],'cyan')  # Json Parsing ..printing the comments ..
                    position = position + 1
                else:
                    print colored('No one had commented on Your post!\n', 'magenta')
        else:
            print colored("No Comments on User's Recent post.\n", 'red')
    else:
        print colored('Status code other than 200 recieved.\n', 'red')

#                  Function declaration to make a comment on the recent post of the user................


def post_a_comment(insta_username):         #     Defining the function ......
    media_id = get_post_id(insta_username)    #   Getting media id by calling the get post id function....
    comment_text = raw_input(colored("Please Write Your comment: ",'green'))
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print colored('POST request url : %s','blue') % (request_url)

    post_comment = requests.post(request_url, payload).json()    #   Fetching json data ...
    if post_comment['meta']['code'] == 200:             #      checking status code ......
        print colored("Successfully added a new comment!",'cyan')
    else:
        print colored("Unable to add comment.Please Try again!!",'red')


#                      Function declaration to make delete negative comments from the recent post.........................


def ploating_negative_positive_comments(insta_username):   #     Defining the function ......
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()






    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            # Here's a naive implementation of how to delete the negative comments
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                print 'negative sentiment:', blob.sentiment.p_neg
                print' positive sentiment:', blob.sentiment.p_pos
                avg_sentiment[0]=avg_sentiment[0]+blob.sentiment.p_pos
                avg_sentiment[1]=avg_sentiment[1]+blob.sentiment.p_neg
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print colored('Comment successfully deleted!\n','cyan')
                    else:
                        print colored('Unable to delete comment!','red')
                else:
                    print colored('Positive comment : %s\n','cyan') % (comment_text)
            plt.pie(avg_sentiment,colors=['green','red'])
            print colored('negative avg','red'),avg_sentiment[1],colored('postive avg','green'),avg_sentiment[0]
            plt.savefig("./fig.png",dpi=300)
            plt.show()
        else:
            print colored('There are no existing comments on the post!','red')
    else:
        print colored('Status code other than 200 received!','red')



#                   Defining the Main function under which above sub-function works by calling ...........


def start_bot():
    while True:
        print colored('\nHey! We Welcomes U to instaBot!','green')
        print colored('\nSelect your menu options:','blue')
        print colored("\nSelect Option:'1'  To Get your own details\n",'green')
        print colored("Select Option:'2'  To Get details of a user \n",'green')
        print colored("Select Option:'3'  To Get your own recent post\n",'green')
        print colored("Select Option:'4'  To Get the recent post of a user \n",'green')
        print colored("Select Option:'5'  To Get a list of people who have liked the recent post of a user\n",'green')
        print colored("Select Option:'6'  To Like the recent post of a user\n",'green')
        print colored("Select Option:'7'  To Get a list of comments on the recent post of a user\n",'green')
        print colored("Select Option:'8'  To comment on the recent post of a user\n",'green')
        print colored("Select Option:'9'  To show piechart between negative and postive comments\n",'green')
        print colored("Select Option:'10' To Exit From The Application..",'green')

        choice = raw_input(colored("\nEnter you choice: ",'blue'))
        if choice.upper() == "1":
            self_info()
        elif choice.upper() == "2":
            insta_username = raw_input(colored("Enter the username of the user: ",'blue'))
            get_user_info(insta_username)
        elif choice.upper() == "3":
            get_own_post()
        elif choice.upper() == "4":
            insta_username = raw_input(colored("Enter the username of the user: ",'blue'))
            get_user_post(insta_username)
        elif choice.upper() == "5":
            insta_username = raw_input(colored("Enter the username of the user: ",'blue'))
            get_like_list(insta_username)
        elif choice.upper() == "6":
            insta_username = raw_input(colored("Enter the username of the user: ",'blue'))
            like_a_post(insta_username)
        elif choice.upper() == "7":
            insta_username = raw_input(colored("Enter the username of the user: ",'blue'))
            get_comment_list(insta_username)
        elif choice.upper() == "8":
            insta_username = raw_input(colored("Enter the username of the user: ",'blue'))
            post_a_comment(insta_username)
        elif choice.upper() == "9":
            insta_username = raw_input(colored("Enter the username of the user: ",'blue'))
            ploating_negative_positive_comments(insta_username)
        elif choice.upper() == "10":
            exit()
        else:
            print colored("sorry! you selected a wrong choice",'red')


#                                Calling the main function ..........to start the application....


if __name__ == '__main__':
    start_bot()