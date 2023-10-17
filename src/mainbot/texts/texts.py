import datetime
from functools import reduce
from src.core.models import Worker, User


async def start_text(project_manager: str, support: str) -> str:
    text = f"""Добро пожаловать в SeoHub⬛️🟧 

💒В твоем распоряжении несколько комнат для подъема твоего SEO💒 
🍌Каждая комната индивидуальна, ведь мы делаем всю работу вручную💦 

💵Стоимость услуги 100 рублей💵 

Менеджер проекта: {project_manager}
Техническая поддержка: {support}"""
    return text


async def profile_text(user: User, user_name: str) -> str:
    text = f"""📱 Ваш профиль: 
➖➖➖➖➖➖➖➖➖➖➖➖➖ 
🔑 Мой ID: {user.id} 
👤 Логин: {user_name} 
➖➖➖➖➖➖➖➖➖➖➖➖➖
💳 Баланс: {user.balance} рублей
✨ Всего заказов: {user.count_orders}"""
    return text


async def information_text(project_manager: str, support: str, theme: str) -> str:
    text = f"""❓Условия манибека: 
⛓SEO не должно быть меньше 45
⛓Видео залито не более 1 часа назад
⛓Канал зарегистрирован не раньше 2021 г.
⛓На канале должно быть более 500 сабов
⛓Видео не должно быть удалено или скрыто
⛓Каждый 4-ый неудачный заказ подряд будет в ЛЮБОМ случае считаться без манибека !

💵Баланс бота выводу не подлежит 
🥷🏻Администрация оставляет за собой право заблокировать пользователя за неуважительное поведение,оскорбление (без возврата имеющихся средств)
☠️За багоюз и умышленное причинение вреда боту выдается БАН
👨🏼‍💻Менеджер проекта: {project_manager}
👨🏼‍💻Техническая поддержка: {support} (писать при возникновении ошибок в боте) 
👨🏼‍💻Тема на форуме: {theme}"""
    return text


async def queue_text(workers: list[Worker]) -> str:
    text = """✅ - Комната открыта
❌ - Комната закрыта

"""
    for worker in workers:
        text += f"\n {'✅' if worker.status else '❌'}{worker.room_emoji}{worker.room_name}{worker.room_emoji} - {worker.busy_spot}/{worker.all_spot}"

    return text


async def payment_text(amount: int, pay_id: int) -> str:
    text = f"Оплата счета на: {amount} рублей \nID заказа: {pay_id}"
    return text


async def log_payment_text(
    state: str,
    now: datetime.datetime,
    external_id: int,
    user_name: str,
    pay_id: str,
    amount: int,
    balance: int = 0,
    method: str = "",
    currency: str = "",
) -> str:
    text = {
        "waiting": f"\n{now}:::> Пользователь @{user_name} {external_id}  проводит попытку пополнения заказа: {pay_id} на сумму {amount} рублей",
        "success": f"\n{now}:::> Пользователь @{user_name} {external_id}  пополнил баланс на сумму: {amount}, id заказа: {pay_id}, баланс пользователя: {balance} метод оплаты: {method} {currency}",
        "broadcast": f"Пользователь @{user_name} пополнил баланс на сумму {amount} рублей ({currency})",
    }

    return text[state]


async def price_text(price: int) -> str:
    text = f"""<b>SeoHub⬛️🟧
🔥Стоимость услуги {price} рублей🔥

Отправьте ссылку на видео:</b>"""
    return text


async def video_response_text(
    video_time: bool, channel_time: bool, channel_sub: bool, seo: bool
) -> str:
    moneyback = all([video_time, channel_time, channel_sub, seo])
    text = ""
    text += "\nSEO &gt; 45" if not seo else ""
    text += "\nВидео выложено более часа наза" if not video_time else ""
    text += "\nКанал создан менее 2 лет назад" if not channel_time else ""
    text += "\nНа канале меньше 500 сабов" if not channel_sub else ""
    text += (
        "\nКомната может принять ❗Без манибека❗"
        if not moneyback
        else "\nВидео удовлетворяет всем условиям"
    )
    text += "\nС вашего баланса списано 100 рублей, ожидайте ответ от комнаты"
    return text


async def worker_order_text(
    moneyback: bool,
    url: str,
    user_id: int,
    user_name: str,
    seo: float,
    created_time: datetime.timedelta,
    subs: int,
    views: int,
    tags: list[str],
) -> str:
    text = f"""Заказ на SEO
Ссылка на видео: {url}
Заказал: {user_id} @{user_name}
{'Заказ без манибека❗️❗️❗️' if not moneyback else 'Заказ c манибеком❗️❗️❗️'}
SEO = {seo}
Загружено = {created_time.seconds//3600} часов назад
Сабы = {subs}
Просмотры = {views}
Теги:
{tags} 
"""

    return text


async def worker_order_access_text(
    order_id: str, order_url: str, user_id: int, user_name: str
) -> str:
    text = f"Вы успешно приняли заказ #{order_id}.\nВидео: {order_url}\nЗаказал:{user_id} @{user_name} \nОтметьте его выполнение"

    return text


async def user_waiting_order_text(photo_name: str, video_id: str) -> str:
    text = (
        f"Пока твой заказ в работе {photo_name} поможет скоротать время❤\n"
        f"Заказ в работе😮‍💨 #{video_id}"
    )

    return text


async def log_order_text(
    state: str, worker_id: int, worker_name: str, video_id: str
) -> str:
    text = {
        "waiting": f"\n{datetime.datetime.now()}:::> Воркер {worker_id} {worker_name} взял заказ #: {video_id}",
        "success": f"\n{datetime.datetime.now()}:::> Воркер {worker_id} {worker_name} выполнил заказ #: {video_id}",
        "failed": f"\n{datetime.datetime.now()}:::> Воркер {worker_id} {worker_name} не выполнил заказ #: {video_id}",
    }

    return text[state]


async def report_order_text(video_id: str, worker: Worker, moneyback: bool) -> str:
    text = f"""Заказ #{video_id} был успешно выполнен
Выполнила комната: {worker.room_emoji}{worker.room_name}{worker.room_emoji}
ID-администратора {worker.id}
{'Видео с манибеком' if moneyback else 'Видео без манибека'}"""

    return text


async def check_seo_text(url: str, seo: float, tags: list[str]) -> str:
    text = f"""Видео: {url}
SEO: {seo}
Теги:
{tags}"""

    return text


async def room_free_text(worker: Worker) -> str:
    text = f"""Комната {worker.room_emoji}{worker.room_name}{worker.room_emoji} освободилась
успей сделать заказ!!!"""

    return text


async def user_information_text(
    user_id: int, user_name: str, balance: int, accept_info: bool
) -> str:
    text = f"""Информация о пользователе:

ID: {user_id}
Name: @{user_name}
Balance: {balance}
Accept: {accept_info}

Укажи что хочешь изименить, например
Balance 500"""

    return text


async def admin_info_text(users: list[User], info: dict) -> str:
    text = f"""⚙️Статистика бота SeoHub

🤵Активных пользователей: {len(users)} чел.
🤵💰Баланс активных пользователей: {reduce(lambda x, y: x+y, [user.balance for user in users])}  руб.
📈SEO-заказов: {reduce(lambda x, y: x+y, [user.count_orders for user in users])}  шт.
Касса:"""

    for coin, coin_info in info.items():
        text += f"\n{coin_info['currency']} : {coin_info['amount']} --> {coin_info['amount_rub']}"

    text += f"\n Общая сумма: {reduce(lambda x,y: x+y, [coin_info['amount_rub'] for (coin, coin_info) in info.items()])}"

    return text
