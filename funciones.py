import aiohttp
from decouple import config

headers = {
    'accept': 'application/json',
}


async def obtener_user(client_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(config('base_url').replace('127.0.0.1', 'djangoapi') + f'userstelegram/{client_id}/',
                               headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json, response.status
            else:
                return {'estado': False}, response.status


async def crear_user(client_id: int, referido: int = None):
    async with aiohttp.ClientSession() as session:
        json_data = {
            'client_id': client_id,
            'referido': referido,
        }
        async with session.post(config('base_url').replace('127.0.0.1', 'djangoapi') + 'userstelegram/',
                                headers=headers, json=json_data) as response:
            if response.status == 201:
                json = await response.json()
                return json


async def update_user(json_data):
    async with aiohttp.ClientSession() as session:
        id_client = json_data['client_id']
        async with session.put(config('base_url').replace('127.0.0.1', 'djangoapi') + f'userstelegram/{id_client}/',
                               headers=headers,
                               json=json_data) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def obtener_metodos_pago():
    async with aiohttp.ClientSession() as session:
        async with session.get(config('base_url').replace('127.0.0.1', 'djangoapi') + 'metodospagos/',
                               headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json
            else:
                return {'count': 0}


async def obtener_planes():
    async with aiohttp.ClientSession() as session:
        async with session.get(config('base_url').replace('127.0.0.1', 'djangoapi') + 'planes/',
                               headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json
            else:
                return {'count': 0}


async def obtener_plan(planid: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(config('base_url').replace('127.0.0.1', 'djangoapi') + f'planes/{planid}/',
                               headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json, response.status
            else:
                return {'estado': False}, response.status


async def obtener_ultima_publicacion(client_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                config('base_url').replace('127.0.0.1', 'djangoapi') + f'ultimapublicacionuser/{client_id}/',
                headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json, response.status
            else:
                return {'estado': False}, response.status


async def obtener_redes():
    async with aiohttp.ClientSession() as session:
        async with session.get(config('base_url').replace('127.0.0.1', 'djangoapi') + 'redes/',
                               headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json
            else:
                return {'count': 0}


async def obtener_user_red():
    async with aiohttp.ClientSession() as session:
        async with session.get(config('base_url').replace('127.0.0.1', 'djangoapi') + f'userredes/',
                               headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def crear_user_redes(json_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(config('base_url').replace('127.0.0.1', 'djangoapi') + 'userredes/', headers=headers,
                                json=json_data) as response:
            if response.status == 201:
                json = await response.json()
                return json


async def crear_user_pago(json_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(config('base_url').replace('127.0.0.1', 'djangoapi') + 'userpago/', headers=headers,
                                json=json_data) as response:
            if response.status == 201:
                json = await response.json()
                return json


async def crear_galeria(json_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(config('base_url').replace('127.0.0.1', 'djangoapi') + 'galeria/', headers=headers,
                                json=json_data) as response:
            if response.status == 201:
                json = await response.json()
                return json


async def crear_publicacion(json_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(config('base_url').replace('127.0.0.1', 'djangoapi') + 'publicacion/', headers=headers,
                                json=json_data) as response:
            if response.status == 201:
                json = await response.json()
                return json


async def crear_user_reaccion(json_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(config('base_url').replace('127.0.0.1', 'djangoapi') + 'usersreaccion/',
                                headers=headers, json=json_data) as response:
            if response.status == 201:
                json = await response.json()
                return json


async def obtener_user_reaccion(client_id: int, messageid: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                config('base_url').replace('127.0.0.1', 'djangoapi') + f'reaccionesuser/{client_id}/{messageid}/',
                headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def obtener_reaccion_cant(reaccionid: int, messageid: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                config('base_url').replace('127.0.0.1', 'djangoapi') + f'reaccioncant/{reaccionid}/{messageid}/',
                headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def eliminar_user(client_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.delete(config('base_url').replace('127.0.0.1', 'djangoapi') + f'userstelegram/{client_id}/',
                                  headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def eliminar_user_redes(client_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.delete(config('base_url').replace('127.0.0.1', 'djangoapi') + f'uredesdelete/{client_id}/',
                                  headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def eliminar_galeria_user(client_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.delete(config('base_url').replace('127.0.0.1', 'djangoapi') + f'galeriauser/{client_id}/',
                                  headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def eliminar_reaccion(reaccion_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                config('base_url').replace('127.0.0.1', 'djangoapi') + f'usersreaccion/{reaccion_id}/',
                headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def update_reaccion(json_data):
    reaccion_id = json_data['id']
    async with aiohttp.ClientSession() as session:
        async with session.put(config('base_url').replace('127.0.0.1', 'djangoapi') + f'usersreaccion/{reaccion_id}/',
                               headers=headers,
                               json=json_data) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def obtener_reaccion():
    async with aiohttp.ClientSession() as session:
        async with session.get(config('base_url').replace('127.0.0.1', 'djangoapi') + 'reaccion/',
                               headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json
            else:
                return {'count': 0}


async def obtener_referidos(client_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(config('base_url').replace('127.0.0.1', 'djangoapi') + f'referidos_detail/{client_id}/',
                               headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json


async def obtener_galeria_user(client_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(config('base_url').replace('127.0.0.1', 'djangoapi') + f'galeriauser/{client_id}/',
                               headers=headers) as response:
            if response.status == 200:
                json = await response.json()
                return json
