class BotResponse:
    ru_ = None
    en_ = None

    def __init__(self, **kwargs) -> None:
        self.format_kwargs = None

        for key, arg in kwargs.items():
            setattr(self, key, arg)

    def format(self, **format_kwargs) -> 'BotResponse':
        self.format_kwargs = format_kwargs
        return self

    def get_response(self, language: str = 'ru') -> str:
        content_attribute = 'en_' if language is None else language + '_'

        if not hasattr(self, content_attribute):
            content_attribute = 'en_'

        content = getattr(self, content_attribute)

        if self.format_kwargs:
            content = content.format(**self.format_kwargs)
            
        return content


bot_responses = {
    'do_not_know': BotResponse(
        ru_='Я пока не знаю ответа на этот вопрос. Попробуйте связаться по следующему адресу: ...',
        en_='I don\'t know the answer'
    ),
    'cant_answer_information': BotResponse(
        ru_='Я не встречался с этим вопросом. Попробуйте пожалуйста связаться по следующему номеру: ...',
        en_='I have never seen the question. Try to find out it here...'
    ),
    'invalid_language': BotResponse(
        en_='I can understand only Russian or English, sorry.'
    ),
    'start_off_top': BotResponse(
        ru_='Расскажите как дела?',
        en_='How is it going?'
    ),
    'start_consultation': BotResponse(
        ru_='Расскажите что вас беспокоит',
        en_='Please, tell me what you are worring about?'
    ),
    'start_information': BotResponse(
        ru_='Вот похожий случай',
        en_='There is similar question'
    ),
    'disease_review': BotResponse(
        ru_=(
            'У вас кажется {disease_name} с вероятностью {disease_probability}.\n'
            'Вывод сделан на основе того, что у вас наблюдаются следующие симптомы: '
            '{symptoms_list}\n'
            'Лечитесь, не болейте!'
        ),
        en_=(
            'Seems like your disease is {disease_name} with {disease_probability} probability.\n'
            'The review is conducted because you have below symtoms: '
            '{symptoms_list}\n'
        ),
    ),
}

action_responses = {
    'do_not_know': BotResponse(
        ru_='Я не знаю такого действия',
        en_='Invalid action. Please try to connect with developers'
    ),
    'like': BotResponse(
        ru_='Хорошо, мы учтем!',
        en_='Okay, thanks!'
    ),
    'dislike': BotResponse(
        ru_='Хорошо, мы учтем! Попытаемся исправится в следующем обновлении',
        en_='Okay, thanks! We will try to fix it.'
    ),
    'switch_to_operator': BotResponse(
        ru_='Переключаем на оператора.',
        en_='We are switching you to the operator.'
    ),
    'break_conversation': BotResponse(
        ru_='Вы остановили общение.',
        en_='You have just stopped the conversation'
    ),
}