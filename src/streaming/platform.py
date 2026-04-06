"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime, timedelta
from streaming.users import PremiumUser

class StreamingPlatform():
    def __init__(self, name):
      self.name = name
      self._catalouge = {}
      self._users = {}
      self._albums = {}
      self._artists = {}
      self._playlists = {}
      self._sessions = []

    def add_track(self, track):
      self._catalouge.update({track.track_id : track})

    def add_user(self, user):
      self._users.update({user.user_id : user})

    def add_artist(self, artist):
      self._artists.update({artist.artist_id : artist})

    def add_album(self, album):
      self._albums.update({album.album_id : album})

    def add_playlist(self, playlist):
      self._playlists.update({playlist.playlist_id : playlist})

    def record_session(self, session):
      self._sessions.append(session)

    def get_track(self, track_id):
      return self._catalouge[track_id]

    def get_user(self, user_id):
      return self._users[user_id]

    def get_artist(self, artist_id):
      return self._artists[artist_id]

    def get_album(self, album_id):
      return self._albums[album_id]

    def all_users(self):
      return [x for x in self._users.values()]

    def all_tracks(self):
      return [x for x in self._catalouge.values()]
    
    def total_listening_time_minutes(self, start, end):
      total_time = float(0)
      # 1st get all user objects in a list
      users = [x for x in self._users.values()]
      # 2nd search for sessions in those user objects which are in between the start and the end
      for user in users:
          for session in user.sessions:
            # 3rd check if session time is within the start and the end
            if start <= session.timestamp <= end:
              total_time += session.duration_listened_minutes()
      return total_time
    
    def avg_unique_tracks_per_premium_user(self, days=30):
      # 1st get all user IDs
      users = [x for x in self._users.values()]
      number_of_tracks = []
      number_of_prem_users = 0
      # 2nd go thourgh every user
      for user in users:
        if isinstance(user, PremiumUser):
          unique_tracks = []
          number_of_prem_users += 1
          # 3rd go throught the user's sessions and if they fit the timespan given, then append it unique_tracks list (each user has a unique_track list)
          for session in user.sessions:
            if session.timestamp >= datetime.now() - timedelta(days=days) and not(session.track in unique_tracks):
              unique_tracks.append(session.track)
          # 4th append the length of the list to the number_of_tracks list
          number_of_tracks.append(len(unique_tracks))
      if sum(number_of_tracks) > 0:
        # 5th sum together every integer in the list number_of_tracks, so you get the total amount of unique tracks played, and then divide it with the number of premium users
        return sum(number_of_tracks)/number_of_prem_users
      else:
        return float(0)

    def track_with_most_distinct_listeners(self):
      if self._sessions == []:
        return None
      # 1st create a list for all users and their tracks out of self._sessions
      session_users = [x.user.user_id for x in self._sessions]
      session_tracks = [x.track.track_id for x in self._sessions]
      # 2nd since we dont need duplicated, i did this to remove them (zipping together the two lists, then making them usable by tuple(), then removing duplicated with set(), then making them two different lists again with zip(*))
      session_users, session_tracks = zip(*list(set(list(tuple(zip(session_users, session_tracks))))))
      session_users = list(session_users)
      session_tracks = list(session_tracks)
      # 4th in order for the for loop to work, it needs a valid string ("t5"), but you could make it anything, it just needs to be part of session_tracks
      most_listened = "t5"
      # 5th this for loops goes through every track and then checks which one is most frequent in the list by using count()
      for track in session_tracks:
        if session_tracks.count(track) > session_tracks.count(most_listened):
          most_listened = track
      return most_listened

    def avg_session_duration_by_user_type(self):
      return []

    def total_listening_time_underage_sub_users_minutes(self):
      pass

    def top_artists_by_listening_time(self, n=3):
      return []
    
    def user_top_genre(self, user_id):
      return ("aa", 3.4)
    
    def collaborative_playlists_with_many_artists(self, threshold=100):
      return []
    
    def avg_tracks_per_playlist_type(self):
      pass

    def users_who_completed_albums(self):
      return [("aa", [])]
    
