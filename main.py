from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton, MessageEntity)
from funciones import *
from validaciones import *

api_id = config('api_id')
api_hash = config('api_hash')
bot_token = config('bot_token')
app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)
arreglo_prueba = []
Grupo = config('Grupo')
Canal = config('Canal')
support = config('support')
Almacen = config('Almacen')

AceptoBTN = 'Acepto ✔'
NoAceptoBTN = 'No acepto ❌'
RegistrarseBTN = "👤 Registrarse 👤"
PlanesBTN = "⚜ Planes ⚜"
TerminosBTN = "⚠️ Términos & condiciones ⚠️"
CancelarBTN = "❌ CANCELAR ❌"
PerfilBTN = "👤 Perfil"
PublicarPerfilBTN = "👤 Publicar Perfil"
ActualizarRedeseBTN = "📲 Actualizar Redes"
ActualizarFotoBTN = "📸 Actualizar Foto"
SubirGaleriaBTN = "🖼 Subir Galeria"
PublicarGaleriaBTN = "🖼 Publicar Galeria"
ReferidoBTN = "🤝 Referido"
GrupoCanalBTN = "🤖 Grupo & Canal"
ActualizarDescripcionBTN = "📋 Actualizar Descripcion"
AjustesBTN = '⚙ Ajustes'
EliminarCuentaBTN = '🗑 Eliminar Cuenta'
EliminarCuentaAceptarBTN = '🗑 Aceptar Eliminacion'
OpcionesPagoBTN = '💱 Opciones de pago'
FinalizarBTN = '⏩ Finalizar ✔️'
CloseBTN = '✖️ Close'
GuardarBTN = '💾 Guardar'
EliminarBTN = '🗑 Eliminar'
EliminarRedesBTN = '🗑 Eliminar Redes'
Boton_Inicio = [[RegistrarseBTN, PlanesBTN]]
Boton_Cancelar = [[CancelarBTN]]
Boton_Autenticado = [[PerfilBTN, PublicarPerfilBTN],
                     [ActualizarRedeseBTN, ActualizarFotoBTN],
                     [SubirGaleriaBTN, PublicarGaleriaBTN],
                     [GrupoCanalBTN, ReferidoBTN],
                     [ActualizarDescripcionBTN, PlanesBTN],
                     [EliminarCuentaBTN]]
Boton_Galeria = [[GuardarBTN, EliminarBTN]]
Boton_Terminos = [AceptoBTN, NoAceptoBTN]
Boton_Eliminar_Cuenta = [[EliminarCuentaAceptarBTN], [CancelarBTN]]

Limite_Galeria = 10


