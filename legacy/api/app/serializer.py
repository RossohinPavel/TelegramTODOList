import pickle
from .users import create_user, get_user_id
from .tasks import create_task


ALLOWED_FUNCS = {
    'create_user': create_user,
    'get_user_id': get_user_id,
    'create_task': create_task
}


class ValidationError(Exception):
    pass


class DataSerializer:
    __slots__ = ('_source_data', '_func', '_params', 'cleaned_data')
    
    def __init__(self, data: bytes) -> None:
        self.cleaned_data = b''
        self._source_data = data
        self._func: callable
        self._params: dict
    
    async def clean(self):
        """Основной вызываемый метод сериализатора. Обрабатывает ошибки по необходимости."""
        try:
            await self._validate()
            data = await self._func(**self._params)
        except Exception as e:
            data = {'error': str(e)}
        self.cleaned_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)

    async def _validate(self):
        """Небольшая проверка на соответствие данных протоколу"""
        data = pickle.loads(self._source_data)
        if not isinstance(data, dict):
            raise ValidationError('Sending data must be a dict')
        if 'func' not in data or 'params' not in data:
            raise ValidationError('Sending data does not match protocol')
        if not isinstance(data['params'], dict):
            raise ValidationError('Sending data does not match protocol')
        self._func = ALLOWED_FUNCS[data['func']]
        self._params = data['params']
