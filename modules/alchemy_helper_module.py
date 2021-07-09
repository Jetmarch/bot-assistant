from bot_module import BotModule



class AlchemyHelperModule(BotModule):
    def __init__(self, vk, db) -> None:
        super().__init__(vk, db)
        self.keywords.extend(['алхимия', 'варки', 'алхим'])
        self.module_name = 'AlchemyHelper'
        self.module_states = {
            None: self.first_stage,
            '1':self.first_stage,
            '2': self.second_stage
        }

    def update(self):
        return super().update()

    def process_request(self, event):
        module_state_for_current_user = self.db.get_user_state(self.module_name, event.user_id)
        if module_state_for_current_user:
            self.module_states[module_state_for_current_user[0]](event)
        else:
            self.first_stage(event)

    def first_stage(self, event):
        #TODO: сделать список сообщений-приветствий и рандомить их каждый раз
        self.vk.send_message(event.user_id, 'Доброй пожаловать в модуль алхимии!\n Укажите количество затраченного катализатора')
        self.db.set_user_state(self.module_name, event.user_id, '2')

    def second_stage(self, event):
        user_arguments = []
        catalyst_cost = 413.25
        count_of_ingredients = 5
        for word in event.text.split():
            if word.isdigit():
                user_arguments.append(int(word))
        if len(user_arguments) != 0:
            total_cost = user_arguments[0] * count_of_ingredients * catalyst_cost
            self.vk.send_message(event.user_id, 'Общие затраты {0}'.format(total_cost))
            self.db.close_user_state(self.module_name, event.user_id)
        else:
            self.vk.send_message(event.user_id, 'Укажите количество катализатора')

        