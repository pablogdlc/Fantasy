import itertools
import time

PRESUPUESTO = 100
CUPOS = {'POR': 1, 'DEF': 4, 'MED': 4, 'DEL': 2}

JUGADORES = [
    # (Nombre, Puesto, Precio, Puntos)[cite: 1]
    ("Ortega", "POR", 9, 5.8),
    ("Lunin", "POR", 6, 4.6),
    ("Remiro", "POR", 4, 3.9),
    ("Koundé", "DEF", 12, 6.4),
    ("Mingueza", "DEF", 7, 5.1),
    ("Vivian", "DEF", 5, 4.2),
    ("Huijsen", "DEF", 9, 5.4),
    ("Cucurella", "DEF", 11, 5.9),
    ("Lejeune", "DEF", 3, 3.1),
    ("Mosquera", "DEF", 6, 4.5),
    ("Pedri", "MED", 18, 8.1),
    ("Baena", "MED", 13, 6.9),
    ("Sučić", "MED", 8, 5.2),
    ("Barrios", "MED", 10, 5.9),
    ("Fermín", "MED", 11, 6.2),
    ("Gaya", "MED", 4, 3.3),
    ("Arambarri", "MED", 6, 4.4),
    ("Mbappé", "DEL", 24, 9.6),
    ("Budimir", "DEL", 9, 6.0),
    ("Oyarzabal", "DEL", 14, 7.2),
    ("Iglesias", "DEL", 7, 4.8),
]

def mostrar_equipo(equipo):
    """Imprime por pantalla los integrantes de un equipo de forma clara."""
    print(f"{'Nombre':<12} | {'Puesto':<6} | {'Precio (M€)':<11} | {'Puntos':<6}")
    print("-" * 45)
    for nombre, puesto, precio, puntos in equipo:
        print(f"{nombre:<12} | {puesto:<6} | {precio:<11} | {puntos:<6.1f}")

def voraz(jugadores, criterio="puntos"):
    if criterio == "puntos":
        lista = sorted(jugadores, key=lambda x: x[3], reverse=True)
    else:  # ratio
        lista = sorted(jugadores, key=lambda x: x[3] / x[2], reverse=True)
    
    conteo = {p: 0 for p in CUPOS}
    equipo = []
    coste_total = 0
    puntos_totales = 0.0

    for nombre, puesto, precio, puntos in lista:
        if conteo[puesto] < CUPOS[puesto] and (coste_total + precio) <= PRESUPUESTO:
            equipo.append((nombre, puesto, precio, puntos))
            conteo[puesto] += 1
            coste_total += precio
            puntos_totales += puntos

    completo = sum(conteo.values()) == sum(CUPOS.values())
    return equipo, coste_total, round(puntos_totales, 2), completo

def opcion_1():
    print("\n" + "="*60)
    print(" 1. ALGORITMOS VORACES (POR PUNTOS Y POR RATIO PUNTOS/PRECIO)")
    print("="*60)
    
    # Voraz por puntos
    eq_pts, c_pts, p_pts, ok_pts = voraz(JUGADORES, "puntos")
    print("\nVERSIÓN A: VORAZ POR PUNTOS")
    mostrar_equipo(eq_pts)
    print(f"Puntos totales: {p_pts} | Coste: {c_pts} M€ | ¿Once completo?: {'Sí' if ok_pts else 'No'}")
    
    # Voraz por ratio
    eq_rat, c_rat, p_rat, ok_rat = voraz(JUGADORES, "ratio")
    print("\nVERSIÓN B: VORAZ POR RATIO (PUNTOS / PRECIO)")
    mostrar_equipo(eq_rat)
    print(f"Puntos totales: {p_rat} | Coste: {c_rat} M€ | ¿Once completo?: {'Sí' if ok_rat else 'No'}")

def fuerza_bruta(jugadores):
    por_puesto = {'POR': [], 'DEF': [], 'MED': [], 'DEL': []}
    for j in jugadores:
        por_puesto[j[1]].append(j)

    comb_por = list(itertools.combinations(por_puesto['POR'], CUPOS['POR']))
    comb_def = list(itertools.combinations(por_puesto['DEF'], CUPOS['DEF']))
    comb_med = list(itertools.combinations(por_puesto['MED'], CUPOS['MED']))
    comb_del = list(itertools.combinations(por_puesto['DEL'], CUPOS['DEL']))

    total_equipos_validos = 0
    mejor_equipo = None
    max_puntos = -1.0
    coste_optimo = 0

    for p in comb_por:
        for d in comb_def:
            for m in comb_med:
                for del_ in comb_del:
                    equipo = p + d + m + del_
                    coste = sum(j[2] for j in equipo)
                    if coste <= PRESUPUESTO:
                        total_equipos_validos += 1
                        pts = sum(j[3] for j in equipo)
                        if pts > max_puntos:
                            max_puntos = pts
                            mejor_equipo = equipo
                            coste_optimo = coste

    return mejor_equipo, coste_optimo, round(max_puntos, 2), total_equipos_validos

def opcion_2():
    print("\n" + "="*60)
    print(" 2. FUERZA BRUTA (EVALUACIÓN EXHAUSTIVA DE COMBINACIONES)")
    print("="*60)
    
    t0 = time.perf_counter()
    eq_fb, c_fb, p_fb, n_comb = fuerza_bruta(JUGADORES)
    t_fb = time.perf_counter() - t0
    
    print(f"\nNúmero total de combinaciones válidas que cumplen presupuesto: {n_comb}")
    print(f"Tiempo de ejecución: {t_fb:.5f} segundos")
    print(f"\nEQUIPO ÓPTIMO (REFERENCIA FUERZA BRUTA)")
    mostrar_equipo(eq_fb)
    print(f"Puntos Totales Óptimos: {p_fb} | Coste Total: {c_fb} M€")

def menu_principal():
    while True:
        
        print("FANTASY")
        print("1. Algoritmos Voraces)")
        print("2. Fuerza Bruta")
        print("0. Salir")
        
        opcion = input("Seleccione una opción (0-2): ").strip()
        
        if opcion == "1":
            opcion_1()
        elif opcion == "2":
            opcion_2()
        elif opcion == "0":
            break
        else:
            print("\n[ERROR] Opción no válida. Por favor, introduzca 0, 1 o 2.")

# Llamada directa al menú al ejecutar el archivo
menu_principal()