from TeleVompy.Interface.window import Window

from settings import BOT_NAME


class Advantage(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '⭐️'
        self.Page.Content.title = f'Почему тебе стоит выбрать именно {BOT_NAME}?'

    async def constructor(self) -> None:
        self.set_advantage('Современный протокол VLESS', 'специально разработанный для обхода интернет-цензуры протокол. Он обеспечивает гибкое и устойчивое соединение, которое маскируется под обычный интернет-трафик')
        self.set_advantage('Глобальная доступность', f'несмотря на то, что <b>{BOT_NAME}</b> находится в Германии, для всех сервисов подключение выглядит как из Америки. Это значит, что ты получаешь неограниченный доступ к контенту без лишних ограничений и с минимальным ping!')
        self.set_advantage('Устойчивость к блокировкам', f'забудь о проблемах с доступом к сервисам, которые блокируют соединения через прокси или VPN. С <b>{BOT_NAME}</b> ты сможешь безпрепятственно заходить на любые платформы (в том числе <b>ChatGPT</b>, <b>Notion</b> и <b>YouTube</b>), где бы ты ни находился!')
        self.set_advantage('Дополнительная безопасность для пользователей .RU', f'для пользователей с доменами в зоне RU предусмотрено дополнительное прокси-соединение. Это не только обеспечивает доступ к сервисам вроде Госуслуг, но и значительно увеличивает защиту <b>{BOT_NAME}</b> от блокировок и проверок со стороны Роскомнадзора')
        self.set_advantage('Защита от нежелательного контента', f'<b>{BOT_NAME}</b> заботится о твоем комфорте! Включенные блокировки рекламы и вредоносных сайтов создают безопасную среду для серфинга')
        self.set_advantage('Мгновенные уведомления', f'служба уведомлений Apple работает напрямую, ислючая <b>{BOT_NAME}</b>, так что ты никогда не пропустишь важные события. Никаких задержек – только мгновенные оповещения!')
        self.Page.Content.text += f'Пробуй <b>{BOT_NAME}</b> уже сегодня и открой новые горизонты анонимного и свободного интернета! 🌍✨'

        self.Page.add_button(model='BBck', row=0, title='В меню', callback=self.CallBack.create(dad='MM'))
        self.Page.add_button(model='Keys', row=0)
    

    def set_advantage(self, title, text) -> None:
        point = '🔹'
        full_title = self.Page.Content.html(title).bold()
        self.Page.Content.text += f"{point} {full_title}: {text}\n\n"