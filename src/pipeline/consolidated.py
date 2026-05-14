# ==============================================================================
# MODULE: Multi-Phase Pipeline.
# DESCRIPTION: Orchestrates Individual and Workbook reports for MLB.
# MÓDULO: Pipeline Multifase.
# DESCRIPCIÓN: Orquesta reportes individuales y tipo Libro para MLB.
# ==============================================================================

import pandas as pd
from src.api.mlb_client import get_player_info, get_player_stats
from src.core.stats_processor import process_yearly_stats, calculate_career_totals
from src.core.formatting import fmt_mlb
from src.export.excel_manager import apply_mlb_styling


def process_player_to_df(player_id):
    """
    Modular helper that fetches, processes, and formats player data.
    Ayudante modular que obtiene, procesa y formatea los datos del jugador.
    """
    info = get_player_info(player_id)
    nombre_completo = info["people"][0].get("fullName", "Jugador")

    # Dynamic naming logic for Excel tabs / Lógica dinámica de nombres para pestañas
    # Special handling for Ronald Acuña Jr. / Manejo especial para Ronald Acuña Jr.
    if "Acuña" in nombre_completo:
        nombre_pestaña = "Acuna Jr"
    else:
        # Take last name and limit to 31 chars / Toma el apellido y limita a 31 caracteres
        nombre_pestaña = nombre_completo.split()[-1][:31]

    raw_data = get_player_stats(player_id)
    lista_stats = process_yearly_stats(raw_data)

    if not lista_stats:
        return None, None

    # Data transformation to DataFrame / Transformación de datos a DataFrame
    df = pd.DataFrame(lista_stats)

    # Career totals calculation / Cálculo de totales de carrera
    fila_totales = calculate_career_totals(df)
    df = pd.concat([df, pd.DataFrame([fila_totales])], ignore_index=True)

    # Standard MLB formatting for percentages / Formateo estándar MLB para porcentajes
    for col in ["AVG", "OBP", "SLG", "OPS"]:
        df[col] = df[col].apply(fmt_mlb)

    return nombre_pestaña, df


def run_mlb_software(player_ids, mode="book"):
    """
    Executes the logic for Phase 1, 2, or 3 based on the selected mode.
    Ejecuta la lógica para la Fase 1, 2 o 3 según el modo seleccionado.
    """
    if mode == "book":
        # Phase 3: All players in one file / Fase 3: Todos los jugadores en un archivo
        output_path = "data/MLB_Consolidated_Report.xlsx"
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            for pid in player_ids:
                pestaña, df = process_player_to_df(pid)
                if df is not None:
                    df.to_excel(writer, sheet_name=pestaña, index=False)
                    apply_mlb_styling(writer, pestaña, df)
        print(f"✅ [PHASE 3] Book generated successfully at: {output_path}")

    elif mode == "individual":
        # Phase 1 & 2: Individual files per player / Fase 1 y 2: Archivos individuales por jugador
        for pid in player_ids:
            pestaña, df = process_player_to_df(pid)
            if df is not None:
                filename = f"data/Report_{pestaña.replace(' ', '_')}.xlsx"
                with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Estadisticas', index=False)
                    apply_mlb_styling(writer, 'Estadisticas', df)
                print(f"✅ [PHASE 1/2] Report generated for: {pestaña}")