import pymongo

cluster = pymongo.MongoClient('mongodb://localhost:27017')
users = cluster.MartingaleStrategy.users
config = cluster.MartingaleStrategy.config


# add info
def add_user(user_id, user_name, nick_name):
    if not users.find_one({"_id": str(user_id)}):
        users.insert_one({
            "_id": str(user_id),
            "telegram_id": str(user_id),
            "user_name": str(user_name),
            "nick_name": str(nick_name),
            "info": None
        })
    else:
        users.update_one({"_id": str(user_id)}, {"$set": {"nick_name": nick_name}})


# get info
def get_password():
    password = config.find_one({"_id": "config"})
    return password['pass']


def get_messages():
    message = config.find_one({"_id": "config"})
    return message['messages']


def get_buttons():
    button = config.find_one({"_id": "config"})
    return button['buttons']


def get_pass():
    passwd = config.find_one({"_id": "config"})
    return passwd['pass']


def get_info_user(user_id):
    info = users.find_one({"_id": str(user_id)})
    return info


def get_coeff():
    info = config.find_one({"_id": "config"})
    return info['coeff']


# edit info
def edit_message_db(_id, message):
    config.update_one({"_id": "config"}, {"$set": {f"messages.{_id}": message}})


def edit_button_db(_id, message):
    config.update_one({"_id": "config"}, {"$set": {f"buttons.{_id}": message}})


def edit_pass_db(message):
    config.update_one({"_id": "config"}, {"$set": {"pass": message}})


def edit_info_user(user_id, info):
    users.update_one({"_id": str(user_id)}, {"$set": {"info": info}})


def edit_coeff(coeff):
    info = coeff.split(":")
    config.update_one({"_id": "config"}, {"$set": {"coeff.0": float(info[0])}})
    config.update_one({"_id": "config"}, {"$set": {"coeff.1": float(info[1])}})
