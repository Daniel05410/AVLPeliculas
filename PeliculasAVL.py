import csv
import plotly.graph_objects as go
import networkx as nx

# Definición de la clase para los nodos del árbol AVL
class NodoAVL:
    def __init__(self, title, worldwide_earnings, domestic_earnings, domestic_percent, foreign_earnings, foreign_percent, year):
        self.title = title
        self.worldwide_earnings = worldwide_earnings
        self.domestic_earnings = domestic_earnings
        self.domestic_percent = domestic_percent
        self.foreign_earnings = foreign_earnings
        self.foreign_percent = foreign_percent
        self.year = year
        self.izquierdo = None
        self.derecho = None
        self.altura = 1

# Funciones auxiliares para manejar el árbol AVL

"Obtener la altura de un nodo dado."
def obtener_altura(nodo):
    if nodo is None:
        return 0
    return nodo.altura

"Obtener el factor de balance de un nodo"
def obtener_balance(nodo):
    if nodo is None:
        return 0
    return obtener_altura(nodo.izquierdo) - obtener_altura(nodo.derecho)

"Realizar rotación a la derecha"
def rotacion_derecha(y):
    x = y.izquierdo
    T2 = x.derecho

    x.derecho = y
    y.izquierdo = T2

    y.altura = max(obtener_altura(y.izquierdo), obtener_altura(y.derecho)) + 1
    x.altura = max(obtener_altura(x.izquierdo), obtener_altura(x.derecho)) + 1

    return x

"Realizar rotacion a la izquierda"
def rotacion_izquierda(x):
    y = x.derecho
    T2 = y.izquierdo

    y.izquierdo = x
    x.derecho = T2

    x.altura = max(obtener_altura(x.izquierdo), obtener_altura(x.derecho)) + 1
    y.altura = max(obtener_altura(y.izquierdo), obtener_altura(y.derecho)) + 1

    return y

"Insertar un nuevo nodo en el arbol"
def insertar_avl(raiz, title, worldwide_earnings, domestic_earnings, domestic_percent, foreign_earnings, foreign_percent, year):
    if raiz is None:
        return NodoAVL(title, worldwide_earnings, domestic_earnings, domestic_percent, foreign_earnings, foreign_percent, year)

    if title < raiz.title:
        raiz.izquierdo = insertar_avl(raiz.izquierdo, title, worldwide_earnings, domestic_earnings, domestic_percent, foreign_earnings, foreign_percent, year)
    elif title > raiz.title:
        raiz.derecho = insertar_avl(raiz.derecho, title, worldwide_earnings, domestic_earnings, domestic_percent, foreign_earnings, foreign_percent, year)
    else:
        return raiz
    
    "Actualizar altura"
    raiz.altura = 1 + max(obtener_altura(raiz.izquierdo), obtener_altura(raiz.derecho))
    
    "Obtener factor de balanceo"
    balance = obtener_balance(raiz)

    "Balancear el árbol tras la inserción"
    if balance > 1 and title < raiz.izquierdo.title:
        return rotacion_derecha(raiz)
    if balance < -1 and title > raiz.derecho.title:
        return rotacion_izquierda(raiz)
    if balance > 1 and title > raiz.izquierdo.title:
        raiz.izquierdo = rotacion_izquierda(raiz.izquierdo)
        return rotacion_derecha(raiz)
    if balance < -1 and title < raiz.derecho.title:
        raiz.derecho = rotacion_derecha(raiz.derecho)
        return rotacion_izquierda(raiz)

    return raiz

"Eliminación de un nodo"
def eliminar_avl(raiz, title):
    if raiz is None:
        return raiz

    if title < raiz.title:
        raiz.izquierdo = eliminar_avl(raiz.izquierdo, title)
    elif title > raiz.title:
        raiz.derecho = eliminar_avl(raiz.derecho, title)
    else:
        "Nodo con un solo hijo o sin hijos"
        if raiz.izquierdo is None:
            temp = raiz.derecho
            raiz = None
            return temp        
        elif raiz.derecho is None:
            temp = raiz.izquierdo
            raiz = None
            return temp

        "Nodo con dos hijos"
        temp = nodo_minimo(raiz.derecho)
        raiz.title = temp.title
        raiz.derecho = eliminar_avl(raiz.derecho, temp.title)

    if raiz is None:
        return raiz

    "Actualizar altura"
    raiz.altura = 1 + max(obtener_altura(raiz.izquierdo), obtener_altura(raiz.derecho))
    
    "Obtener factor de balanceo"
    balance = obtener_balance(raiz)

    "Balanceo tras eliminación"
    if balance > 1 and obtener_balance(raiz.izquierdo) >= 0:
        return rotacion_derecha(raiz)
    if balance > 1 and obtener_balance(raiz.izquierdo) < 0:
        raiz.izquierdo = rotacion_izquierda(raiz.izquierdo)
        return rotacion_derecha(raiz)
    if balance < -1 and obtener_balance(raiz.derecho) <= 0:
        return rotacion_izquierda(raiz)
    if balance < -1 and obtener_balance(raiz.derecho) > 0:
        raiz.derecho = rotacion_derecha(raiz.derecho)
        return rotacion_izquierda(raiz)

    return raiz

