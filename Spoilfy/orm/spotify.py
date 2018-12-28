#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - ./common.py

import json
import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
# Package Import Hint: $ python -m Spoilfy.orm.spotify
from common import Base, engine, Resource, Reference


# ==============================================================
# >>>>>>>>>>>[    Provider's ORMs [Spotify]     ] >>>>>>>>>>>>>>
# ==============================================================
"""
Provider:
    Spotify is a [MediaProvider].
Explain:
"""


class SpotifyResource(Resource):
    __abstract__ = True

    href = Column('href', String)
    external_urls = Column('external_urls', String)



class SpotifyAccount(SpotifyResource):
    """ [ Store User Accounts with Spotify ]
        Information might involve with Authentication / Password.
    """
    __tablename__ = 'spotify_Accounts'

    followers = Column('followers', Integer, default=0)
    images = Column('images', String)

    @classmethod
    def add(cls, jsondata):
        user = cls(
            uri = jsondata['uri'],
            id = jsondata['id'],
            type = jsondata['type'],
            provider = 'spotify',
            name = jsondata['display_name'],
            external_urls = jsondata['external_urls']['spotify'],
            followers = jsondata['followers']['total'],
            href = jsondata['href'],
            images = str(jsondata['images'])
        )
        cls.session.merge(user)
        # cls.session.commit()
        print('[  OK  ] Inserted Spotify User: {}.'.format( user.name ))

        return user



class SpotifyTrack(SpotifyResource):
    """ [ Track resources in Spotify ]
    """
    __tablename__ = 'spotify_Tracks'

    atids = Column('artist_ids', String)
    #-> When is_local=True, the URI is NONE
    is_local = Column('is_local', Boolean)

    disc_number = Column('disc_number', Integer)
    duration_ms = Column('duration_ms', Integer)
    markets = Column('available_markets', String)
    preview_url = Column('preview_url', String)
    popularity = Column('popularity', Integer)
    explicit = Column('explicit', Boolean)


    @classmethod
    def add(cls, jsondata):
        j = jsondata['track']
        item = cls(
            uri = j['uri'],
            name = j['name'],
            id = j['id'],
            type = j['type'],
            provider = 'spotify',
            is_local = j['is_local'],
            atids = ','.join([ a['id'] for a in j['artists'] ]),
            disc_number = j['disc_number'],
            duration_ms = j['duration_ms'],
            markets = ','.join([ m for m in j['available_markets'] ]),
            preview_url = j['preview_url'],
            popularity = j['popularity'],
            explicit = j['explicit'],
            href = j['href'],
            external_urls = j['external_urls']['spotify']
        )
        cls.session.merge( item )   #Merge existing data
        #cls.session.commit()  #-> Better to commit after multiple inserts

        return item


class SpotifyAlbum(SpotifyResource):
    """ [ Album resources in Spotify ]
    """
    __tablename__ = 'spotify_Albums'

    atids = Column('artist_ids', String)
    tids = Column('track_ids', String)

    release_date = Column('release_date', String)
    release_date_precision = Column('release_date_precision', String)
    total_tracks = Column('total_tracks', Integer)
    lable = Column('lable', String)
    popularity = Column('popularity', Integer)
    copyrights = Column('copyrights', String)
    album_type = Column('album_type', String)
    external_ids = Column('external_ids', String)


    @classmethod
    def add(cls, jsondata):
        d = jsondata['album']
        item = cls(
            uri = d['uri'],
            name = d['name'],
            id = d['id'],
            type = d['type'],
            provider = 'spotify',
            atids = ','.join([ a['id'] for a in d['artists'] ]),
            tids = ','.join([ a['id'] for a in d['tracks']['items'] ]),
            album_type = d['album_type'],
            release_date = d['release_date'],
            release_date_precision = d['release_date_precision'],
            total_tracks = d['total_tracks'],
            lable = d['label'],
            popularity = d['popularity'],
            copyrights = str(d['copyrights']),
            href = d['href'],
            external_urls = str(d['external_urls']),
            external_ids = str(d['external_ids'])
        )
        cls.session.merge( item )
        #cls.session.commit()  #-> Better to commit after multiple inserts
        return item



