import requests

API_KEY = "2237852967a142e9ad6302f2ed07c45f"
BASE_URL = "https://api.football-data.org/v4/"

def obtener_partidos(competicion="PL"):  
    url = f"{BASE_URL}competitions/{competicion}/matches"
    headers = {"X-Auth-Token": API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    datos = obtener_partidos()
    if datos:
        print("🔹 Datos de partidos obtenidos con éxito.")
        print(datos)
