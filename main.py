from nicegui import ui

from gui import openlp, sbp, spotify


with ui.element("div").classes("max-w-lg bg-slate-400 w-full"):
    ui.label("Get SBP file")
    sbp.main()

with ui.element("div").classes("max-w-lg bg-slate-400 w-full"):
    ui.label("Add To OpenLP")

with ui.element("div").classes("max-w-lg bg-slate-400 w-full"):
    ui.label("Spotify Playlist")

ui.run()
