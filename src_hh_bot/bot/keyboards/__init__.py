from .base import k_back, k_back_reply, k_cancel
from .factories import Ban, Form, Response, Tag
from .form_fields import k_form_fields, rk_back_to_menu_form
from .menu import (
    k_end_viewing_form,
    k_main_menu,
    k_my_form_menu,
    k_promocode_menu,
    k_start_menu,
    k_view_form_menu,
)
from .options_menu import (
    k_accept_or_reject,
    k_ban,
    k_confirm_del_form,
    k_options_for_photo,
    k_skip,
    k_subscribe,
    k_view_response,
)
from .tags import (
    ik_gen_tags_form_12,
    ik_gen_tags_form_34,
    rk_gen_tags_form_12,
    rk_gen_tags_form_34,
)
from .types_of_reg import k_types_of_reg
