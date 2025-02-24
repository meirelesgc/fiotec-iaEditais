import streamlit as st
from hooks import taxonomy, publication as order
from datetime import datetime


def main():
    typifications = taxonomy.get_typifications()

    def format_date(date_str):
        if isinstance(date_str, str):
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
            return dt.strftime('%d/%m/%Y %H:%M:%S')
        return None

    orders = order.get_order()

    @st.dialog('Adicionar Edital', width='large')
    def create_order():
        with st.form(key='create_order_form'):
            name = st.text_input('Nome do edital')
            type = st.multiselect(
                'Tipo do edital',
                options=typifications,
                format_func=lambda t: t['name'],
            )
            if st.form_submit_button('Adicionar Edital'):
                order.post_order(name, type)
                st.success('Edital criado com sucesso!')

    @st.dialog('Adicionar Versão', width='large')
    def create_release(ord):
        uploaded_file = st.file_uploader('Escolha um arquivo PDF', type='pdf')
        if st.button('Enviar arquivo') and uploaded_file:
            with st.status('Analisando versão...', expanded=True) as status:
                order.post_release(uploaded_file, ord['id'])
                status.update(label='Analise concluida!', state='complete')

    def show_release(r):
        for t in r['taxonomy']:
            st.subheader('🧵 Tipificação:')
            st.caption(t['name'])
            for tx in t['taxonomy']:
                st.subheader('🪢 Taxonomia:')
                st.caption(tx['title'])
                for br in tx['branch']:
                    st.subheader('🪡 Ramo:')
                    st.caption(br['title'])
                    emote = '✅' if br['evaluate']['fulfilled'] else '❌'
                    st.write(f'Descrição: {br["description"]}')
                    st.write(f'Critério cumprido: {emote}')
                    st.write(f'Feedback: {br["evaluate"]["feedback"]}')
                    st.divider()

    st.title('📊 Gestão de Editais')
    st.divider()
    if st.button('➕ Adicionar Edital', use_container_width=True):
        create_order()

    if not orders:
        st.error('Nenhum edital encontrado.')
    for index, o in enumerate(orders):
        container = st.container()
        a, b, c = container.columns([5, 1, 1])
        a.subheader(o['name'])

        if b.button(
            '➕ Adicionar',
            key=o['id'],
            use_container_width=True,
        ):
            create_release(o)
        if c.button(
            '🗑️ Excluir',
            use_container_width=True,
            key=f'delete_{o["id"]}',
        ):
            order.delete_order(o['id'])

        release_list = sorted(
            order.get_release(o['id']),
            key=lambda r: r['created_at'],
            reverse=True,
        )

        for index, r in enumerate(release_list):
            st.header(f'{index + 1} - {format_date(r["created_at"])}')
            with st.expander('Detalhes'):
                show_release(r)
                if st.button('🗑️ Excluir', key=f'delete_{o["id"]}_{r["id"]}'):
                    order.delete_release(r['id'])
