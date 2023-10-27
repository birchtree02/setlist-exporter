from nicegui import ui, events
import zipfile

import os
import sys


from song_tools.sbp import SBP_backup as SBP
from song_tools import chordpro_parser
import logging


def main(state, next_page, default_set: str=""):
    def get_set_from_dataFile():
        dataFile_path = os.path.join(os.path.expanduser("~"), "Downloads", "dataFile.txt")
        sbp = SBP(dataFile_path)
        update_state(sbp)

    def update_state(sbp):
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
                    update_state(sbp)
                    return

    if default_set:
        ui.button("Click here to start!", on_click=get_set_from_dataFile)
    else:
        with ui.element("div").classes("flex justify-center items-center p-4"):
            ui.markdown("## Upload a .sbp file")
            ui.upload(on_upload=handle_upload, auto_upload=True).classes("object-center")
