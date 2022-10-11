import random
from collections.abc import Iterable


SUPPORT_LANGUAGE_FORMATS = ["ru", "en"]


class BotResponse:
    ru_ = ""
    en_ = ""

    def __init__(self, **kwargs) -> None:
        self.format_kwargs = None

        for key, arg in kwargs.items():
            setattr(self, key, arg)

    def format(self, **format_kwargs) -> "BotResponse":
        self.format_kwargs = format_kwargs
        return self

    def get_kwargs(self) -> dict:
        if self.format_kwargs is not None:
            return self.format_kwargs

        return {}

    def get_response(self, language: str = "ru") -> str:
        content_attribute = (language or "") + "_"
        content = getattr(self, content_attribute, None)

        if not content:
            content = getattr(self, "ru_", None) or getattr(self, "en_")

        if isinstance(content, list):
            content = random.choice(content)

        if self.format_kwargs:
            content = content.format(**self.format_kwargs)

        return content

    def __add__(self, other: "BotResponse") -> "BotResponse":
        response = BotResponse()

        for lang in SUPPORT_LANGUAGE_FORMATS:
            content_attr = "".join([lang, "_"])

            setattr(
                response,
                content_attr,
                " ".join([self.get_response(lang), other.get_response(lang)]),
            )

        format_kwargs = {}
        format_kwargs.update(self.get_kwargs())
        format_kwargs.update(other.get_kwargs())

        response.format(**format_kwargs)

        return response


bot_responses = {
    "do_not_know": BotResponse(
        ru_="Я пока не знаю ответа на этот вопрос. Попробуйте связаться по следующему адресу: ...",
        en_="I don't know the answer",
    ),
    "cant_answer_information": BotResponse(
        ru_="Я не знаю ответ на этот вопрос. Попробуйте пожалуйста связаться по следующему номеру: ...",
        en_="I have never seen the question. Try to find out it here...",
    ),
    "invalid_language": BotResponse(
        en_="I can understand only Russian or English, sorry."
    ),
    "start_off_top": BotResponse(ru_="Расскажите как дела?", en_="How is it going?"),
    "start_consultation": BotResponse(
        ru_="Расскажите что вас беспокоит",
        en_="Please, tell me what you are worring about?",
    ),
    "start_information": BotResponse(
        ru_="Вот похожий случай", en_="There is similar question"
    ),
    "internal_error": BotResponse(
        ru_="Что-то пошло не так. Попробуйте связаться с разработчиками или остановить общение. Ошибка: {error}",
        en_="Something is wrong. Try to contact the developers or interrupt the conversation. Error: {error}",
    ),
    "disease_review": BotResponse(
        ru_=("С вероятностью {disease_probability}% у вас {disease_name}.\n"),
        en_=(
            "Seems like your disease is {disease_name} with {disease_probability}%.\n"
        ),
    ),
    "default_details": BotResponse(
        ru_=[
            "Думаю вам стоит связаться с врачами с следующими симптомами {symptoms_list}. Вы можете это сделать нажав на кнопку.",
            "Мои предположения могут быть ошибочными, но в любом случае стоит связаться с врачами.",
        ],
        en_=[
            "I think you should contact the doctors with the following symptoms {symptoms_list}. You can do this by clicking on the button.",
            "My assumptions may be wrong, but in any case, it is worth contacting the doctors.",
        ],
    ),
    "appendicitis_details": BotResponse(
        ru_=[
            (
                "Если приступ острой боли миновал, это не значит, что вы в безопасности. Пожалуйста, "
                "свяжитесь с медиками по телефону 122, вам необходимо сдать тест и выяснить точный диагноз!"
            ),
            (
                "Для решения, что именно следует предпринять дальше необходимо вызвать скорую помощь, "
                "это можно сделать по телефону 122"
            ),
            (
                "Я собрал Ваши симптомы и готов передать их в службу скорой помощи, нажмите подтверждение действия"
            ),
            (
                "К сожалению, аппендицит не является безобидной болезнью и требует своевременно "
                "оказанной неотложной помощи, давайте позвоним в 122"
            ),
            (
                "Имеет смысл связаться с медиками и вызвать скорую помощь, так как осложнения от "
                "аппендицита могут серьезно влиять на жизнеспособность человека"
            ),
        ],
        en_=[
            (
                "Just because the pain is gone, it doesn't mean you're safe. Please,"
                 "contact the doctors by phone 122, you need to pass the test and find out the exact diagnosis!"
            ),
            (
                "To decide what exactly should be done next, you need to call an ambulance,"
                 "this can be done by calling 122"
            ),
            (
                "I have collected your symptoms and am ready to transfer them to the ambulance service, press confirmation of action"
            ),
            (
                "Unfortunately, appendicitis is not a harmless disease and requires timely "
                 "an emergency, let's call 122"
            ),
            (
                "It makes sense to contact the doctors and call an ambulance, as complications from"
                 "appendicitis can seriously affect a person's vitality"
            ),
        ],
    ),
    "orvi_details": BotResponse(
        ru_=[
            "Это нередкое явление для наших широт… Вам нужны жаропонижающие препараты, капли для носа и покой. Я бы также советовал вызвать врача. Вызываем?",
            "Я собрал следующие симптомы {symptoms_list} и готов их передать в регистратуру вашей поликлиники, давайте вызовем врача на дом?",
            "Это значит, что кто-то из окружающих передал Вам вирус. Само по себе ОРВИ не опасно. Однако могут случиться осложнения при неправильном назначении препаратов. Давайте на всякий случай вызовем доктора?",
            "Не стоит недооценивать это заболевание, давайте вызовем врача? Для этого я готов передать собранные симптомы в регистратуру.",
        ],
        en_=[
            "This is not uncommon for our latitudes ... You need antipyretic drugs, nasal drops and peace. I would also advise calling a doctor. Calling?",
            "I have collected the following symptoms {symptoms_list} and am ready to transfer them to the registry of your clinic, let's call a doctor at home?",
            "This means that someone around you has passed the virus on to you. ARVI itself is not dangerous. However, complications can occur if the drugs are not prescribed correctly. Let's just call the doctor, shall we?",
            "Do not underestimate this disease, let's call a doctor? To do this, I am ready to transfer the collected symptoms to the registry.",
        ]
    ),
    "migraine_details": BotResponse(
        ru_=[
            "Вам следует обеспечить себе покой, прекратить любую работу, особенно физическую. Стоит положить на голову холодный компресс и лечь на кровать. Для купирования головной боли примите анальгетик. Желательно вызвать врача!",
            "Вам нужен свежий воздух, по возможности стоит лечь. Для купирования головной боли примите анальгетик. Если у вас еще нет четких рекомендаций от вашего постоянного доктора, давайте вызовем участкового врача на дом, он поможет выбрать нужное лекарство и научиться узнавать приступ мигрени заранее. Вызываем?",
            "Это заболевание довольно типично для жителей мегаполиса,  принято считать, чтос ним можно справиться самостоятельно (помогут анальгетики), однако я советую также проконсультироваться с врачом: мы можем оформить заявку на приход врача на дом или записать вас на прием в поликлинику.",
        ],
        en_=[
            "You should ensure yourself peace, stop any work, especially physical. It is worth putting a cold compress on your head and lie down on the bed. Take an analgesic to relieve a headache. It is advisable to call a doctor!",
            "You need fresh air, if possible, you should lie down. Take an analgesic to relieve a headache. If you do not yet have clear recommendations from your regular doctor, let's call the local doctor at home, he will help you choose the right medicine and learn how to recognize a migraine attack in advance. Calling?",
            "This disease is quite typical for residents of the metropolis, it is generally accepted that you can cope with it on your own (analgesics will help), but I also advise you to consult a doctor: we can apply for a doctor to come to your home or make an appointment with you at the clinic.",
        ],
    ),
    "stage_info": BotResponse(
        ru_="(Сейчас мы находимся в сценарии {stage_info}) <br>", en_="(Currently we in {stage_info}) <br>"
    ),
}

