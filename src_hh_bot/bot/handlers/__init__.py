from aiogram import Router


def setup_message_routers() -> Router:
    from . import (any_unknown_message, start, reg_one, reg_two)
    router = Router()
    router.include_router(start.router)
    router.include_router(reg_one.router)
    router.include_router(reg_two.router)
    router.include_router(any_unknown_message.router)
    
    # router.include_router(bot_messages.router)
    return router