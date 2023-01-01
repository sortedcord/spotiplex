from deezer_python.client import Client
from deezer_python.pagination import PaginatedList
from deezer_python.resources import (
    Album,
    Artist,
    Chart,
    Editorial,
    Episode,
    Genre,
    Playlist,
    Podcast,
    Radio,
    Resource,
    Track,
    User,
)

__version__ = "5.8.1"
__all__ = [
    "Album",
    "Artist",
    "Chart",
    "Client",
    "Editorial",
    "Episode",
    "Genre",
    "PaginatedList",
    "Playlist",
    "Podcast",
    "Radio",
    "Resource",
    "Track",
    "User",
]

USER_AGENT = f"Deezer Python API Wrapper v{__version__}"
