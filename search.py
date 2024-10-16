from services import library_service

import streamlit as st
import pandas as pd


st.set_page_config(layout="wide", page_title="List of libraries in Indonesia", page_icon="📖")

class PerpustakaanSearchApp:
    def __init__(self):
        self.items_per_page = 10
        if 'page' not in st.session_state:
            st.session_state.page = 0
    
    def __reset_page(self):
        """reset session page"""
        st.session_state.page = 0
    
    def __get_options(self, data):
        """mengembalikan option dengan nama"""
        return sorted(list(set(data)))
    
    def __get_options_with_ids(self, data):
        """mengembalikan option dengan id dan nama"""
        return [(item['id'], item['nama']) for item in data]
    
    def search_libraries(self, jenis_perpustakaan, subjenis, provinsi, kab_kota, kecamatan, kelurahan_desa):
        """proses pencarian data perpustakaan"""
        start = st.session_state.page * self.items_per_page
        data = library_service.get_libraries(
            jenis_perpustakaan if jenis_perpustakaan != 'Semua' else '',
            subjenis if subjenis != 'Semua' else '',
            provinsi if provinsi != 'Semua' else '',
            kab_kota if kab_kota != 'Semua' else '',
            kecamatan if kecamatan != 'Semua' else '',
            kelurahan_desa if kelurahan_desa != 'Semua' else '',
            start=start
        )
        
        # menampilkan data jika ada
        if data:
            if data.get("data"):
                df = pd.DataFrame(data.get("data", []), index=range(start + 1, start + len(data.get("data", [])) + 1))
                df.columns = ["NPP", "Nama Perpustakaan", "Lembaga", "Alamat", "Telepon", "Email", "Website", "Jenis", "Subjenis", "Status", "Kode Pos", "Provinsi", "Kabupaten/Kota", "Kecamatan", "Kelurahan/Desa"]
                
                st.info(f"Menampilkan {start + 1} - {start + len(data.get('data', []))} dari {data.get('total', 0)} data")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning('Tidak ada data yang ditemukan.')
        else:
            st.warning('Tidak ada data yang ditemukan.')

        # pagination
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("Previous", disabled=st.session_state.page == 0, use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

        with col2:
            total_pages = (data.get('total', 0) + self.items_per_page - 1) // self.items_per_page
            current_page = st.session_state.page + 1
            
            start_page = max(1, current_page - 1)
            end_page = min(total_pages, start_page + 2)
            
            page_buttons = st.columns(3)
            for i, page in enumerate(range(start_page, end_page + 1)):
                if page == current_page:
                    page_buttons[i].button(str(page), key=f"page_{page}", use_container_width=True, disabled=True)
                else:
                    if page_buttons[i].button(str(page), key=f"page_{page}", use_container_width=True):
                        st.session_state.page = page - 1
                        st.rerun()

        with col3:
            is_last_page = start + len(data.get('data', [])) >= data.get('total', 0)
            if not is_last_page:
                if st.button("Next", use_container_width=True):
                    st.session_state.page += 1
                    st.rerun()
            else:
                st.button("Next", use_container_width=True, disabled=True)

    def run(self):
        """run app"""
        st.markdown("<h1 style='text-align: center;'>🔍 Pencarian Perpustakaan di Indonesia</h1>", unsafe_allow_html=True)
        
        # form pencarian
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            # baris pertama
            col_jenis, col_subjenis = st.columns(2)
            with col_jenis:
                if 'jenis_perpustakaan_options' not in st.session_state:
                    st.session_state.jenis_perpustakaan_options = ['Semua'] + self.__get_options(library_service.get_jenis_perpustakaan())
                jenis_perpustakaan = st.selectbox('Jenis Perpustakaan', st.session_state.jenis_perpustakaan_options, on_change=self.__reset_page)
            with col_subjenis:
                if jenis_perpustakaan != 'Semua':
                    if 'subjenis_options' not in st.session_state:
                        st.session_state.subjenis_options = ['Semua'] + self.__get_options(library_service.get_subjenis(jenis_perpustakaan))
                    subjenis = st.selectbox('Subjenis', st.session_state.subjenis_options, on_change=self.__reset_page)
                else:
                    subjenis = st.selectbox('Subjenis', ['Semua'], on_change=self.__reset_page)
            
            # baris kedua
            col_provinsi, col_kab_kota = st.columns(2)
            with col_provinsi:
                if 'provinsi_options' not in st.session_state:
                    st.session_state.provinsi_options = [('', 'Semua')] + self.__get_options_with_ids(library_service.get_provinsi())
                provinsi = st.selectbox('Provinsi', options=st.session_state.provinsi_options, format_func=lambda x: x[1], on_change=self.__reset_page)
            with col_kab_kota:
                if provinsi[0] != '':
                    kab_kota_options = [('', 'Semua')] + self.__get_options_with_ids(library_service.get_kab_kota(provinsi[0]))
                else:
                    kab_kota_options = [('', 'Semua')]
                kab_kota = st.selectbox('Kabupaten/Kota', options=kab_kota_options, format_func=lambda x: x[1], on_change=self.__reset_page)
            
            # baris ketiga
            col_kecamatan, col_kelurahan = st.columns(2)
            with col_kecamatan:
                if kab_kota[0] != '':
                    kecamatan_options = [('', 'Semua')] + self.__get_options_with_ids(library_service.get_kecamatan(kab_kota[0]))
                else:
                    kecamatan_options = [('', 'Semua')]
                kecamatan = st.selectbox('Kecamatan', options=kecamatan_options, format_func=lambda x: x[1], on_change=self.__reset_page)
            with col_kelurahan:
                if kecamatan[0] != '':
                    kelurahan_desa_options = [('', 'Semua')] + self.__get_options_with_ids(library_service.get_kelurahan_desa(kecamatan[0]))
                else:
                    kelurahan_desa_options = [('', 'Semua')]
                kelurahan_desa = st.selectbox('Kelurahan/Desa', options=kelurahan_desa_options, format_func=lambda x: x[1], on_change=self.__reset_page)
        
        # proses pencarian
        self.search_libraries(
            jenis_perpustakaan=jenis_perpustakaan,
            subjenis=subjenis,
            provinsi=provinsi[0],
            kab_kota=kab_kota[0],
            kecamatan=kecamatan[0],
            kelurahan_desa=kelurahan_desa[0]
        )
    


if __name__ == "__main__":
    app = PerpustakaanSearchApp()
    app.run()




