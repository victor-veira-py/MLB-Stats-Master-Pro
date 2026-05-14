# ==============================================================================
# MAIN INTERFACE: MLB Stats Master Pro
# INTERFAZ PRINCIPAL: MLB Stats Master Pro
# DEVELOPED BY: VICTOR ARMANDO DE OLIVEIRA RODRÍGUEZ
# ==============================================================================

import os
import shutil
from src.pipeline.consolidated import run_mlb_software
from src.api.mlb_client import search_player_id


def clear_console():
    """Cleans the terminal screen / Limpia la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def clean_data_folder():
    """
    Deletes all files inside the /data folder.
    Elimina todos los archivos dentro de la carpeta /data.
    """
    folder = 'data'
    print(f"\n🧹 [SYSTEM] Cleaning folder: {folder}...")
    print(f"🧹 [SISTEMA] Limpiando carpeta: {folder}...")

    try:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            # We don't delete .gitkeep / No borramos el .gitkeep
            if filename == ".gitkeep":
                continue
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print("✅ Folder is now empty / Carpeta vacía ahora.")
    except Exception as e:
        print(f"❌ Error cleaning folder / Error limpiando carpeta: {e}")


def get_dynamic_player_ids():
    """Asks for names and retrieves IDs / Pide nombres y recupera IDs"""
    print("\n" + "-" * 75)
    print("📝 Enter names separated by commas (e.g.: Jose Altuve, Aaron Judge)")
    print("📝 Ingrese nombres separados por comas (ej.: Jose Altuve, Aaron Judge)")
    entrada = input(">>> ")

    nombres = [n.strip() for n in entrada.split(",") if n.strip()]
    ids_encontrados = []

    for nombre in nombres:
        p_id, full_name = search_player_id(nombre)
        if p_id:
            print(f"   ✅ Found / Encontrado: {full_name} (ID: {p_id})")
            ids_encontrados.append(str(p_id))
        else:
            print(f"   ❌ Not found / No encontrado: {nombre}")
    return ids_encontrados


def show_menu():
    """Bilingual Menu Display / Pantalla de Menú Bilingüe"""
    print("\n" + "=" * 75)
    print("⚾ MLB STATS MASTER PRO - BY VICTOR ARMANDO".center(75))
    print("=" * 75)
    print("  1. [PHASE 1] SINGLE REPORT (SEARCH BY NAME)")
    print("     [FASE 1] REPORTE ÚNICO (BUSCAR POR NOMBRE)")
    print("-" * 75)
    print("  2. [PHASE 2] MULTIPLE INDIVIDUAL REPORTS (CUSTOM LIST)")
    print("     [FASE 2] REPORTES INDIVIDUALES MÚLTIPLES (LISTA PERSONALIZADA)")
    print("-" * 75)
    print("  3. [PHASE 3] CONSOLIDATED WORKBOOK (CUSTOM LIST)")
    print("     [FASE 3] LIBRO CONSOLIDADO (LISTA PERSONALIZADA)")
    print("-" * 75)
    print("  4. CLEAN DATA FOLDER / LIMPIAR CARPETA DATA")
    print("-" * 75)
    print("  5. EXIT / SALIR")
    print("=" * 75)


def main():
    # Ensure data folder exists / Asegurar que la carpeta data existe
    if not os.path.exists('data'):
        os.makedirs('data')

    while True:
        show_menu()
        choice = input("\n>>> Select an option / Seleccione opción (1-5): ")

        if choice == "5":
            print("\n👋 Closing... Goodbye VICTOR ARMANDO!")
            break

        if choice == "4":
            clean_data_folder()

        elif choice in ["1", "2", "3"]:
            ids = get_dynamic_player_ids()
            if not ids:
                print("\n⚠️ No players found / No hay jugadores.")
            else:
                if choice == "1":
                    run_mlb_software([ids[0]], mode="individual")
                elif choice == "2":
                    run_mlb_software(ids, mode="individual")
                elif choice == "3":
                    run_mlb_software(ids, mode="book")
        else:
            print("\n⚠️ Invalid Input / Entrada Inválida.")

        input("\nPress Enter to return / Presione Enter para volver...")
        clear_console()


if __name__ == "__main__":
    main()