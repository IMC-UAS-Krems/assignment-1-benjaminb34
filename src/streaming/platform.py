from datetime import datetime, timedelta
from streaming.users import PremiumUser, FamilyMember
from streaming.playlists import CollaborativePlaylist
from streaming.tracks import Song

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
    


  # QUERIES 1 - 10

    # Q1: Total Cumulative Listening Time
    def total_listening_time_minutes(self, start, end):
      total_time = float(0)
      users = [x for x in self._users.values()]
      for user in users:   
          for session in user.sessions:
            if start <= session.timestamp <= end:
              total_time += session.duration_listened_minutes()
      return total_time
    
    # Q2: Average Unique Tracks per Premium User
    def avg_unique_tracks_per_premium_user(self, days=30):
      users = [x for x in self._users.values()]
      number_of_tracks = []
      number_of_prem_users = 0
      for user in users:
        if isinstance(user, PremiumUser):
          unique_tracks = []
          number_of_prem_users += 1
          for session in user.sessions:
            if session.timestamp >= datetime.now() - timedelta(days=days) and not(session.track in unique_tracks):
              unique_tracks.append(session.track)
          number_of_tracks.append(len(unique_tracks))
      if sum(number_of_tracks) > 0:
        return sum(number_of_tracks)/number_of_prem_users
      else:
        return float(0)

    # Q3: Track with Most Distinct Listeners
    def track_with_most_distinct_listeners(self):
      if self._sessions == []:
        return None
      session_users = [x.user.user_id for x in self._sessions]
      session_tracks = [x.track.track_id for x in self._sessions]
      #since we dont need duplicated, i did this to remove them (zipping together the two lists, then making them usable by tuple(), then removing duplicated with set(), then making them two different lists again with zip(*))
      session_users, session_tracks = zip(*list(set(list(tuple(zip(session_users, session_tracks))))))
      session_users = list(session_users)
      session_tracks = list(session_tracks)
      #in order for the for loop to work, it needs a valid string ("t5"), but you could make it anything, it just needs to be part of session_tracks
      most_listened = "t5"
      for track in session_tracks:
        if session_tracks.count(track) > session_tracks.count(most_listened):
          most_listened = track
      return most_listened

    # Q4: Average Session Duration by User Type
    def avg_session_duration_by_user_type(self):
      users = {}
      result = []
      for user in self._users.values():
        if not (user.name in users):
          users[user.name] = 0
        listened = 0
        for session in user.sessions:
          listened += session.duration_listened_seconds
        users[user.name] = users[user.name] + listened
      for element in users:
        # this part just counts how many users for each type is in the list by the .count() method. the element is the name of the user type
        number_of_users_per_type = [x.name for x in self._users.values() if x.sessions].count(element)
        result.append((element, float(users[element]/number_of_users_per_type)))
      return sorted(result, key=lambda x : x[1], reverse=True)

    # Q5: Total Listening Time for Underage Sub-Users
    def total_listening_time_underage_sub_users_minutes(self):
      total_listening_time = 0
      for user in self._users.values():
        if user.age < 18 and isinstance(user, FamilyMember):
          for session in user.sessions:
            total_listening_time += session.duration_listened_seconds
      return float(total_listening_time)

    # Q6: Top Artists by Listening Time
    def top_artists_by_listening_time(self, n=5):
      time_by_artists = {}
      for session in self._sessions:
        if not session.track.artist in time_by_artists:
          time_by_artists[session.track.artist] = session.duration_listened_seconds
        else:
          time_by_artists[session.track.artist] += session.duration_listened_seconds
      result = [(x, float(time_by_artists[x])) for x in time_by_artists.keys()]
      return sorted(result, key=lambda x: x[1], reverse=True)[:n]

    # Q7: User's Top Genre
    def user_top_genre(self, user_id):
      if user_id not in self._users or len(self._users[user_id].sessions) == 0:
        return None
      user = self._users[user_id]
      listened_genres = {}
      for session in user.sessions:
        if session.track.genre not in listened_genres:
          listened_genres[session.track.genre] = session.duration_listened_seconds
        else:
          listened_genres[session.track.genre] += session.duration_listened_seconds
      largest = max(listened_genres, key=lambda x: x[1])
      denominator = sum(listened_genres[x] for x in listened_genres)
      return (largest, int(listened_genres[largest]*100/denominator))
    
    # Q8: Collaborative Playlists with Many Artists
    def collaborative_playlists_with_many_artists(self, threshold=3):
      result = []
      for playlist in self._playlists.values():
        if isinstance(playlist, CollaborativePlaylist) and len(set([x.artist for x in playlist.tracks if isinstance(x, Song)])) > threshold:
          result.append(playlist)
      return result
    
    # Q9: Average Tracks per Playlist Type
    def avg_tracks_per_playlist_type(self):
      result = {}
      num_play = 0
      num_coll = 0
      for playlist in self._playlists.values():
        if isinstance(playlist, CollaborativePlaylist):
          if playlist not in result:
            result["CollaborativePlaylist"] = len(playlist.tracks)
          else:
            result["CollaborativePlaylist"] += len(playlist.tracks)
          num_coll += 1
        else:
          if playlist not in result:
            result["Playlist"] = len(playlist.tracks)
          else:
            result["Playlist"] += len(playlist.tracks)
          num_play += 1
        if "Playlist" not in result:
          result["Playlist"] = 0
          num_play = 1
        if "CollaborativePlaylist" not in result:
          result["CollaborativePlaylist"] = 0
          num_coll = 1
        result["CollaborativePlaylist"] = result["CollaborativePlaylist"]/num_coll
        result["Playlist"] = result["Playlist"]/num_play
      return result

    # Q10: Users Who Completed Albums
    def users_who_completed_albums(self):
      result = []
      for user in self._users.values():
        listened = []
        total_albums = []
        for session in user.sessions:
          listened.append(session.track.track_id)
        for album in self._albums.values():
          if album.track_ids().issubset(listened):
            total_albums.append(album.title)
          result.append((user, total_albums))
      return result
    
