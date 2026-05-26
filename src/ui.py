import streamlit as st
from typing import Any, Dict, List, Optional
from PIL import Image

TITLE_PLACEHOLDER = "✨ Repertório Atual - Selecione uma música"
BUTTON_LINK_TEMPLATE = "<div style='text-align:center'><a href=\"{url}\" target=\"_blank\" class=\"outline-btn\">{label}</a></div>"

# Aplicado negrito nos termos solicitados usando Markdown (**)
SELECT_SONG_HELP_MESSAGE = (
    "🎵 **Toque na caixa acima** para ver partitura e audio da música selecionada bem como as anotações do Maestro."
    "Ou **Acione os botões abaixo** para acessar o repertório completo."
    
)
SELECT_REPERTOIRE_HELP_MESSAGE = (
     "🎵 **Toque na caixa acima** para ver partitura e audio da música selecionada, bem como as anotações do Maestro."
    " Ou **Acione os botões abaixo** para acessar o repertório completo."
)

VOICE_OPTIONS = ["SATB (Geral)", "Soprano", "Contralto", "Tenor", "Baixo", "Uníssono"]
DEFAULT_PARTITURAS_LINK = "https://drive.google.com/drive/folders/1XZHr5fjzXGacJRyllwe5FypcyKSfj7y7"
DEFAULT_MAESTRO_LINK = "https://drive.google.com/drive/u/1/folders/1RmUwx8afSD3K5egvbnBbpUKSwxKfN6du"

PAGE_CSS = """
    <style>
    /* Configuração global do fundo do app para o tom creme acolhedor */
    .stApp {
        background-color: #FDFBF7 !important;
    }
    
    /* Remove a margem interna superior padrão do container do Streamlit */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
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
    /* Esconde a barra estrutural vazia do topo */
    .stAppHeader {
        display: none !important;
    }
    
    /* Configuração global das fontes de títulos nativos para a cor grafite */
    h1, h2, h3, h4, h5, h6, .stSubheader p {
        color: #2D2D2D !important;
    }
    
    /* Customização dos seletores nativos do Streamlit (Dropdown/Listbox) */
    div[data-baseweb="select"] > div {
        background-color: #F5EBE6 !important;
        border: 1px solid #4A5D4E !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] * {
        color: #2D2D2D !important;
        font-weight: 500 !important;
    }
    
    /* Ajuste fino na margem superior da caixa de seleção */
    div[data-testid="stSelectbox"] {
        margin-top: 0px !important;
        margin-bottom: 0px !important;
    }

    /* EQUALIZAÇÃO DE ESPAÇOS: Controla estritamente as margens dos blocos de texto st.info */
    div[data-testid="stNotification"] {
        margin-top: 12px !important;
        margin-bottom: 12px !important;
    }

    /* Botões de ação principais em blocos preenchidos */
    .action-buttons { display:flex; gap:12px; justify-content:center; margin-bottom:12px; flex-wrap:wrap; }
    .outline-btn {
        border: none !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
        text-decoration: none !important;
        color: #FFFFFF !important;
        background-color: #4A5D4E !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 600 !important;
        box-sizing: border-box !important;
        width: 100% !important;
        height: 55px !important;
        font-size: 16px !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05) !important;
        
        /* GARANTE RESPIRO NO TELEMÓVEL: Espaço mínimo vertical ao empilhar */
        margin-bottom: 12px !important; 
    }
    .outline-btn:hover { 
        background-color: #3D4A3E !important;
        color: #FFFFFF !important; 
        text-decoration: none !important; 
    }
    
    /* Estilo padrão para botões desabilitados do Streamlit */
    .stButton>button:disabled, .stButton>div>button:disabled {
        border-radius: 12px !important;
        height: 55px !important;
        font-size: 16px !important;
        margin-bottom: 12px !important;
        background-color: #E0E0E0 !important;
        color: #A0A0A0 !important;
    }
    
    /* Customização dos blocos de Código/Texto (Anotações do Maestro) para Card Pêssego */
    div[data-testid="stCodeBlock"] {
        background-color: #F7ECE1 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(163, 112, 76, 0.2) !important;
        padding: 14px !important;
        margin-bottom: 15px !important;
    }
    /* Força o texto interno das anotações e tokens de texto a ficarem em cinza-grafite */
    div[data-testid="stCodeBlock"] code, 
    div[data-testid="stCodeBlock"] span {
        color: #2D2D2D !important;
        font-family: inherit !important;
        font-size: 17px !important;
        font-weight: 500 !important;
    }
    
    /* Estilização aplicada também aos botões nativos padrão do Streamlit (Ex: "Próximo evento") */
    .stButton>button,
    .stButton>div>button {
        border-radius: 12px !important;
        height: 55px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        background-color: #4A5D4E !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 8px 12px !important;
        margin-bottom: 12px !important;
    }
    .stButton>button:hover,
    .stButton>div>button:hover {
        background-color: #3D4A3E !important;
    }
    </style>
"""

