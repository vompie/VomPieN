from TeleVompy.Interface.window import Window

from database.sql import get_user_by_id, get_user, update_user_by_id
from update_client import update_client


class BanUser(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '☠️'
        self.Page.Content.title = 'Забанить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return
        
        user = await get_user_by_id(id=self.relayed_payload.Us)
        update_result = await update_user_by_id(id=self.relayed_payload.Us, columns=['is_banned', 'user_lvl'], values=[1, 0])
        if not update_result:
            return
        await update_client(tlg_id=user['tlg_id'], enabled=False)


class UnBanUser(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '😇'
        self.Page.Content.title = 'Разбанить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return
        
        user = await get_user_by_id(id=self.relayed_payload.Us)
        update_result = await update_user_by_id(id=self.relayed_payload.Us, columns=['is_banned', 'user_lvl'], values=[0, 0])
        if not update_result:
            return
        await update_client(tlg_id=user['tlg_id'], enabled=False)
        

class PromotionAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🦷'
        self.Page.Content.title = 'Повысить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return
        
        await update_user_by_id(id=self.relayed_payload.Us, columns=['user_lvl'], values=[1])


class DemotedAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🧄'
        self.Page.Content.title = 'Разжаловать'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return
        
        await update_user_by_id(id=self.relayed_payload.Us, columns=['user_lvl'], values=[-1])
