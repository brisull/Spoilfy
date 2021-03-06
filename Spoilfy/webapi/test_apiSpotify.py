#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from apiSpotify import SpotifyAPI


# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


class TestSpotifyAPI(unittest.TestCase):

    def setUp(self):
        # Get auth info
        with open('./.spotify_app.json', 'r') as f:
            data = json.loads(f.read())
            # self.api = SpotifyAPI(data)

    def test_get_a_track(self):
        # print('[FETCHING] a track...')
        # print( '\t', api.get_a_track('4Uyn4iboGtdgqXXSyErTyO').get('name') )
        pass

    def test_get_a_album(self):
        # print('[FETCHING] an album...')
        # print( '\t', api.get_a_album('2Y9IRtehByVkegoD7TcLfi').get('name') )
        pass

    def test_get_a_artist(self):
        # print('[FETCHING] an artist...')
        # print( '\t', api.get_a_artist('0L8ExT028jH3ddEcZwqJJ5').get('name') )
        pass

    def test_get_a_playlist(self):
        # print('[FETCHING] a playlist...')
        # print( '\t', api.get_a_playlist('1N0IfF495qdmrcRB8kAXrf').get('name') )
        pass

    def test_get_album_tracks(self):
        # print('[FETCHING] album tracks...')
        # for page in api.get_album_tracks('2Y9IRtehByVkegoD7TcLfi'):
            # tracks = [ o['name'] for o in page['items'] ]
            # print( '\t', len(tracks), 'tracks' )
        pass

    def test_get_playlist_tracks(self):
        # for page in api.get_playlist_tracks('1N0IfF495qdmrcRB8kAXrf'):
            # tracks = [ o['track']['name'] for o in page['items'] ]
            # print( '\t', len(tracks), 'tracks' )
        pass

    def test_get_my_profile(self):
        # print( api.get_my_profile()['display_name'] )
        pass

    def test_get_my_tracks(self):
        # for t in api.get_my_tracks():
            # print('At {} / {}, {} per page, Next URL: {}'.format(
                # t.get('offset'), t.get('total'), t.get('limit'), t.get('next')
            # ))
        pass

    def test_get_my_albums(self):
        # for t in api.get_my_albums():
            # print('At {} / {}, {} per page, Next URL: {}'.format(
                # t.get('offset'), t.get('total'), t.get('limit'), t.get('next')
            # ))
        pass

    def test_get_my_artists(self):
        # for t in api.get_my_artists():
            # # Artist list DOESN'T support [limit], [offset]
            # print('Total {}, Next URL: {}'.format(
                # t.get('artists').get('total'), t.get('artists').get('next')
            # ))
        pass

    def test_get_my_playlists(self):
        pass


if __name__ == '__main__':
    unittest.main()
