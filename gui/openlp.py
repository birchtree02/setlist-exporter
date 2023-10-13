from nicegui import ui
from state import ApplicationState


def main(state: ApplicationState, next_page):
    for song in state.song_list:
        ui.label(song.title)
