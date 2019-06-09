import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class SugleNetwork(object):
    def __init__(self):
        self.users = {}

    def create_account(self, new_account):
        if new_account.username not in self.users:
            self.users[new_account.username] = new_account
            print("Creating account for: " + new_account.username)
            return True
        else:
            print("Error in creating account.")
            return False

    def add_friend(self, current_user, friend_user):
        if current_user in self.users and friend_user in self.users:
            self.users[current_user].add_friend(self.users[friend_user])
            print("Adding %s to %s's friend list"%(friend_user, current_user))
            return True
        else:
            print("Error in adding friend.")
            return False

    def remove_friend(self, current_user, friend_user):
        if current_user in self.users and friend_user in self.users:
            self.users[current_user].remove_friend(self.users[friend_user])
            print("%s has been removed from %s friend's list." %(friend_user, current_user))
            return True
        else:
            print("Error in removing friend.")
            return False

    def get_friend_news(self, current_user, friend_user):
        if current_user in self.users and friend_user in self.users[current_user].friends:
            print("Getting news from %s"%friend_user)
            return self.users[friend_user].get_all_news()
        else:
            print("Error in getting news.")
            return False

    def get_all_friends_latest_news(self, current_user):
        if current_user in self.users:
            all_news = {}
            for friend in self.users[current_user].friends:
                all_news[friend] = self.users[current_user].friends[friend].get_latest_news()
            print("Getting all news from %s's friends."%current_user)
            return all_news
        else:
            print("Error in getting latest news.")
            return False

    def post_message(self, from_user, dest_user, message):
        if from_user in self.users and dest_user in self.users:
            self.users[dest_user].add_to_inbox(from_user, message)
            print("Message posted to %s."%dest_user)
            return True
        else:
            print("Error in posting message.")
            return False

    def get_friend_info(self, from_user, friend_user):
        if from_user in self.users and friend_user in self.users:
            print("Gettin info from %s." % friend_user)
            return self.users[friend_user].personal_info
        else:
            print("Error in getting personal info.")
            return False

    def add_news(self, user, news):
        if user in self.users:
            self.users[user].add_news(news)
            print("News added to %s." % user)
            return True
        else:
            print("Error in adding news.")
            return False

    def read_messages(self, user):
        if user in self.users:
            print("Reading inbox for %s." % user)
            return self.users[user].read_inbox()
        else:
            print("Error in reading message.")
            return False
    def edit_personal_info(self, user, info_dict):
        if user in self.users:
            if info_dict['name'] != '':
                self.users[user].personal_info['name'] =info_dict['name']
            if info_dict['email'] != '':
                self.users[user].personal_info['email'] =info_dict['email']
            if info_dict['favourite_food'] != '':
                self.users[user].personal_info['favourite_food'] =info_dict['favourite_food']
            print("Info edited for %s." % user)
            return True
        else:
            print("Error in editing info.")
            return False

    def get_user_account(self, user):
        if user in self.users:
            print("Retrieving account for %s." % user)
            return self.users[user]
        else:
            print("Error in Retrieving account.")
            return False


def run_pyro_daemon(network_name, ipaddress):
    try:
        with Pyro4.Daemon(ipaddress) as daemon:
            ns = Pyro4.locateNS()
            uri = daemon.register(SugleNetwork)
            ns.register('net.sugle.' + network_name, uri)
            daemon.requestLoop()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
    network_name = 'oka'
    ipaddress = 'localhost'
    run_pyro_daemon(network_name, ipaddress)