@app.on_callback_query()
async def answer(client, callback_query):
    client_id = callback_query.from_user.id
    try:
        user_telegram, status = await obtener_user(client_id)
        if callback_query.data == 'DEL':
            await client.delete_messages(client_id, callback_query.message.id)
            await callback_query.answer(
                "Cancelar",
                show_alert=False)
        elif callback_query.data == EliminarRedesBTN:
            await eliminar_user_redes(client_id)
            await callback_query.answer(
                "Redes eliminadas",
                show_alert=False)
        elif callback_query.data == CloseBTN:
            await client.delete_messages(client_id, callback_query.message.id)
            await callback_query.answer(
                CloseBTN,
                show_alert=False)
        elif callback_query.data == OpcionesPagoBTN and user_telegram['estado']:
            metodos_pag = await obtener_metodos_pago()
            listaaux = []
            for metodos_pa in metodos_pag['results']:
                listaaux.append([metodos_pa['nombre']])
            listaaux.append([CancelarBTN])
            await client.send_message(client_id, 'Seleccione uno de los metodos de pagos',
                                      reply_markup=ReplyKeyboardMarkup(
                                          listaaux,
                                          resize_keyboard=True)
                                      )
        elif callback_query.data == OpcionesPagoBTN and not user_telegram['estado']:
            await client.send_message(client_id, 'Registrese para poder acceder a esta opción')
            await callback_query.answer(
                OpcionesPagoBTN,
                show_alert=False)
        elif callback_query.data == 'planes':
            planes = await obtener_planes()
            listaux = []
            listaux2 = []
            for plane in planes['results']:
                if len(listaux2) != 2:
                    listaux2.append(InlineKeyboardButton(
                        plane['nombre'], callback_data=plane['nombre']))
                else:
                    listaux.append(listaux2)
                    listaux2 = [InlineKeyboardButton(
                        plane['nombre'], callback_data=plane['nombre'])]
            listaux.append(listaux2)
            listaux.append([InlineKeyboardButton(
                CloseBTN, callback_data=CloseBTN)])
            await client.edit_message_text(client_id, callback_query.message.id,
                                           'User id: ' +
                                           str(client_id) + '\n\n' +
                                           planes['results'][0]['descripcion'],
                                           reply_markup=InlineKeyboardMarkup(listaux))
            await callback_query.answer(
                "<=",
                show_alert=False)

        elif callback_query.data == 'desaprobado':
            client_id2 = int(str(callback_query.message.text).split()[-1])
            await client.delete_messages(support, callback_query.message.id)
            await client.send_message(client_id2,
                                      'Su pago no fue aprobado debido a que no se pudo comprobar el pago. Para mas '
                                      'informacion consulte con el soporte',
                                      reply_markup=ReplyKeyboardMarkup(
                                          Boton_Autenticado,
                                          resize_keyboard=True)
                                      )
            await callback_query.answer(
                "La cuenta fue desaprobada correctamente",
                show_alert=False)
        else:
            redes = await obtener_redes()
            for redes_soc in redes['results']:
                if callback_query.data == redes_soc['nombre']:
                    nombre = redes_soc['nombre']
                    url = redes_soc['url']
                    if user_telegram['estado']:
                        await client.send_message(client_id, f'Agregue su enlace de perfil de {nombre}\n\nEjemplo: '
                                                             f'{url}username',
                                                  reply_markup=ReplyKeyboardMarkup(
                                                      Boton_Cancelar,
                                                      resize_keyboard=True
                                                  )
                                                  )
                        user_telegram['ultimomsg'] = nombre
                        await update_user(user_telegram)
                        await callback_query.answer(
                            nombre,
                            show_alert=False)
                        return 1
                    else:
                        await client.send_message(client_id, f'Agregue su enlace de perfil de {nombre}\n\nEjemplo: '
                                                             f'{url}username',
                                                  reply_markup=ReplyKeyboardMarkup(
                                                      [[FinalizarBTN], [
                                                          CancelarBTN]],
                                                      resize_keyboard=True
                                                  )
                                                  )
                        user_telegram['ultimomsg'] = nombre
                        await update_user(user_telegram)
                        await callback_query.answer(
                            nombre,
                            show_alert=False)
                        return 1
            planes = await obtener_planes()
            for plane in planes['results']:
                if callback_query.data == plane['nombre'] and user_telegram['estado'] and plane['id'] == 1:
                    await client.edit_message_text(client_id, callback_query.message.id, plane['descripcion'],
                                                   reply_markup=InlineKeyboardMarkup(
                                                       [
                                                           [InlineKeyboardButton(
                                                               '<=', callback_data='planes')]
                                                       ]
                                                   )
                                                   )
                    await callback_query.answer(
                        str(plane['nombre']),
                        show_alert=False)
                    return 1

                elif callback_query.data == plane['nombre'] and user_telegram['estado']:
                    await client.edit_message_text(client_id, callback_query.message.id, plane['descripcion'],
                                                   reply_markup=InlineKeyboardMarkup(
                                                       [
                                                           [InlineKeyboardButton(OpcionesPagoBTN,
                                                                                 callback_data=OpcionesPagoBTN)],
                                                           [InlineKeyboardButton(
                                                               '<=', callback_data='planes')]
                                                       ]
                                                   )
                                                   )
                    user_telegram['ultimomsg'] = str(plane['id'])
                    await update_user(user_telegram)
                    await callback_query.answer(
                        str(plane['nombre']),
                        show_alert=False)
                    return 1
                elif callback_query.data == plane['nombre'] and not user_telegram['estado']:
                    await client.edit_message_text(client_id, callback_query.message.id, plane['descripcion'],
                                                   reply_markup=InlineKeyboardMarkup(
                                                       [
                                                           [InlineKeyboardButton(
                                                               '<=', callback_data='planes')]
                                                       ]
                                                   )
                                                   )
                    user_telegram['ultimomsg'] = str(plane['id'])
                    await callback_query.answer(
                        str(plane['nombre']),
                        show_alert=False)
                    return 1
            metodos_pagos = await obtener_metodos_pago()
            for metodos_pago in metodos_pagos['results']:
                if callback_query.data == metodos_pago['siglas']:
                    siglas = metodos_pago['siglas']
                    await client.send_message(client_id, 'Envie una captura de la transferencia')
                    user_telegram['ultimomsg'] += ',' + siglas
                    await update_user(user_telegram)
                    await callback_query.answer(
                        siglas,
                        show_alert=False)
                    return 1
            for metodos_pago in metodos_pagos['results']:
                if callback_query.data == str(metodos_pago['nombre']):
                    client_id2 = int(
                        str(callback_query.message.text).split()[-1])
                    await client.delete_messages(support, callback_query.message.id)
                    user2, status = await obtener_user(client_id2)
                    user2['estado'] = True
                    json_dat = {
                        'metodo': metodos_pago['id'],
                        'user': client_id2,
                    }
                    await crear_user_pago(json_dat)
                    if user2['referido'] is not None:
                        plan, status = await obtener_plan(int(user2['ultimomsg']))
                        if metodos_pago['siglas'] == 'CUP':
                            saldo_cup, status = await obtener_user(user2['referido'])
                            saldo_cup['saldo_cup'] += plan['precio'] * metodos_pago['valor_cambio'] * 0.1
                            await update_user(saldo_cup)
                        elif metodos_pago['siglas'] == 'MLC':
                            saldo_mlc, status = await obtener_user(user2['referido'])
                            saldo_mlc['saldo_mlc'] += plan['precio'] * metodos_pago['valor_cambio'] * 0.1
                            await update_user(saldo_mlc)
                        elif metodos_pago['siglas'] == 'USDT':
                            saldo_usdt, status = await obtener_user(user2['referido'])
                            saldo_usdt['saldo_usdt'] += plan['precio'] * metodos_pago['valor_cambio'] * 0.1
                        elif metodos_pago['siglas'] == 'SALDO':
                            saldo_movil, status = await obtener_user(user2['referido'])
                            saldo_movil['saldo_movil'] += plan['precio'] * metodos_pago['valor_cambio'] * 0.1
                            await update_user(saldo_movil)
                    user2['plan'] = int(user2['ultimomsg'])
                    user2['ultimomsg'] = ''
                    await update_user(user2)
                    await client.send_message(client_id2, 'Su pago fue aprobado',
                                              reply_markup=ReplyKeyboardMarkup(
                                                  Boton_Autenticado,
                                                  resize_keyboard=True)
                                              )
                    await callback_query.answer(
                        "La cuenta fue aprobada correctamente",
                        show_alert=False)
                    return 1
            reacciones = await obtener_reaccion()
            for reaccion in reacciones['results']:
                if callback_query.data == str(reaccion['nombre']):
                    reaccions = await obtener_user_reaccion(client_id, callback_query.message.id)
                    if len(reaccions) == 0:
                        data = {
                            'actor': client_id,
                            'id_reaccion': reaccion['id'],
                            'message': callback_query.message.id,
                        }

                        await crear_user_reaccion(data)
                        auxlista = []
                        for reaccions2 in reacciones['results']:
                            cant = await obtener_reaccion_cant(reaccions2['id'], callback_query.message.id)
                            auxlista.append(InlineKeyboardButton(  # Opens the inline interface in the current chat
                                reaccions2['nombre'] + ' ' + str(cant['cant']),
                                callback_data=reaccions2['nombre']
                            ))
                        await client.edit_message_reply_markup(
                            Canal, callback_query.message.id,
                            InlineKeyboardMarkup([auxlista]))
                        await callback_query.answer(
                            str(reaccion['nombre']),
                            show_alert=False)
                        return 1
                    else:
                        if reaccions[0]['id_reaccion'] == reaccion['id']:
                            await eliminar_reaccion(reaccions[0]['id'])
                        else:
                            jsdata = reaccions[0]
                            jsdata['id_reaccion'] = reaccion['id']
                            await update_reaccion(jsdata)
                        auxlista = []
                        for reaccions3 in reacciones['results']:
                            cant = await obtener_reaccion_cant(reaccions3['id'], callback_query.message.id)
                            auxlista.append(InlineKeyboardButton(  # Opens the inline interface in the current chat
                                reaccions3['nombre'] + ' ' + str(cant['cant']),
                                callback_data=reaccions3['nombre']
                            ))
                        await client.edit_message_reply_markup(
                            Canal, callback_query.message.id,
                            InlineKeyboardMarkup([auxlista]))
                        await callback_query.answer(
                            str(reaccion['nombre']),
                            show_alert=False)
                        return 1

    except Exception as e:
        await error(client, client_id, e.args[0])


