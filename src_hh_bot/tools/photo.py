from aiogram.utils.media_group import MediaGroupBuilder


def ids_to_media_group(string_ids: str, caption: str = None):
    ids = ids_to_list(string_ids)
    media_group = MediaGroupBuilder(caption=caption)
    for id_ in ids:
        media_group.add_photo(media=id_)
    return media_group.build()


def ids_to_list(string_ids: str):
    ids = list(map(lambda x: x.strip(), string_ids.split(",")))
    return ids
