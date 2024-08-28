from django.urls import path
from .views import (
    DictionaryListView, DictionaryElementsView, CheckElementView,
)

app_name = 'refbooks'

urlpatterns = [
    path('', DictionaryListView.as_view(), name='list'),
    path('<int:id>/elements/', DictionaryElementsView.as_view(),
         name='elements'),
    path('<int:id>/check-element/', CheckElementView.as_view(),
         name='check-element'),
]

"""
URL конфигурация для справочников.

Определяет маршруты для работы со справочниками, их элементами и
проверки элементов:
- `list`: Получение списка всех справочников или фильтрация по дате.
- `elements`: Получение элементов конкретного справочника по его
идентификатору.
- `check-element`: Проверка наличия элемента в конкретной версии справочника.
"""