import streamlit as st
from typing import Any, Dict, List, Optional

PAGE_CSS = """
    <style>
    /* Esconde o botão de Deploy e o menu do GitHub no topo direito */
    .stAppDeployButton {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden !important;
    }
    /* Esconde o menu de opções padrão do Streamlit */
    header {
        visibility: hidden !important;
    }
    /* Esconde o rodapé 'Made with Streamlit' */
    footer {
        visibility: hidden !important;
    }
    /* Ajusta o espaçamento do topo que ficou vazio */
    .stAppHeader {
        display: none !important;
    }
    </style>
"""


def set_page_config_and_styles() -> None:
    st.set_page_config(
        page_title="Coral Ases - Pasta Digital",
        page_icon="🎵",
        layout="centered"
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)


def build_title_list(songs: List[Dict[str, Any]]) -> List[str]:
    titles = ["✨ Escolha a música..."]
    titles.extend(s["title"] for s in songs)
    return titles


def find_song_by_slug(songs: List[Dict[str, Any]], musica_no_link: Optional[str]) -> Optional[Dict[str, Any]]:
    if not musica_no_link:
        return None

    busca_slug = musica_no_link.replace("-", " ").lower()
    return next((s for s in songs if s["title"].lower() == busca_slug), None)


def render_main_header() -> None:
    st.markdown(
        "<h3 style='text-align: center; margin-top: 0px; margin-bottom: 10px;'>Pasta Digital - Coral Ases</h3>",
        unsafe_allow_html=True
    )


def render_main_document_link() -> None:
    st.link_button(
        "📄 ACESSAR LETRAS DE TODO O REPERTÓRIO",
        "https://docs.google.com/document/d/1zBgtUXYp7m-QBz2EejqSb7hvqUB6DmVrCJn2iIFsEqE/edit?usp=sharing",
        use_container_width=True
    )


def render_song_details(song: Dict[str, Any]) -> None:
    st.markdown("---")
    st.subheader(f" {song['title']}")
    # st.write(f"**Compositor/Arranjo:** {song['composer']} | **Partituras em revisão**")

    if song.get("document_link"):
        st.link_button(
            "📄 ACESSAR DOCUMENTO",
            song["document_link"],
            use_container_width=True
        )

    if song.get("drive_folder_link"):
        st.link_button(
            "📂 ABRIR PARTITURA OU OUVIR ÁUDIO",
            song["drive_folder_link"],
            use_container_width=True,
            type="primary"
        )
    else:
        st.button("❌ Arquivos não vinculados no Drive", disabled=True, use_container_width=True)

    st.markdown("---")
    st.subheader("🐦‍🎵 Letra da Música")
    st.code(song["lyrics"], language="text", wrap_lines=True)


def render_empty_state(is_admin: bool) -> None:
    st.warning("👋 Olá! Nenhuma música foi cadastrada no acervo ainda.")
    if not is_admin:
        st.write("Se você é o regente/administrador, adicione `?admin=true` ao final do link para cadastrar.")


def render_admin_panel(db: Any, songs: List[Dict[str, Any]], title_options: List[str]) -> None:
    st.markdown("---")
    st.subheader("🛠️ Painel do Regente / Administrador")

    tab_cadastrar, tab_alterar, tab_excluir = st.tabs(["➕ Cadastrar", "📝 Alterar", "❌ Excluir"])

    with tab_cadastrar:
        with st.form("form_cadastro", clear_on_submit=True):
            new_title = st.text_input("Título da Música *")
            new_composer = st.text_input("Compositor *")
            new_voice = st.selectbox("Voz", ["SATB (Geral)", "Soprano", "Contralto", "Tenor", "Baixo", "Uníssono"], key="cad_voice")
            new_folder = st.text_input("Link da Pasta no Google Drive")
            new_lyrics = st.text_area("Letra da Música", key="cad_lyrics")

            if st.form_submit_button("Salvar Nova Música"):
                if new_title and new_composer:
                    payload = {
                        "title": new_title.strip(),
                        "composer": new_composer.strip(),
                        "voice_type": new_voice,
                        "lyrics": new_lyrics,
                        "drive_folder_link": new_folder.strip()
                    }
                    db.save_song(payload)
                    st.success("Música cadastrada!")
                    st.rerun()
                else:
                    st.error("Preencha os campos obrigatórios.")

    with tab_alterar:
        if not songs:
            st.caption("Nenhuma música para alterar.")
        else:
            musica_para_alterar = st.selectbox("Escolha a música que deseja modificar:", options=title_options, key="sel_alterar")
            song_edit = next(s for s in songs if s["title"] == musica_para_alterar)

            with st.form("form_alterar"):
                edit_title = st.text_input("Título da Música *", value=song_edit["title"])
                edit_composer = st.text_input("Compositor *", value=song_edit["composer"])
                vozes = ["SATB (Geral)", "Soprano", "Contralto", "Tenor", "Baixo", "Uníssono"]
                idx_voice = vozes.index(song_edit["voice_type"]) if song_edit["voice_type"] in vozes else 0
                edit_voice = st.selectbox("Voz", vozes, index=idx_voice, key="edit_voice")
                edit_folder = st.text_input("Link da Pasta no Google Drive", value=song_edit.get("drive_folder_link", ""))
                edit_lyrics = st.text_area("Letra da Música", value=song_edit["lyrics"], key="edit_lyrics")

                if st.form_submit_button("Atualizar Dados"):
                    if edit_title and edit_composer:
                        updated_payload = {
                            "title": edit_title.strip(),
                            "composer": edit_composer.strip(),
                            "voice_type": edit_voice,
                            "lyrics": edit_lyrics,
                            "drive_folder_link": edit_folder.strip()
                        }
                        db.update_song(song_edit["title"], updated_payload)
                        st.success("Música atualizada com sucesso!")
                        st.rerun()
                    else:
                        st.error("Título e Compositor não podem ficar vazios.")

    with tab_excluir:
        if not songs:
            st.caption("Nenhuma música para excluir.")
        else:
            musica_para_excluir = st.selectbox("Escolha a música que deseja remover:", options=title_options, key="sel_excluir")
            st.warning(f"Atenção: Tem certeza que deseja apagar '{musica_para_excluir}'?")
            if st.button("🔴 CONFIRMAR EXCLUSÃO", use_container_width=True):
                db.delete_song(musica_para_excluir)
                st.success("Removida!")
                st.rerun()
