from bot_module import BotModule



class AlchemyHelperModule(BotModule):
    def __init__(self, vk) -> None:
        super().__init__(vk)
        self.keywords.extend(['алхимия', 'варки', 'алхим'])

    def update(self):
        return super().update()

    def process_request(self, event):
        user_arguments = []
        for word in event.text.split():
            if word.isdigit():
                user_arguments.append(int(word))
        catalyst_cost = 413.25
        count_of_ingredients = 5
        total_cost = user_arguments[0] * count_of_ingredients * catalyst_cost

        self.vk.send_message(event.user_id, 'Общие затраты {0}'.format(total_cost))  