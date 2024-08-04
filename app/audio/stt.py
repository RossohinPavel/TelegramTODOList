"""
Скрипт для перевода аудио в текст
Вся сложность - привести аудио к нужному формату. 
Для мальенькой модели нужно иметь аудио в wav формате с кодировкой (16bit mono 256 kbit)
Образец c правильной кодировкой - test16k.wav
"""
from vosk import Model, KaldiRecognizer
from typing import Self
from pathlib import Path
from pydub import AudioSegment
from asyncio import Lock
import io, json


class STT:
    """Перевод речи в текст."""
    __slots__ = 'wave_binary', 'text'

    __SAMPLE_RATE = 16000
    __current_dir = Path(__file__).parent
    __model = Model(str(__current_dir))
    __rec = KaldiRecognizer(__model, __SAMPLE_RATE)
    # __rec.SetWords(True)
    __lock = Lock()

    @classmethod
    async def from_ogg_binary(cls, ogg_binary: io.BytesIO) -> Self:
        """Создает STT объект на основе .ogg аудио"""
        ogg: AudioSegment = AudioSegment.from_ogg(ogg_binary)
        ogg = ogg.set_frame_rate(cls.__SAMPLE_RATE)
        ogg = ogg.set_channels(1)
        ogg = ogg.set_sample_width(2)
        return cls(ogg.raw_data)

    def __init__(self, wave_binary: io.BytesIO):
        self.wave_binary = wave_binary
        self.text = ''

    async def recognition(self) -> str:
        """Запускает процесс распознания. Возвращает распознанный текст"""
        async with self.__lock:
            res = self.__rec.AcceptWaveform(self.wave_binary)
            text = self.__rec.FinalResult()
        self.text = json.loads(text)['text'] or 'unrecognized'
        return self.text