@app.on_message(filters.command(['start']) & filters.private)
async def inicio(client, message):
    print(message)
    client_id = message.from_user.id
    username = message.from_user.username
    if username is None:
        username = 'User'
    try:
        users, status = await obtener_user(client_id)
        if len(message.command) == 2:
            await validar_ref(message.command[-1], client_id)
            if status != 200:
                await crear_user(client_id, int(message.command[-1]))

        if not users['estado']:
            await client.send_message(
                client_id,
                f'Hola {username}, bienvenido a nuestra plataforma para aumentar seguidores, incluso convertirse en '
                'influencer. '
                'Por favor proceda a registrarse en el sistema presionando el botón debajo.',
                reply_markup=ReplyKeyboardMarkup(
                    Boton_Inicio,
                    resize_keyboard=True
                )
            )
        else:
            await client.send_message(
                client_id,
                f'Hola {username}, bienvenido a nuestra plataforma para aumentar seguidores, incluso convertirse en '
                'influencer. ',
                reply_markup=ReplyKeyboardMarkup(
                    Boton_Autenticado,
                    resize_keyboard=True)
            )
    except Exception as e:
        await error(client, client_id, e.args[0])


@app.on_message(filters.text & filters.private)
async def echo(client, message):
    client_id = message.from_user.id
    print(message)
    username = message.from_user.username
    if username is None:
        username = 'User'
    try:
        users2, status = await obtener_user(client_id)
        if message.text == RegistrarseBTN:
            await client.send_message(client_id, '⚠️ ⚠️⚠️ ATENCIÓN ⚠️ ⚠️⚠️\n'
                                                 'Antes de continuar en nuestro sistema debes tener en cuenta lo '
                                                 'siguiente:\n\n '
                                                 '❕❕ Tus datos estaran almacenados de forma SEGURA Y PRIVADA en '
                                                 'nuestros servidores, solo daremos acceso a la informción requerida '
                                                 'para generar su publicidad y ayudarle en su objetivo❕❕\n\n'
                                                 '❗️ ❗️Para continuar debes aceptar estos terminos y condiciones '
                                                 f'sobre tus datos presionando el botón {AceptoBTN}❗️❗️',
                                      reply_markup=ReplyKeyboardMarkup(
                                          [Boton_Terminos],
                                          resize_keyboard=True
                                      )
                                      )
        elif message.text == AceptoBTN:
            if not users2['estado']:
                if status != 200:
                    await crear_user(client_id)
                await client.send_message(client_id, '⚠️Términos aceptados ⚠️')
                await client.send_message(client_id, 'Envie su nombre completo al bot',
                                          reply_markup=ReplyKeyboardMarkup(
                                              Boton_Cancelar,
                                              resize_keyboard=True
                                          ))
                await update_user({'client_id': client_id, 'ultimomsg': '01'})
            else:
                await client.send_message(client_id, 'Ya se encuentra registrado')
        elif message.text == NoAceptoBTN:
            if status == 200:
                users2['ultimomsg'] = ''
                await update_user(users2)
            await client.send_message(client_id, '⚠️Términos no aceptados ⚠️')
            await client.send_message(client_id, '⛔️ Accion Cancelada ⛔️')
            await client.send_message(
                client_id,
                "❗️ Siga en nuestro sistema, ¿que desea hacer ahora? ❗️",
                reply_markup=ReplyKeyboardMarkup(
                    Boton_Inicio,
                    resize_keyboard=True
                )
            )

        elif message.text == CancelarBTN and not users2['estado']:
            if status == 200:
                users2['ultimomsg'] = ''
                await update_user(users2)
            await client.send_message(client_id, '⛔️ Accion Cancelada ⛔️')
            await client.send_message(
                client_id,
                "❗️ Siga en nuestro sistema, ¿que desea hacer ahora? ❗️",
                reply_markup=ReplyKeyboardMarkup(
                    Boton_Inicio,
                    resize_keyboard=True
                )
            )
        elif message.text == CancelarBTN and users2['estado']:
            users2['ultimomsg'] = ''
            await update_user(users2)
            await client.send_message(client_id, '⛔️ Accion Cancelada ⛔️')
            await client.send_message(
                client_id,
                "❗️ Siga en nuestro sistema, ¿que desea hacer ahora? ❗️",
                reply_markup=ReplyKeyboardMarkup(
                    Boton_Autenticado,
                    resize_keyboard=True
                )
            )
        elif message.text == PublicarGaleriaBTN:
            galeria_user = await obtener_galeria_user(client_id)
            if not galeria_user:
                raise Exception('No hay galerias')
            feacha_galeria = datetime.datetime.strptime(str(galeria_user[-1]['fecha_creacion']), '%Y-%m-%d')
            plan, status = await obtener_plan(users2['plan'])
            tiempo_evaluar = plan['horas_republicacion']
            await validar_tiempo_transcurrido(feacha_galeria, tiempo_evaluar, users2['plan'])
            for gal_user in galeria_user:
                await app.send_cached_media(Canal, str(gal_user['fotos_galeria']))
            await client.send_message(client_id, 'Su galeria a sido publicada satisfactoriamente en el canal')

        elif message.text == SubirGaleriaBTN and users2['estado']:
            users2['ultimomsg'] = 'Galeria'
            await client.send_message(client_id, f'Esta es tu galería {username}, puedes enviar fotos, '
                                                 'incluso videos para que los otros usuarios de la plataforma '
                                                 'consuman de tu contenido y ganar aún más popularidad y seguidores '
                                                 'en la plataforma.',
                                      reply_markup=ReplyKeyboardMarkup(
                                          Boton_Galeria, resize_keyboard=True))
            await update_user(users2)
        elif message.text == GuardarBTN and users2['estado']:
            users2['ultimomsg'] = ''
            await update_user(users2)
            await client.send_message(client_id, '✅✅✅ Galeria guardada ✅✅✅')
            await client.send_message(
                client_id,
                "❗️ Siga en nuestro sistema, ¿que desea hacer ahora? ❗️",
                reply_markup=ReplyKeyboardMarkup(
                    Boton_Autenticado,
                    resize_keyboard=True
                )
            )
        elif message.text == EliminarBTN and users2['estado']:
            users2['ultimomsg'] = ''
            await update_user(users2)
            await client.send_message(client_id, '⛔️ Galeria eliminada ⛔️')
            await client.send_message(
                client_id,
                "❗️ Siga en nuestro sistema, ¿que desea hacer ahora? ❗️",
                reply_markup=ReplyKeyboardMarkup(
                    Boton_Autenticado,
                    resize_keyboard=True
                )
            )
            await eliminar_galeria_user(client_id)

        elif message.text == PlanesBTN:
            planes = await obtener_planes()
            listaux = []
            listaux2 = []
            for plane in planes['results']:
                if len(listaux2) != 2:
                    listaux2.append(InlineKeyboardButton(
                        plane['nombre'], callback_data=plane['nombre']))
                else:
                    listaux.append(listaux2)
                    listaux2 = [InlineKeyboardButton(
                        plane['nombre'], callback_data=plane['nombre'])]
            listaux.append(listaux2)
            listaux.append([InlineKeyboardButton(
                CloseBTN, callback_data=CloseBTN)])
            await client.send_message(client_id,
                                      'User id: ' +
                                      str(client_id) + '\n\n' +
                                      planes['results'][0]['descripcion'],
                                      reply_markup=InlineKeyboardMarkup(listaux))
        elif message.text == EliminarCuentaBTN:
            await client.send_message(client_id, 'Esta seguro que desea eliminar su cuenta?\n\nEsta acción no se '
                                                 'puede revertir',
                                      reply_markup=ReplyKeyboardMarkup(
                                          Boton_Eliminar_Cuenta, resize_keyboard=True)
                                      )
        elif message.text == EliminarCuentaAceptarBTN:
            await eliminar_user(client_id)
            await client.send_message(client_id, 'Su cuenta ha sido eliminada')
            await client.send_message(client_id, 'Gracias por usar nuestro servicio',
                                      reply_markup=ReplyKeyboardMarkup(
                                          Boton_Inicio, resize_keyboard=True)
                                      )
        elif message.text == ActualizarFotoBTN and users2['estado']:
            if users2['estado']:
                await client.send_message(client_id, 'Envie una nueva foto de perfil',
                                          reply_markup=ReplyKeyboardMarkup(
                                              Boton_Cancelar,
                                              resize_keyboard=True
                                          ))
                users2['ultimomsg'] = 'Foto'
                await update_user(users2)
        elif message.text == ActualizarRedeseBTN and users2['estado']:
            if users2['estado']:
                redes = await obtener_redes()
                listaux = []
                listaux2 = []
                for red in redes['results']:
                    if len(listaux2) != 2:
                        listaux2.append(InlineKeyboardButton(
                            red['nombre'], callback_data=red['nombre']))
                    else:
                        listaux.append(listaux2)
                        listaux2 = [InlineKeyboardButton(
                            red['nombre'], callback_data=red['nombre'])]
                listaux.append(listaux2)
                listaux.append([InlineKeyboardButton(
                    EliminarRedesBTN, callback_data=EliminarRedesBTN)])
                listaux.append([InlineKeyboardButton(
                    CloseBTN, callback_data=CloseBTN)])
                await client.send_message(client_id,
                                          'Seleccione las redes sociales que desea agregar o actualizar',
                                          reply_markup=InlineKeyboardMarkup(
                                              listaux
                                          ))
        elif message.text == ReferidoBTN and users2['estado']:
            enlaceref = 'http://t.me/FollowTheVip2Bot?start=' + str(client_id)
            cantref = await obtener_referidos(client_id)
            cantref = cantref['cant']
            saldo_cup = users2['saldo_cup']
            saldo_usdt = users2['saldo_usdt']
            saldo_mlc = users2['saldo_mlc']
            saldo_movil = users2['saldo_movil']
            mensaje = f'Este es tu panel de referidos {username}, con él podrás obtener datos que te ' \
                      f'harán crecer más ' \
                      f'rápido📈.\n\n' \
                      f'Acá abajo tienes tu enlace personal y demás informaciones.\n\n{enlaceref}\n\n' \
                      f'Usted tiene {cantref} referidos\n\nSu saldo acumulado de CUP es de {saldo_cup}\n\n' \
                      f'Su saldo acumulado de USDT es de {saldo_usdt}\n\n' \
                      f'Su saldo acumulado de MLC es de {saldo_mlc}\n\n' \
                      f'Su saldo acumulado de Movil es de {saldo_movil}\n\n'
            await client.send_message(client_id, mensaje)
        elif message.text == GrupoCanalBTN and users2['estado']:
            await client.send_message(
                client_id,
                "Unase a nuestro canal y grupo para que esta al tanto de todas las informaciones",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(  # Opens a web URL
                                "Canal",
                                url="https://t.me/" + Canal
                            ),
                            InlineKeyboardButton(  # Opens a web URL
                                "Grupo",
                                url="https://t.me/" + Grupo
                            ),
                        ]]
                )
            )
        elif message.text == ActualizarDescripcionBTN and users2['estado']:
            if users2['estado']:
                await client.send_message(client_id, 'Entre una descripcion de usted para que el resto '
                                                     'de usuarios de la comunidad conozcan mas sobre sus gustos',
                                          reply_markup=ReplyKeyboardMarkup(
                                              Boton_Cancelar,
                                              resize_keyboard=True
                                          )
                                          )
                users2['ultimomsg'] = ActualizarDescripcionBTN
                await update_user(users2)
        elif message.text == FinalizarBTN and users2['nombre'] is not None and users2['descripcion'] is not None:
            users2['estado'] = True
            await update_user(users2)
            await client.send_message(
                client_id,
                "Unase a nuestro canal y grupo para que este al tanto de todas las informaciones",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(  # Opens a web URL
                                "Canal",
                                url="https://t.me/" + Canal
                            ),
                            InlineKeyboardButton(  # Opens a web URL
                                "Grupo",
                                url="https://t.me/" + Grupo
                            ),
                        ]]
                )
            )
            await client.send_message(client_id, f'GENIAL {username} 😁, su registro se efectuó correctamente. Solo '
                                                 'que actualmente su plan es el   FREE o GRATIS el cual ❌no  tiene '
                                                 'todos los privilegios necesarios para usted❌, por favor, '
                                                 f'👇PRECIONE EL BOTÓN {PlanesBTN} ACÁ ABAJO  Y ESCOJA EL DE SU '
                                                 'PREFERENCIA PARA ALCANZAR SU OBJETIVO 👇',
                                      reply_markup=ReplyKeyboardMarkup(
                                          Boton_Autenticado,
                                          resize_keyboard=True)
                                      )
        elif message.text == PerfilBTN and users2['estado']:
            if users2['estado']:
                nombre = users2['nombre']
                descripcion = users2['descripcion']
                user_redes = await obtener_user_red()
                redes = await obtener_redes()
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
                    # cadena = str(sms['redes']) + ': \n\n' + '👉Sigueme👈\n\n'
                    cadena = str(sms['redes'])
                    smsredes += auxi
                    smsredes += cadena
                    listentities.append(MessageEntity(type=MessageEntityType.TEXT_LINK, offset=pos,
                                                      length=len(sms['redes']) + 1, url=str(sms['username'])))
                    pos += len(cadena) + 5
                    auxi = ',   '
                mensaje_base += smsredes
                await client.send_photo(client_id, users2['foto'],
                                        caption=mensaje_base,
                                        caption_entities=listentities,
                                        )

        elif message.text == PublicarPerfilBTN and users2['estado']:
            ultima_publicacion, status = await obtener_ultima_publicacion(client_id)
            if status == 200:
                fecha = datetime.datetime.fromisoformat(
                    str(ultima_publicacion['fecha_publicacion']).split('.')[0])
                plan, status = await obtener_plan(users2['plan'])
                tiempo_evaluar = plan['horas_republicacion']
                await validar_tiempo_transcurrido(fecha, tiempo_evaluar, users2['plan'])
            nombre = users2['nombre']
            descripcion = users2['descripcion']
            user_redes = await obtener_user_red()
            redes = await obtener_redes()
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
                # cadena = str(sms['redes']) + ': \n\n' + '👉Sigueme👈\n\n'
                cadena = str(sms['redes'])
                smsredes += auxi
                smsredes += cadena
                listentities.append(MessageEntity(type=MessageEntityType.TEXT_LINK, offset=pos,
                                                  length=len(sms['redes']) + 1, url=str(sms['username'])))
                pos += len(cadena) + 5
                auxi = ',   '
            mensaje_base += smsredes
            reacciones = await obtener_reaccion()
            auxlista = []
            for reaccion in reacciones['results']:
                auxlista.append(InlineKeyboardButton(  # Opens the inline interface in the current chat
                    reaccion['nombre'] + ' 0',
                    callback_data=reaccion['nombre']
                ))
            smspublicacion = await client.send_photo(Canal, users2['foto'],
                                                     caption=mensaje_base,
                                                     caption_entities=listentities,
                                                     reply_markup=InlineKeyboardMarkup(
                                                         [auxlista]
                                                     )
                                                     )
            await client.send_message(client_id, 'Visite el canal para ver la publicacion',
                                      reply_markup=InlineKeyboardMarkup([[
                                          InlineKeyboardButton(  # Opens a web URL
                                              "Canal",
                                              url="https://t.me/" + Canal
                                          )]]))
            json_date = {
                'message': smspublicacion.id,
                'client_id': client_id,
            }
            await crear_publicacion(json_date)

        else:
            if status != 200:
                return 0
            elif not users2['estado']:
                if users2['ultimomsg'] == '01':
                    await validar_nombre(message.text)
                    users2['nombre'] = message.text
                    await client.send_message(
                        client_id,
                        'Perfecto👌, su nombre se ha guardado correctamente.\n\nPor favor 🙏 entre una descripción de '
                        'usted para que el resto de usuarios de nuestra comunidad conozcan mas sobre sus gustos y '
                        'preferencias.')
                    users2['ultimomsg'] = '02'
                    await update_user(users2)
                elif users2['ultimomsg'] == '02':
                    await validar_descripcion(message.text)
                    users2['descripcion'] = message.text
                    await client.send_message(client_id, 'Genial 😁 su descripcion se ha guardado '
                                                         'correctamente.\n\nEnvienos una Foto 📸 para tomarla como '
                                                         'foto principal en su perfil.')
                    users2['ultimomsg'] = '03'
                    await update_user(users2)
                elif users2['ultimomsg'] == ActualizarDescripcionBTN:
                    await validar_descripcion(message.text)
                    users2['descripcion'] = message.text
                    users2['ultimomsg'] = ''
                    await client.send_message(client_id, 'Su descripcion se guardo correctamente')
                    await update_user(users2)
            redes = await obtener_redes()
            for redes_soc in redes['results']:
                if users2['ultimomsg'] == redes_soc['nombre']:
                    users2['ultimomsg'] = ''
                    json_data = {
                        'username': message.text,
                        'redes': redes_soc['id'],
                        'user': client_id,
                    }
                    await validar_url(message.text, redes_soc['url'])
                    await crear_user_redes(json_data)
                    await update_user(users2)
                    if not users2['estado']:
                        await client.send_message(client_id, 'Su cuenta se agrego correctamente')
                    else:
                        await client.send_message(client_id, 'Su cuenta se agrego correctamente',
                                                  reply_markup=ReplyKeyboardMarkup(
                                                      Boton_Autenticado,
                                                      resize_keyboard=True))
                    return 1
            metodos_pagos = await obtener_metodos_pago()
            for metodos_pago in metodos_pagos['results']:
                if message.text == metodos_pago['nombre']:
                    if users2['estado']:
                        plan, status = await obtener_plan(int(users2['ultimomsg']))
                        pago = plan['precio'] * metodos_pago['valor_cambio']
                        mensaje_guia = metodos_pago['mensaje_guia']
                        mensaje_pago = f'Muy bien {username}, para empezar a ' \
                                       f'generar seguidores y poder gestionar todo lo necesario debe realizar la  ' \
                                       f'transferencia de {pago}$ a {mensaje_guia}. UNA VEZ ' \
                                       f'REALIZADA LA TRANSFERENCIA ' \
                                       f'PRESIONE EL BOTÓN [ Confirmar pago ]'
                        await client.send_message(client_id,
                                                  mensaje_pago,
                                                  reply_markup=InlineKeyboardMarkup(
                                                      [[InlineKeyboardButton(
                                                          # Opens the inline interface in the current chat
                                                          "Confirmar Pago",
                                                          callback_data=metodos_pago['siglas']
                                                      ), InlineKeyboardButton(
                                                          # Opens the inline interface in the current chat
                                                          "Cancelar",
                                                          callback_data="DEL"
                                                      )]]
                                                  ))
                    return 1
    except Exception as e:
        await error(client, client_id, e.args[0])


