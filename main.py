import os
from gestor_datos import GestorDatos
from models.usuario import Usuario

RUTA_DATOS = os.path.join(os.path.dirname(__file__), "data", "obras.json")


def mostrar_menu():
    print("\n" + "=" * 45)
    print("           MULTIVERSOGUIDE (v5)")
    print("      Tu guía antes del multiverso")
    print("=" * 45)
    print("[1] Buscar obra por título (parcial)")
    print("[2] Listar todas las obras (por año)")
    print("[3] Filtrar obras")
    print("[4] Buscar obra por título exacto (árbol)")
    print("[5] Listar ordenado alfabéticamente (árbol)")
    print("[6] Explorar categorías (árbol general)")
    print("[7] Top imprescindibles (ranking)")
    print("[8] Marcar una obra como vista")
    print("[9] Explorar conexiones (grafo)")
    print("[10] Salir")
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


def _mostrar_arbol_con_sangria(gestor):
    print()
    for nivel, nodo in gestor.jerarquia.recorrido_preorden():
        marca = "" if nivel == 0 else "└── "
        if nodo.obra is None:
            cantidad = gestor.jerarquia.contar_obras(nodo)
            print("    " * max(nivel - 1, 0) + marca + f"{nodo.nombre} ({cantidad})")
        else:
            print("    " * max(nivel - 1, 0) + marca + nodo.nombre)


def _mostrar_por_niveles(gestor):
    print()
    nivel_actual = -1
    for nivel, nodo in gestor.jerarquia.recorrido_por_niveles():
        if nivel != nivel_actual:
            nivel_actual = nivel
            print(f"\nNivel {nivel}:")
        print(f"  - {nodo.nombre}")


def _buscar_categoria(gestor):
    nombre = input("Nombre de la categoría u obra: ")
    nodo = gestor.jerarquia.buscar(nombre)
    if nodo is None:
        print("\nNo se encontró esa categoría ni obra.")
        return
    print("\nRuta: " + " > ".join(gestor.jerarquia.camino_a(nodo.nombre)))
    if nodo.obra is not None:
        mostrar_resultados([nodo.obra])
    else:
        obras = gestor.jerarquia.obras_de(nodo)
        print(f"Contiene {len(obras)} obra(s):")
        mostrar_resultados(obras)


def accion_explorar_categorias(gestor):
    while True:
        print("\n--- EXPLORAR CATEGORÍAS ---")
        print("[a] Ver el árbol completo")
        print("[b] Ver por niveles")
        print("[c] Buscar una categoría u obra (y ver su ruta)")
        print("[d] Volver")
        opcion = input("Elegí: ").strip().lower()
        if opcion == "a":
            _mostrar_arbol_con_sangria(gestor)
        elif opcion == "b":
            _mostrar_por_niveles(gestor)
        elif opcion == "c":
            _buscar_categoria(gestor)
        elif opcion == "d":
            break
        else:
            print("Opción inválida.")


def accion_top_imprescindibles(gestor, usuario):
    perfil = input("Perfil (casual/fan) [Enter = " + usuario.perfil + "]: ").strip().lower()
    if perfil in Usuario.PERFILES_VALIDOS:
        usuario.perfil = perfil
    try:
        n = int(input("¿Cuántas obras querés en el ranking? [Enter = 5]: ").strip() or 5)
    except ValueError:
        print("\nIngresá un número entero.")
        return
    ranking = gestor.top_n(n, perfil=usuario.perfil, excluir=usuario.obras_vistas)
    if not ranking:
        print("\nNo hay obras para mostrar (¿ya viste todo?).")
        return
    print(f"\nTOP {len(ranking)} imprescindibles - perfil {usuario.perfil}")
    print("-" * 52)
    for posicion, (puntaje, obra) in enumerate(ranking, start=1):
        print(f"{posicion}. {obra.titulo:<45} {puntaje:>5.2f}")
    if usuario.obras_vistas:
        print(f"\n(Excluidas {len(usuario.obras_vistas)} obra(s) que ya viste)")


def accion_marcar_vista(gestor, usuario):
    titulo = input("Título EXACTO de la obra que ya viste: ")
    obra = gestor.buscar_exacto_arbol(titulo)
    if obra is None:
        print("\nNo se encontró esa obra.")
        return
    usuario.marcar_vista(obra.titulo)
    print(f"\nListo, '{obra.titulo}' queda marcada como vista.")


