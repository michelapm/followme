import asyncio
import datetime
import os

import requests


async def validar_vacio(v: str):
    await asyncio.sleep(0.0001)
    if v == '' or v == ' ':
        raise Exception('Recuerde que no puede haber campos vacios')


async def validar_numero(num: str):
    await validar_vacio(num)
    await asyncio.sleep(0.0001)
    chars = ['0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9']
    for n in num:
        if n in chars:
            continue
        else:
            raise Exception('Recuerde que hay campos que solo aceptan numeros')


async def validar_ref(ref: str, client_id: int):
    await asyncio.sleep(0.0001)
    chars = ['0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9']
    for n in ref:
        if n in chars:
            continue
        else:
            raise Exception('El enlace de referido no es correcto')
    if client_id == int(ref):
        raise Exception('Recuerde que no se puede referir a si mismo')


async def validar_nombre(nombre: str):
    await asyncio.sleep(0.0001)
    if len(nombre) < 3:
        raise Exception('El nombre debe tener al menos 3 caracteres')
    elif len(nombre) > 50:
        raise Exception('El nombre debe tener menos de 50 caracteres')
    elif nombre.isdigit():
        raise Exception('El nombre no puede estar compuesto por numeros')


async def validar_descripcion(descripcion: str):
    await asyncio.sleep(0.0001)
    chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
             'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
             'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'á', 'é', 'í', 'ó', 'ú', 'ñ', ' ']
    if len(descripcion) < 20:
        raise Exception('Su descripcion debe tener al menos 20 caracteres para ser valida, reintente ponerla de nuevo')
    for n in descripcion:
        if n in chars:
            continue
        else:
            print(n)
            raise Exception('Su descripcion no puede contener caracteres especiales')


async def validar_url(url: str, validar: str):
    await asyncio.sleep(0.0001)
    if url.find(validar) == -1:
        raise Exception('El enlace de su red social esta escrito incorrectamente, reintente ponerlo de nuevo')


async def error(client, client_id, msg):
    prueba = await client.send_message(client_id, msg)
    await asyncio.sleep(5)
    await client.delete_messages(client_id, prueba.id)


async def validar_tiempo_transcurrido(fecha: datetime.datetime, tiempo_evaluar: int, plan: int):
    await asyncio.sleep(0.0001)
    ahora = datetime.datetime.now()
    transcurrido = ahora - fecha
    tiempo_transcurrido = transcurrido.total_seconds() / 3600
    if tiempo_transcurrido <= tiempo_evaluar:
        if plan > 1:
            raise Exception(f'El bot se encarga de publicar sus anuncios cada {round(tiempo_evaluar)} horas '
                            f'automaticamente')
        raise Exception(f'El tiempo debe ser mayor a {round(tiempo_evaluar)} horas para publicar, reintente '
                        f'mas tarde')


# async def validar_tiempo_galeria(fecha: datetime.datetime):
#     await asyncio.sleep(0.0001)
#     ahora = datetime.datetime.now()
#     transcurrido = ahora - fecha
#     tiempo_transcurrido = transcurrido.total_seconds() / 3600
#     if tiempo_transcurrido <= 720:
#         raise Exception(f'El tiempo debe ser mayor a un mes')


def validator_img(foto):
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        files={
            'image': open(foto, 'rb'),
        },
        headers={'api-key': '305864f2-484b-4603-b156-e389af14c05f'}
    )
    print(r.json())
    try:
        os.remove(foto)
    except:
        print('No se pudo eliminar la foto')
    if r.json()['output']['nsfw_score'] > 0.65:
        raise Exception('No puede subir imagenes con partes intimas desnudas')
