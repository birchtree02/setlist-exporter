import os
import sys
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
    default_set_mode = False

    if getattr(sys, "frozen", False):
        # Code is running as a bundled executable (PyInstaller)
        app.dir = sys._MEIPASS
    else:
        # Code is running from the development environment
        app.dir = os.path.dirname(os.path.abspath(__file__))
        default_set_mode = True

    def open_modules(state):
        with openlp_div:
            openlp.main(state)
        with spotify_div:
            spotify.main(state)

    with ui.element("div").classes("max-w-lg bg-slate-400 w-full"):
        ui.label("Get SBP file")
        sbp.main(app, lambda state: open_modules(state), default_set=default_set_mode)

    with ui.element("div").classes("max-w-lg bg-slate-400 w-full") as openlp_div:
        ui.label("Add To OpenLP")

    with ui.element("div").classes("max-w-lg bg-slate-400 w-full") as spotify_div:
        ui.label("Spotify Playlist")



if getattr(sys, "frozen", False):
    ui.run(
        reload=False,
        port=native_mode.find_open_port(),
        native=True,
    )
else:
    ui.run(
        # reload=False,
        port=native_mode.find_open_port(),
        # native=True,
    )
