def split_course_division(input_string):
    """
    Toma una cadena en el formato '7°4' y separa el Curso y la División.

    Args:
        input_string (str): La cadena a procesar.

    Returns:
        tuple: Una tupla con el Curso y la División como enteros.
    """
    try:
        curso, division = input_string.split('°')
        return int(curso), int(division)
    except ValueError:
        raise ValueError("El formato de la cadena debe ser 'X°Y', donde X y Y son números.")