import random

from django.shortcuts import HttpResponse

# Lista de hechos de Chuck Norris
FACTS_LIST = [
    {
        'id': 1,
        'fact': 'Chuck Norris contó hasta el infinito. Dos veces.'
    },
    {
        'id': 2,
        'fact': 'Chuck Norris puede dividir por cero.'
    },
    {
        'id': 3,
        'fact': 'Chuck Norris puede reproducir un CD en un tocadiscos.'
    },
    {
        'id': 4,
        'fact': 'Las lágrimas de Chuck Norris curan el cáncer. Lástima que jamás haya llorado.'
    },
    {
        'id': 5,
        'fact': 'Chuck Norris dona sangre a menudo. Pero rara vez es la suya.'
    }
]


def home_view(request):
    # Creamos la tabla de hechos
    facts_table = '<ul>'
    for fact in FACTS_LIST:
        facts_table += f'<li><a href="/facts/{fact["id"]}">Hecho {fact["id"]}</a></li>'
    facts_table += '</ul>'
    # Creamos el contenido de la respuesta
    content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chuck Norris</title>
    </head>
    <body>
        <p>Hechos de Chuck Norris</p>
        <blockquote>{facts_table}</blockquote>
    </body>
    </html>
    '''
    # Creamos la respuesta
    return HttpResponse(content)


def fact_view(request, fact_id):
    try:
        # Seleccionamos un hecho específico
        current_fact = next(
            (fact['fact'] for fact in FACTS_LIST if fact['id'] == fact_id))
        # Creamos el contenido de la respuesta
        content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chuck Norris</title>
        </head>
        <body>
            <p>Este es un hecho de Chuck Norris con ID {fact_id}</p>
            <blockquote>{current_fact}</blockquote>
        </body>
        </html>
        '''
        # Creamos la respuesta
        return HttpResponse(content)
    except StopIteration:
        # En caso de que el ID no exista, se genera la excepción StopIteration,
        # la cual gestionamos con el siguiente código
        content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chuck Norris</title>
        </head>
        <body>
            <p>El hecho con ID {fact_id} no existe</p>
        </body>
        </html>
        '''
        # Creamos la respuesta
        return HttpResponse(content, status=404)


def random_view(request):
    # Seleccionamos un hecho aleatorio
    current_fact = random.choice(FACTS_LIST)
    # Creamos el contenido de la respuesta
    content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chuck Norris</title>
    </head>
    <body>
        <p>Este es un hecho aleatorio de Chuck Norris</p>
        <blockquote>{current_fact['fact']}</blockquote>
    </body>
    </html>
    '''
    # Creamos la respuesta
    return HttpResponse(content)
