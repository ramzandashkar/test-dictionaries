from django.db import models


class Dictionary(models.Model):
    """
    Модель справочника.

    Эта модель представляет справочник, который содержит информацию о
    различных категориях или типах данных. Справочник имеет уникальный код,
    название и необязательное описание.

    Поля:
    - `code`: Уникальный код справочника (строка).
    - `name`: Название справочника (строка).
    - `description`: Описание справочника (строка, опционально).

    Методы:
    - `__str__()`: Возвращает название справочника.
    """
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return self.name


class DictionaryVersion(models.Model):
    """
    Модель версии справочника.

    Эта модель представляет версию конкретного справочника. Каждая версия
    имеет уникальное название, дату начала действия и связана с определённым
    справочником.

    Поля:
    - `dictionary`: Ссылка на справочник,
     к которому относится версия (внешний ключ).
    - `version`: Название версии справочника (строка).
    - `start_date`: Дата начала действия версии (дата).

    Методы:
    - `__str__()`: Возвращает название справочника и версию.
    """
    dictionary = models.ForeignKey(
        Dictionary, on_delete=models.CASCADE, related_name='versions',
    )
    version = models.CharField(max_length=50)
    start_date = models.DateField()

    class Meta:
        unique_together = ('dictionary', 'version', 'start_date')
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"

    def __str__(self):
        return f"{self.dictionary.name} - {self.version}"


class DictionaryElement(models.Model):
    """
    Модель элемента справочника.

    Эта модель представляет элемент конкретной версии справочника.
    Каждый элемент имеет уникальный код и значение,
    которые ассоциированы с определённой версией.

    Поля:
    - `version`: Ссылка на версию справочника,
    к которой относится элемент (внешний ключ).
    - `code`: Код элемента справочника (строка).
    - `value`: Значение элемента справочника (строка).

    Методы:
    - `__str__()`: Возвращает код и значение элемента.
    """
    version = models.ForeignKey(
        DictionaryVersion, on_delete=models.CASCADE, related_name='elements'
    )
    code = models.CharField(max_length=100)
    value = models.CharField(max_length=300)

    class Meta:
        unique_together = ('version', 'code')
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"

    def __str__(self):
        return f"{self.code}: {self.value}"
