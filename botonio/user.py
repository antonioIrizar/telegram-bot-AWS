__author__ = 'antonioirizar'

from boto3 import resource
from boto3.exceptions import ResourceNotExistsError
from boto3.session import Session

from botonio.create_service_aws import Instance


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self._state = 0
        self.account = None
        self._credentials = {}
        self._client = None
        self._instance = None

    def process_message(self, message):
        if self._state == 0:
            self._state = 1
            return 'Hola %s soy botonio, tu asistente para AWS o tu peor pesadilla!\n Antes de empezar tenemos que configurar algunas cositas, cual es el id de tu cuenta de AWS.' % self.name

        if self._state == 1:
            try:
                if len(str(message)) != 12:
                    raise ValueError
                self.account = int(message)
                self._state = 2
                return 'Bien ya tenemos tu numero de cuenta, prosigamos, dame tu access key'
            except ValueError:
                return 'Eso no es un numero de cuenta valido!! Vuelve a intentarlo, paquete.'

        if self._state == 2:
            self._credentials['aws_access_key_id'] = message
            self._state = 3
            return 'Y por ultimo dame tu secret key'

        if self._state == 3:
            self._credentials['aws_secret_access_key'] = message
            self._state = 4
            return 'Bien ya tengo todo para minear bitcoins gratis.\n Bueno que servicio quieres usar de AWS?'

        if self._state == 4:
            try:
                service = message.lower()
                resource(service)
            except ResourceNotExistsError as e:
                str_excp = str(e)
                services = str_excp.split('The available resources are:')[1]
                return 'Vamos a calmarnos. Eso no existe en AWS que yo sepa. Servicios Existentes:%s ' % services

            if service != 'ec2':
                return 'Bueno vale ... Soy un poco inutil y no se usar ese servicios. Hazlo tu con boto, Vago! Hasta nunca.'
            session_boto3 = Session(**self._credentials)
            self._client = session_boto3.resource('ec2', region_name='eu-west-1')
            self._state = 5
            return 'Muy bien quieres una maquina de amazon, pero antes de continuar, necesito saber el tamaño'

        if self._state == 5:
            str_lower = message.lower()
            if str_lower.find('grande'):
                self._instance = Instance('t2.micro')
                self._state = 6
                return 'Cutre! No conozco a nadie tan rata como tu pero bueno.\n ¿Cuantas maquinas quieres?', 1
            elif str_lower.find('pequeña'):
                self._instance = Instance('t2.nano')
                self._state = 6
                return 'Animal! Estas seguro de que necesitas esa maquina. Aunque amazon estara encantado.\n¿Cuantas maquinas quieres?', 1
            else:
                return 'Pero que quieres decir aprende hablar!'

        if self._state == 6:
            try:
                if int(message) > 5:
                    return "Eso son demsaidas maquinas para arrancar!!!!!! pone menos."
                self._instance.number_instances = int(message)
                self._client.create_instances(**self._instance.configure())
                self._state = 4
                return 'Arrancando!!!!!\n ¿Que servicio quieres usar de AWS?'
            except KeyError:
                return 'Pon numeros... cansino!'
