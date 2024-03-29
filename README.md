# Python CSK modulation module

Реализация модулятора и демодулятора CSK (модуляция циклическим сдвигом) для ГНСС

## Запуск приложения
- Установка виртуального окружения

Для настройки виртуального окружения рекомендуется установить менеджер пакетов
`poetry`. Инструкцию по установке см на [Официальном сайте](https://python-poetry.org/docs/#installing-with-the-official-installer)

- Активация виртуального окружения Poetry. `poetry shell`

- Установка зависимостей `poetry install`

- Запуск приложения `python3 main.py`. Для очистки локального кеша перед
  запуском нужно добавить флаг `--flush-cache`. Команда будет выглядить
  следующим образом: `python3 main.py --flush-cache`.

## Блоки программы
1. Генератор M-последовательности
2. CSK-модулятор
3. CSK-демодулятор
4. Графический модуль для отображения результатов на графиках

## Техническое задание

### Цель данного програмного обеспечения

Обеспечить возможность наглядного исследования (с графиками) эффекстивности
CSK модуляции для использоваения в спутниковых навигационных системах.

Также данное ПО должно легко конфигурироваться и иметь параметы для настройки.

### Описание модулей ПО

##### Генератор M-последовательности
Данный модуль берётся из прошлой работы. Для совместимости с данным
программным обеспечением генератор требует доработок и рефакторинга.

В качестве параметра принимает длину последовательности

#### CSK модулятор
Моудлятор берёт модулируемое сообщение, разбивает его на слова, затем
согласно алфавиту сдвигает исходную последовательность и перемножает на её
несдвинутую версию. После данной операции исходный сигнал домножается на косинус.

#### CSK демодулятор
Имеется две возможности реализации:
- С использованием банка корреляторов и вычислением максимальной корреляции
- С использованием преобразования Фурье

В данном ПО будет реализована версия, в основе которой лежит Быстрое Преобразование
Фурье.

Демодулятор на основе БПФ работает следующим образом:
- Делает БПФ ПСП
- Делает БПФ входного сигнала
- Перемножает два сигнала
- На выходе получается ОБПФ произведения двух сигналов

В качестве параметра принимает длину алфавита

#### Графический модуль
Для графического модуля используется библиотеки plotly и dash
