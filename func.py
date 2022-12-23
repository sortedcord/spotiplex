import pickle

class Song():
    def __init__(self, track_name, track_artist, spot_track_id=None, duration=None):
        self.name = track_name
        self.artist = track_artist
        
        self.spot_id = spot_track_id
        self.duration = duration

        self.matching_tracks = []
        self.confirmed_matching_track = None
        self.confirmed_matching_track_index = None

        self.deezer = {
            'id': None,
        }

    def update_status(self):
        if not self.matching_tracks:
            self.display_color = 'red'
        elif self.matching_tracks and not self.confirmed_matching_track:
            self.display_color = 'gold3'
        elif self.matching_tracks and self.confirmed_matching_track:
            self.display_color = 'cyan2'

    def cache_track(self):
        try:
            with open('song_cache.pickle', 'rb+') as f:
                song_cache = pickle.load(f)
            
                for song in song_cache:
                    if self == song:
                        pass
                    elif self.name == song.name and self.artist == song.artist:
                        song_cache.remove(song)
                        song_cache.append(self)
                        
                
                song_cache.append(self)
        
        except:
            song_cache = [self]
        
        # If the songcache is corrupted, it will be overwritten
        with open('song_cache.pickle', 'wb') as f:
            pickle.dump(song_cache, f)