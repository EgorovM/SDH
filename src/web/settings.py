LOCALES = {
    "ru": {
        "today": "Сегодня",
        "chat": "Чат",
        "switch_to_operator": "Переключиться к оператору",
        "switch_to_conversation": "Переключиться на режим болталки",
        "switch_to_appointment": "Записаться к врачу",
        "get_info": "Получить информацию о местоположении больницы",
        "break_conversation": "Остановить общение",
        "virtual_assistent": "Виртуальный ассистент",
        "like_message": "Мне понравился ответ",
        "do_not_like_message": "Мне не понравился ответ",
        "do_not_like_message_wrong_scenario": "Неверный сценарий",
        "wrong_scenario_physician": "Я хотел записать к врачу",
        "wrong_scenario_conversation": "Я хотел поболтать",
        "wrong_scenario_question": "Я хотел получить ответ на вопрос",
        "wrong_response": "Не тот ответ",
        "do_not_like_message_rude_response": "Грубый ответ",
        "do_not_like_message_unsense_response": "Ответ не имеет смысла",
        "initial_message": """Я умный бот, который может вас записать к врачу, <br> \
            дать ответ на интересующий вопрос или просто поболтать. <br> \
            Общайтесь со мной как бы вы общались с колл-центром. <br> \
            Если я не могу ответить на вопрос - нажите на кнопку 'Переключить к оператору' <br> \
            Если хотите остановить сценарий - нажмите на кнопку 'Остановить общение' <br> \
            Я умею отвечать на очень базовые вопросы, по типу <a href="#" onclick="breakConversation(); sendMessage('Как добраться до больницы?')">"Где находиться больница?"</a><br> \
            Так же, если вы попросите меня записать к врачу: <a href="#" onclick="breakConversation(); sendMessage('Хочу записаться к врачу')">"Хочу записаться к врачу"</a>, то я начну собирать симптомы. <br> \
            Если же, вы захотите начать общение: <a href="#" onclick="breakConversation(); sendMessage('Привет, как дела?')">"Привет, как дела"</a> - я вас пойму. <br> \
        """,
        "how_to_get_hospital": "Как добраться до больницы",
        "i_would_like_to_make_an_appointment": "Хочу записаться к врачу",
        "hello_message": "Привет, как дела?",
        "hi_message": "Привет!",
    },
    "en": {
        "today": "Today",
        "chat": "Chat",
        "switch_to_operator": "Switch to operator",
        "switch_to_conversation": "Switch to conversation mode",
        "switch_to_appointment": "Make an appointment",
        "get_info": "Get the location info",
        "break_conversation": "Break conversation",
        "virtual_assistent": "Virtual assistent",
        "like_message": "I did like response",
        "do_not_like_message": "I did not like response",
        "do_not_like_message_wrong_scenario": "Wrong scenario",
        "wrong_scenario_physician": "I wanted to make an appointment",
        "wrong_scenario_conversation": "I wanted to have a conversation",
        "wrong_scenario_question": "I wanted to get information",
        "wrong_response": "Wrong response",
        "do_not_like_message_rude_response": "Rude response",
        "do_not_like_message_unsense_response": "Response do not make any sense",
        "initial_message": """I am a bot, who can make an appointment <br> \
            give some information about the organization or just swop lies. <br> \
            If I can't give an relevant response - just push 'Swith to operator' <br> \
            If I do not guessed the scenario - click 'Break conversation' <br> \
            I can give a some basic information, like <a href="#" onclick="breakConversation(); sendMessage('Where is the hospital')">"Where is the hospital?"</a><br> \
            Or you can ask for an appointment: <a href="#" onclick="breakConversation(); sendMessage('I would like to make an appointment')">"I would like to make an appointment"</a>, I will start collecting symptoms from you. <br> \
            If you just would like to start an conversation: <a href="#" onclick="breakConversation(); sendMessage('Hi, how are you?')">"Hi, how are you"</a> - I will understand your purposes. <br> \
        """,
        "how_to_get_hospital": "How to get the hospital",
        "i_would_like_to_make_an_appointment": "I would like to make an appointment",
        "hello_message": "Hi, how are you?",
        "hi_message": "Hi!",
    },
}