import datetime
import locale


def get_formatted_date():
    """Возвращает текущую дату и время в формате 'День недели, день месяца месяц часы:минуты'."""
    try:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    except locale.Error:
        print("Warning: Could not set locale to ru_RU.UTF-8.  Using default locale.")

    now = datetime.datetime.now()
    return now.strftime("%A, %d %B %H:%M")


current_date = get_formatted_date()
print(current_date)