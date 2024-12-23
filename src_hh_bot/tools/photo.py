from aiogram.utils.media_group import MediaGroupBuilder


def ids_to_media_group(ids: list, caption: str = None):
    media_group = MediaGroupBuilder(caption=caption)
    for id_ in ids:
        media_group.add_photo(media=id_)
    return media_group.build()
