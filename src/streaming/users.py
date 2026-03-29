"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

class User:
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []
    
    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_seconds(self):
        return sum([x.duration_listened_seconds for x in self.sessions])
    
    def total_listening_minutes(self):
        return float(sum([x.duration_listened_seconds for x in self.sessions])/60)  
    
    def unique_tracks_listened(self):
        return set([x.track.track_id for x in self.sessions])

class FreeUser(User):
    def __init__(self, user_id, name, age):
        User.__init__(self, user_id, name, age)
        MAX_SKIPS_PER_HOURS = 6

class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start):
        User.__init__(self, user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(User):
    def __init__(self, user_id, name, age):
        User.__init__(self, user_id, name, age)
        self.sub_users = []

    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        return [self] + self.sub_users

class FamilyMember(User):
    def __init__(self, user_id, name, age, parent):
        User.__init__(self, user_id, name, age)
        self.parent = parent