from ..messenger import Messenger, Message


class Invoice(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Send the invoice message
        
        Parameters
        ----------
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """
        super().__init__(*args, **kwargs)

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        message = await self.bot.send_invoice(
            chat_id=self.User.chat_id,
            title=self.Page.Payment.title,
            description=self.Page.Payment.description,
            provider_token=self.payments_token,
            currency=self.Page.Payment.currency,
            is_flexible=self.Page.Payment.is_flexible,
            prices=self.Page.Payment.prices,
            start_parameter=self.Page.Payment.start_parameter,
            payload=self.Page.Payment.payload,
            message_effect_id=self.Page.effect
        )

        return message
