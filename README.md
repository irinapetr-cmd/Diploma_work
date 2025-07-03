# Автоматизированное тестирование сервиса Кинопоиск

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Pytest](https://img.shields.io/badge/pytest-8.3.5-green)
![Allure](https://img.shields.io/badge/allure-2.14.3-orange)
![Selenium](https://img.shields.io/badge/selenium-4.33.0-red)

Этот проект содержит автоматизированные тесты для веб-сайта и API Кинопоиска.

## Структура проекта

- `config/` - настройки и тестовые данные
- `pages/` - Page Object модели
- `tests/` - тесты (UI и API)
- `utils/` - вспомогательные утилиты

## 📋 Предварительные требования

Перед началом работы убедитесь, что у вас установлено:
- Python 3.7 или новее
- Браузеры Chrome и Firefox
- Allure Commandline ([инструкция по установке](https://docs.qameta.io/allure/#_installing_a_commandline))

## ⚙️ Установка

1. Клонируйте репозиторий:
bash
git clone https://github.com/ваш-username/ваш-репозиторий.git
cd ваш-репозиторий

## Зависимости

Установите зависимости из файла `requirements.txt`: 
pip install -r requirements.txt

## Запуск всех тестов:


## Запуск только UI тестов:
pytest tests/test_ui.py -m ui --alluredir=allure-results
pytest tests/ --alluredir=allure-results
## Запуск только API тестов:
pytest tests/test_api.py -m api --alluredir=allure-results

## Для генерации отчета Allure:
allure serve allure-results

## Тестовые данные

Тестовые данные можно изменить в файле `config/test_data.py`.