action_responses = {
    "do_not_know": BotResponse(
        ru_="Я не знаю такого действия",
        en_="Invalid action. Please try to connect with developers",
    ),
    "like": BotResponse(ru_="Хорошо, мы учтем!", en_="Okay, thanks!"),
    "dislike": BotResponse(
        ru_="Хорошо, мы учтем! Попытаемся исправится в следующем обновлении",
        en_="Okay, we'll learn! We'll try to fix it in the next update",
    ),
    "dislike_rude_response": BotResponse(
        ru_="Извините пожалуйста, мы попытаемся исправить грубое поведение.",
        en_="I'm sorry, we'll try to fix the rude behavior",
    ),
    "dislike_dont_make_sense": BotResponse(
        ru_="Я вас понял, примем к сведению", en_="I understand you, take note"
    ),
    "dislike_wrong_scenario_physician": BotResponse(
        ru_='Хорошо, попробуйте пожалуйста нажать на кнопку "Записаться к врачу"',
        en_="Okay, please try to click on the 'Make an appointment' button",
    ),
    "dislike_wrong_scenario_conversation": BotResponse(
        ru_='Хорошо, попробуйте пожалуйста нажать на кнопку "Переключиться на режим болталки"',
        en_='Okay, please try to click on the button "Switch to chat mode"',
    ),
    "dislike_wrong_scenario_question": BotResponse(
        ru_="Мы в следующий раз добавим ответ на этот вопрос",
        en_="We will add an answer to this question next time",
    ),
    "switch_to_operator": BotResponse(
        ru_="Переключаем на оператора.", en_="We are switching you to the operator."
    ),
    "break_conversation": BotResponse(
        ru_="Вы остановили общение.", en_="You have just stopped the conversation"
    ),
}
