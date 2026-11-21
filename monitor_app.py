"""Aplicación de monitorización de una app de descargas y caídas."""

import sys
from typing import Final
import logging

# Añadid aquí las importaciones que necesitéis.

# ---------------------------------------------------------------------------
# Datos de la aplicación. Sustituid los del ejemplo APP-00 por los vuestros.
# ---------------------------------------------------------------------------
CODIGO: Final[str] = "APP-06"
NOMBRE: Final[str] = "Agenda Escolar"
# Una posición por semana, de la 1 a la 12. 0 descargas: app retirada.
DESCARGAS: Final = [1_200, 1_350, 1_280, 1_500, 0, 1_720,
                    2_050, 1_810, 1_980, 2_310, 2_200, 2_150]
CAIDAS: Final = [14, 12, 15, 9, 0, 22,
                 31, 8, 6, 9, 5, 4]

# ---------------------------------------------------------------------------
# Datos del programa. Solo hay que cambiar AUTORES.
# ---------------------------------------------------------------------------
VERSION_PROGRAMA: Final[str] = "1.0.0"
AUTORES: Final[str] = "Carlos Buitrago Alcaraz · Luciano Gómez Gálvez · José Antonio Collado López"
PENDIENTE: Final[str] = "  (opción pendiente de implementar)"

# ---------------------------------------------------------------------------
# Constantes comunes.
# ---------------------------------------------------------------------------
ANCHO: Final[int] = 44
POR_MIL: Final[int] = 1_000
UMBRAL_ESTABLE: Final[float] = 5.0       # caídas por cada mil descargas
UMBRAL_ACEPTABLE: Final[float] = 10.0
UMBRAL_REVISAR: Final[float] = 15.0
OPCION_SALIR: Final[int] = 9

# ---------------------------------------------------------------------------
# Constantes de la pareja. Todo valor fijo del programa va aquí, con nombre.
# ---------------------------------------------------------------------------

UMBRAL_BUSQUEDA_MIN: Final[float] = 0.0
UMBRAL_BUSQUEDA_MAX: Final[float] = 1_000.0
OBJETIVO_DESCARGAS_MAX: Final[int] = 1_000_000
CRECIMIENTO_MIN: Final[float] = 0.5
CRECIMIENTO_MAX: Final[float] = 50.0
MAX_SEMANAS_PREVISION: Final[int] = 104
POR_CIENTO: Final[int] = 100

# ---------------------------------------------------------------------------
# Excepciones propias de la pareja. Aquí va SemanaNoValida (opción 7).
# ---------------------------------------------------------------------------

class SemanaNoValida(Exception):
    """Error cuando la semana no es válida."""
    pass



# ---------------------------------------------------------------------------
# Funciones auxiliares. tasa_caidas viene hecha; el resto, con su docstring,
# las completáis vosotros. No cambiéis sus cabeceras.
# ---------------------------------------------------------------------------
def tasa_caidas(descargas: int, caidas: int) -> float:
    """Devuelve las caídas por cada mil descargas.

    Lanza ZeroDivisionError si la semana no tiene descargas.
    """


    if descargas == 0:
        raise ZeroDivisionError("Esta semana no tiene descargas")

    return caidas / descargas * POR_MIL









def estado(descargas: int, caidas: int) -> str:
    """Devuelve el estado de una semana según su tasa de caídas.

    Es uno de estos textos: "Estable", "Aceptable", "Revisar", "Crítica" o
    "Mantenimiento", este último si la semana no tiene descargas.
    """

    if descargas == 0:
        return "Mantenimiento"

    tasa = tasa_caidas(descargas,caidas)

    if tasa < UMBRAL_ESTABLE:
        return "Estable"
    elif tasa < UMBRAL_ACEPTABLE:
        return "Aceptable"
    elif tasa < UMBRAL_REVISAR:
        return "Revisar"
    else:
        return "Crítica"



def pedir_entero(mensaje: str, minimo: int, maximo: int) -> int:
    """Pide un entero entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un entero o está fuera de rango, avisa y
    lo vuelve a pedir.
    """

    while True:
        try:
            numero = int(input(mensaje))

            if minimo <= numero <= maximo:
                return numero
            else:
                print(f"introduce un numero entre {minimo} y {maximo}: ")



        except ValueError:
            print("Tienes que introducir un numero entero.")





def pedir_real(mensaje: str, minimo: float, maximo: float) -> float:
    """Pide un número real entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un número o está fuera de rango, avisa y
    lo vuelve a pedir.
    """



    while True:
        try:
            numero = float(input(mensaje))
            if minimo <= numero <= maximo:
                return numero
            else:
                print(f"introduce un numero entre {minimo} y {maximo}: ")


        except ValueError:
            print("Tienes que introducir un numero entero")