def set_page_config_and_styles() -> None:
    st.set_page_config(
        page_title="Coral Ases",
        page_icon="🎵",
        layout="centered"
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)


def build_title_list(songs: List[Dict[str, Any]]) -> List[str]:
    titles = [TITLE_PLACEHOLDER]
    titles.extend(s["title"] for s in songs)
    return titles


def find_song_by_slug(songs: List[Dict[str, Any]], musica_no_link: Optional[str]) -> Optional[Dict[str, Any]]:
    if not musica_no_link:
        return None

    busca_slug = musica_no_link.replace("-", " ").lower()
    return next((s for s in songs if s["title"].lower() == busca_slug), None)


def render_main_header() -> None:
    """Carrega o logotipo da medalha e exibe o cabeçalho centralizado."""
    try:
        image = Image.open("data/logo_coral.png")
        col_left, col_logo, col_right = st.columns([1, 2, 1])
        with col_logo:
            st.image(image, use_container_width=True)
            
    except FileNotFoundError:
        pass

    # Aplicado margem negativa de -35px para aproximar o título do topo o máximo possível
    st.markdown(
        """
        <div style="text-align: center; margin-top: -35px; margin-bottom: 20px;">
            <h1 style="margin: 0px; font-weight: 700; color: #2D2D2D; font-family: 'Playfair Display', Georgia, serif;">Coral Ases</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_main_subtitle() -> None:
    st.markdown(
        """
        <div style="display: flex; align-items: center; text-align: center; margin-bottom: 25px;">
            <div style="flex: 1; border-bottom: 1px solid #4A5D4E; opacity: 0.3; margin-right: 15px;"></div>
            <p style="margin: 0px; font-size: 20px; color: #2D2D2D; opacity: 0.8; white-space: nowrap;">Preparação para o ensaio</p>
            <div style="flex: 1; border-bottom: 1px solid #4A5D4E; opacity: 0.3; margin-left: 15px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_link_button(url: str, label: str) -> None:
    st.markdown(BUTTON_LINK_TEMPLATE.format(url=url, label=label), unsafe_allow_html=True)


def render_next_event_button() -> bool:
    """Renderiza o botão do próximo evento logo após o cabeçalho."""
    return st.button("Próximo evento", use_container_width=True, key="btn_next_event")


def render_main_action_buttons(
    lyrics_url: str = "https://docs.google.com/document/d/1zBgtUXYp7m-QBz2EejqSb7hvqUB6DmVrCJn2iIFsEqE/edit?usp=sharing",
    partituras_url: str = DEFAULT_PARTITURAS_LINK,
    maestro_url: str = DEFAULT_MAESTRO_LINK,
) -> None:
    """Renderiza os três botões principais após a seleção de música."""
    cols = st.columns([1, 1, 1])
    with cols[0]:
        render_link_button(lyrics_url, "Letras")
    with cols[1]:
        render_link_button(partituras_url, "Partituras")
    with cols[2]:
        render_link_button(maestro_url, "Fala Maestro")


def render_song_details(song: Dict[str, Any]) -> None:
    st.subheader(f"{song['title']}")

    if song.get("document_link"):
        st.markdown(
            f'<a href="{song["document_link"]}" target="_blank" class="outline-btn">📄 ACESSAR DOCUMENTO</a>',
            unsafe_allow_html=True
        )

    st.markdown("#### 🎶 Anotações do maestro")
    
    st.code(song["lyrics"], language="text", wrap_lines=True)

    if song.get("drive_folder_link"):
        st.markdown(
            f'<a href="{song["drive_folder_link"]}" target="_blank" class="outline-btn">📂 Mostrar partituras e áudio da música</a>',
            unsafe_allow_html=True
        )
    else:
        st.button("❌ Arquivos não vinculados no Drive", disabled=True, use_container_width=True)


def render_empty_state(is_admin: bool) -> None:
    st.markdown(
        """
        <div style="background-color: #F7ECE1; padding: 20px; border-radius: 12px; border: 1px solid rgba(163, 112, 76, 0.2); color: #2D2D2D; margin-bottom: 15px;">
            <span style="font-size: 20px;">🎵</span> <br>
            {message}
        </div>
        """.format(message=SELECT_SONG_HELP_MESSAGE), 
        unsafe_allow_html=True
    )
    if is_admin:
        st.write("Se você é o regente/administrador, adicione `?admin=true` ao final do link para cadastrar.")


def render_editor_next_event(next_event_text: str, db: Any) -> None:
    with st.form("form_next_event", clear_on_submit=False):
        edited_text = st.text_area("Texto do próximo evento", value=next_event_text, height=200)
        if st.form_submit_button("Gravar próximo evento"):
            db.save_next_event(edited_text or "")
            st.success("Texto do próximo evento gravado com sucesso.")
            st.rerun()


def render_viewer_next_event(next_event_text: str) -> None:
    if next_event_text:
        st.markdown(next_event_text)
    else:
        st.info("Nenhum texto cadastrado para o próximo evento. Peça ao administrador para gravar o texto.")


def render_next_event_area(next_event_text: str, is_admin: bool, db: Any) -> None:
    with st.expander("📌 Próximo evento", expanded=True):
        if is_admin:
            render_editor_next_event(next_event_text, db)
        else:
            render_viewer_next_event(next_event_text)


def render_admin_tab_add(db: Any) -> None:
    with st.form("form_cadastro", clear_on_submit=True):
        new_title = st.text_input("Título da Música *")
        new_composer = st.text_input("Compositor *")
        new_voice = st.selectbox("Voz", VOICE_OPTIONS, key="cad_voice")
        new_folder = st.text_input("Link da Pasta no Google Drive")
        new_lyrics = st.text_area("🎶 Anotações do maestro", key="cad_lyrics")

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


def render_admin_tab_edit(db: Any, songs: List[Dict[str, Any]], title_options: List[str]) -> None:
    if not songs:
        st.caption("Nenhuma música para alterar.")
        return

    musica_para_alterar = st.selectbox("Escolha a música que deseja modificar:", options=title_options, key="sel_alterar")
    song_edit = next(s for s in songs if s["title"] == musica_para_alterar)

    with st.form("form_alterar"):
        edit_title = st.text_input("Título da Música *", value=song_edit["title"])
        edit_composer = st.text_input("Compositor *", value=song_edit["composer"])
        idx_voice = VOICE_OPTIONS.index(song_edit["voice_type"]) if song_edit["voice_type"] in VOICE_OPTIONS else 0
        edit_voice = st.selectbox("Voz", VOICE_OPTIONS, index=idx_voice, key="edit_voice")
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
                st.success("Música updated com sucesso!")
                st.rerun()
            else:
                st.error("Título e Compositor não podem ficar vazios.")


def render_admin_tab_delete(db: Any, songs: List[Dict[str, Any]], title_options: List[str]) -> None:
    if not songs:
        st.caption("Nenhuma música para excluir.")
        return

    musica_para_excluir = st.selectbox("Escolha a música que deseja remover:", options=title_options, key="sel_excluir")
    st.warning(f"Atenção: Tem certeza que deseja apagar '{musica_para_excluir}'?")
    if st.button("🔴 CONFIRMAR EXCLUSÃO", use_container_width=True):
        db.delete_song(musica_para_excluir)
        st.success("Removida!")
        st.rerun()


def render_admin_tab_next_events(db: Any) -> None:
    current_next_event = db.load_next_event()
    with st.form("form_proximos_eventos", clear_on_submit=False):
        prox_text = st.text_area("Quadro de próximos eventos", value=current_next_event, height=200)
        if st.form_submit_button("Atualizar quadro de próximos eventos"):
            db.save_next_event(prox_text or "")
            st.success("Quadro de próximos eventos atualizado com sucesso.")
            st.rerun()


def render_admin_panel(db: Any, songs: List[Dict[str, Any]], title_options: List[str]) -> None:
    st.markdown("---")
    st.subheader("🛠️ Painel do Regente / Administrador")

    tab_cadastrar, tab_alterar, tab_excluir, tab_proximos = st.tabs(["➕ Cadastrar", "📝 Alterar", "❌ Excluir", "📌 Próximos eventos"])

    with tab_cadastrar:
        render_admin_tab_add(db)

    with tab_alterar:
        render_admin_tab_edit(db, songs, title_options)

    with tab_excluir:
        render_admin_tab_delete(db, songs, title_options)

    with tab_proximos:
        render_admin_tab_next_events(db)