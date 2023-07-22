from aiogram import Router


def get_handlers_router() -> Router:
    from tg_bot.handlers.user import get_user_router
    from tg_bot.handlers.admin import get_admin_router

    router = Router()

    user_router = get_user_router()
    admin_router = get_admin_router()

    router.include_router(user_router)
    router.include_router(admin_router)

    return router
