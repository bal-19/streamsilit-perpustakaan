from dotenv import load_dotenv

import streamlit as st
import requests
import os


load_dotenv()

api_url = os.getenv("API_URL")
        
@st.cache_data(ttl=1800, show_spinner=False)
def get_jenis_perpustakaan() -> list:
    res = requests.get(f"{api_url}/list/type")
    if res.status_code == 200:
        return res.json().get("types", [])
    else:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def get_subjenis(jenis_perpustakaan: str) -> list:
    res = requests.get(f"{api_url}/list/subtype/{jenis_perpustakaan}")
    if res.status_code == 200:
        return res.json().get("subtypes", [])
    else:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def get_provinsi() -> list[dict]:
    res = requests.get(f"{api_url}/list/region/provinces")
    if res.status_code == 200:
        return res.json().get("data", [])
    else:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def get_kab_kota(provinsi: str) -> list[dict]:
    res = requests.get(f"{api_url}/list/region/regencies/{provinsi}")
    if res.status_code == 200:
        return res.json().get("data", [])
    else:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def get_kecamatan(kab_kota: str) -> list[dict]:
    res = requests.get(f"{api_url}/list/region/districts/{kab_kota}")
    if res.status_code == 200:
        return res.json().get("data", [])
    else:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def get_kelurahan_desa(kecamatan: str) -> list[dict]:
    res = requests.get(f"{api_url}/list/region/villages/{kecamatan}")
    if res.status_code == 200:
        return res.json().get("data", [])
    else:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def get_libraries(jenis_perpustakaan: str, subjenis: str, provinsi: str, kab_kota: str, kecamatan: str, kelurahan_desa: str, start: int) -> list[dict]:
    params = {
        "type_name": jenis_perpustakaan,
        "subtype_name": subjenis,
        "province_id": provinsi,
        "regency_id": kab_kota,
        "subdistrict_id": kecamatan,
        "village_id": kelurahan_desa,
        "start": start,
        "length": "10"
    }
    
    res = requests.get(f"{api_url}/data", params=params)
    if res.status_code == 200:
        return res.json()
    else:
        return None
