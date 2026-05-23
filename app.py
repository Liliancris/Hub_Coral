import streamlit as st
from src.database import RepertoireDB
from src.ui import (
    build_title_list,
    find_song_by_slug,
    render_admin_panel,
    render_empty_state,
    render_main_header,
    render_main_document_link,
    render_song_details,
    set_page_config_and_styles,
)

set_page_config_and_styles()

db = RepertoireDB()
songs = db.load_songs()

params_dict = dict(st.query_params)
musica_no_link = params_dict.get("musica", None)
is_admin = params_dict.get("admin", "false").lower() == "true"

render_main_header()
render_main_document_link()

song_titles = [s["title"] for s in songs]
lista_titulos_selectbox = build_title_list(songs)

song_inicial = find_song_by_slug(songs, musica_no_link)

indice_inicial = 0
if song_inicial and song_inicial["title"] in lista_titulos_selectbox:
    indice_inicial = lista_titulos_selectbox.index(song_inicial["title"])

if songs:
    opcao_selecionada = st.selectbox(
        "",
        options=lista_titulos_selectbox,
        index=indice_inicial
    )

    if opcao_selecionada != lista_titulos_selectbox[0]:
        song = next((s for s in songs if s["title"] == opcao_selecionada), songs[0])
        render_song_details(song)
    else:
        st.info("🎵 Aguardando sua seleção! Toque na caixa cinza acima para abrir a lista de músicas do ensaio.")
else:
    render_empty_state(is_admin)

if is_admin:
    render_admin_panel(db, songs, song_titles)

