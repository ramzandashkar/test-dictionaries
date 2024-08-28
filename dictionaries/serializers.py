from rest_framework import serializers
from .models import Dictionary, DictionaryVersion, DictionaryElement


class DictionarySerializer(serializers.ModelSerializer):
    """
    Сериализатор для справочников.

    Этот сериализатор преобразует экземпляры модели `Dictionary` в формат JSON
    и наоборот. Он используется для представления базовой информации о
    справочниках.

    Поля:
    - `id`: Идентификатор справочника (целое число).
    - `code`: Код справочника (строка).
    - `name`: Название справочника (строка).

    Примеры:
    - Преобразование экземпляра модели в JSON:
      ```json
      {
        "id": 1,
        "code": "001",
        "name": "Пример справочника"
      }
      ```
    """
    class Meta:
        model = Dictionary
        fields = ['id', 'code', 'name']


class DictionaryVersionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для версий справочников.

    Этот сериализатор преобразует экземпляры модели `DictionaryVersion` в
    формат JSON и наоборот. Он используется для представления информации о
    версиях справочников.

    Поля:
    - `id`: Идентификатор версии (целое число).
    - `dictionary`: Ссылка на справочник
    (целое число, идентификатор справочника).
    - `version`: Версия справочника (строка).
    - `start_date`: Дата начала действия версии (дата).

    Примеры:
    - Преобразование экземпляра модели в JSON:
      ```json
      {
        "id": 1,
        "dictionary": 1,
        "version": "1.0",
        "start_date": "2022-01-01"
      }
      ```
    """
    class Meta:
        model = DictionaryVersion
        fields = ['id', 'dictionary', 'version', 'start_date']


class DictionaryElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для элементов справочников.

    Этот сериализатор преобразует экземпляры модели `DictionaryElement` в
    формат JSON и наоборот. Он используется для представления информации о
    элементах конкретной версии справочника.

    Поля:
    - `code`: Код элемента справочника (строка).
    - `value`: Значение элемента справочника (строка).

    Примеры:
    - Преобразование экземпляра модели в JSON:
      ```json
      {
        "code": "001",
        "value": "Пример значения"
      }
      ```
    """
    class Meta:
        model = DictionaryElement
        fields = ['code', 'value']
