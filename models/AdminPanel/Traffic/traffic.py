from TeleVompy.Interface.window import Window

from database.sql import get_user
from statsquery import stats_query

class Traffic(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '📈'
        self.Page.Content.title = 'Трафик'
        self.Page.Content.text = 'Его нет'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            return self.Action.set_action(ActionType=self.Action.types.REDIRECT, redirect_to='MM')

        result, stats_str = await stats_query()
        print(result, stats_str)

        # back button        
        self.Page.add_button(model='BBck', row=0, callback=self.CallBack.create(dad='AdminPanel'))
    