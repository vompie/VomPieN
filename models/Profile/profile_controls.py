from TeleVompy.Interface.window import Window


from database.sql import get_user_by_id, get_user, update_user
from update_client import update_client


class BanUser(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '☠️'
        self.Page.Content.title = 'Забанить'
        self.Action.set_action(ActionType=self.Action.types.TOGGLE)

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            return self.Action.set_action(ActionType=self.Action.types.REDIRECT, redirect_to='MM')
        
        # get user
        user = await get_user_by_id(id=self.relayed_payload.Us)
        if not user:
            return
        
        # update user
        update_result = await update_user(tlg_id=user['tlg_id'], columns=['is_banned', 'user_lvl'], values=[1, 0])
        if not update_result:
            return

        await update_client(tlg_id=user['tlg_id'], enabled=False)

        # add subseq message
        self.SubsequentMessage.add(page=self.create_page(model_name='UpdCfg'))

        # send information message
        from bot_service.utils import send_msg
        await send_msg(chat_id=user['tlg_id'], model='InfoMsg', title='Твой аккаунт забанен', text='Обнови список команд: /menu')


class UnBanUser(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '😇'
        self.Page.Content.title = 'Разбанить'
        self.Action.set_action(ActionType=self.Action.types.TOGGLE)

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            return self.Action.set_action(ActionType=self.Action.types.REDIRECT, redirect_to='MM')
        
        # get user
        user = await get_user_by_id(id=self.relayed_payload.Us)
        if not user:
            return
        
        # update user   
        update_result = await update_user(tlg_id=user['tlg_id'], columns=['is_banned', 'user_lvl'], values=[0, 0])
        if not update_result:
            return
        
        await update_client(tlg_id=user['tlg_id'], enabled=True)

        # add subseq message
        self.SubsequentMessage.add(page=self.create_page(model_name='UpdCfg'))
        
        # send information message
        from bot_service.utils import send_msg
        await send_msg(chat_id=user['tlg_id'], model='InfoMsg', title='Твой аккаунт разбанен', text='Обнови список команд: /menu')
        

class PromotionAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🦷'
        self.Page.Content.title = 'Повысить'
        self.Action.set_action(ActionType=self.Action.types.TOGGLE)

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            return self.Action.set_action(ActionType=self.Action.types.REDIRECT, redirect_to='MM')
        
        # get user
        user = await get_user_by_id(id=self.relayed_payload.Us)
        if not user:
            return

        # update user
        update_result = await update_user(tlg_id=user['tlg_id'], columns=['user_lvl'], values=[1])
        if not update_result:
            return
        
        # send information message
        from bot_service.utils import send_msg
        await send_msg(chat_id=user['tlg_id'], model='InfoMsg', title='Ты повышен до администратора', text='Обнови список команд: /menu')


class DemotedAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🧄'
        self.Page.Content.title = 'Разжаловать'
        self.Action.set_action(ActionType=self.Action.types.TOGGLE)

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            return self.Action.set_action(ActionType=self.Action.types.REDIRECT, redirect_to='MM')
        
        # get user
        user = await get_user_by_id(id=self.relayed_payload.Us)
        if not user:
            return

        update_result = await update_user(tlg_id=user['tlg_id'], columns=['user_lvl'], values=[-1])
        if not update_result:
            return
        
        # send information message
        from bot_service.utils import send_msg
        await send_msg(chat_id=user['tlg_id'], model='InfoMsg', title='Ты разжалован', text='Обнови список команд: /menu')