"Encuentra el nodo con el valor mínimo en el árbol AVL."
def nodo_minimo(nodo):
    if nodo is None or nodo.izquierdo is None:
        return nodo
    return nodo_minimo(nodo.izquierdo)

"Buscar un nodo por titulo de pelicula"
def buscar(nodo, nombre):
    if nodo is None or nodo.title == nombre:
        return nodo

    if nombre < nodo.title:
        return buscar(nodo.izquierdo, nombre)

    return buscar(nodo.derecho, nombre)

"Buscar un nodo dado el año de estreno y una cantidad de ingresos minima"
def buscar_por_criterios(nodo, year=None, foreign_earnings_min=None):
    resultados = []

    def _buscar(n):
        if n is None:
            return
        if year is not None and n.year == year:
            if n.domestic_percent < n.foreign_percent and n.foreign_earnings >= foreign_earnings_min:
                resultados.append(n)
        _buscar(n.izquierdo)
        _buscar(n.derecho)

    _buscar(nodo)
    return resultados

"Hacer el recorrido por niveles del árbol"
def recorrido_por_niveles(nodo):
    if nodo is None:
        print("El árbol está vacío.")
        return

    niveles = []
    def _recorrido(n, nivel):
        if n is None:
            return
        if len(niveles) <= nivel:
            niveles.append([])
        niveles[nivel].append(n.title)
        _recorrido(n.izquierdo, nivel + 1)
        _recorrido(n.derecho, nivel + 1)
    
    _recorrido(nodo, 0)
    for i, nivel in enumerate(niveles):
        print(f"Nivel {i}: " + " -> ".join(nivel))

"Obtener el nivel de un nodo"
def obtener_nivel(raiz, nodo):
    def _buscar_nivel(n, actual, nivel):
        if n is None:
            return -1
        if n == actual:
            return nivel
        izq = _buscar_nivel(n.izquierdo, actual, nivel + 1)
        if izq != -1:
            return izq
        return _buscar_nivel(n.derecho, actual, nivel + 1)

    return _buscar_nivel(raiz, nodo, 0)

"Encontrar el padre de un nodo"
def encontrar_padre(raiz, nodo):
    def _buscar_padre(n, hijo):
        if n is None or n.izquierdo == hijo or n.derecho == hijo:
            return n
        if hijo.title < n.title:
            return _buscar_padre(n.izquierdo, hijo)
        else:
            return _buscar_padre(n.derecho, hijo)

    return _buscar_padre(raiz, nodo)

"Encontrar el abuelo de un nodo"
def encontrar_abuelo(raiz, nodo):
    padre = encontrar_padre(raiz, nodo)
    if padre is None:
        return None
    return encontrar_padre(raiz, padre)

"Encontrar el tio de un nodo"
def encontrar_tio(raiz, nodo):
    padre = encontrar_padre(raiz, nodo)
    abuelo = encontrar_abuelo(raiz, nodo)
    if abuelo is None:
        return None
    if abuelo.izquierdo == padre:
        return abuelo.derecho
    else:
        return abuelo.izquierdo

"Construir el árbol a partir del dataset"
def construir_arbol_desde_csv(archivo_csv):
    raiz = None
    with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for fila in reader:
            title = fila['Title']
            worldwide_earnings = int(fila['Worldwide Earnings'])
            domestic_earnings = int(fila['Domestic Earnings'])
            domestic_percent = float(fila['Domestic Percent Earnings'])
            foreign_earnings = int(fila['Foreign Earnings'])
            foreign_percent = float(fila['Foreign Percent Earnings'])
            year = int(fila['Year'])
            raiz = insertar_avl(raiz, title, worldwide_earnings, domestic_earnings, domestic_percent, foreign_earnings, foreign_percent, year)
    return raiz

"Exportar el arbol a .gexf para poder ser visuaizado"
def exportar_a_gexf(raiz, archivo_salida):
    G = nx.DiGraph()

    def _agregar_nodos_edges(nodo):
        if nodo is not None:
            G.add_node(nodo.title, 
                       worldwide_earnings=nodo.worldwide_earnings,
                       domestic_earnings=nodo.domestic_earnings,
                       domestic_percent=nodo.domestic_percent,
                       foreign_earnings=nodo.foreign_earnings,
                       foreign_percent=nodo.foreign_percent,
                       year=nodo.year)
            if nodo.izquierdo:
                G.add_edge(nodo.title, nodo.izquierdo.title)
                _agregar_nodos_edges(nodo.izquierdo)
            if nodo.derecho:
                G.add_edge(nodo.title, nodo.derecho.title)
                _agregar_nodos_edges(nodo.derecho)
    
    _agregar_nodos_edges(raiz)
    nx.write_gexf(G, archivo_salida)

