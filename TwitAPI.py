import twitter as pt

# Depth for the DFS used in ret_data
DEPTH_LIMIT = 4


def start_api(consumerID, consumerSECRET, accessID, accessSECRET):
    """ Returns the usable Twitter API that runs the front-end of TwitCat. Utilizes the access token credentials.
        Returns the username and the api connection to Twitter to be used
        in the future
    """
    api = pt.Api(consumer_key=consumerID, consumer_secret=consumerSECRET, access_token_key=accessID,
                 access_token_secret=accessSECRET, sleep_on_rate_limit=True)
    user = input("enter your username (do not include @): ")
    return api, user

# the resulting dictionary that is used in get_data. used as a global so that scope is not an issue
final_data = dict()


def get_data(subject, api, user):
    """ Takes in the subject the user wants to search for, the API given by start_api as well as the user's name.
        Utilizes DFS algorithm ret_data to find friends of friends and also of those who are popular among the subject
        searched for and adds them to final_dict. Returns a dictionary of userIDs, which contain dictionaries
        of the separate attributes for each user found.
    """
    followers = api.GetFollowers(screen_name=user, total_count=200)
    friends = api.GetFriends(screen_name=user, total_count=200)
    top_users = api.GetUsersSearch(term=subject, count=10, include_entities=True)
    for follower in followers:
        try:
            ret_data(follower, 0, api)
            final_data[follower.id] = follower
        except:
            pass
    for friend in friends:
        try:
            ret_data(friend, 0, api)
            final_data[friend.id] = friend
        except:
            pass
    for user in top_users:
        try:
            ret_data(user, 0, api)
            final_data[user.id] = user
        except:
            pass
    return final_data


def ret_data(ID, depth, api):
    """ A Depth First Search that looks for users related to the one entered in the search, then adds them to the
        final dictionaries of users. Does not return anything, merely appends to the final_data dictionary
    """
    if depth > DEPTH_LIMIT:
        return
    for friend in api.GetFriends(user_id=ID.id, total_count=10):
        ret_data(friend, depth + 1, api)
        final_data[friend.id] = friend
    final_data[ID.id] = ID


def make_follow(users, consumer_key, consumer_secret, access_id, access_secret):
    """ takes in the recommended users from logic.py and user login credentials along with API credentials and
        sets the user to follow all of the recommended users, returns True if sucessfull, else False
    """
    try:
        api = pt.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_id,
                     access_token_secret=access_secret, sleep_on_rate_limit=True)
        for user in users:
            api.CreateFriendship(user_id=user)
        return True
    except:
        return False








