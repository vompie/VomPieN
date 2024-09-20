from TeleVompy.Interface.window import Window
from database.sql import get_user_by_id, get_user_keys, get_user, update_user_by_id, update_client, update_client_by_tlg_id


class Profile(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🧛🏻'
        self.Page.Content.title = 'Личный кабинет'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # from users/admins
        if self.relayed_payload.Us:
            user = await get_user_by_id(id=self.relayed_payload.Us)
        # from main menu/command/profile
        else:
            user = await get_user(tlg_id=self.User.chat_id)

        # get keys
        enabled_keys = await get_user_keys(tlg_id=user['tlg_id'], enabled=True)
        all_keys = await get_user_keys(tlg_id=user['tlg_id'], enabled=None)
        # username for admin mode
        if self.self_profile['is_admin'] > 0:
            username = f"@{user['username']}" if user['username'] else user['tlg_id']
            level = ''
            if user['is_admin'] == -1:
                level = '(разжалован)'
            elif user['is_admin'] > 0:
                level = f"(администратор {user['is_admin']}ур.)"
            elif user['is_banned'] == 1:
                level = '(забанен)'
            self.Page.Content.title =  f"{username} {level}"
        # created at
        self.Page.Content.text += f"Зарегистрирован: {user['created_at']}"
        # keys count
        self.Page.Content.text += f"\nКлючей: {len(enabled_keys)}/{len(all_keys)}"

        # control buttons for admin mode
        is_block = (self.self_profile['tlg_id'] == user['tlg_id']) or (user['is_admin'] >= self.self_profile['is_admin'])
        if self.self_profile['is_admin'] > 0 and self.relayed_payload.dad != None and self.relayed_payload.dad != 'MM':
            # unban / ban
            if user['is_banned']:
                self.Page.add_button(model='UnBanUser', row=0, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload), block=is_block, answer='cant_unban')
            else:
                self.Page.add_button(model='BanUser', row=0, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload), block=is_block, answer='cant_ban')
            # demoted / promotion from admin
            if user['is_banned']:
                is_block = True 
            if user['is_admin'] > 0: 
                self.Page.add_button(model='DemotedAdmin', row=0, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload), block=is_block, answer='cant_demoted')
            else:
                self.Page.add_button(model='PromotionAdmin', row=0, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload), block=is_block, answer='cant_promotion')
        
        # set Back to
        if not self.relayed_payload.Bt:
            self.relayed_payload.Bt = 'Profile'

        # back button
        if not self.relayed_payload.dad or self.relayed_payload.dad == 'MM' or self.relayed_payload.Bt == 'Profile':
            self.Page.add_button(model='BBck', row=1, title='В меню', callback=self.CallBack.create(dad='MM'))
        else:
            self.Page.add_button(model='BBck', row=1, callback=self.CallBack.copy(payload=self.relayed_payload, dad=self.relayed_payload.Bt))
        
        # keys button
        self.Page.add_button(model='Keys', row=1, callback=self.CallBack.copy(payload=self.relayed_payload, dad=self.name))  


class BanUser(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '☠️'
        self.Page.Content.title = 'Забанить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        user = await get_user_by_id(id=self.relayed_payload.Us)
        if not user:
            return
        await update_user_by_id(id=self.relayed_payload.Us, columns=['is_banned', 'is_admin'], values=[1, 0])
        await update_client_by_tlg_id(tlg_id=user['tlg_id'], columns=['is_enabled'], values=[0])

class UnBanUser(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '😇'
        self.Page.Content.title = 'Разбанить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        user = await get_user_by_id(id=self.relayed_payload.Us)
        if not user:
            return
        await update_user_by_id(id=self.relayed_payload.Us, columns=['is_banned'], values=[0])
        await update_client_by_tlg_id(tlg_id=user['tlg_id'], columns=['is_enabled'], values=[1])
        

class PromotionAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🦷'
        self.Page.Content.title = 'Повысить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        await update_user_by_id(id=self.relayed_payload.Us, columns=['is_admin'], values=[1])

class DemotedAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🧄'
        self.Page.Content.title = 'Разжаловать'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        await update_user_by_id(id=self.relayed_payload.Us, columns=['is_admin'], values=[-1])
