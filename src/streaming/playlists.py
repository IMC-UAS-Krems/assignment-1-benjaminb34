"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

class Playlist:
    def __init__(self, playlist_id, name, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []

    def add_track(self, track):
        if not(track in self.tracks):
            self.tracks.append(track)

    def remove_track(self, track_id):
        for index, track in enumerate(self.tracks):
            if track.track_id == track_id:
                self.tracks.pop(index)

    def total_duration_seconds(self):
        return sum([x.duration_seconds for x in self.tracks])

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner):
        Playlist.__init__(self, playlist_id, name, owner)
        self.contributors = [owner]

    def add_contributor(self, user):
        if not(user in self.contributors):
            self.contributors.append(user)

    def remove_contributor(self, user):
        if user != self.owner:
            self.contributors.remove(user)