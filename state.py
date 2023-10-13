class ApplicationState:
    def __init__(self):
        self.sbp_imported = False
        self.song_list: List[Song] = None
        self.openlp_db = None
        self.openlp_connected = False
        self.spotify_connected = False
