import os

from nicegui import ui
from state import ApplicationState


def main(state: ApplicationState):
    def handle_openlp_path(e):
        path = path_from_user.value
        if path.endswith("/") or path.endswith("\\"):
            path = path[:-1]
        if not path.endswith("openlp"):
            ui.notify("Path must end with 'openlp'")
        else:
            # TODO: check this is actually a valid openlp data folder
            with open(openlp_file, "w") as f:
                f.write(path)
            ui.notify("Path saved")
            div.clear()
            main(state)

    with ui.element("div") as div:
        # Get OpenLP data folder from openlp.txt
        # check openlp.txt exists
        openlp_file = os.path.join(state.dir, "openlp.txt")

        if not os.path.exists(openlp_file):
            # If it doesn't exist, ask user for
            ui.label("No data folder found. Enter path below:")
            path_from_user = ui.input("openlp_path").on(
                "keydown.enter", handle_openlp_path
            )
        else:
            # If it does exist, read it
            with open(openlp_file, "r") as f:
                openlp_path = f.read()

            # Then, load it

            # Then, show the list of songs
            for song in state.song_list:
                ui.label(song.title)
