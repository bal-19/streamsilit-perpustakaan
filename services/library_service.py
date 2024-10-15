from dotenv import load_dotenv

import requests
import os


load_dotenv()

class LibraryService:
    def __init__(self) -> None:
        self.base_url = os.getenv("BASE_URL")
    
    def get_jenis_perpustakaan(self) -> list:
        res = requests.get(f"{self.base_url}/list/type")
        if res.status_code == 200:
            return res.json().get("types", [])
        else:
            return []
    
    def get_subjenis(self, jenis_perpustakaan: str) -> list:
        res = requests.get(f"{self.base_url}/list/subtype/{jenis_perpustakaan}")
        if res.status_code == 200:
            return res.json().get("subtypes", [])
        else:
            return []
    
    def get_provinsi(self) -> list[dict]:
        res = requests.get(f"{self.base_url}/list/region/provinces")
        if res.status_code == 200:
            return res.json().get("data", [])
        else:
            return []
    
    def get_kab_kota(self, provinsi: str) -> list[dict]:
        res = requests.get(f"{self.base_url}/list/region/regencies/{provinsi}")
        if res.status_code == 200:
            return res.json().get("data", [])
        else:
            return []
    
    def get_kecamatan(self, kab_kota: str) -> list[dict]:
        res = requests.get(f"{self.base_url}/list/region/districts/{kab_kota}")
        if res.status_code == 200:
            return res.json().get("data", [])
        else:
            return []
    
    def get_kelurahan_desa(self, kecamatan: str) -> list[dict]:
        res = requests.get(f"{self.base_url}/list/region/villages/{kecamatan}")
        if res.status_code == 200:
            return res.json().get("data", [])
        else:
            return []
    
    def get_libraries(self, jenis_perpustakaan: str, subjenis: str, provinsi: str, kab_kota: str, kecamatan: str, kelurahan_desa: str, start: int) -> list[dict]:
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
        
        res = requests.get(f"{self.base_url}/data", params=params)
        if res.status_code == 200:
            return res.json()
        else:
            return None
