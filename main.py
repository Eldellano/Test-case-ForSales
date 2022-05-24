import requests
from bitrix24 import *
from datetime import date, timedelta, datetime
from typing import NoReturn
from art import tprint
import schedule
import time


def new_task_for_bitrix(holiday: date) -> NoReturn:
    """Создаем новую задачу в bitrix24"""

    print('[+] Пытаемся отправить')
    bx24 = Bitrix24('https://b24-p0k65a.bitrix24.ru/rest/1/i4bneefsemxn248o/')
    bx24.callMethod('tasks.task.add', fields={'TITLE': 'Грядет праздник!',
                                              'DESCRIPTION': f'{holiday} будет государственный праздник',
                                              'RESPONSIBLE_ID': 1,
                                              'START_DATE_PLAN': holiday})
    print('[+] Задача в bitrix24 создана')


def get_day():
    """Получаем дату (сегодня + 3 дня), проверяем будний ли это день,
    если будний, проверяем является ли он выходным.
    Если выходной в будний день значит день праздничный"""

    date_for_check = date.today() + timedelta(days=3)
    print('[+] Проверка запущена')
    if datetime.isoweekday(date_for_check) in range(1, 6):
        resp = requests.get(f'https://isdayoff.ru/{date_for_check}')
        if resp.text == '1':  # 0 - рабочий день, 1 - нерабочий день
            tprint("HOLIDAY", font="small")
            new_task_for_bitrix(date_for_check)  # создаем задачу в bitrix24
        else:
            print('[+] Не праздник, увы(')


def main():
    """Запускаем проверку по расписанию, каждый день в 03:00"""

    print('[+] Проверка по расписанию запущена')
    schedule.every().day.at('03:00').do(get_day)
    # print(schedule.idle_seconds())
    while True:
        schedule.run_pending()
        time.sleep(1)  # прерываем выполнение -> защищаемся от высокой нагрузки на cpu


if __name__ == '__main__':
    main()
