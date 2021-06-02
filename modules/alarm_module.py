from bot_module import BotModule



class AlarmModule(BotModule):
    def __init__(self, vk) -> None:
        super().__init__(vk)
        self.keywords.extend(['будильник', 'таймер', 'напоминание', 'напомни'])

    
    def update(self):
        return super().update()


    def process_request(self, event):
        self.vk.send_message(event, "Заглушка будильника/напоминаний")
        