@app.on_message(filters.photo & filters.private)
async def foto_perfil(client, message):
    client_id = message.from_user.id
    user, status = await obtener_user(client_id)
    try:
        if user['ultimomsg'] == '03' and not user['estado'] and status == 200:
            file = await app.download_media(message)
            await asyncio.to_thread(validator_img, file)
            foto = await client.forward_messages(Almacen, client_id, message.id)
            user['foto'] = str(foto.photo.file_id)
            redes = await obtener_redes()
            listaux = []
            listaux2 = []
            for red in redes['results']:
                if len(listaux2) != 2:
                    listaux2.append(InlineKeyboardButton(
                        red['nombre'], callback_data=red['nombre']))
                else:
                    listaux.append(listaux2)
                    listaux2 = [InlineKeyboardButton(
                        red['nombre'], callback_data=red['nombre'])]
            listaux.append(listaux2)
            await client.send_message(client_id,
                                      'Su foto se ha guardado correctamente, ya casi terminamos 🙂, '
                                      'ahora procederemos a guardar tus redes sociales\n\n'
                                      'Agregue su enlace de perfil 👤 en Facebook o demás redes, esto lo puedes hacer '
                                      'mediante el navegador del celular📱 o de la computadora 💻, entras a tu perfil '
                                      'personal y copias la dirección web, debe ser parecida al ejemplo debajo, '
                                      'si aún así desconoce como hacerlo pida ayuda a un amigo',
                                      reply_markup=InlineKeyboardMarkup(
                                          listaux
                                      ))
            await client.send_message(client_id,
                                      'Ejemplo: https://www.facebook.com/username\n'
                                      'Una vez termine de agregar todas sus redes sociales presione el botón finalizar',
                                      reply_markup=ReplyKeyboardMarkup(
                                          [[FinalizarBTN], [CancelarBTN]],
                                          resize_keyboard=True))

            user['ultimomsg'] = ''
            await update_user(user)
        elif user['ultimomsg'] == 'Foto' and user['estado']:
            file = await app.download_media(message)
            await asyncio.to_thread(validator_img, file)
            foto = await client.forward_messages(Almacen, client_id, message.id)
            user['foto'] = str(foto.photo.file_id)
            user['ultimomsg'] = ''
            await client.send_message(client_id, 'Su foto se actualizo correctamente',
                                      reply_markup=ReplyKeyboardMarkup(
                                          Boton_Autenticado,
                                          resize_keyboard=True)
                                      )
            await update_user(user)
        elif user['ultimomsg'] == 'Galeria' and user['estado']:
            galeria_user = await obtener_galeria_user(client_id)
            if len(galeria_user) >= Limite_Galeria:
                await client.send_message(client_id, 'A alcanzado el limite que puede subir a su galeria')
            file = await app.download_media(message)
            await asyncio.to_thread(validator_img, file)
            foto = await client.forward_messages(Almacen, client_id, message.id)
            json_dta = {
                'fotos_galeria': str(foto.photo.file_id),
                'client_id': client_id,
            }
            await crear_galeria(json_dta)
        elif user['estado'] and len(str(user['ultimomsg']).split(',')) == 2:
            metodos_pagos = await obtener_metodos_pago()
            for metodos_pago in metodos_pagos['results']:
                if str(user['ultimomsg']).split(',')[1] == metodos_pago['siglas']:
                    plan, status = await obtener_plan(int(str(user['ultimomsg']).split(',')[0]))
                    await client.forward_messages(support, client_id, message.id)
                    await client.send_photo(support, user['foto'])
                    await client.send_message(support,
                                              'Pago de ' +
                                              str(plan['precio']) +
                                              '$, metodo de pago '
                                              + str(user['ultimomsg']).split(',')[1] + f' Aprobar user {client_id}',
                                              reply_markup=InlineKeyboardMarkup(
                                                  [[InlineKeyboardButton(
                                                      # Opens the inline interface in the current chat
                                                      "Confirmar Pago",
                                                      callback_data=str(
                                                          metodos_pago['nombre'])
                                                  ), InlineKeyboardButton(
                                                      # Opens the inline interface in the current chat
                                                      "Cancelar",
                                                      callback_data="desaprobado"
                                                  )]]
                                              ))
                    await client.send_message(client_id,
                                              'Espere pacientemente a que su pago sea '
                                              'aprobado '
                                              ' y no interactue con el bot durante este proceso',
                                              reply_markup=ReplyKeyboardMarkup(
                                                  Boton_Cancelar,
                                                  resize_keyboard=True))
                    user['ultimomsg'] = str(plan['id'])
                    await update_user(user)
                    return 1
    except Exception as e:
        await error(client, client_id, e.args[0])


@app.on_message(filters.video & filters.private)
async def video(client, message):
    client_id = message.from_user.id
    user, status = await obtener_user(client_id)
    if user['ultimomsg'] == 'Galeria' and user['estado']:
        galeria_user = await obtener_galeria_user(client_id)
        if len(galeria_user) >= Limite_Galeria:
            await client.send_message(client_id, 'A alcanzado el limite que puede subir a su galeria')
        file = await app.download_media(message)
        await asyncio.to_thread(validator_img, file)
        foto = await client.forward_messages(Almacen, client_id, message.id)
        json_dta = {
            'fotos_galeria': str(foto.photo.file_id),
            'client_id': client_id,
        }
        await crear_galeria(json_dta)


app.run()
