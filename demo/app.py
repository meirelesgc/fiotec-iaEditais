import streamlit as st
from streamlit_pdf_viewer import pdf_viewer


from hooks import source, taxonomy
from datetime import datetime

st.set_page_config(
    page_title='Demonstração da API',
    layout='wide',
    initial_sidebar_state='expanded',
    page_icon='📄',
)


POST_SOURCE = DELETE_SOURCE = False
CREATE_TAXONOMY = POST_TAXONOMY = DELETE_TAXONOMY = PUT_TAXONOMY = False

tab1, tab2, tab3 = st.tabs(['Fontes', 'Taxonomia', 'Analise'])


def format_date(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
    return dt.strftime('%d/%m/%Y %H:%M:%S')


sources = source.get_source()


@st.dialog('Adicionar Fonte')
def create_source():
    POST_SOURCE = False
    uploaded_file = st.file_uploader('Escolha um arquivo PDF', type='pdf')
    POST_SOURCE = st.button('Enviar arquivo')
    if POST_SOURCE and uploaded_file:
        source.post_source(uploaded_file)
        POST_SOURCE = False


with tab1:
    container = st.container()
    a, b = container.columns([3, 1])

    a.button('Fontes', use_container_width=True)

    POST_SOURCE = b.button('➕ Adicionar Fonte', use_container_width=True)
    if POST_SOURCE:
        create_source()

    st.subheader('Lista de Fontes')
    if not sources:
        st.error('No sources found.')

    for _ in sources:
        st.write(f'{_["name"][:-4]}')
        with st.expander(f'ID: __{_["id"]}__'):
            st.write(f'**Criado em:** {format_date(_["created_at"])}')
            update_at = (
                format_date(_['updated_at']) if _['updated_at'] else 'N/A'
            )
            st.write(f'**Atualizado em:** {update_at}')
            DELETE_SOURCE = st.button('Excluir', key=f'exclude_{_["id"]}')
            st.divider()
            pdf_viewer(
                input=source.get_source_file(_['id']),
                key=f'pdf_viewer_{_["id"]}',
                width='100%',
            )
            if DELETE_SOURCE:
                source.delete_source(_['id'])
                DELETE_SOURCE = False

with tab2:

    @st.dialog('Criar Taxonomia')
    def create_taxonomy(_):
        def xpto(x):
            return x['name'][:-4]

        with st.form(key='create_taxonomy_form'):
            title = st.text_input('Título da Taxonomia')
            description = st.text_area('Descrição da Taxonomia')
            selected_sources = st.multiselect(
                'Fontes', sources, format_func=xpto
            )
            POST_TAXONOMY = st.form_submit_button('Criar Taxonomia')

        if POST_TAXONOMY:
            taxonomy.post_taxonomy(title, description, selected_sources)
            st.success('Taxonomia criada com sucesso!')
            POST_TAXONOMY = False

    container = st.container()
    a, b = container.columns([3, 1])

    a.button('Taxonomias', use_container_width=True)
    CREATE_TAXONOMY = b.button('➕ Criar Taxonomia', use_container_width=True)
    if CREATE_TAXONOMY:
        create_taxonomy()
        CREATE_TAXONOMY = False

    taxonomies = taxonomy.get_taxonomy()

    def show_taxonomies(_):
        st.write(f'**ID:** {_["id"]}')
        st.write(f'**Fontes** {_["source"]}')
        st.write(f'**Criado em:** {format_date(_["created_at"])}')
        update_at = format_date(_['updated_at']) if _['updated_at'] else 'N/A'
        st.write(f'**Atualizado em:** {update_at}')
        st.divider()

    def show_branches(_):
        data = taxonomy.get_branches_by_taxonomy_id(_['id'])
        st.dataframe(data, use_container_width=True)

    @st.dialog('Atualizar raiz da taxonomia')
    def update_taxonomy_form(_):
        def xpto(x):
            return x['name'][:-4]

        st.write(f'Atualizar Taxonomia: {_["title"]}')
        with st.form(key=f'form_update_{_["id"]}'):
            new_title = st.text_input('Título', _['title'])
            new_description = st.text_area('Descrição', _['description'])
            new_source = st.multiselect(
                'Fonte',
                sources,
                default=_['source'],
                format_func=xpto,
            )
            submitted = st.form_submit_button('Atualizar')

            if submitted:
                updated_data = {
                    'id': _['id'],
                    'title': new_title,
                    'description': new_description,
                    'source': new_source,
                    'created_at': _['created_at'],
                    'updated_at': datetime.now().isoformat(),
                }

                taxonomy.put_taxonomy(updated_data)
                st.success('Taxonomia atualizada com sucesso!')
                st.rerun()

    st.subheader('Lista de taxonomias')
    for _ in taxonomies:
        st.write(f'{_["title"]}')
        with st.expander(f'Descrição: __{_["description"]}__'):
            show_taxonomies(_)

            container = st.container()
            a, b = container.columns(2)

            DELETE_TAXONOMY = a.button(
                'Deletar Taxonomia',
                key=f'delete_{_["id"]}',
                use_container_width=True,
            )
            PUT_TAXONOMY = b.button(
                'Atualizar Taxonomia',
                key=f'update_{_["id"]}',
                use_container_width=True,
            )
            if PUT_TAXONOMY:
                update_taxonomy_form(_)
                PUT_TAXONOMY = False

            if DELETE_TAXONOMY:
                taxonomy.delete_taxonomy(_['id'])
                st.success('Taxonomia deletada com sucesso!')
                DELETE_TAXONOMY = False

            st.button(
                'Lista de ramos',
                use_container_width=True,
                key=f'branches_{_["id"]}',
            )
            show_branches(_)
