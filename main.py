import os
from gestor_datos import GestorDatos

RUTA_DATOS = os.path.join(os.path.dirname(__file__), "data", "obras.json")


def mostrar_menu():
    print("\n" + "=" * 45)
    print("           MULTIVERSOGUIDE (v2)")
    print("      Tu guía antes del multiverso")
    print("=" * 45)
    print("[1] Buscar obra por título (parcial)")
    print("[2] Listar todas las obras (por año)")
    print("[3] Filtrar obras")
    print("[4] Buscar obra por título exacto (árbol)")
    print("[5] Listar ordenado alfabéticamente (árbol)")
    print("[6] Salir")
    print("=" * 45)


def mostrar_resultados(obras):
    if not obras:
        print("\nNo se encontraron resultados.")
        return
    print()
    for obra in obras:
        print(obra.obtener_info())
        print("-" * 40)


def accion_buscar(gestor):
    texto = input("Ingresá el título (o parte de él): ")
    resultados = gestor.buscar_por_titulo(texto)
    mostrar_resultados(resultados)


def accion_listar(gestor):
    obras = gestor.listar_todas(orden_por_anio=True)
    mostrar_resultados(obras)


def accion_filtrar(gestor):
    print("\nDejá vacío cualquier campo que no quieras usar como filtro.")
    tipo = input("Tipo (pelicula/serie/comic): ").strip() or None
    fase = input("Fase/Saga: ").strip() or None
    personaje = input("Personaje: ").strip() or None
    resultados = gestor.filtrar(tipo=tipo, fase=fase, personaje=personaje)
    mostrar_resultados(resultados)


def accion_buscar_arbol(gestor):
    titulo = input("Ingresá el título EXACTO: ")
    obra = gestor.buscar_exacto_arbol(titulo)
    mostrar_resultados([obra] if obra else [])


def accion_listar_arbol(gestor):
    obras = gestor.listar_ordenado_por_titulo()
    mostrar_resultados(obras)


def main():
    try:
        gestor = GestorDatos(RUTA_DATOS)
    except FileNotFoundError as error:
        print(f"Error al iniciar: {error}")
        return

    acciones = {
        "1": accion_buscar,
        "2": accion_listar,
        "3": accion_filtrar,
        "4": accion_buscar_arbol,
        "5": accion_listar_arbol,
    }

    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()

        if opcion == "6":
            print("¡Hasta la próxima, viajero del multiverso!")
            break
        elif opcion in acciones:
            acciones[opcion](gestor)
        else:
            print("\nOpción inválida, probá de nuevo.")


if __name__ == "__main__":
    main()