class SpotifyArtist(SpotifyResource):
    """ [ Artist resources in Spotify ]
    """
    __tablename__ = 'spotify_Artists'

    genres = Column('genres', String)
    followers = Column('followers', Integer)
    popularity = Column('popularity', Integer)


    @classmethod
    def add(cls, jsondata):
        d = jsondata
        item = cls(
            uri = d['uri'],
            name = d['name'],
            id = d['id'],
            type = d['type'],
            provider = 'spotify',
            genres = str(d['genres']),
            followers = d['followers']['total'],
            popularity = d['popularity'],
            href = d['href'],
            external_urls = str(d['external_urls'])
        )
        cls.session.merge( item )   #Merge existing data
        #cls.session.commit()  #-> Better to commit after multiple inserts
        return item



class SpotifyPlaylist(SpotifyResource):
    """ [ Playlist resources in Spotify ]
    """
    __tablename__ = 'spotify_Playlists'

    owner_id = Column('owner_id', String)
    snapshot_id = Column('snapshot_id', String)
    tids = Column('track_ids', String)

    total_tracks = Column('total_tracks', Integer)
    followers = Column('followers', Integer)
    collaborative = Column('collaborative', Boolean)
    description = Column('description', String)
    public = Column('public', Boolean)
    images = Column('images', String)

    @classmethod
    def add(cls, jsondata):
        j = jsondata
        u = j['uri'].split(':')
        item = cls(
            uri = '{}:{}:{}'.format(u[0],u[3],u[4]),
            name = j['name'],
            id = j['id'],
            type = j['type'],
            provider = 'spotify',
            owner_id = j['owner']['id'],
            snapshot_id = j['snapshot_id'],
            total_tracks = j['tracks']['total'],
            public = j['public'],
            collaborative = j['collaborative'],
            images = str(j['images']),
            href = j['href'],
            external_urls = j['external_urls']['spotify'],
            #-> [Keys below are to be retrieved dynamically]:
            #tids = str(j['tracks']['href']),
            #followers = j['followers']['total'],
            #description = j['description'],
        )
        cls.session.merge( item )   #Merge existing data
        #-> Temporary: For test only to solve repeated ID issue.
        cls.session.commit()  #-> Better to commit after multiple inserts
        return item





# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_SpotifyAccount():
    try:
        SpotifyAccount.__table__.drop(engine)
        SpotifyAccount.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add an account
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_profile.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        item = SpotifyAccount.add(jsondata)
        # Add reference
        Reference.add(item)



def test_SpotifyTrack():
    try:
        SpotifyTrack.__table__.drop(engine)
        SpotifyTrack.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add a track
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_tracks.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = SpotifyTrack.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)

    # Get tracks from DB
    #SpotifyTrack.session.query()


def test_SpotifyAlbum():
    try:
        SpotifyAlbum.__table__.drop(engine)
        SpotifyAlbum.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add an album
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_albums.json', 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyAlbum.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)


def test_SpotifyArtist():
    try:
        SpotifyArtist.__table__.drop(engine)
        SpotifyArtist.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add an artist
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_artists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyArtist.add_resources(jsondata['artists']['items'])
        # Add reference
        Reference.add_resources(items)



def test_SpotifyPlaylist():
    try:
        SpotifyPlaylist.__table__.drop(engine)
        SpotifyPlaylist.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add a playlist
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_playlists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyPlaylist.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)



def test_query_track():
    print( SpotifyTrack.query.all() )

    # Get all spotify tracks of a user
    # print( Resource.metadata.__dict__['tables'] )




if __name__ == '__main__':
    test_SpotifyAccount()
    test_SpotifyTrack()
    test_SpotifyAlbum()
    test_SpotifyArtist()
    test_SpotifyPlaylist()
    # test_query_track()

