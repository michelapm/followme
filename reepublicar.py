import datetime
import time
from pyrogram import Client
from pyrogram.enums import MessageEntityType
from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton, MessageEntity)
import requests
from decouple import config

Canal = config('Canal')
headers = {
    'accept': 'application/json',
}
api_id = config('api_id')
api_hash = config('api_hash')
bot_token = config('bot_token')
app = Client(
    "republica_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

s = requests.Session()


def obtener_user_registrado():
    r = s.get(config('base_url').replace(
        '127.0.0.1', 'djangoapi') + 'userstelegramregistrado/', headers=headers)
    return r


def obtener_ult_publicacion(client_id):
    r = s.get(config('base_url').replace(
        '127.0.0.1', 'djangoapi') + f'ultimapublicacionuser/{client_id}/', headers=headers)
    return r.json()


def obtener_plan(idplan: int):
    r = s.get(config('base_url').replace(
        '127.0.0.1', 'djangoapi') + f'planes/{idplan}/', headers=headers)
    return r.json()


def validar_tiempo_transcurrido(fecha: datetime.datetime, tiempo_evaluar: int):
    ahora = datetime.datetime.now()
    transcurrido = ahora - fecha
    tiempo_transcurrido = transcurrido.total_seconds() / 3600
    if tiempo_transcurrido >= tiempo_evaluar:
        return True
    else:
        return False


def obtener_user_red():
    user_red = s.get(config('base_url').replace(
        '127.0.0.1', 'djangoapi') + f'userredes/', headers=headers)
    return user_red.json()


def obtener_redes():
    user_red = s.get(config('base_url').replace(
        '127.0.0.1', 'djangoapi') + 'redes/', headers=headers)
    return user_red.json()


def obtener_reaccion():
    user_red = s.get(config('base_url').replace(
        '127.0.0.1', 'djangoapi') + 'reaccion/', headers=headers)
    return user_red.json()


def filter_user(user):
    if user['plan'] > 1:
        return True
    else:
        return False


def crear_publicacion(json_data):
    s.post(config('base_url').replace('127.0.0.1', 'djangoapi') + 'publicacion/', headers=headers,
           json=json_data)


def obtener_galeria_user(client_id):
    r = s.get(config('base_url').replace('127.0.0.1', 'djangoapi') + f'galeriauser/{client_id}/',
              headers=headers)
    return r.json()


def pub_auto():
    while 1:
        response = obtener_user_registrado()
        print('entro')
        if response.status_code == 200:
            listauser = filter(filter_user, response.json()['results'])
            for user in listauser:
                client_id = user['client_id']
                r = obtener_ult_publicacion(client_id)
                fecha = datetime.datetime.fromisoformat(
                    str(r['fecha_publicacion']).split('.')[0])
                plan = obtener_plan(user['plan'])
                tiempo_evaluar = plan['horas_republicacion']
                if validar_tiempo_transcurrido(fecha, tiempo_evaluar):
                    nombre = user['nombre']
                    descripcion = user['descripcion']
                    user_redes = obtener_user_red()
                    redes = obtener_redes()
                    listanew = []
                    for user_red in user_redes['results']:
                        if user_red['user'] == client_id:
                            for red in redes['results']:
                                if red['id'] == user_red['redes']:
                                    user_red['redes'] = red['nombre']
                                    listanew.append(user_red)
                    smsredes = ''
                    mensaje_base = f'📛 {nombre}\n\n📋 {descripcion}\n\n👉🏻Siganme: \n\n'
                    pos = len(mensaje_base) + 4
                    listentities = []
                    auxi = ''
                    for sms in listanew:
                        cadena = str(sms['redes'])
                        smsredes += auxi
                        smsredes += cadena
                        listentities.append(MessageEntity(type=MessageEntityType.TEXT_LINK, offset=pos,
                                                          length=len(sms['redes']) + 1, url=str(sms['username'])))
                        pos += len(cadena) + 5
                        auxi = ',   '
                    mensaje_base += smsredes
                    reacciones = obtener_reaccion()
                    auxlista = []
                    for reaccion in reacciones['results']:
                        auxlista.append(InlineKeyboardButton(  # Opens the inline interface in the current chat
                            reaccion['nombre'] + ' 0',
                            callback_data=reaccion['nombre']
                        ))
                    with app:
                        smspublicacion = app.send_photo(Canal, user['foto'],
                                                        caption=mensaje_base,
                                                        caption_entities=listentities,
                                                        reply_markup=InlineKeyboardMarkup(
                                                            [auxlista]
                                                        )
                                                        )
                        json_date = {
                            'message': smspublicacion.id,
                            'client_id': client_id,
                        }
                        crear_publicacion(json_date)
                        galeria_user = obtener_galeria_user(client_id)
                        if not galeria_user:
                            print('No hay galerias')
                        else:
                            for gal_user in galeria_user:
                                app.send_cached_media(Canal, str(gal_user['fotos_galeria']))
        else:
            print(response.status_code)
        time.sleep(120)


pub_auto()
