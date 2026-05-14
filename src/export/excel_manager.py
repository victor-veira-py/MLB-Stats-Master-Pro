# ==============================================================================
# MODULE: Excel Reporting Manager
# DESCRIPTION: Professional formatting with error suppression (Green triangles).
# MÓDULO: Gestor de Reportes Excel
# DESCRIPCIÓN: Formateo profesional con supresión de errores (Triángulos verdes).
# ==============================================================================

import pandas as pd

def apply_mlb_styling(writer, sheet_name, df):
    """
    Applies the corporate MLB look and feel and removes green warning triangles.
    Aplica el estilo corporativo de MLB y elimina los triángulos verdes de advertencia.
    """
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Style Definitions / Definición de Estilos
    f_header = workbook.add_format({
        'bold': True, 'bg_color': '#1F4E78', 'font_color': 'white', 'align': 'center', 'border': 1
    })
    f_data = workbook.add_format({'align': 'center', 'border': 1, 'border_color': '#D9D9D9'})
    f_total = workbook.add_format({'bold': True, 'bg_color': '#F2F2F2', 'align': 'center', 'border': 1})

    worksheet.hide_gridlines(2)

    # FIX: Suppress "Number stored as text" warnings / Elimina los triángulos verdes
    # We cover the entire data range / Cubrimos todo el rango de datos
    worksheet.ignore_errors({'number_stored_as_text': f'A1:Z{len(df) + 2}'})

    # Dynamic Column Scaling / Ajuste dinámico de columnas
    for i, col in enumerate(df.columns):
        ancho = max(df[col].astype(str).map(len).max(), len(col)) + 3
        worksheet.set_column(i, i, ancho, f_data)
        worksheet.write(0, i, col, f_header)

    # Career Row Formatting (Last Row) / Formato de fila CARRERA
    idx_ultima = len(df)
    for i in range(len(df.columns)):
        worksheet.write(idx_ultima, i, df.iloc[-1, i], f_total)

def save_individual_excel(df, filename, sheet_name='Estadisticas'):
    """Saves a single DataFrame to its own file / Guarda un solo DataFrame en su propio archivo."""
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        apply_mlb_styling(writer, sheet_name, df)