"Funciones del menú principal"
def accion(op, estado, raiz, nodo_seleccionado):
    match op:
        case 1:
            print('Va a ingresar una nueva película.')
            titulo = str(input('Ingrese el nombre de la película: '))
            year = int(input('Ingrese año de estreno de la película: '))
            worldwide_earnings = int(input('Ingresos en taquilla a nivel mundial: '))
            domestic_earnings = int(input('Ingresos en taquilla a nivel nacional: '))
            foreign_earnings = int(input('Ingresos en taquilla a nivel internacional: '))
            domestic_percent_earnings = float((domestic_earnings/worldwide_earnings)*100)
            foreign_percent_earnings = float((foreign_earnings/worldwide_earnings)*100)
            raiz = insertar_avl(raiz, titulo, worldwide_earnings, domestic_earnings, domestic_percent_earnings, foreign_earnings, foreign_percent_earnings, year)
            print('Se insertó correctamente.')
            exportar_a_gexf(raiz, 'arbol.gexf')
            return estado, raiz, nodo_seleccionado
        case 2:
            nombre = str(input('Ingrese el nombre de la película que desea eliminar: '))
            raiz = eliminar_avl(raiz, nombre)
            exportar_a_gexf(raiz, 'arbol.gexf')
            print('Se eliminó correctamente.')
            return estado, raiz, nodo_seleccionado
        case 3:
            name = str(input('Ingrese el nombre de la película que desea buscar: '))
            resultado_busqueda = buscar(raiz, name)
            if resultado_busqueda:
                print(f"\nNodo encontrado: {resultado_busqueda.title}")
                print(f"Worldwide Earnings: {resultado_busqueda.worldwide_earnings}")
                print(f"Domestic Earnings: {resultado_busqueda.domestic_earnings}")
                print(f"Domestic Percent: {resultado_busqueda.domestic_percent}")
                print(f"Foreign Earnings: {resultado_busqueda.foreign_earnings}")
                print(f"Foreign Percent: {resultado_busqueda.foreign_percent}")
                print(f"Year: {resultado_busqueda.year}")
                nodo_seleccionado = resultado_busqueda
            else:
                print("\nPelícula no encontrada.")
            return estado, raiz, nodo_seleccionado
        case 4:
            estreno = int(input('Ingrese el año de estreno de la película: '))
            earnings = int(input('Ingresos a nivel internacional mayores o iguales a: '))
            resultados = buscar_por_criterios(raiz, estreno, earnings)
            print('Películas que cumplen los criterios:')
            for nodo in resultados:
                print(nodo.title)
            # Seleccionar un nodo de los resultados
            if resultados:
                titulo_seleccionado = str(input('Ingrese el título de la película para realizar operaciones adicionales: '))
                nodo_seleccionado = next((n for n in resultados if n.title == titulo_seleccionado), None)
                if nodo_seleccionado:
                    print(f"\nNodo seleccionado: {nodo_seleccionado.title}")
                else:
                    print('Título no encontrado en los resultados.')
                    nodo_seleccionado = None
            else:
                nodo_seleccionado = None
            return estado, raiz, nodo_seleccionado
        case 5:
            print("\nRecorrido por niveles del árbol (solo nombres):")
            recorrido_por_niveles(raiz)
            return estado, raiz, nodo_seleccionado
        case 6:
            if nodo_seleccionado is not None:
                print(f"\nOperaciones con el nodo seleccionado: {nodo_seleccionado.title}")
                print(f"Nivel del nodo: {obtener_nivel(raiz, nodo_seleccionado)}")
                print(f"Factor de balanceo del nodo: {obtener_balance(nodo_seleccionado)}")
                padre = encontrar_padre(raiz, nodo_seleccionado)
                if padre:
                    print(f"Padre del nodo: {padre.title}")
                else:
                    print("El nodo no tiene padre.")
                abuelo = encontrar_abuelo(raiz, nodo_seleccionado)
                if abuelo:
                    print(f"Abuelo del nodo: {abuelo.title}")
                else:
                    print("El nodo no tiene abuelo.")
                tio = encontrar_tio(raiz, nodo_seleccionado)
                if tio:
                    print(f"Tío del nodo: {tio.title}")
                else:
                    print("El nodo no tiene tío.")
            else:
                print("No hay nodo seleccionado para realizar operaciones.")
            return estado, raiz, nodo_seleccionado
        case 7:
            estado = 0
            return estado, raiz, nodo_seleccionado
        case _:
            print('Opción inválida.')
            return estado, raiz, nodo_seleccionado

# Inicialización del árbol AVL
raiz = construir_arbol_desde_csv('dataset_movies.csv')
nodo_seleccionado = None

# Menú principal
estado = 1
while estado == 1:
    print('Películas:')
    print('1. Insertar película.')
    print('2. Eliminar una película.')
    print('3. Buscar una película.')
    print('4. Buscar varias películas por año e ingresos a nivel internacional.')
    print('5. Recorrer el árbol por niveles.')
    print('6. Realizar operaciones sobre el nodo seleccionado.')
    print('7. Salir')
    opcion = int(input('Ingrese la acción que desea realizar: '))
    estado, raiz, nodo_seleccionado = accion(opcion, estado, raiz, nodo_seleccionado)