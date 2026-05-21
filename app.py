import streamlit as st
from src.database import RepertoireDB

# 1. CONFIGURAÇÃO DE JANELA E LAYOUT
st.set_page_config(
    page_title="Coral Ases - Pasta Digital",
    page_icon="🎵",
    layout="centered"
)

# 2. INICIALIZAÇÃO DA INSTÂNCIA DO BANCO
db = RepertoireDB()
songs = db.load_songs()

# 3. TRATAMENTO SEGURO DOS PARÂMETROS DA URL
params_dict = dict(st.query_params)
musica_no_link = params_dict.get("musica", None)
is_admin = params_dict.get("admin", "false").lower() == "true"

# --- LOGOTIPO DO CORAL ASES CONVERTIDO EM VETOR TEXTUAL SEGURO ---
# Esta string reconstrói o passarinho e a marca do Coral Ases diretamente na tela do celular
LOGO_BASE64 = (
    "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 200' width='100%'>"
    "<rect width='320' height='200' rx='15' fill='%23111111'/>"
    "<text x='35' y='80' font-family='Arial, sans-serif' font-weight='900' font-size='22' fill='%23ffffff' letter-spacing='3'>Coral</text>"
    "<text x='25' y='145' font-family='Impact, Arial Black, sans-serif' font-weight='900' font-size='72' fill='%23ffffff' letter-spacing='1'>ases</text>"
    "<text x='37' y='175' font-family='Arial, sans-serif' font-size='13' fill='%23ffffff' letter-spacing='1'>Minas Gerais</text>"
    "<path d='M225,125 C225,100 245,60 260,45 C263,42 268,43 268,47 C264,55 260,70 265,75 C275,65 285,67 282,75 C272,100 245,135 225,125 Z' fill='%23ffffff'/>"
    "<path d='M250,55 C250,55 258,35 272,35 C273,35 274,37 273,38 C267,42 262,52 262,52 Z' fill='%23ffffff'/>"
    "<circle cx='255' cy='62' r='2.5' fill='%23111111'/>"
    "<path d='M225,125 C210,135 200,165 235,160 C255,158 260,135 250,115' stroke='%23fee180' stroke-width='6' fill='none' stroke-linecap='round'/>"
    "<circle cx='208' cy='152' r='14' fill='%23fee180'/>"
    "<path d='M250,115 C240,110 230,130 252,145' stroke='%23fee180' stroke-width='5' fill='none' stroke-linecap='round'/>"
    "<circle cx='244' cy='144' r='11' fill='%23fee180'/>"
    "</svg>"
)

# Renderização do cabeçalho unificado com o Logo reconstruído
st.image(LOGO_BASE64, width=220)
st.markdown("## Pasta Digital")

# 4. PROCESSAMENTO DE SELEÇÃO DE MÚSICA
song_inicial = None
lista_titulos = [s["title"] for s in songs] if songs else []

if musica_no_link and songs:
    busca_slug = musica_no_link.replace("-", " ").lower()
    for s in songs:
        if s["title"].lower() == busca_slug:
            song_inicial = s
            break

indice_inicial = 0
if song_inicial and song_inicial["title"] in lista_titulos:
    indice_inicial = lista_titulos.index(song_inicial["title"])

# 5. RENDERIZAÇÃO DA TELA DO IDOSO (Otimizada para Celular)
if songs:
    st.write("Selecione a música abaixo para acompanhar a letra:")
    
    opcao_selecionada = st.selectbox(
        "👉 TOQUE AQUI PARA MUDAR A MÚSICA:", 
        options=lista_titulos,
        index=indice_inicial
    )
    
    song = next((s for s in songs if s["title"] == opcao_selecionada), songs[0])
    
    st.markdown("---")
    st.header(f"🎤 {song['title']}")
    st.write(f"**Compositor/Arranjo:** {song['composer']} | **Naipe recomendado:** {song['voice_type']}")
    
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
    st.subheader("📝 Letra da Música")
    st.code(song["lyrics"], language="text", wrap_lines=True)

else:
    st.warning("👋 Olá! Nenhuma música foi cadastrada no acervo ainda.")
    if not is_admin:
        st.write("Se você é o regente/administrador, adicione `?admin=true` ao final do link para cadastrar.")

# 6. PAINEL DO ADMINISTRADOR (CRUD Completo)
if is_admin:
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
            musica_para_alterar = st.selectbox("Escolha a música que deseja modificar:", options=lista_titulos, key="sel_alterar")
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
            musica_para_excluir = st.selectbox("Escolha a música que deseja remover:", options=lista_titulos, key="sel_excluir")
            st.warning(f"Atenção: Tem certeza que deseja apagar '{musica_para_excluir}'?")
            if st.button("🔴 CONFIRMAR EXCLUSÃO", use_container_width=True):
                db.delete_song(musica_para_excluir)
                st.success("Removida!")
                st.rerun()