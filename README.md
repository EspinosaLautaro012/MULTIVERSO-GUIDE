# MULTIVERSO-GUIDE
 
GRUPO 12

Dominio elegido: Universo cinematográfico y expandido de Marvel (películas, series y cómics del MCU)

Con el estreno de la nueva película de Avengers en diciembre, es un dominio con actualidad y con un problema real y concreto (la sobrecarga de contenido acumulado en los últimos años). Además, la estructura del universo Marvel se presta naturalmente a las estructuras de datos del TP: jerarquía por fases/sagas (árbol), ranking de imprescindibles (heap), y conexiones entre personajes/eventos que atraviesan distintas obras (grafo).

Problema que resuelve:  
Con el estreno de la nueva película de Avengers en diciembre, muchos espectadores vieron las primeras fases del MCU pero perdieron el hilo de series, spin-offs y cómics recientes. No saben qué contenido es imprescindible ver antes de ir al cine, ni tienen tiempo de ver todo el catálogo acumulado. MultiversoGuide arma una guía personalizada de qué mirar antes del estreno, priorizando lo esencial y respetando el tiempo disponible del usuario.

Usuario objetivo:
Alguien que vio las películas más conocidas del MCU (Iron Man, Endgame, etc.) pero no siguió series ni cómics recientes, y quiere ponerse al día antes de diciembre sin ver todo el catálogo. A futuro, el sistema también contemplará distintos perfiles: usuarios "fanáticos" que quieren ver todo el contenido relacionado, y usuarios "casuales" que solo necesitan lo esencial.

Funcionalidades iniciales:
1. Buscar una obra (película/serie/cómic) por título y ver su información (fase, año, duración, personajes).
2. Ver el watch order recomendado, ordenado cronológicamente o por fase.
3. Consultar el Top-N de contenido imprescindible antes del estreno, priorizado por relevancia.
4. Explorar obras relacionadas a un personaje o evento.
5. Buscar el camino mínimo de contenido entre dos obras (por ejemplo, de "Iron Man" a la nueva Avengers).

 DIAGRAMA INCIAL DE CLASES

Obra
titulo, tipo, año, duración, fase, rating
+ buscar(), obtener_info()	FaseSaga
nombre, orden	Usuario
perfil (fan/casual)
+ recomendar(), camino_minimo()
Personaje
nombre	Evento
nombre, descripción	


• Obra pertenece a una FaseSaga (jerarquía → árbol general).
• Obra tiene una lista de Personaje que aparecen en ella.
• Personaje participa en Evento, y un Evento puede estar contado en varias Obra (esto arma el grafo de conexiones).
• Usuario tiene un perfil (fan/casual) y usa Obra para calcular recomendaciones y caminos mínimos.

=== MULTIVERSOGUIDE ===
1. Buscar obra
2. Ver watch order recomendado
3. Top imprescindibles antes del estreno
4. Explorar por personaje/evento
5. Camino mínimo entre dos obras
6. Salir
 
> Elegir una opción: 3
 
Top 5 imprescindibles antes de Avengers 5:
1. Loki (T1-T2) - introduce la TVA y el multiverso
2. Spider-Man: No Way Home - cruce de multiversos, villanos clásicos
3. Avengers: Infinity War / Endgame - arco central del Snap
4. Deadpool & Wolverine - conecta X-Men al MCU vía la TVA
5. Doctor Strange en el Multiverso de la Locura - expande el multiverso y variantes




╔════════════════════════════════════╗
║         MULTIVERSOGUIDE             ║
║  Tu guía antes del multiverso        ║
╠════════════════════════════════════╣
║ [1] Buscar obra                     ║
║ [2] Watch order recomendado         ║
║ [3] Top imprescindibles             ║
║ [4] Explorar por personaje/evento    ║
║ [5] Camino mínimo entre obras        ║
║ [6] Salir                            ║
╚════════════════════════════════════╝

# modelos/obra.py
class Obra:
    def __init__(self, titulo, genero, rating, anio, fase):
        self._titulo = titulo
        self._genero = genero
        self._rating = rating
        self._anio = anio
        self._fase = fase

    # Getters
    def get_titulo(self):
        return self._titulo

    def get_genero(self):
        return self._genero

    def get_rating(self):
        return self._rating

    def get_anio(self):
        return self._anio

    def get_fase(self):
        return self._fase

    def obtener_info(self):
        return f"{self._titulo} ({self._genero}, {self._anio}) - Fase {self._fase} ⭐{self._rating}"

    def __repr__(self):
        return self.obtener_info()


# modelos/usuario.py
class Usuario:
    def __init__(self, perfil="casual"):
        self._perfil = perfil

    def recomendar(self, obras):
        # versión mínima: devuelve las 3 con mejor rating
        return sorted(obras, key=lambda o: o.get_rating(), reverse=True)[:3]

    def __repr__(self):
        return f"Usuario perfil: {self._perfil}"
    [    
    {"titulo": "Iron Man", "genero": "Acción", "rating": 8.5, "anio": 2008, "fase": 1},
    {"titulo": "Avengers: Endgame", "genero": "Acción", "rating": 9.0, "anio": 2019, "fase": 3},
    {"titulo": "Loki", "genero": "Serie", "rating": 8.7, "anio": 2021, "fase": 4},
    {"titulo": "Doctor Strange en el Multiverso de la Locura", "genero": "Fantasía", "rating": 7.9, "anio": 2022, "fase": 4},
    {"titulo": "Spider-Man: No Way Home", "genero": "Acción", "rating": 8.6, "anio": 2021, "fase": 4}]
