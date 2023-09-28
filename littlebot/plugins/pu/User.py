class User(object):

    def __init__(self, user_id, oauth_token, oauth_token_secret, uid=0):
        self.user_id = user_id
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.uid = uid