def _pedir_obra(gestor, mensaje):
    """Pide un título (puede ser parcial) y devuelve la obra elegida,
    o None si no hay una coincidencia única."""
    texto = input(mensaje)
    coincidencias = gestor.buscar_por_titulo(texto)
    if not coincidencias:
        print("\nNo se encontró ninguna obra con ese texto.")
        return None
    if len(coincidencias) > 1:
        print("\nHay varias coincidencias, escribí un poco más del título:")
        for obra in coincidencias:
            print(f"  - {obra.titulo}")
        return None
    return coincidencias[0]


def _ver_conectadas(gestor):
    obra = _pedir_obra(gestor, "Obra (título o parte del título): ")
    if obra is None:
        return
    conectadas = gestor.obras_conectadas(obra.titulo)
    if not conectadas:
        print(f"\n'{obra.titulo}' no comparte personajes con ninguna otra obra del catálogo.")
        return
    print(f"\nObras conectadas con '{obra.titulo}':")
    for otra, personajes in conectadas:
        print(f"  - {otra.titulo}  (comparten: {', '.join(personajes)})")


def _ver_conexion_entre_dos(gestor):
    obra_a = _pedir_obra(gestor, "Primera obra: ")
    if obra_a is None:
        return
    obra_b = _pedir_obra(gestor, "Segunda obra: ")
    if obra_b is None:
        return
    if obra_a.titulo == obra_b.titulo:
        print("\nEscribiste la misma obra dos veces.")
        return
    comunes = gestor.conexion_entre(obra_a.titulo, obra_b.titulo)
    if comunes:
        print(f"\n'{obra_a.titulo}' y '{obra_b.titulo}' están conectadas.")
        print(f"Personajes en común: {', '.join(comunes)}")
    else:
        print(f"\n'{obra_a.titulo}' y '{obra_b.titulo}' NO están conectadas directamente.")


def _ver_grafo_completo(gestor):
    grafo = gestor.grafo
    print("\nLista de adyacencia (cada obra y las obras con las que se conecta):\n")
    for obra in sorted(grafo.vertices(), key=lambda o: o.titulo):
        vecinos = [a.destino for a in grafo.vecinos(obra.titulo)]
        detalle = ", ".join(vecinos) if vecinos else "(sin conexiones)"
        print(f"{obra.titulo}\n    -> {detalle}")


def _ver_estadisticas_grafo(gestor):
    grafo = gestor.grafo
    print("\nEstadísticas del grafo:")
    print(f"  Obras (vértices):          {grafo.cantidad_vertices()}")
    print(f"  Conexiones entre obras:    {grafo.cantidad_aristas() // 2}")
    print(f"  Densidad:                  {grafo.densidad():.1%}")
    mas_conectada = max(grafo.vertices(), key=lambda o: grafo.grado(o.titulo))
    print(f"  Obra más conectada:        {mas_conectada.titulo} ({grafo.grado(mas_conectada.titulo)} conexiones)")
    aislados = grafo.aislados()
    if aislados:
        print("  Obras sin conexiones:      " + ", ".join(o.titulo for o in aislados))


def accion_explorar_conexiones(gestor):
    while True:
        print("\n--- EXPLORAR CONEXIONES ---")
        print("[a] Ver obras conectadas con una obra")
        print("[b] Ver qué comparten dos obras")
        print("[c] Ver el grafo completo")
        print("[d] Ver estadísticas del grafo")
        print("[e] Volver")
        opcion = input("Elegí: ").strip().lower()
        if opcion == "a":
            _ver_conectadas(gestor)
        elif opcion == "b":
            _ver_conexion_entre_dos(gestor)
        elif opcion == "c":
            _ver_grafo_completo(gestor)
        elif opcion == "d":
            _ver_estadisticas_grafo(gestor)
        elif opcion == "e":
            break
        else:
            print("Opción inválida.")


def main():
    try:
        gestor = GestorDatos(RUTA_DATOS)
    except FileNotFoundError as error:
        print(f"Error al iniciar: {error}")
        return

    usuario = Usuario("Invitado", perfil="casual")

    acciones = {
        "1": accion_buscar,
        "2": accion_listar,
        "3": accion_filtrar,
        "4": accion_buscar_arbol,
        "5": accion_listar_arbol,
        "6": accion_explorar_categorias,
        "9": accion_explorar_conexiones,
    }

    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()

        if opcion == "10":
            print("¡Hasta la próxima, viajero del multiverso!")
            break
        elif opcion == "7":
            accion_top_imprescindibles(gestor, usuario)
        elif opcion == "8":
            accion_marcar_vista(gestor, usuario)
        elif opcion in acciones:
            acciones[opcion](gestor)
        else:
            print("\nOpción inválida, probá de nuevo.")


if __name__ == "__main__":
    main()
