# ==============================================================================
# MODULE: Statistics Processor
# DESCRIPTION: Logic for data cleaning and career totals calculation.
# MÓDULO: Procesador de Estadísticas
# DESCRIPCIÓN: Lógica para limpieza de datos y cálculo de totales de carrera.
# ==============================================================================

import pandas as pd


def process_yearly_stats(data):
    """
    Parses API JSON response into a structured list of hitting stats.
    Analiza la respuesta JSON de la API en una lista estructurada de bateo.
    """
    # Validation of the API structure / Validación de la estructura de la API
    if "stats" not in data or not data["stats"][0]["splits"]:
        return None

    splits = data["stats"][0]["splits"]
    lista_temporadas = []

    for s in splits:
        stat = s.get("stat", {})
        ab = int(stat.get("atBats", 0))

        # We skip rows without At Bats to keep data clean / Saltamos filas sin AB para limpiar datos
        if ab == 0: continue

        # Management of team names or totals / Gestión de nombres de equipo o totales
        nombre_equipo = s.get("team", {}).get("name", "TOTAL")

        lista_temporadas.append({
            "TEMPORADA": int(s.get("season")),
            "EQUIPO": nombre_equipo,
            "J": int(stat.get("gamesPlayed", 0)),
            "AB": ab,
            "R": int(stat.get("runs", 0)),
            "H": int(stat.get("hits", 0)),
            "2B": int(stat.get("doubles", 0)),
            "3B": int(stat.get("triples", 0)),
            "HR": int(stat.get("homeRuns", 0)),
            "RBI": int(stat.get("rbi", 0)),
            "BB": int(stat.get("baseOnBalls", 0)),
            "HBP": int(stat.get("hitByPitch", 0)),
            "K": int(stat.get("strikeOuts", 0)),
            "SB": int(stat.get("stolenBases", 0)),
            "CS": int(stat.get("caughtStealing", 0)),
            # Floats are kept for subsequent math / Mantenemos floats para cálculos posteriores
            "AVG": float(stat.get("avg", 0)),
            "OBP": float(stat.get("obp", 0)),
            "SLG": float(stat.get("slg", 0)),
            "OPS": float(stat.get("ops", 0))
        })
    return lista_temporadas


def calculate_career_totals(df):
    """
    Calculates lifetime statistics based on the processed DataFrame.
    Calcula las estadísticas de por vida basadas en el DataFrame procesado.
    """
    # Filter to avoid duplicating totals from the API / Filtro para evitar duplicar totales de la API
    df_solo_equipos = df[df["EQUIPO"] != "TOTAL"]

    # Summation and Average logic / Lógica de sumatorias y promedios
    fila_totales = {
        "TEMPORADA": "",
        "EQUIPO": "CARRERA",
        "J": df_solo_equipos["J"].sum(),
        "AB": df_solo_equipos["AB"].sum(),
        "R": df_solo_equipos["R"].sum(),
        "H": df_solo_equipos["H"].sum(),
        "2B": df_solo_equipos["2B"].sum(),
        "3B": df_solo_equipos["3B"].sum(),
        "HR": df_solo_equipos["HR"].sum(),
        "RBI": df_solo_equipos["RBI"].sum(),
        "BB": df_solo_equipos["BB"].sum(),
        "HBP": df_solo_equipos["HBP"].sum(),
        "K": df_solo_equipos["K"].sum(),
        "SB": df_solo_equipos["SB"].sum(),
        "CS": df_solo_equipos["CS"].sum(),
        # Weighted career average calculation / Cálculo de promedio de carrera ponderado
        "AVG": df_solo_equipos["H"].sum() / df_solo_equipos["AB"].sum() if df_solo_equipos["AB"].sum() > 0 else 0,
        "OBP": df_solo_equipos["OBP"].mean(),
        "SLG": df_solo_equipos["SLG"].mean(),
        "OPS": df_solo_equipos["OPS"].mean()
    }
    return fila_totales