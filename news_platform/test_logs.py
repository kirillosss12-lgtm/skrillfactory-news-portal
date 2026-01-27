import os
import django
import logging

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_platform.settings')  # Укажите ваше имя проекта
django.setup()


def run_tests():
    # Получаем логгеры
    log_django = logging.getLogger('django')
    log_request = logging.getLogger('django.request')
    log_security = logging.getLogger('django.security')
    log_db = logging.getLogger('django.db.backends')

    print("\n--- ЗАПУСК ТЕСТОВ ЛОГИРОВАНИЯ ---")

    # 1. Тест консоли (работает при DEBUG = True)
    print("\n[1] Проверка консоли:")
    log_django.debug("DEBUG: Сообщение без пути.")
    log_django.warning("WARNING: Сообщение с PATHNAME.")
    try:
        1 / 0
    except ZeroDivisionError:
        log_django.error("ERROR: Сообщение со СТЕКОМ.")

    # 2. Тест файлов (при DEBUG = False)
    print("\n[2] Проверка файлов (если DEBUG=False):")
    log_django.info("INFO: Должно быть в general.log.")
    log_security.info("SECURITY: Должно быть в security.log.")

    # 3. Тест errors.log и Почты
    print("\n[3] Проверка ошибок и почты:")
    try:
        raise Exception("Тестовая ошибка запроса")
    except Exception:
        # Должно быть в errors.log (со стеком) и на почте (БЕЗ стека)
        log_request.error("Ошибка в django.request!", exc_info=True)


if __name__ == "__main__":
    run_tests()