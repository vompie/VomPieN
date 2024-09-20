from TeleVompy.Interface.window import Window
from database.sql import get_users, get_user


class Admins(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🧙🏻'
        self.Page.Content.title = 'Администраторы'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return
        
        # get admins
        admins = await get_users(admins=True)

        # back button
        self.Page.add_button(model='BBck', row=1, callback=self.CallBack.create(dad='AdminPanel'))

        # return immediately
        if not admins or not len(admins):
            return
        
        # setup select
        if self.relayed_payload.Us:
            self.relayed_payload.sl = self.relayed_payload.Us
            self.relayed_payload_del_attr(attr='Us')
        # pagination
        self.Pagination.add(dataset=admins, content_setter=self.content_setter, id_getter=self.id_getter)

        # callback
        callback = self.CallBack.copy(payload=self.relayed_payload, dad=self.name)
        callback.payload.Us = self.relayed_payload.sl
        callback.payload.Bt = self.name
        callback.payload.del_attr(attr='sl')

        # new admin button
        # self.Page.add_button(model='Profile', row=1, title='Профиль', callback=callback, block=(not self.relayed_payload.sl), answer='admin_not_select')
        
        # info button
        self.Page.add_button(model='Profile', row=1, title='Профиль', callback=callback, block=(not self.relayed_payload.sl), answer='admin_not_select')


    def content_setter(self, item: dict) -> tuple[str, str]:
        header = f"@{item['username']}" if item['username'] else item['tlg_id']
        footer = f"Уровень: {item['user_lvl']}\nЗарегистрирован: {item['created_at']}"
        # привел людей: ...
        return header, footer

    def id_getter(self, item: dict) -> None:
        return item['id']
    