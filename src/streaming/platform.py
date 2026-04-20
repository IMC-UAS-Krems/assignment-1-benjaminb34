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
        number_of_users_per_type = [x.name for x in self._users.values() if x.sessions].count(element)
        result.append((element, float(users[element]/number_of_users_per_type)))
     
      return sorted(result, key=lambda x : x[1], reverse=True)

    def total_listening_time_underage_sub_users_minutes(self):
      total_listening_time = 0
      for user in self._users.values():
        if user.age < 18 and isinstance(user, FamilyMember):
          for session in user.sessions:
            total_listening_time += session.duration_listened_seconds
      return float(total_listening_time)

    def top_artists_by_listening_time(self, n=5):
      time_by_artists = {}
      for session in self._sessions:
        if not session.track.artist in time_by_artists:
          time_by_artists[session.track.artist] = session.duration_listened_seconds
        else:
          time_by_artists[session.track.artist] += session.duration_listened_seconds
      
      result = [(x, float(time_by_artists[x])) for x in time_by_artists.keys()]
      print(sorted(result, key=lambda x: x[1], reverse=True)[:n])
      return sorted(result, key=lambda x: x[1], reverse=True)[:n]

    
    def user_top_genre(self, user_id):
      if user_id not in self._users or len(self._users[user_id].sessions) == 0:
        return None
      user = self._users[user_id]
      print(user.name)
      listened_genres = {}
      for session in user.sessions:
        print(session.session_id)
        if session.track.genre not in listened_genres:
          listened_genres[session.track.genre] = session.duration_listened_seconds
        else:
          listened_genres[session.track.genre] += session.duration_listened_seconds
        print(listened_genres)
      largest = max(listened_genres, key=lambda x: x[1])
      denominator = sum(listened_genres[x] for x in listened_genres)
      return (largest, int(listened_genres[largest]*100/denominator))
    
    def collaborative_playlists_with_many_artists(self, threshold=3):
      result = []
      for playlist in self._playlists.values():
        if isinstance(playlist, CollaborativePlaylist) and len(set([x.artist for x in playlist.tracks if isinstance(x, Song)])) > threshold:
          result.append(playlist)
      return result
    
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
    
