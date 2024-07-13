from aiogram.filters import Filter
from aiogram.types import Message
import tools


class GetTextButton(Filter):
    def __init__(self, name: str) -> None:
        self.name = name

    async def __call__(self, message: Message) -> bool:
        return message.text == await tools.get_text_button(self.name)


class FilterByTag(Filter):

    async def __call__(self, message: Message) -> bool:
        return (
            message.text in await tools.get_tags()
            or message.text in await tools.get_tags(name_tags="tags_form_34")
        )

