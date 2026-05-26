import streamlit as st
from typing import Any, Dict, List, Optional
from src.database import RepertoireDB
from src.ui import (
    DEFAULT_MAESTRO_LINK,
    DEFAULT_PARTITURAS_LINK,
    SELECT_REPERTOIRE_HELP_MESSAGE,  # Mantida a mensagem que fica após a caixa
    TITLE_PLACEHOLDER,
    build_title_list,
    find_song_by_slug,
    render_admin_panel,
    render_empty_state,
    render_main_header,
    render_next_event_area,
    render_main_subtitle,
    render_main_action_buttons,
    render_next_event_button,
    render_song_details,
    set_page_config_and_styles,
)


def initialize_session_state() -> None:
    if "selected_title" not in st.session_state:
        st.session_state["selected_title"] = TITLE_PLACEHOLDER
    if "show_next_event" not in st.session_state:
        st.session_state["show_next_event"] = False


def parse_query_params() -> Dict[str, Any]:
    return st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()


def parse_single_query_value(query_params: Dict[str, Any], key: str, default: str = "") -> Optional[str]:
    value = query_params.get(key, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value


def is_admin_mode(query_params: Dict[str, Any]) -> bool:
    admin_value = parse_single_query_value(query_params, "admin", "false")
    return str(admin_value).strip().lower() in ("true", "1", "yes", "on")


def get_initial_song_index(song: Optional[Dict[str, Any]], title_list: List[str]) -> int:
    if song and song["title"] in title_list:
        return title_list.index(song["title"])
    return 0


def get_display_link(song: Optional[Dict[str, Any]]) -> str:
    if song and song.get("drive_folder_link"):
        return song["drive_folder_link"]
    return DEFAULT_PARTITURAS_LINK


def get_selected_song(songs: List[Dict[str, Any]], selected_title: str) -> Optional[Dict[str, Any]]:
    if selected_title and selected_title != TITLE_PLACEHOLDER:
        return next((song for song in songs if song["title"] == selected_title), None)
    return None


def render_song_selection(
    songs: List[Dict[str, Any]],
    title_list: List[str],
    initial_index: int,
    next_event_text: str,
    is_admin: bool,
    db: RepertoireDB,
) -> None:
    # 1. O botão que controla a abertura do evento continua aqui
    if render_next_event_button():
        st.session_state["show_next_event"] = not st.session_state["show_next_event"]

    # 2. MUDANÇA CRUCIAL: O acordeon do Próximo evento agora renderiza ANTES do subtítulo
    if st.session_state["show_next_event"]:
        render_next_event_area(next_event_text, is_admin, db)

    # 3. O subtítulo "Preparação para o ensaio" foi movido para baixo do acordeon
    render_main_subtitle()

    # Barra seletora de músicas (Dropdown)
    st.selectbox(
        "",
        options=title_list,
        index=initial_index,
        key="selected_title",
    )

    # Bloco de ajuda posicionado APÓS a barra seletora (mantido ativo)
    selected_song = get_selected_song(songs, st.session_state["selected_title"])
    if not selected_song:
        st.info(SELECT_REPERTOIRE_HELP_MESSAGE)

    partituras_link = get_display_link(selected_song)

    if selected_song:
        render_song_details(selected_song)

    render_main_action_buttons(
        partituras_url=partituras_link,
        maestro_url=DEFAULT_MAESTRO_LINK,
    )


def main() -> None:
    set_page_config_and_styles()
    db = RepertoireDB()
    songs = db.load_songs()
    initialize_session_state()

    query_params = parse_query_params()
    musica_no_link = parse_single_query_value(query_params, "musica", None)
    is_admin = is_admin_mode(query_params)

    render_main_header()

    if is_admin:
        st.success("Modo admin ativo — Cadastro de músicas liberado mais abaixo.")
    elif "admin" in query_params:
        admin_raw = parse_single_query_value(query_params, "admin", "false")
        st.warning(
            f"Parâmetro admin detectado como '{admin_raw}'. Use '?admin=true' para liberar o CRUD."
        )

    song_titles = [song["title"] for song in songs]
    title_list = build_title_list(songs)
    song_inicial = find_song_by_slug(songs, musica_no_link)
    initial_index = get_initial_song_index(song_inicial, title_list)

    if songs:
        next_event_text = db.load_next_event()
        render_song_selection(songs, title_list, initial_index, next_event_text, is_admin, db)
    else:
        render_empty_state(is_admin)

    if is_admin:
        render_admin_panel(db, songs, song_titles)


if __name__ == "__main__":
    main()