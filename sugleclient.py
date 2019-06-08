import sys
import Pyro4
import Pyro4.util
from suglework import SugleAccount
import time


sys.excepthook = Pyro4.util.excepthook
Pyro4.config.SERIALIZER = 'pickle'

# You can change the network name to create a separate network
network_name = 'oka'

network = Pyro4.Proxy("PYRONAME:net.sugle." + network_name)
def print_menu():
    menu = """
    1. Create account
    2. Add friend
    3. Get friend's personal info
    4. Add to my news post
    5. Get friend's news
    6. Get latest news from all friends
    7. Message a friend
    8. Read my inbox
    9. Edit my info
    10. Exit
    """
    print(menu)

def create_account():
    user_name = raw_input('Create user name: ')
    full_name = raw_input('Your full name: ')
    account = SugleAccount(user_name, full_name)
    network.create_account(account)
    return user_name

def add_friend(account_name):
    if account_name != '':
        friend_name = raw_input("Enter friend's user name: ")
        network.add_friend(account_name, friend_name)
        return friend_name
    else:
        return False

def get_friend_info(account_name):
    if account_name != '':
        friend_name = raw_input("Enter your friend's user name: ")
        info = network.get_friend_info(account_name, friend_name)
        return info
    else:
        return False

def display_personal_info(info):
    print(info)

def add_news(account_name):
    if account_name != '':
        news_update = raw_input("Enter your news update: ")
        network.add_news(account_name, news_update)
        return True
    else:
        return False

def get_friend_news(account_name):
    if account_name != '':
        friend_name = raw_input("Enter your friend's user name: ")
        news = network.get_friend_news(account_name, friend_name)
        return news
    else:
        return False


def display_friend_news(news):
    print(news)

def get_latest_news(account_name):
    if account_name != '':
        news = network.get_all_friends_latest_news(account_name)
        return news
    else:
        return False

def display_latest_news(news):
    print(news)

def post_message(account_name):
    if account_name != '':
        friend_name = raw_input("Enter your friend's username: ")
        message = raw_input("Enter your message: ")
        network.post_message(account_name, friend_name, message)
        return True
    else:
        return False

def read_inbox(account_name):
    messages = network.read_messages(account_name)
    print(messages)

def edit_info(account_name):
    if account_name != '':
        my_account = network.get_user_account(account_name)
        full_name = raw_input("Enter your full name [leave empty for no change]:")
        email = raw_input("Enter your email [leave empty for no change]: ")
        fav_food = raw_input("Enter your favourite food [leave empty for no change]: ")
        info_dict = {'name': full_name,
                     'email': email,
                     'favourite_food': fav_food}
        status = network.edit_personal_info(account_name, info_dict)
        return status
    else:
        return False
done = False
account_name = None

while not done:
    print_menu()
    choice = raw_input("Enter your choice: ")
    if choice == '10':
        done = True
    elif choice == '1':
        status = create_account()
        print(status)
        if status != '':
            account_name = status
            print('Account created: ' + account_name)
        else:
            print("Error: Cannot create account.")
    elif choice == '2':
        status = add_friend(account_name)
        if status != '':
            friend_name = status
            print('Friend %s added to your account.'% friend_name)
        else:
            print("Error: Cannot add friend.")
    elif choice == '3':
        status = get_friend_info(account_name)
        if status != '':
            info = status
            display_personal_info(info)
        else:
            print("Error: Cannot get friend's personal info.")
    elif choice == '4':
        status = add_news(account_name)
        if not status:
            print("News added to your page.")
        else:
            print("Error: Cannot add news to your page.")
    elif choice == '5':
        status = get_friend_news(account_name)
        if status != '':
            news = status
            display_friend_news(news)
        else:
            print("Error: Cannot get friend's news")
    elif choice == '6':
        status = get_latest_news(account_name)
        if status != '':
            news = status
            display_latest_news(news)
        else:
            print("Error: Cannot get latest news.")
    elif choice == '7':
        status = post_message(account_name)
        if not status:
            print("Message sent.")
        else:
            print("Error: Message cannot be sent.")
    elif choice == '8':
        status = read_inbox(account_name)
    elif choice == '9':
        status = edit_info(account_name)
        if not status:
            print("Info editted.")
        else:
            print("Error: Cannot edit personal info.")
    else:
        print('Invalid choice. Try again.')
