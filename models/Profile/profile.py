from TeleVompy.Interface.window import Window

from settings import BOT_SMILE, MAX_CLIENT_KEYS, MAX_ADMINS_KEYS
from database.sql import get_user, get_user_left_join_keys, get_user_left_join_keys_by_user_id, get_user_by_key_id


class Profile(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = BOT_SMILE
        self.Page.Content.title = 'Профиль'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # from users_admins -> admin
        if self.relayed_payload.Bt == 'UsersAdmins':
            user_keys = await get_user_left_join_keys_by_user_id(id=self.relayed_payload.Us)
        # from keys -> admin
        if self.relayed_payload.Bt == 'AdminPanel':
            user = await get_user_by_key_id(id=self.relayed_payload.Ks)
            user_keys = await get_user_left_join_keys(tlg_id=user['tlg_id'])
        # from main menu/command -> user
        else:
            user_keys = await get_user_left_join_keys(tlg_id=self.User.chat_id) 

        # username for admin mode
        if self.self_profile['user_lvl'] > 0:
            # username
            username = f"@{user_keys[0]['username']}" if user_keys[0]['username'] else user_keys[0]['tlg_id']
            status = '(пользователь)'
            if user_keys[0]['user_lvl'] == -1:
                status = '(разжалован)'
            elif user_keys[0]['user_lvl'] > 0:
                status = f"(администратор {user_keys[0]['user_lvl']}ур.)"
            elif user_keys[0]['is_banned'] == 1:
                status = '(забанен)'
            self.Page.Content.title =  f"{username} {status}"
        # keys count
        if len(user_keys) == 1 and not user_keys[0]['cid']:
            keys_count = 0
        elif len(user_keys) == 1 and user_keys[0]['cid']:
            keys_count = 1
        else:
            keys_count = len(user_keys)
        # max generate keys
        max_keys = MAX_CLIENT_KEYS
        if user_keys[0]['is_banned']:
            max_keys = -1
        elif user_keys[0]['user_lvl'] == 1:
            max_keys = MAX_ADMINS_KEYS
        elif user_keys[0]['user_lvl'] > 1:
            max_keys = 99
        keys_count = f"Ключей (всего/максимально): {keys_count}/{max_keys}"
        # invites count
        invites_count = f"Друзей приведено: {user_keys[0]['referals']}"
        # created at
        created_at = f"Зарегистрирован: {user_keys[0]['users_created_at']}"
        # full info
        full_info = f"{invites_count}\n{keys_count}\n{created_at}"
        self.Page.Content.text = self.Page.Content.html(full_info).code()

        # control buttons for admin mode
        if self.self_profile['user_lvl'] > 0 and self.relayed_payload.Bt:
            is_block = (self.self_profile['tlg_id'] == user_keys[0]['tlg_id']) or (user_keys[0]['user_lvl'] >= self.self_profile['user_lvl'])
            # unban / ban
            if user_keys[0]['is_banned']:
                self.Page.add_button(model='UnBanUser', row=0, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload), block=is_block, answer='cant_unban')
            else:
                self.Page.add_button(model='BanUser', row=0, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload), block=is_block, answer='cant_ban')
            # demoted / promotion from admin
            if user_keys[0]['is_banned']:
                is_block = True 
            if user_keys[0]['user_lvl'] > 0: 
                self.Page.add_button(model='DemotedAdmin', row=0, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload), block=is_block, answer='cant_demoted')
            else:
                self.Page.add_button(model='PromotionAdmin', row=0, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload), block=is_block, answer='cant_promotion')
        
        # back button        
        if self.relayed_payload.Bt == 'UsersAdmins':
            self.Page.add_button(model='BBck', row=1, callback=self.CallBack.copy(payload=self.relayed_payload, dad='UsersAdmins'))
        elif self.relayed_payload.Bt == 'AdminPanel':   
            self.Page.add_button(model='BBck', row=1, callback=self.CallBack.copy(payload=self.relayed_payload, dad='Keys'))
        else:
            self.Page.add_button(model='BBck', row=1, title='В меню', callback=self.CallBack.create(dad='MM'))

        # keys button for admins
        if self.self_profile['user_lvl'] > 0 and self.relayed_payload.Bt == 'UsersAdmins':
            self.Page.add_button(model='Keys', row=1, callback=self.CallBack.copy(payload=self.relayed_payload, dad=self.name))
        # new key button for admins
        elif self.self_profile['user_lvl'] > 0 and self.relayed_payload.Bt == 'AdminPanel':
            # max generate keys for UsersAdmins and MainMenu views
            max_keys = MAX_CLIENT_KEYS
            if user_keys[0]['is_banned']:
                max_keys = -1
            elif self.self_profile['user_lvl'] == 1:
                max_keys = MAX_ADMINS_KEYS
            elif self.self_profile['user_lvl'] > 1:
                max_keys = 99
            is_block = len(user_keys) >= max_keys
            # new key button
            self.Page.add_button(model='NewKey', row=1, title='Добавить ключ', callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='cant_create_key')
        # invite user button for users
        else:
            self.Page.add_button(model='InviteUser', row=1, title='Привести друга')  
