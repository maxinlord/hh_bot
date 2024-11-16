from aiogram import Router


def setup_message_routers() -> Router:
    from . import (
        admin,
        answ_responses,
        any_unknown_message,
        commands,
        errors,  # noqa: F401
        my_form,
        reg_four,
        reg_one,
        reg_three,
        reg_two,
        start,
        subscribe,
        view_form,
    )

    router = Router()
    router.include_router(start.router)
    router.include_router(reg_one.router)
    router.include_router(reg_two.router)
    router.include_router(reg_three.router)
    router.include_router(reg_four.router)
    router.include_router(view_form.router)
    router.include_router(my_form.router)
    router.include_router(answ_responses.router)
    router.include_router(commands.router)
    router.include_router(admin.router)
    router.include_router(subscribe.router)
    router.include_router(any_unknown_message.router)
    # router.include_router(errors.router)

    # router.include_router(bot_messages.router)
    return router
