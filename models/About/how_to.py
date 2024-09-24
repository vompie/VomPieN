from TeleVompy.Interface.window import Window
from settings import BOT_NAME


class HowTo(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '💡'
        self.Page.Content.title = 'Использование'
        self.Page.Content.text = f'Для подключения к {BOT_NAME} необходимо установить приложение, поддерживающее протокол VLESS\nМногие из них предоставляют визуальный интерфейс, облегчающий настройку и управление подключениями\nТы можешь выбрать клиент в зависимости от используемой операционной системы и устройства\nВот некоторые из них ⤵️\n'

    async def constructor(self) -> None:
        # Cross-platform
        self.Page.Content.text += self.Page.Content.html('\nCross-platform\n').bold()
        # Hiddify
        self.set_about(
            title='Hiddify',
            des='Кроссплатформенный клиент для любой современной OS, который предлагает широкий спектр возможностей: автоматический выбор узла, режим настройки, удаленные профили и т.д.',
            des_dop='Удобный интерфейс, не содержит рекламы и поддерживает все необходимые протоколы',
            link='https://github.com/hiddify/hiddify-next'
        )
        # Qv2ray
        self.set_about(
            title='Qv2ray',
            des='Это кроссплатформенное приложение, доступное для Windows, macOS и Linux',
            des_dop='Платформа-агностичный интерфейс, поддержка нескольких транспортов и протоколов, поддержка подписок',
            link='https://github.com/Qv2ray/Qv2ray'
        )

        # Windows
        self.Page.Content.text += self.Page.Content.html('\nWindows\n').bold()
        # V2RayN
        self.set_about(
            title='V2RayN',
            des='Популярный графический интерфейс, который поддерживает множество протоколов, включая VLESS',
            des_dop='Удобный интерфейс, поддержка нескольких серверов, автоматическое обновление подписок, интеграция с другими VPN',
            link='https://github.com/2dust/v2rayN'
        )
        # Nekobox
        self.set_about(
            title='Nekobox',
            des='Cамый функциональный, удобный и продуманный клиент c поддержкой множества протоколов',
            des_dop='Интерфейс действительно удобный: сервера можно группировать по вкладкам и шарить стандартной ссылкой или QR-кодом',
            link='https://github.com/MatsuriDayo/nekoray'
        )

        # Android
        self.Page.Content.text += self.Page.Content.html('\nAndroid\n').bold()
        # V2RayNG
        self.set_about(
            title='V2RayNG',
            des='Мобильное приложение для Android, один из самых популярных клиентов для Android',
            des_dop='Легкий и интуитивно понятный интерфейс, поддержка различных протоколов, включая VLESS и VMess',
            link='https://github.com/2dust/v2rayNG'
        )
        # Nekobox Android
        self.set_about(
            title='Nekobox Android',
            des='Nekobox только под Android',
            des_dop='Поддерживает всё, что актуально на сегодняшний день',
            link='https://github.com/2dust/v2rayNG'
        )

        # iOS
        self.Page.Content.text += self.Page.Content.html('\niOS\n').bold()
        # Shadowrocket
        self.set_about(
            title='Shadowrocket',
            des='Платное и самое функциональное приложение для iOS',
            des_dop='Поддержка множества протоколов, включая VLESS, интуитивно понятный интерфейс, работа с прокси',
            link='https://apps.apple.com/us/app/shadowrocket/id932747118'
        )
        # Streisand
        self.set_about(
            title='Streisand',
            des='Популярный бесплатный клиент с поддержкой всех современных протоколов',
            des_dop='Минималистичный интерфейс и отсутствие рекламы',
            link='https://apps.apple.com/us/app/streisand/id6450534064'
        )
        # FoXray
        self.set_about(
            title='FoXray',
            des='Один из лучших бесплатных клиентов, который поддерживает все что нужно',
            des_dop='Приятный интерфейс и работа без проблем',
            link='https://apps.apple.com/ru/app/foxray/id6448898396'
        )

        # macOS
        self.Page.Content.text += self.Page.Content.html('\nmacOS\n').bold()
        # V2RayX
        self.set_about(
            title='V2RayX',
            des='Приложение для macOS, которое позволяет легко настроить и подключиться через VLES',
            des_dop='Простота настройки, интеграция с macOS, поддержка VLESS',
            link='https://github.com/Cenmrev/V2RayX'
        )

        self.Page.add_button(model='BBck', row=0, title='В меню', callback=self.CallBack.create(dad='MM'))


    def set_about(self, title: str, des: str, link: str, des_dop: str = '') -> None:
        # title
        full_title = self.Page.Content.html(title).bold()
        # description
        des_dop = f"{self.Page.Content.html(des_dop).italic()}\n" if des_dop else ''
        download = self.Page.Content.html('Установить').link(link)
        # text
        full_text = self.Page.Content.html(f'{full_title}\n{des}\n{des_dop}\n{download}', husk=False).quote_exp()
        self.Page.Content.text += f"\n{full_text}\n"
