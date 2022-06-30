import random
from collections.abc import Iterable


SUPPORT_LANGUAGE_FORMATS = ['ru', 'en']


class BotResponse:
    ru_ = ''
    en_ = ''

    def __init__(self, **kwargs) -> None:
        self.format_kwargs = None

        for key, arg in kwargs.items():
            setattr(self, key, arg)

    def format(self, **format_kwargs) -> 'BotResponse':
        self.format_kwargs = format_kwargs
        return self

    def get_kwargs(self) -> dict:
        if self.format_kwargs is not None:
            return self.format_kwargs
        
        return {}

    def get_response(self, language: str = 'ru') -> str:
        content_attribute = language or '' + '_'
        content = getattr(self, content_attribute, None)

        if not content:
            content = getattr(self, 'ru_', None) or getattr(self, 'en_')
        
        if isinstance(content, list):
            content = random.choice(content)

        if self.format_kwargs:
            content = content.format(**self.format_kwargs)
            
        return content

    def __add__(self, other: 'BotResponse') -> 'BotResponse':
        response = BotResponse()

        for lang in SUPPORT_LANGUAGE_FORMATS:
            content_attr = ''.join([lang, '_'])

            setattr(
                response, 
                content_attr,
                ' '.join([self.get_response(lang), other.get_response(lang)])
            )

        format_kwargs = {}
        format_kwargs.update(self.get_kwargs())
        format_kwargs.update(other.get_kwargs())

        response.format(**format_kwargs)

        return response


bot_responses = {
    'do_not_know': BotResponse(
        ru_='Я пока не знаю ответа на этот вопрос. Попробуйте связаться по следующему адресу: ...',
        en_='I don\'t know the answer'
    ),
    'cant_answer_information': BotResponse(
        ru_='Я не знаю ответ на этот вопрос. Попробуйте пожалуйста связаться по следующему номеру: ...',
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
    'internal_error': BotResponse(
        ru_='Что-то пошло не так. Попробуйте связаться с разработчиками или остановить общение. Ошибка: {error}',
        en_='Something is wrong. Try to contact the developers or interrupt the conversation. Error: {error}'
    ),
    'disease_review': BotResponse(
        ru_=(
            'С вероятностью {disease_probability}% у вас {disease_name}.\n'
        ),
        en_=(
            'Seems like your disease is {disease_name} with {disease_probability}%.\n'
        ),
    ),
    'default_details': BotResponse(
        ru_=[
            'Думаю вам стоит связаться с врачами с следующими симптомами {symptoms_list}. Вы можете это сделать нажав на кнопку.',
            'Мои предположения могут быть ошибочными, но в любом случае стоит связаться с врачами.',
        ]
    ),
    'appendicitis_details': BotResponse(
        ru_=[
            (
                'Если приступ острой боли миновал, это не значит, что вы в безопасности. Пожалуйста, '
                'свяжитесь с медиками по телефону 122, вам необходимо сдать тест и выяснить точный диагноз!'
            ),
            (
                'Для решения, что именно следует предпринять дальше необходимо вызвать скорую помощь, '
                'это можно сделать по телефону 122'
            ),
            (
                'Я собрал Ваши симптомы и готов передать их в службу скорой помощи, нажмите подтверждение действия'
            ),
            (
                'К сожалению, аппендицит не является безобидной болезнью и требует своевременно '
                'оказанной неотложной помощи, давайте позвоним в 122'
            ),
            (
                'Имеет смысл связаться с медиками и вызвать скорую помощь, так как осложнения от '
                'аппендицита могут серьезно влиять на жизнеспособность человека'
            )
        ]
    ),
    'orvi_details': BotResponse(
        ru_=[
            'Это нередкое явление для наших широт… Вам нужны жаропонижающие препараты, капли для носа и покой. Я бы также советовал вызвать врача. Вызываем?',
            'Я собрал следующие симптомы {symptoms_list} и готов их передать в регистратуру вашей поликлиники, давайте вызовем врача на дом?',
            'Это значит, что кто-то из окружающих передал Вам вирус. Само по себе ОРВИ не опасно. Однако могут случиться осложнения при неправильном назначении препаратов. Давайте на всякий случай вызовем доктора?',
            'Не стоит недооценивать это заболевание, давайте вызовем врача? Для этого я готов передать собранные симптомы в регистратуру.',
        ]
    ),
    'migraine_details': BotResponse(
        ru_=[
            'Вам следует обеспечить себе покой, прекратить любую работу, особенно физическую. Стоит положить на голову холодный компресс и лечь на кровать. Для купирования головной боли примите анальгетик. Желательно вызвать врача!',
            'Вам нужен свежий воздух, по возможности стоит лечь. Для купирования головной боли примите анальгетик. Если у вас еще нет четких рекомендаций от вашего постоянного доктора, давайте вызовем участкового врача на дом, он поможет выбрать нужное лекарство и научиться узнавать приступ мигрени заранее. Вызываем?',
            'Это заболевание довольно типично для жителей мегаполиса,  принято считать, чт ос ним можно справиться самостоятельно (помогут анальгетики), однако я советую также проконсультироваться с врачом: мы можем оформить заявку на приход врача на дом или записать вас на прием в поликлинику.'
        ]
    )
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
