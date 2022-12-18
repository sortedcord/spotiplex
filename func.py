import pickle

class Song():
    def __init__(self, track_name, track_artist, spot_track_id=None, duration=None):
        self.name = track_name
        self.artist = track_artist
        
        self.spot_id = spot_track_id
        self.duration = duration

        self.matching_tracks = []

    def cache_track(self):
        try:
            with open('song_cache.pickle', 'rb+') as f:
                song_cache = pickle.load(f)
            
                for song in song_cache:
                    if self == song:
                        return
                
                song_cache.append(self)
        
        except:
            song_cache = [self]
        
        # If the songcache is corrupted, it will be overwritten
        with open('song_cache.pickle', 'wb') as f:
            pickle.dump(song_cache, f)