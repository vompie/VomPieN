from TeleVompy.Interface.window import Window

from database.sql import get_users, get_user


class UsersAdmins(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '👥' # '🧙🏻'
        self.Page.Content.title = 'Пользователи' # 'Администраторы'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return
        
        # users or admins
        is_admins = True if self.relayed_payload.Adm else False
        if is_admins:
            self.Page.smile = '🧙🏻'
            self.Page.Content.title = 'Администраторы'

        # get users/admins
        users_admins = await get_users(admins=is_admins)

        # back button
        self.Page.add_button(model='BBck', row=1, callback=self.CallBack.create(dad='AdminPanel'))

        # return immediately
        if not users_admins or not len(users_admins):
            return
         
        # setup select
        if self.relayed_payload.Us:
            self.relayed_payload.sl = self.relayed_payload.Us
            self.relayed_payload_del_attr(attr='Us')
            
        # pagination
        self.Pagination.add(dataset=users_admins, content_setter=self.content_setter, id_getter=self.id_getter)

        # callback
        callback = self.CallBack.copy(payload=self.relayed_payload, dad=self.name)
        callback.payload.Us = self.relayed_payload.sl
        callback.payload.Bt = self.name
        callback.payload.del_attr(attr='sl')

        # info button
        self.Page.add_button(model='Profile', row=1, callback=callback, block=(not self.relayed_payload.sl), answer='user_admin_not_select')


    def content_setter(self, item: dict) -> tuple[str, str]:
        # header
        username = f"@{item['username']}" if item['username'] else item['tlg_id']
        status = '(пользователь)'
        if item['user_lvl'] == -1:
            status = '(разжалован)'
        elif item['user_lvl'] > 0:
            status = f"(администратор {item['user_lvl']}ур.)"
        elif item['is_banned'] == 1:
            status = '(забанен)'
        header = f"{username} {status}"
        # footer
        invites = f"Друзей приведено: {item['referals']}"
        created_at = f"Зарегистрирован: {item['created_at']}"
        footer = f"{invites}\n{created_at}"
        footer = self.Page.Content.html(footer).code()
        return header, footer

    def id_getter(self, item: dict) -> None:
        return item['id']
