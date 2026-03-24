"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""

class Track:
    def __init__(self, track_id, title, duration_seconds, genre):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self):
        return self.duration_seconds/60

class Song(Track):
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        Track.__init__(self, track_id, title, duration_seconds, genre,)
        self.artist = artist

class Podcast(Track):
    def __init__(self, track_id, title, duration_seconds, genre, host, description):
        Track.__init__(self, track_id, title, duration_seconds, genre,)
        self.host = host
        self.description = description