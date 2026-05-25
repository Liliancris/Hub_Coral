import streamlit as st
from src.database import RepertoireDB
from src.ui import (
    build_title_list,
    find_song_by_slug,
    render_admin_panel,
    render_empty_state,
    render_main_header,
    render_main_subtitle,
    render_maestro_notes_modal,
    render_next_event_area,
    render_main_action_buttons,
    render_next_event_button,
    render_song_details,
    set_page_config_and_styles,
)

set_page_config_and_styles()

db = RepertoireDB()
songs = db.load_songs()

# session state for selected title so we can render buttons before the selectbox
if "selected_title" not in st.session_state:
    # default to the placeholder used in build_title_list
    st.session_state["selected_title"] = "✨ Ou veja o repertório do ensaio"
if "show_next_event" not in st.session_state:
    st.session_state["show_next_event"] = False

query_params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
musica_no_link = query_params.get("musica", None)
if isinstance(musica_no_link, list):
    musica_no_link = musica_no_link[0] if musica_no_link else None

admin_raw = query_params.get("admin", "false")
if isinstance(admin_raw, list):
    admin_raw = admin_raw[0] if admin_raw else "false"
query_is_admin = str(admin_raw).strip().lower() in ("true", "1", "yes", "on")

# Admin mode is enabled only via URL query string
is_admin = query_is_admin

render_main_header()

if is_admin:
    st.success("Modo admin ativo — Cadastro de músicas liberado mais abaixo.")
elif "admin" in query_params:
    st.warning(f"Parâmetro admin detectado como '{admin_raw}'. Use '?admin=true' para liberar o CRUD.")

song_titles = [s["title"] for s in songs]
lista_titulos_selectbox = build_title_list(songs)

song_inicial = find_song_by_slug(songs, musica_no_link)

indice_inicial = 0
if song_inicial and song_inicial["title"] in lista_titulos_selectbox:
    indice_inicial = lista_titulos_selectbox.index(song_inicial["title"])

if songs:
    opcao_selecionada = st.session_state.get("selected_title")
    if opcao_selecionada and opcao_selecionada != lista_titulos_selectbox[0]:
        sel_song = next((s for s in songs if s["title"] == opcao_selecionada), None)
        partituras_link = sel_song.get("drive_folder_link", "https://drive.google.com/drive/folders/1XZHr5fjzXGacJRyllwe5FypcyKSfj7y7") if sel_song else "https://drive.google.com/drive/folders/1XZHr5fjzXGacJRyllwe5FypcyKSfj7y7"
    else:
        partituras_link = "https://drive.google.com/drive/folders/1XZHr5fjzXGacJRyllwe5FypcyKSfj7y7"

    next_event_text = db.load_next_event()
    show_next_event = render_next_event_button()
    if show_next_event:
        st.session_state["show_next_event"] = not st.session_state["show_next_event"]

    render_main_subtitle()

    if st.session_state["show_next_event"]:
        render_next_event_area(next_event_text, is_admin, db)

    st.selectbox(
        "",
        options=lista_titulos_selectbox,
        index=indice_inicial,
        key="selected_title"
    )

    opcao_selecionada = st.session_state.get("selected_title")
    if opcao_selecionada and opcao_selecionada != lista_titulos_selectbox[0]:
        song = next((s for s in songs if s["title"] == opcao_selecionada), songs[0])
        render_song_details(song)
    else:
        song = None
        st.info("🎵 Toque na caixa acima para ver partitura e audios da música selecionada. Ou acione os botões abaixo para acessar o repertório completo bem como as orientações do maestro. ")

    render_main_action_buttons(
        partituras_url=partituras_link,
        maestro_url="https://drive.google.com/drive/u/1/folders/1RmUwx8afSD3K5egvbnBbpUKSwxKfN6du"
    )
else:
    render_empty_state(is_admin)

if is_admin:
    render_admin_panel(db, songs, song_titles)

