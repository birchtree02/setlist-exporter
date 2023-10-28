from datetime import datetime, timedelta
import requests

from nicegui import ui

from song_tools.spotify_tools import SpotifyTools as Spotify

from song_tools.song import Song
from state import ApplicationState


def main(state: ApplicationState):
    def retry():
        ui.notify("Trying to connect...")
        status_div.clear()
        main(state)

    with ui.element("div") as status_div:
        try:
            spotify = Spotify("ed.jd.birchall")
            state.spotify_connected = True
        except requests.exceptions.ConnectionError:
            # TODO: get this to work properly
            # TODO: handle getting spotify cred
            ui.notify("Couldn't connect to Spotify")
            ui.label("Couldn't connect to Spotify")
            ui.button("Try Again", on_click=lambda: retry)

    if not state.spotify_connected:
        return

    playlist_tracks = []

    def render_song(song: Song):
        tracks = spotify.get_song_details(song.title, song.author, limit=5)
        for track in tracks:
            with render_track(track):
                with ui.element("div").classes("1/5"):
                    # use a closure to capture the current value of the 'song' variable
                    def add_to_playlist_closure(track=track):
                        # TODO: add in correct position
                        playlist_tracks.append(track)
                        render_playlist()
                        stepper.next()

                    ui.button(
                        "+",
                        on_click=add_to_playlist_closure,
                    ).classes("bg-white text-black w-full rounded-lg mb-2")

    def render_playlist():
        playlist_div.clear()
        with playlist_div:
            for track in playlist_tracks:
                with render_track(track):
                    with ui.element("div").classes("1/5"):
                        def remove_from_playlist_closure(track=track):
                            playlist_tracks.remove(track)
                            render_playlist()

                        ui.button(
                            "-",
                            on_click=remove_from_playlist_closure
                        ).classes("bg-white text-black w-full rounded-lg mb-2")

    def export_playlist(title=default_playlist_title()):
        uris = [track["uri"] for track in playlist_tracks]
        spotify.create_playlist(title, uris)
        ui.notify("Playlist sent to Spotify!")

    with ui.stepper().props("vertical").classes("w-full bg-slate-300") as stepper:
        for song in state.song_list:
            with ui.step(song.title):
                render_song(song)
                with ui.stepper_navigation():
                    ui.button("Next", on_click=stepper.next)
                    ui.button("Back", on_click=stepper.previous).props("flat")

    with ui.element("div") as playlist_div:
        pass
    render_playlist()
    ui.button("Send to spotify", on_click=export_playlist)


def render_track(track):
    # 'album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit',
    # 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity',
    # 'preview_url', 'track_number', 'type', 'uri'
    name = track["name"]
    artists = ", ".join([artist["name"] for artist in track["artists"]])
    album = track["album"]["name"]
    duration = track["duration_ms"]
    album_artwork = track["album"]["images"][0]["url"]
    preview_url = track["preview_url"]

    with ui.element("div").classes(
        "bg-slate-100 dark:bg-slate-600 dark:text-white rounded-lg w-full flex h-12 m-1"
    ) as track_div:
        with ui.element("div").classes("w-1/5"):
            # TODO: add audio preview
            ui.image(source=album_artwork).classes(
                "rounded-sm display-block h-10 w-10 m-1"
            )

        with ui.element("div").classes("w-3/5"):
            ui.label(name).classes("font-bold truncate")
            ui.label(artists).classes("text-gray-600 dark:text-gray-100 truncate")

    return track_div

def default_playlist_title():
    today = datetime.now()
    days_until_sunday = (6 - today.weekday()) % 7
    next_sunday = today + timedelta(days=days_until_sunday)
    formatted_date = next_sunday.strftime("%d/%m/%y")
    title = "Sunday Setlist"
    title += " " + formatted_date

    return title
