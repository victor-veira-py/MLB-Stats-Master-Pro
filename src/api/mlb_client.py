# ==============================================================================
# MODULE: MLB StatsAPI Client
# DESCRIPTION: Handles direct communication with MLB's official StatsAPI.
# MÓDULO: Cliente de StatsAPI de MLB
# DESCRIPCIÓN: Maneja la comunicación directa con la API oficial de MLB.
# ==============================================================================

import requests

BASE_URL = "https://statsapi.mlb.com/api/v1"


def search_player_id(name):
    """
    Searches for a player by name and returns their unique MLB ID.
    Busca a un jugador por nombre y devuelve su ID único de MLB.
    """
    # Search for active players / Buscar entre jugadores activos
    url = f"{BASE_URL}/people/search?names={name.replace(' ', '%20')}&activeStatus=BOTH"
    response = requests.get(url).json()

    if "people" in response and len(response["people"]) > 0:
        # Returns the first match / Devuelve la primera coincidencia
        return response["people"][0]["id"], response["people"][0]["fullName"]
    return None, None


def get_player_info(player_id):
    """
    Retrieves general player metadata (Full name, position, etc.)
    Recupera metadatos generales del jugador (Nombre completo, posición, etc.)
    """
    response = requests.get(f"{BASE_URL}/people/{player_id}")
    return response.json()


def get_player_stats(player_id):
    """
    Queries year-by-year hitting statistics for a specific player.
    Consulta estadísticas de bateo año por año para un jugador específico.
    """
    url = f"{BASE_URL}/people/{player_id}/stats?stats=yearByYear&group=hitting&sportIds=1"
    response = requests.get(url)
    return response.json()