def semana_valida(texto: str) -> int:
    """Convierte el texto en un número de semana de los datos.

    Lanza SemanaNoValida si no es un entero o está fuera de rango.
    """

    try:
        semana = int(texto)
    except ValueError:
        raise SemanaNoValida(f"«{texto}» no es un número de semana")

    if semana < 1 or semana > len(DESCARGAS):
        raise SemanaNoValida(f"la semana {semana} no existe: "f"hay de 1 a {len(DESCARGAS)}")

    return semana


def comprobar_datos() -> int:
    """Revisa los datos semanales y devuelve el número de errores.

    Registra cada error con logging.error y cada semana de mantenimiento
    con logging.warning.
    """
    errores = 0

    if len(DESCARGAS) != len(CAIDAS):
        logging.error("Listas diferentes")
        errores += 1

    semana = 1

    for descargas, caidas in zip(DESCARGAS, CAIDAS):
        if descargas < 0:
            logging.error("descargas negativas")
            errores += 1

        if caidas < 0:
            logging.error("Caidas negativas")
            errores += 1

        if caidas > descargas:
            logging.error("Demasiadas caidas")
            errores += 1

        if descargas == 0:
            logging.warning(f"semana {semana}: mantenimiento")

        semana += 1

    return errores


# ---------------------------------------------------------------------------
# Menú y opciones. La opción 1 viene hecha y la 2 tiene dos errores.
# ---------------------------------------------------------------------------
def mostrar_menu() -> None:
    """Se muestra el menú de opciones y se pide la opción elegida."""
    linea = "=" * ANCHO
    print(f"\n{linea}")
    print(linea)
    print("1. Listado semanal")
    print("2. Resumen")
    print("3. Estabilidad por semana")
    print("4. Primera semana que alcanza un umbral")
    print("5. Mejor racha sin problemas")
    print("6. Previsión de crecimiento")
    print("7. Consultar una semana")
    print("8. Comprobar los datos")
    print(f"{OPCION_SALIR}. Salir")

def opcion_1_listado() -> None:
    """Muestra las descargas, las caídas y la tasa de cada semana."""
    print(f"{'Semana':>6}{'Descargas':>11}{'Caídas':>8}{'Tasa ‰':>9}")
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        try:
            tasa = f"{tasa_caidas(descargas, caidas):.1f}"
        except ZeroDivisionError:
            tasa = "—"
        print(f"{semana:>6}{descargas:>11}{caidas:>8}{tasa:>9}")


def opcion_2_resumen() -> None:
    """Muestra los totales, la media y las semanas extremas."""
    total_descargas = 0
    total_caidas = 0
    activas = 0
    mas = 0
    semana_mas = 0
    menos = 0
    semana_menos = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        activas += 1
        total_descargas += descargas
        total_caidas += caidas
        if descargas > mas:
            mas = descargas
            semana_mas = semana ## Primer error corregido.
        if semana_menos == 0 or descargas < menos: ## Segundo error corregido.
            menos = descargas
            semana_menos = semana
    media = total_descargas / activas
    tasa = tasa_caidas(total_descargas, total_caidas)
    print(f"Semanas activas:     {activas} de {len(DESCARGAS)}")
    print(f"Total de descargas:  {total_descargas}")
    print(f"Media semanal:       {media:.1f}")
    print(f"Más descargas:       semana {semana_mas} ({mas})")
    print(f"Menos descargas:     semana {semana_menos} ({menos})")
    print(f"Total de caídas:     {total_caidas}")
    print(f"Tasa global:         {tasa:.1f} ‰")


def opcion_3_estabilidad() -> None:
    """Muestra el estado de cada semana y cuenta las de cada tipo."""

    estables = 0
    aceptables = 0
    revisar = 0
    criticas = 0
    mantenimiento = 0


    for semana, (descargas, caidas) in enumerate(
        zip(DESCARGAS, CAIDAS), start=1
    ):
        estado_semana = estado(descargas, caidas)
        print(f"Semana {semana}: {estado_semana}")

        match estado_semana:
            case "Estable":
                estables += 1
            case "Aceptable":
                aceptables += 1
            case "Revisar":
                revisar += 1
            case "Crítica":
                criticas += 1
            case "Mantenimiento":
                mantenimiento += 1


    print("-" * ANCHO)
    print(f"Estables: {estables} · Aceptables: {aceptables} · Revisar: {revisar}")
    print(f"Criticas: {criticas} · Mantenimiento: {mantenimiento}")


def opcion_4_umbral() -> None:
    """Busca la primera semana activa que alcanza el umbral indicado. """
    umbral = pedir_real(
        "Umbral en caídas por mil: ",
        UMBRAL_BUSQUEDA_MIN,
        UMBRAL_BUSQUEDA_MAX,
    )

    for semana, (descargas, caidas) in enumerate(
        zip(DESCARGAS, CAIDAS), start=1
    ):
        if descargas == 0:
            continue

        tasa = tasa_caidas(descargas, caidas)
        if tasa >= umbral:
            print(f"Primera semana: {semana} ({tasa} ‰)")
            break

    else:
        print(f"Ninguna semana alcanza {umbral} ‰")



