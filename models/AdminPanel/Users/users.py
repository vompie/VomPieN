from TeleVompy.Interface.window import Window
from database.sql import get_users


class Users(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '👥'
        self.Page.Content.title = 'Пользователи'

    async def constructor(self) -> None:
        # get users
        users = await get_users(admins=False)
        # back button
        self.Page.add_button(model='BBck', row=1, callback=self.CallBack.create(dad='AdminPanel'))     
        # return immediately
        if not users or not len(users):
            return 
        # pagination
        self.Pagination.add(dataset=users, content_setter=self.content_setter, id_getter=self.id_getter)

        # callback
        callback = self.CallBack.copy(payload=self.relayed_payload, dad=self.name)
        callback.payload.Us = self.relayed_payload.sl
        callback.payload.del_attr(attr='sl')

        # info button
        self.Page.add_button(model='Profile', row=1, title='Посмотреть', callback=callback, block=(not self.relayed_payload.sl), answer='user_not_select')


    def content_setter(self, item: dict) -> tuple[str, str]:
        header = item['tlg_id']
        if item['username']:
            header = f"@{item['username']}"
        footer = f"Зарегистрирован: {item['created_at']}"
        return header, footer

    def id_getter(self, item: dict) -> None:
        return item['id']
