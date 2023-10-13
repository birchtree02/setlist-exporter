from nicegui import ui, native_mode
import logging

from gui import openlp, sbp, spotify
from state import ApplicationState

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(filename)s:%(lineno)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


@ui.page("/")
def main():
    app = ApplicationState()

    def open_openlp(state, div):
        with div:
            openlp.main(state, lambda state: open_spotify(state, spotify_div))

    def open_spotify():
        pass

    with ui.element("div").classes("max-w-lg bg-slate-400 w-full"):
        ui.label("Get SBP file")
        sbp.main(app, lambda state: open_openlp(state, openlp_div))

    with ui.element("div").classes("max-w-lg bg-slate-400 w-full") as openlp_div:
        ui.label("Add To OpenLP")

    with ui.element("div").classes("max-w-lg bg-slate-400 w-full") as spotify_div:
        ui.label("Spotify Playlist")


ui.run(
    port=native_mode.find_open_port(),
)
