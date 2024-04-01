from aiogram.utils.media_group import MediaGroupBuilder


def parser_ids_photo(string_ids: str):
    ids = list(map(lambda x: x.strip(), string_ids.split()))
    media_group = MediaGroupBuilder()
    for id_ in ids:
       media_group.add_photo(media=id_)
    return media_group.build()