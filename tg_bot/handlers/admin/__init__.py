from aiogram import Router


def get_admin_router() -> Router:
    from . import admin_menu

    router = Router()
    router.include_router(admin_menu.router)

    return router