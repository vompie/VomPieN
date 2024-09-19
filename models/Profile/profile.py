from TeleVompy.Interface.window import Window
from database.sql import get_user_by_id, get_user_keys, get_user, update_user_by_id, update_client


class Profile(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🧛🏻'
        self.Page.Content.title = 'Личный кабинет'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        # from users/admins or main menu
        if self.relayed_payload.Us:
            user = await get_user_by_id(id=self.relayed_payload.Us)
        else:
            user = await get_user(tlg_id=self.User.chat_id)
        # get keys
        enabled_keys = await get_user_keys(tlg_id=user['tlg_id'], enabled=True)
        all_keys = await get_user_keys(tlg_id=user['tlg_id'], enabled=None)
        # username for admin mode
        if self.self_profile['is_admin'] > 0:
            username = user['tlg_id']
            if user['username']:
                username = f"@{user['username']}"
            level = ''
            if user['is_admin'] == -1:
                level = '(разжалован)'
            elif user['is_admin'] > 0:
                level = f"(администратор {user['is_admin']}ур.)"
            self.Page.Content.title =  f"{username} {level}"
        # created at
        self.Page.Content.text += f"Зарегистрирован: {user['created_at']}"
        # keys count
        self.Page.Content.text += f"\nКлючей: {len(enabled_keys)}/{len(all_keys)}"
        
        # control buttons for admin mode
        is_block = self.self_profile['tlg_id'] == user['tlg_id'] or user['is_admin'] >= self.self_profile['is_admin']
        if self.self_profile['is_admin'] > 0:
            # unban
            if user['is_banned']:
                self.Page.add_button(model='UnBanUser', row=0, callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='cant_unban_yourself')
            # ban
            else:
                self.Page.add_button(model='BanUser', row=0, callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='cant_ban_yourself')
            if user['is_banned']:
                is_block = True
            # demoted from admin 
            if user['is_admin'] > 0: 
                self.Page.add_button(model='DemotedAdmin', row=0, callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='cant_demoted_yourself')
            # promotion to admin
            else:
                self.Page.add_button(model='PromotionAdmin', row=0, callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='cant_promotion_yourself')
        # back button
        # to main menu
        if self.self_profile['is_admin'] < 1 or not self.relayed_payload.Us:
            self.Page.add_button(model='BBck', row=1, title='В меню', callback=self.CallBack.create(dad='MM'))
        # to admins
        elif user['is_admin'] > 0:
            self.Page.add_button(model='BBck', row=1, callback=self.CallBack.copy(payload=self.relayed_payload))
        # to users
        else:
            self.Page.add_button(model='BBck', row=1, callback=self.CallBack.copy(payload=self.relayed_payload))

        # keys button
        # if self.relayed_payload.Us
        self.Page.add_button(model='UAKeys', row=1, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload))  


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
        await update_client(tlg_id=user['tlg_id'], columns=['is_enabled'], values=[0])
        self.relayed_payload.dad = 'Profile'

    
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
        await update_client(tlg_id=user['tlg_id'], columns=['is_enabled'], values=[1])
        self.relayed_payload.dad = 'Profile'


class PromotionAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🦷'
        self.Page.Content.title = 'Повысить'
        self.Action.action_type = "click"

    async def constructor(self) -> None:
        await update_user_by_id(id=self.relayed_payload.Us, columns=['is_admin'], values=[1])
        self.relayed_payload_recreate(items={'dad': 'Users'})


class DemotedAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🧄'
        self.Page.Content.title = 'Разжаловать'
        self.Action.action_type = "click"

    async def constructor(self) -> None:
        await update_user_by_id(id=self.relayed_payload.Us, columns=['is_admin'], values=[-1])
        self.relayed_payload_recreate(items={'dad': 'Admins'})
