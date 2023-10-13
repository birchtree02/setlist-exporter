from nicegui import ui, events
import zipfile

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "song_tools"))

from song_tools.sbp import SBP_backup as SBP
from song_tools import chordpro_parser
import logging


def main(state, next_page):
    def handle_upload(e: events.UploadEventArguments):
        logging.info(f"Got file: {e.name}")
        zip_file = zipfile.ZipFile(e.content)

        for file_name in zip_file.namelist():
            with zip_file.open(file_name) as file:
                # TODO: process the file in sbp.py instead of here
                logging.debug(f"Processing file: {file_name}")
                if file_name == "dataFile.txt":
                    logging.debug("Found dataFile.txt")
                    sbp = SBP(backup_text=file.read().decode("utf-8"), folder=None)
                    song_list, notes = sbp.get_setlist_info(0)

                    song_list = [
                        chordpro_parser.getSongFromFile(
                            sbp.get_song_file_from_id(song[2])
                        )
                        for song in song_list
                    ]

        state.song_list = song_list
        state.sbp_imported = True

        next_page(state)

    with ui.element("div").classes("flex justify-center items-center p-4"):
        ui.markdown("## Upload a .sbp file")
        ui.upload(on_upload=handle_upload, auto_upload=True).classes("object-center")
