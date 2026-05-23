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
    /* Botões de ação arredondados (outline, sem preenchimento) */
    .action-buttons { display:flex; gap:12px; justify-content:center; margin-bottom:12px; flex-wrap:wrap; }
    .outline-btn {
        border: 1px solid rgba(0,0,0,0.6);
        border-radius: 999px;
        padding: 8px 12px;
        text-decoration: none;
        color: inherit;
        background: transparent;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        box-sizing: border-box;
        width: 100%; /* occupy entire column width */
        height: 40px; /* consistent height */
        font-size: 14px;
    }
    .outline-btn:hover { background: rgba(0,0,0,0.03); }
    /* Estilo para botões nativos do Streamlit (mantém aparência consistente) */
    .stButton>button, .stButton>div>button {
        border: 1px solid rgba(0,0,0,0.6) !important;
        border-radius: 999px !important;
        padding: 8px 12px !important;
        background: transparent !important;
        width: 100% !important; /* fill column */
        height: 40px !important;
        font-weight: 600 !important;
        box-sizing: border-box !important;
    }
    </style>
"""


def set_page_config_and_styles() -> None:
    st.set_page_config(
        page_title="Coral Ases - Preparação para o Ensaio",
        page_icon="🎵",
        layout="centered"
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)


def build_title_list(songs: List[Dict[str, Any]]) -> List[str]:
    titles = ["✨ Clique para estudar as músicas do próximo ensaio"]
    titles.extend(s["title"] for s in songs)
    return titles




def find_song_by_slug(songs: List[Dict[str, Any]], musica_no_link: Optional[str]) -> Optional[Dict[str, Any]]:
    if not musica_no_link:
        return None

    busca_slug = musica_no_link.replace("-", " ").lower()
    return next((s for s in songs if s["title"].lower() == busca_slug), None)


import streamlit as st
from typing import Any, Dict, List, Optional
from PIL import Image  # <-- Adicione esta importação no topo do arquivo ui.py

# ... (Mantenha o PAGE_CSS e as outras funções acima) ...

def render_main_header() -> None:
    """Carrega o logotipo da medalha e exibe o cabeçalho centralizado."""
    try:
        # Tenta carregar a imagem da pasta assets/
        # Certifique-se de que o caminho 'assets/logo_coral.png' está correto
        image = Image.open("data/logo_coral.png")
        
        # Centraliza a imagem no topo
        # columns([1,2,1]) cria três colunas, a do meio é o dobro do tamanho das laterais
        col_left, col_logo, col_right = st.columns([1, 2, 1])
        
        with col_logo:
            # Mostra a imagem com a largura máxima da coluna (use_container_width=True)
            st.image(image, use_container_width=True)
            
    except FileNotFoundError:
        # Se a imagem não for encontrada, mostra apenas o texto (para não travar o app)
        pass

    # Exibe o título e o subtítulo centralizados logo abaixo do logo
    st.markdown(
        """
        <div style="text-align: center; margin-top: 10px; margin-bottom: 20px;">
            <h2 style="margin: 0px; font-weight: 700; color: var(--text-color);">
                Coral Ases
            </h2>
            <p style="margin: 0px; font-size: 15px; color: var(--secondary-text-color); font-style: italic;">Preparação para o ensaio</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_main_document_link() -> None:
    st.markdown(
        "[📄 Letras do repertório](https://docs.google.com/document/d/1zBgtUXYp7m-QBz2EejqSb7hvqUB6DmVrCJn2iIFsEqE/edit?usp=sharing)",
        unsafe_allow_html=True
    )


def render_top_action_buttons(
    lyrics_url: str = "https://docs.google.com/document/d/1zBgtUXYp7m-QBz2EejqSb7hvqUB6DmVrCJn2iIFsEqE/edit?usp=sharing",
    partituras_url: str = "https://drive.google.com/drive/folders/1XZHr5fjzXGacJRyllwe5FypcyKSfj7y7",
    maestro_url: str = "https://drive.google.com/drive/u/1/folders/1RmUwx8afSD3K5egvbnBbpUKSwxKfN6du",
) -> None:
    """Renderiza três botões arredondados (outline): Letras, Partituras e Anotações do maestro."""
    cols = st.columns([1,1,1])
    with cols[0]:
        st.markdown(f"<div style='text-align:center'><a href=\"{lyrics_url}\" target=\"_blank\" class=\"outline-btn\">Letras</a></div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"<div style='text-align:center'><a href=\"{partituras_url}\" target=\"_blank\" class=\"outline-btn\">Partituras</a></div>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"<div style='text-align:center'><a href=\"{maestro_url}\" target=\"_blank\" class=\"outline-btn\">Fala Maestro</a></div>", unsafe_allow_html=True)


def render_maestro_notes_modal(songs: List[Dict[str, Any]]) -> None:
    with st.expander("📝 Anotações do maestro", expanded=True):
        st.write("Anotações do maestro de todo o repertório do ensaio.")
        if not songs:
            st.info("Nenhuma música cadastrada ainda.")
            return

        for song in songs:
            st.markdown(f"### {song['title']}")
            if song.get("composer"):
                st.markdown(f"**Compositor:** {song['composer']}")
            if song.get("voice_type"):
                st.markdown(f"**Voz:** {song['voice_type']}")
            st.code(song.get("lyrics", "(Sem anotações)"), language="text", wrap_lines=True)
            st.markdown("---")


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
            "📂 Mostrar partituras e áudio da música",
            song["drive_folder_link"],
            use_container_width=True,
            type="primary"
        )
    else:
        st.button("❌ Arquivos não vinculados no Drive", disabled=True, use_container_width=True)

    st.markdown("---")
    st.subheader(" Anotações do maestro")
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
            new_lyrics = st.text_area("Anotações do maestro", key="cad_lyrics")

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
                edit_lyrics = st.text_area("Anotações do maestro", value=song_edit["lyrics"], key="edit_lyrics")

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