def opcion_5_racha() -> None:
    """Muestra la racha más larga de semanas en estado Estable o Aceptable."""
    mejor_racha = 0
    inicio_mejor = 0
    racha_actual = 0
    inicio_actual = 0

    for semana, (descargas, caidas) in enumerate(
        zip(DESCARGAS, CAIDAS), start=1
    ):
        estado_semana = estado(descargas, caidas)

        if estado_semana == "Mantenimiento":
            continue

        if estado_semana in ("Estable", "Aceptable"):
            if racha_actual == 0:
                inicio_actual = semana
            racha_actual += 1
            if racha_actual > mejor_racha:
                mejor_racha = racha_actual
                inicio_mejor = inicio_actual
        else:
            racha_actual = 0

    if mejor_racha == 0:
        print("No hay ninguna semana en estado Estable o Aceptable.")
    else:
        etiqueta = "semana" if mejor_racha == 1 else "semanas"
        print(
            f"Mejor racha: {mejor_racha} {etiqueta}, "
            f"desde la semana {inicio_mejor}."
            )


def opcion_6_prevision() -> None:
    """Calcula en cuántas semanas se alcanza un objetivo de descargas"""
    ultima_activa = 0
    for descargas in DESCARGAS:
        if descargas > 0:
            ultima_activa = descargas

    if ultima_activa == 0:
        print("No hay ninguna semana activa para calcular la previsión.")
        return

    print(f"Descargas de la última semana activa: {ultima_activa}")

    objetivo = pedir_entero(
        "Objetivo semanal de descargas: ",
        ultima_activa + 1,
        OBJETIVO_DESCARGAS_MAX,
    )

    crecimiento = pedir_real(
        "Crecimiento semanal en %: ",
        CRECIMIENTO_MIN,
        CRECIMIENTO_MAX,
    )

    factor_crecimiento = 1 + crecimiento / POR_CIENTO
    descargas_estimadas = float(ultima_activa)
    semanas = 0

    while descargas_estimadas < objetivo:
        if semanas == MAX_SEMANAS_PREVISION:
            print(
                f"No se alcanza el objetivo en {MAX_SEMANAS_PREVISION} "
                f"semanas ({descargas_estimadas:.0f} descargas)."
            )
            break
        descargas_estimadas *= factor_crecimiento
        semanas += 1
    else:
        etiqueta = "semana" if semanas == 1 else "semanas"
        print(
            f"Se alcanza el objetivo en {semanas} {etiqueta} "
            f"({descargas_estimadas:.0f} descargas)."
        )


def opcion_7_consulta() -> None:
    """Selecciona una semana y se muestra su estado y la acción recomendada."""


    texto = input("Semana (1-12): ")

    try:
        semana = semana_valida(texto)
    except SemanaNoValida as error:
        print(f"No se puede consultar: {error}")
        return

    for numero, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):

        if numero == semana:
            estado_semana = estado(descargas, caidas)

            match estado_semana:
                case "Estable":
                    accion = "Sin acciones"
                case "Aceptable":
                    accion = "Vigilar en la próxima versión"
                case "Revisar":
                    accion = "Revisar los informes de errores"
                case "Crítica":
                    accion = "Publicar una versión correctora urgente"
                case "Mantenimiento":
                    accion = "La app no estuvo publicada esa semana"

            print(f"Descargas: {descargas}")
            print(f"Caídas: {caidas}")
            print(f"Estado: {estado_semana}")
            print(f"Acción: {accion}")
            break


def opcion_8_comprobar() -> None:
    """Avisa si los datos semanales tienen errores y cuántos."""

    errores = comprobar_datos()

    if errores == 0:
        print(f"Datos correctos: {len(DESCARGAS)} semanas")
    else:
        print(f"Los datos tienen {errores} errores.")


def main() -> None:
    """Configura el registro, valida los datos y ejecuta el menú principal."""
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s"
    )

    if comprobar_datos() > 0:
        sys.exit("Los datos semanales tienen errores: corrígelos antes de continuar.")

    print(f"Monitor de estabilidad {VERSION_PROGRAMA})")

    try:
        while True:
            mostrar_menu()
            entrada = input("Opción: ").strip()

            try:
                opcion = int(entrada)
            except ValueError:
                print(f"«{entrada}» no es una de opción")
                continue

            match opcion:
                case 1:
                    opcion_1_listado()
                case 2:
                    opcion_2_resumen()
                case 3:
                    opcion_3_estabilidad()
                case 4:
                    opcion_4_umbral()
                case 5:
                    opcion_5_racha()
                case 6:
                    opcion_6_prevision()
                case 7:
                    opcion_7_consulta()
                case 8:
                    opcion_8_comprobar()
                case 9:
                    respuesta = input("¿Seguro que quieres salir? (s/n): ").strip().lower()
                    if respuesta.lower() == "s":
                        break
                case _:
                    print(
                        f"Elige una opción entre 1 y 9."
                    )
    except KeyboardInterrupt:
        print("\nPrograma interrumpido.")

    print(f"Fin del monitor de {CODIGO}")


if __name__ == "__main__":
    main()
