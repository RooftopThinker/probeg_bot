import asyncio
import aiohttp
from config import AMOCRM_TOKEN, SYSADMIN_ID, TerminalKey, PASSWORD, NotificationURL, PRICE
import hashlib
import datetime


async def new_lead(full_name, phone, email, telegram_id, telegram_username, referrer_telegram_id, referrer_full_name,
                   referrer_telegram_username, company_name, position):
    url = 'https://probusinessandsport.amocrm.ru/api/v4/leads/complex'
    data = [
        {
            "name": f"Сделка {full_name}",
            "pipeline_id": 9213346,
            "status_id": 73994858,
            "_embedded": {
                "contacts": [
                    {
                        "name": full_name,
                        "created_by": 0,
                        "custom_fields_values": [
                            {
                                "field_id": 1347645,
                                "values": [
                                    {
                                        "value": phone
                                    }
                                ]
                            },
                            {
                                "field_id": 1347647,
                                "values": [
                                    {
                                        "value": email
                                    }
                                ]
                            },
                            {
                                "field_id": 1374583,
                                "values": [
                                    {
                                        "value": telegram_id
                                    }
                                ]
                            },
                            {
                                "field_id": 1354009,
                                "values": [
                                    {
                                        "value": telegram_username
                                    }
                                ]
                            },
                            {
                                "field_id": 1374585,
                                "values": [
                                    {
                                        "value": referrer_telegram_id
                                    }
                                ]
                            },
                            {
                                "field_id": 1354013,
                                "values": [
                                    {
                                        "value": referrer_full_name
                                    }
                                ]
                            },
                            {
                                "field_id": 1354015,
                                "values": [
                                    {
                                        "value": referrer_telegram_username
                                    }
                                ]
                            },
                            {
                                "field_id": 1375007,
                                "values": [
                                    {
                                        "value": company_name
                                    }
                                ]
                            },
                            {
                                "field_id": 1347643,
                                "values": [
                                    {
                                        "value": position
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    ]
    headers = {"Authorization": f"Bearer {AMOCRM_TOKEN}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, timeout=10, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"Ошибка при POST запросе к {url}: {e}")
        return None
    except asyncio.TimeoutError:
        print(f"Превышен таймаут при POST запросе к {url}")
        return None


async def notify_sysadmin(bot, message):
    await bot.send_message(text=message, chat_id=SYSADMIN_ID)


def generate_token(params: dict, password: str) -> str:
    """
    Генерирует токен (подпись) для запроса по правилам, указанным в документации.
    """

    params_with_password = params.copy()
    params_with_password['Password'] = password

    sorted_params = dict(sorted(params_with_password.items()))

    concatenated_string = ''.join(str(value) for value in sorted_params.values())

    sha256_hash = hashlib.sha256(concatenated_string.encode('utf-8')).hexdigest()

    return sha256_hash


async def init_payment(telegram_id):
    """
    Создаёт платёж
    """
    url = 'https://securepay.tinkoff.ru/v2/Init'
    params = {
        "TerminalKey": TerminalKey,

        "Amount": PRICE,

        "OrderId": int(str(datetime.datetime.utcnow().timestamp()).split('.')[0] + str(telegram_id)),

        "NotificationURL": NotificationURL,

        "PayType": 'O'}
    token = generate_token(params, PASSWORD)
    params['Token'] = token
    headers = {'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params, timeout=10, headers=headers) as response:
            response.raise_for_status()
            return await response.json(), params


params = {
    "TerminalKey": "1733912605907DEMO",
    "Amount": 140000,
    "OrderId": "13",
    "NotificationURL": "https://rkaype-185-8-125-251.ru.tuna.am/test/"
}

token = generate_token(params, PASSWORD)
print(token)

