from typing import List

from song_tools.song import Song

class ApplicationState:
    def __init__(self):
        self.sbp_imported: bool = False
        self.song_list: List[Song] = []
        self.openlp_db: List[tuple] = []
        self.openlp_connected: bool = False
        self.spotify_connected: bool = False
        self.dir: str = ""
