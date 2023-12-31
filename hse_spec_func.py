import datetime
import random

import db_functions

crow_type = {
    "usual": "*usual ворона:*\nПохоже, вы обычная ворона среди деловых будней",
    "deadline": "*deadline ворона:*\nОй! Нет времени объяснять, у меня дедл горит!",
    "minor": "*minor ворона:*\nТааак, у кого-то сегодня день майнора. Ну что, чилл дома?",
    "home": "*home ворона:*\n* отсутствует большая часть информации, так как данная ворона в Вышке появляется крайне редко *",
    "indoor": "*indoor university ворона:*\n24 / 7 в университете... Погоди, а у тебя вообще дом есть??",
    "bot": "*bot ворона:*\nВы посмотрите, да это жесткий бот с утра и до самого вечера!",
    "no_hw": "*no_hw ворона:*\nДЗ? Не, не слышали",
    "hw": "*hw ворона:*\nДЗ? Да только его и делаю!",
    "chill": "*chill ворона:*\nВсе окей, на расслабоне, на чилле...",
    "sleepy": "*sleepy ворона:*\nК первой паре! Эх, даже десятая кружка кофе уже не спасает",
    "tired": "*tired ворона:*\nЕсли ты чувствуешь себя усталой и разбитой вороной, то это твой знак сделать перерыв!",
    "exam": "*exam ворона:*\nХей! Да у кого-то сессия на носу! Все получится, мы в тебя верим!",
    "colloc": "*colloc ворона:*\nАААА коллок на носу!",
    "kr": "*kr ворона:*\nТебе лучше вовремя заботать ту предстоящую кр)",
    "grusha": "*grusha cafe ворона:*\nЭта модная ворона берет латте на миндальном только в Груше",
    "complex": "*complex lunch ворона:*\n* стоит в очереди за комплексом, это надолго *"
}

motivation = {
    "exam": ["У тебя получится сдать все экзамены на отлично!",
             "На экзамене не паникуй: сделай вдох - выдох, и вперед - решать задания!",
             "Успокойся, ты все сдашь)",
             "Сегодня удача на твоей стороне!",
             "Тайм менеджмент при подготовке к экзамену - вот залог успеха!",
             "Перед экзаменом важно хорошо выспаться!",
             "На экзамене перепроверь свои ответы перед сдачей - и дело в шляпе!"],

    "not_exam": [
        "«Есть два способа прожить жизнь: или так, будто чудес не бывает, или так, будто вся жизнь — чудо»\n(Альберт Эйнштейн)",
        "«Будьте тем изменением, которое вы хотите видеть в мире»\n(Махатма Ганди)",
        "«Это всегда кажется невозможным, пока не будет сделано»\n(Нельсон Мандела)",
        "«Действие - это не только результат мотивации, но и ее причина»\n(Марк Мэнсон)",
        "«Успех — это умение двигаться от неудачи к неудаче, не теряя энтузиазма»\n(Уинстон Черчилль)",
        "«Как только вы выбираете надежду, все возможно»\n(Кристофер Рив)",
        "«Всё, что ты можешь вообразить — реально»\n(Пабло Пикассо)",
        "«Возможности не приходят сами — вы создаете их»\n(Крис Гроссер)",
        "«Лучший способ взяться за что-то — перестать говорить и начать делать»\nУолт Дисней "]
}


def generate_random_crow(user_id):
    today = datetime.datetime.now()

    last_time = db_functions.get_crow_time(user_id)
    if last_time:
        if datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S') - today < datetime.timedelta(hours=24):
            return db_functions.get_crow(user_id)

    random_crow = random.choice(list(crow_type.keys()))
    crow_text = crow_type[random_crow]
    db_functions.set_crow(user_id, random_crow, crow_text, today.strftime('%Y-%m-%d %H:%M:%S'))

    return [random_crow, crow_text]


def generate_random_motivation(user_id):
    today = datetime.datetime.now()
    last_time = db_functions.get_motivation_time(user_id)
    if last_time:
        if datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S') - today < datetime.timedelta(hours = 24):
            return db_functions.get_motivation(user_id)
    sdate = datetime.datetime.strptime("2023-12-21", '%Y-%m-%d')
    edate = datetime.datetime.strptime("2023-12-29", '%Y-%m-%d')
    if sdate <= today <= edate:
        random_motivation = random.choice(motivation['exam'])
    else:
        random_motivation = random.choice(motivation['not_exam'])
    db_functions.set_motivation(user_id, random_motivation, today.strftime('%Y-%m-%d %H:%M:%S'))
    return random_motivation
