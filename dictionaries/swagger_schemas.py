from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


dictionary_list_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'date', openapi.IN_QUERY, description="Дата в формате ГГГГ-ММ-ДД (опционально)",
            type=openapi.TYPE_STRING, required=False
        )
    ],
    responses={
        200: openapi.Response(
            description="Список справочников",
            examples={
                "application/json": {
                    "refbooks": [
                        {"id": 1, "code": "001", "name": "Справочник 1", "description": "Описание 1"},
                        {"id": 2, "code": "002", "name": "Справочник 2", "description": "Описание 2"}
                    ]
                }
            }
        ),
        400: "Неверный формат даты. Используйте ГГГГ-ММ-ДД."
    }
)

dictionary_elements_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'version', openapi.IN_QUERY, description="Версия справочника (опционально)",
            type=openapi.TYPE_STRING, required=False
        )
    ],
    responses={
        200: openapi.Response(
            description="Список элементов справочника",
            examples={
                "application/json": {
                    "elements": [
                        {"code": "001", "value": "Пример элемента 1"},
                        {"code": "002", "value": "Пример элемента 2"}
                    ]
                }
            }
        )
    }
)

check_element_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'code', openapi.IN_QUERY, description="Код элемента справочника (обязательно)",
            type=openapi.TYPE_STRING, required=True
        ),
        openapi.Parameter(
            'value', openapi.IN_QUERY, description="Значение элемента справочника (обязательно)",
            type=openapi.TYPE_STRING, required=True
        ),
        openapi.Parameter(
            'version', openapi.IN_QUERY, description="Версия справочника (опционально)",
            type=openapi.TYPE_STRING, required=False
        )
    ],
    responses={
        200: openapi.Response(
            description="Результат проверки",
            examples={
                "application/json": {"exists": True},
                "application/json": {"exists": False}
            }
        ),
        404: "Версия справочника не найдена"
    }
)
