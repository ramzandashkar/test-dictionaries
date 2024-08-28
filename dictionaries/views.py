from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dictionary, DictionaryElement, DictionaryVersion
from .serializers import DictionarySerializer, DictionaryElementSerializer
from .swagger_schemas import (
    dictionary_list_schema, dictionary_elements_schema, check_element_schema,
)


class DictionaryListView(APIView):
    """
    Получение списка справочников.

    Этот метод обрабатывает GET-запросы для получения списка справочников.
    Можно указать опциональный параметр `date`, чтобы получить только те
    справочники, которые имеют действительные версии на указанную дату.

    Параметры запроса:
    - `date` (опционально): Дата в формате ГГГГ-ММ-ДД. Если указана, возвращает
      только справочники с версиями, чья дата начала (`start_date`)
      до или на указанную дату. Если параметр не указан, возвращаются все
      справочники.

    Формат ответа:
    - `refbooks`: Список справочников. Каждый справочник содержит поля:
        - `id`: Идентификатор справочника.
        - `code`: Код справочника.
        - `name`: Название справочника.

    Примеры:
    - Запрос без параметров:
      `GET /refbooks/`
      Ответ: Все доступные справочники.

    - Запрос с параметром `date`:
      `GET /refbooks/?date=2024-08-30`
      Ответ: Справочники с версиями, действительными на 30 августа 2024 года.

    В случае ошибки в формате даты возвращается код состояния 400 с сообщением
    об ошибке:.
    {
    "error": "Неверный формат даты. Используйте ГГГГ-ММ-ДД."
    }
    """

    @dictionary_list_schema
    def get(self, request, *args, **kwargs):
        date = request.query_params.get('date')

        if date:
            try:
                query_date = timezone.datetime.strptime(
                    date, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {"error": "Неверный формат даты. Используйте ГГГГ-ММ-ДД."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            queryset = Dictionary.objects.filter(
                versions__start_date__lte=query_date
            ).distinct()
        else:
            queryset = Dictionary.objects.all()

        serializer = DictionarySerializer(queryset, many=True)

        response_data = {"refbooks": serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)


class DictionaryElementsView(APIView):
    """
    Получение элементов справочника.

    Этот метод обрабатывает GET-запросы для получения элементов справочника по
    его идентификатору. Можно указать опциональный параметр `version` для
    получения элементов конкретной версии справочника.

    Параметры запроса:
    - `version` (опционально): Версия справочника. Если указана, возвращает
      только элементы этой версии. Если параметр не указан, возвращаются
      элементы всех версий справочника.

    Параметры URL:
    - `id`: Идентификатор справочника.

    Формат ответа:
    - `elements`: Список элементов справочника. Каждый элемент содержит поля:
        - `code`: Код элемента.
        - `value`: Значение элемента.

    Примеры:
    - Запрос для получения элементов справочника с ID 1:
      `GET /refbooks/1/elements/`
      Ответ: Все элементы справочника с ID 1.

    - Запрос для получения элементов конкретной версии:
      `GET /refbooks/1/elements/?version=1.0`
      Ответ: Элементы версии 1.0 справочника с ID 1.
    """

    @dictionary_elements_schema
    def get(self, request, *args, **kwargs):
        dictionary_id = self.kwargs['id']
        version = self.request.query_params.get('version')

        if version:
            elements = DictionaryElement.objects.filter(
                version__dictionary_id=dictionary_id, version__version=version
            )
        else:
            elements = DictionaryElement.objects.filter(
                version__dictionary_id=dictionary_id
            )

        serializer = DictionaryElementSerializer(elements, many=True)

        response_data = {"elements": serializer.data}

        return Response(response_data)


class CheckElementView(APIView):
    """
    Проверка существования элемента справочника.

    Этот метод обрабатывает GET-запросы для проверки, существует ли элемент
    справочника с заданным кодом и значением в определенной версии справочника.
    Если версия не указана, проверяется текущая версия справочника.

    Параметры запроса:
    - `code`: Код элемента справочника.
    - `value`: Значение элемента справочника.
    - `version` (опционально): Версия справочника. Если указана, проверяет
      элемент в этой версии. Если параметр не указан, проверяется элемент
      в текущей версии справочника.

    Параметры URL:
    - `id`: Идентификатор справочника.

    Формат ответа:
    - `exists`: Логическое значение (`true` или `false`), указывающее на
      существование элемента с заданным кодом и значением в указанной версии
      справочника.

    Примеры:
    - Запрос для проверки элемента в текущей версии:
      `GET /refbooks/1/check-element/?code=001&value=Пример`
      Ответ: `{"exists": true}` или `{"exists": false}`.

    - Запрос для проверки элемента в конкретной версии:
      `GET /refbooks/1/check-element/?code=001&value=Пример&version=1.0`
      Ответ: `{"exists": true}` или `{"exists": false}`.

    В случае, если версия не найдена, возвращается код состояния 404 с
    соответствующим сообщением.
    """

    @check_element_schema
    def get(self, request, id):
        code = request.query_params.get('code')
        value = request.query_params.get('value')
        version_param = request.query_params.get('version')

        if version_param:
            try:
                version = DictionaryVersion.objects.get(
                    dictionary_id=id, version=version_param
                )
            except DictionaryVersion.DoesNotExist:
                return Response(
                    {"exists": False}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            current_date = timezone.now().date()
            version = DictionaryVersion.objects.filter(
                dictionary_id=id, start_date__lte=current_date
            ).order_by('-start_date').first()

            if not version:
                return Response(
                    {"exists": False}, status=status.HTTP_404_NOT_FOUND
                )

        exists = DictionaryElement.objects.filter(
            version=version, code=code, value=value
        ).exists()

        return Response(
            {"exists": exists},
            status=status.HTTP_200_OK
        )
