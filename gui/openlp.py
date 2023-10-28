import os
import re

from nicegui import ui
from state import ApplicationState
import song_tools.openlp
from song_tools.song import Song
from song_tools.openlp import service
from song_tools import openlyrics_parser


def main(state: ApplicationState):
    # TODO: move setup stuff to a different function
    def handle_openlp_path(_, path):
        if path.endswith("/") or path.endswith("\\"):
            path = path[:-1]
        if not path.endswith("openlp"):
            ui.notify("Path must end with 'openlp'")
        else:
            # TODO: check this is actually a valid openlp data folder
            openlp_file = os.path.join(state.dir, "openlp.txt")
            with open(openlp_file, "w") as f:
                f.write(path)
            ui.notify("Path saved")
            div.clear()
            main(state)

    def handle_openlp_opened(_):
        if service.available():
            ui.notify("Connected to OpenLP!")
            div.clear()
            main(state)
        else:
            ui.notify("OpenLP not found. Try again!")

    def setup():
        # Get OpenLP data folder from openlp.txt
        # check openlp.txt exists
        openlp_file = os.path.join(state.dir, "openlp.txt")

        if not os.path.exists(openlp_file):
            # If it doesn't exist, ask user for
            ui.label("No data folder found. Enter path below:")
            path_from_user = ui.input("openlp_path").on(
                    "keydown.enter", lambda e: handle_openlp_path(e, path_from_user)
            )
        elif not service.available():
            ui.label("OpenLP doesn't appear to be open. Open it, then click below")
            ui.button("I've opened OpenLP!", on_click= lambda e: handle_openlp_opened(e, service))
        else:
            # If it does exist, read it
            with open(openlp_file, "r") as f:
                openlp_path = f.read()

            # Then, load it
            data_folder = openlp_path+"/data"
            state.openlp_db = song_tools.openlp.load_database(data_folder)

            return True

    def render_song(song: Song):
        # TODO: warn the user if the OpenLP song is probably incorrect (e.g. if over 50% of lines are different)
        # TODO: option to download xml song to be imported to OpenLP
        # TODO: some way of refreshing the OpenLP database
        def show_diff(song, openlp_song):
            with ui.dialog(value=True) as dialog, ui.card():
                # TODO: cange name of first_match and first_match_song
                first_match = (openlp_song[0], openlp_song[6], openlp_song[2], openlp_song[7])
                first_match_song = openlyrics_parser.OpenLyricsParser().parse_open_lyrics(
                    *first_match[:3]
                )

                diff_string1, diff_string2 = song.diff(first_match_song)
                with ui.element("div").classes("grid grid-cols-2"):
                    # TODO: compress this code by having colour_by_start_character take a dictionary of chars and their respective colours
                    with ui.element("div"):
                        ui.markdown("**SBP showing lines not in OpenLP**")
                        if diff_string1:
                            diff_string1 = colours_by_start_characters(
                                    diff_string1,
                                    {"\-":"red",
                                     "\%":"orange",
                                     "\*":"orange"}
                                )
                            ui.markdown(diff_string1.replace("\n", "<br>"))
                        else:
                            ui.markdown("*All lines in SBP are in OpenLP*")
                    with ui.element("div"):
                        ui.markdown("**OpenLP showing lines not in SBP**")
                        if diff_string2:
                            diff_string2 = colours_by_start_characters(
                                    diff_string2,
                                    {"\+":"green",
                                     "\%":"orange",
                                     "\*":"orange"}
                                )
                            ui.markdown(diff_string2.replace("\n", "<br>"))
                        else:
                            ui.markdown("*All lines in OpenLP are in SBP*")

                ui.button(
                    "Add to OpenLP",
                    on_click=lambda: service.add_song_by_id(first_match[3]),
                )




        name, openlp_result = song_tools.openlp.find_song(song, state.openlp_db)
        ui.markdown(f"Matched with __{name.title()}__ in OpenLP.")
        ui.button("View differences", on_click=lambda: show_diff(song, openlp_result))
        ui.button("Add to set", on_click=lambda: service.add_song_by_id(openlp_result[7]))


    with ui.element("div") as div:
        if not setup():
            return

        with ui.stepper().props("vertical").classes("w-full bg-slate-300") as stepper:
            # TODO: Move the stepper into a shared function with spotify/other modules which takes a rendering function as parameter
            for song in state.song_list:
                with ui.step(song.title):
                    render_song(song)
                    with ui.stepper_navigation():
                        ui.button("Next", on_click=stepper.next)
                        ui.button("Back", on_click=stepper.previous).props("flat")

def colours_by_start_characters(diff_string, char_to_colour: dict):
    for (char, colour) in char_to_colour.items():
        diff_string = colour_by_start_character(diff_string, char, colour)

    return diff_string

def colour_by_start_character(diff_string, char, colour):
    return re.sub(
        r"^(" + char + ".*)$",
        rf'<span style="color: {colour};">\1</span>',
        diff_string,
        flags=re.MULTILINE,
    )

