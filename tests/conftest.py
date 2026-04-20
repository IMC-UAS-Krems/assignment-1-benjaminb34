"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import (
    AlbumTrack,
    SingleRelease,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


# ---------------------------------------------------------------------------
# Helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # well within 30-day window
OLD    = FIXED_NOW - timedelta(days=60)   # outside 30-day window


@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # Artists
    # ------------------------------------------------------------------
    pixels  = Artist("a1", "Pixels", genre="pop")
    neon = Artist("a2", "Neon Dreams", genre="synthwave")
    ember = Artist("a3", "Ember Lane", genre="indie")
    atlas = Artist("a4", "Atlas Echo", genre="alternative")
    nova = Artist("a5", "Nova Pulse", genre="electronic")
    sage = Artist("a6", "Sage River", genre="folk")
    
    for artist in (pixels, neon, ember, atlas, nova, sage):
        platform.add_artist(artist)

    # ------------------------------------------------------------------
    # Albums & AlbumTracks
    # ------------------------------------------------------------------
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain",      180, "pop",  pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon",    210, "pop",  pixels, track_number=2)
    t3 = AlbumTrack("t3", "Vector Fields",   195, "pop",  pixels, track_number=3)
    for track in (t1, t2, t3):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(dd)

    nd1 = Album("alb2", "Midnight Circuit", artist=neon, release_year=2021)
    t4 = AlbumTrack("t4", "Electric Dusk",   200, "synthwave", neon, track_number=1)
    t5 = AlbumTrack("t5", "Neon Skyline",    215, "synthwave", neon, track_number=2)
    for track in (t4, t5):
        nd1.add_track(track)
        platform.add_track(track)
        neon.add_track(track)
    platform.add_album(nd1)

    nd2 = Album("alb3", "Retro Future", artist=neon, release_year=2023)
    t6 = AlbumTrack("t6", "Chrome Nights",   205, "synthwave", neon, track_number=1)
    t7 = AlbumTrack("t7", "Laser Hearts",    198, "synthwave", neon, track_number=2)
    for track in (t6, t7):
        nd2.add_track(track)
        platform.add_track(track)
        neon.add_track(track)
    platform.add_album(nd2)
    
    el1 = Album("alb4", "Fading Lights", artist=ember, release_year=2020)
    t8  = AlbumTrack("t8", "Soft Ashes",     190, "indie", ember, track_number=1)
    t9  = AlbumTrack("t9", "Quiet Glow",     175, "indie", ember, track_number=2)
    for track in (t8, t9):
        el1.add_track(track)
        platform.add_track(track)
        ember.add_track(track)
    platform.add_album(el1)

    el2 = Album("alb5", "Golden Evenings", artist=ember, release_year=2022)
    t10 = AlbumTrack("t10", "Warm Air",      185, "indie", ember, track_number=1)
    t11 = AlbumTrack("t11", "Last Light",    178, "indie", ember, track_number=2)
    for track in (t10, t11):
        el2.add_track(track)
        platform.add_track(track)
        ember.add_track(track)
    platform.add_album(el2)
    
    ae1 = Album("alb6", "Wander Signals", artist=atlas, release_year=2019)
    t12 = AlbumTrack("t12", "Lost Frequencies", 210, "alternative", atlas, track_number=1)
    t13 = AlbumTrack("t13", "Northbound",       220, "alternative", atlas, track_number=2)
    for track in (t12, t13):
        ae1.add_track(track)
        platform.add_track(track)
        atlas.add_track(track)
    platform.add_album(ae1)

    ae2 = Album("alb7", "Gravity Maps", artist=atlas, release_year=2024)
    t14 = AlbumTrack("t14", "Falling Lines",    205, "alternative", atlas, track_number=1)
    t15 = AlbumTrack("t15", "Orbiting You",     215, "alternative", atlas, track_number=2)
    for track in (t14, t15):
        ae2.add_track(track)
        platform.add_track(track)
        atlas.add_track(track)
    platform.add_album(ae2)
    
    np1 = Album("alb8", "Starlight Drive", artist=nova, release_year=2021)
    t16 = AlbumTrack("t16", "Photon Rush",   230, "electronic", nova, track_number=1)
    t17 = AlbumTrack("t17", "Night Engine",  225, "electronic", nova, track_number=2)
    for track in (t16, t17):
        np1.add_track(track)
        platform.add_track(track)
        nova.add_track(track)
    platform.add_album(np1)

    t18 = SingleRelease("t18", "Plasma Beat",   240, "electronic", nova, datetime(2022, 8, 1))
    t19 = SingleRelease("t19", "Zero Gravity",  235, "electronic", nova, datetime(2026, 1, 19))
    for track in (t18, t19):
        platform.add_track(track)
        nova.add_track(track)
    
    sr1 = Album("alb10", "Whispering Pines", artist=sage, release_year=2018)
    t20 = AlbumTrack("t20", "Forest Song", 210, "folk", sage, track_number=1)
    t21 = AlbumTrack("t21", "Riverbend", 200, "folk", sage, track_number=2)
    for track in (t20, t21):
        sr1.add_track(track)
        platform.add_track(track)
        sage.add_track(track)
    platform.add_album(sr1)

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice",   age=30)
    bob   = PremiumUser("u2", "Bob",   age=25, subscription_start=date(2023, 1, 1))
    rob = FreeUser("u3", "Rob",   age=27)
    john = FamilyAccountUser("u4", "John", age=45)
    ashley = FamilyMember("u5", "Ashley", age=20, parent=john)
    david = FamilyMember("u6", "David", age=17, parent=john)
    john.add_sub_user(ashley)
    john.add_sub_user(david)

    for user in (alice, bob, rob, john, ashley, david):
        platform.add_user(user)

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------
    s1 = ListeningSession("s1", john, t21, datetime(2024, 1, 1), 200)
    s2 = ListeningSession("s2", john, t10, datetime(2026, 3, 15), 185)
    s3 = ListeningSession("s3", bob, t1, datetime(2023, 5, 6), 180)
    s4 = ListeningSession("s4", bob, t6, datetime(2026, 3, 10), 205)
    s5 = ListeningSession("s5", john, t21, datetime(2022, 1, 1), 200)
    s6 = ListeningSession("s6", ashley, t5, datetime(2023, 3, 15), 215)
    s7 = ListeningSession("s7", david, t1, datetime(2024, 5, 6), 180)
    s8 = ListeningSession("s8", rob, t16, datetime(2024, 3, 10), 230)
    s9 = ListeningSession("s9", david, t1, datetime(2024, 5, 3), 180)
    s10 = ListeningSession("s10", david, t6, datetime(2022, 3, 10), 205)
    s11 = ListeningSession("s11", david, t6, datetime(2022, 3, 11), 205)
    s12 = ListeningSession("s12", david, t6, datetime(2022, 3, 12), 205)
    s13 = ListeningSession("s13", ashley, t1, datetime(2022, 3, 12), 180)
    john.add_session(s1)
    john.add_session(s2)
    bob.add_session(s3)
    bob.add_session(s4)
    john.add_session(s5)
    ashley.add_session(s6)
    david.add_session(s7)
    rob.add_session(s8)
    david.add_session(s9)
    david.add_session(s10)
    david.add_session(s11)
    david.add_session(s12)
    ashley.add_session(s13)
    for session in [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13]:
        platform.record_session(session)
    
    return platform


@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD
