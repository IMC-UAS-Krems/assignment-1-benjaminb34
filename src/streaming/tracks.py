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
from abc import ABC

class Track(ABC):
    def __init__(self, track_id, title, duration_seconds, genre):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self):
        return self.duration_seconds/60
    
    def __eq__(self, other):
        return isinstance(self, Track) and isinstance(other, Track) and self.track_id == other.track_id

class Song(Track):
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        Track.__init__(self, track_id, title, duration_seconds, genre,)
        self.artist = artist

class Podcast(Track):
    def __init__(self, track_id, title, duration_seconds, genre, host="", description=""):
        Track.__init__(self, track_id, title, duration_seconds, genre,)
        self.host = host
        self.description = description

class AudiobookTrack(Track):
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator):
        Track.__init__(self, track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator

class AlbumTrack(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number):
        Song.__init__(self, track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = None

class SingleRelease(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date):
        Song.__init__(self, track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date

class NarrativeEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host="", description="", season=0, episode_number=0):
        Podcast.__init__(self, track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number

class InterviewEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host="", description="", guest=""):
        Podcast.__init__(self, track_id, title, duration_seconds, genre, host, description)
        self.guest = guest