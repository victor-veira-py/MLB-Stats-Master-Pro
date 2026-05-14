# ==============================================================================
# UTILITY: MLB Visual Formatting
# DESCRIPTION: Applies standard baseball percentage formats (.XXX).
# UTILIDAD: Formateo Visual de MLB
# DESCRIPCIÓN: Aplica formatos estándar de porcentajes de béisbol (.XXX).
# ==============================================================================

def fmt_mlb(valor):
    """
    Converts numeric values to MLB string format (e.g., 0.300 -> .300).
    Convierte valores numéricos a formato de cadena MLB (ej. 0.300 -> .300).
    """
    try:
        return f"{float(valor):.3f}".replace("0.", ".")
    except (ValueError, TypeError):
        return ".000"