from handlers import start, menu, payment, cancellation, referral_link
from handlers.admin import export_to_excel, mailing, accept_or_decline, respond_to_application, show_menu, change_mission_text, stats
from middlewares.registration import RegistrationMiddleware
from aiogram import Dispatcher
from middlewares.db import DbSessionMiddleware
from data.database import sessionmaker


async def setup_dispatcher(dispatcher: Dispatcher):
    dispatcher.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dispatcher.message.middleware(RegistrationMiddleware())
    dispatcher.include_routers(start.router, menu.router, export_to_excel.router,
                               mailing.router, accept_or_decline.router, respond_to_application.router,
                               payment.router, cancellation.router, show_menu.router, change_mission_text.router,
                               stats.router, referral_link.router)

