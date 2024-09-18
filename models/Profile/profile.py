from TeleVompy.Interface.window import Window
from database.sql import get_user_by_id, get_user_keys, update_user_by_id


class Profile(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🧛🏻'
        self.Page.Content.title = 'Личный кабинет'

    async def constructor(self) -> None:
        
        user = await get_user_by_id(id=self.relayed_payload.Us)
        keys = await get_user_keys(tlg_id=user['tlg_id'], enabled=None)

        # Имя
        username = user['tlg_id']
        if user['username']:
            username = f"@{user['username']}"
        if user['is_admin'] == -1:
            username = f"{username} (разжалован)"
        self.Page.Content.title = f'{username}'
        # Зарегистрирован
        self.Page.Content.text += f"Зарегистрирован: {user['created_at']}"
        # Количество ключей
        self.Page.Content.text += f"\nКлючей: {len(keys)}"

        # Разжаловать администратора
        # is_block = self.User.chat_id == user['tlg_id'] 
        # self.Page.add_button(model='DemotedAdmin', row=0, callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='can_demoted_yourself')
        # Назад
        # self.Page.add_button(model='BBck', row=1, callback=self.CallBack.copy(payload=self.relayed_payload))
        # self.Page.add_button(model='BBck', row=0, title='В меню', callback=self.CallBack.create(dad='MM'))
        # Ключи
        self.Page.add_button(model='Keys', row=1, callback=self.CallBack.copy(payload=self.relayed_payload))  
    