from aiogram import Router


def get_user_router() -> Router:
    from . import main_user_menu, strategy_user

    router = Router()
    router.include_router(main_user_menu.router)
    router.include_router(strategy_user.router)

    return router
