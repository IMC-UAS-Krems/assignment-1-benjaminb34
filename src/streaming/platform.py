"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

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
              total_time += session.duration_listened_minutes
      return total_time
    
    def avg_unique_tracks_per_premium_user(self, days=30):
      return float()

    def track_with_most_distinct_listeners(self):
      pass

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
    
