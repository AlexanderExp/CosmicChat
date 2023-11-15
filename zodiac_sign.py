def chineese_zodiac(year):
    z = { 0: "Крыса",
          1: "Бык", 
          2: "Тигр", 
          3: "Кролик", 
          4: "Дракон", 
          5: "Змея", 
          6: "Лошадь", 
          7: "Овца" , 
          8: 'Обезьяна', 
          9: 'Курица', 
          10: 'Собака', 
          11: 'Свинья'}

    return z[year % 12]
 
def zodiac(month,day):
        z = ['Водолей', 'Рыбы', 'Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', "Скорпион", "Стрелец", "Козерог"] 
        d =(20,19,21,20,21,22,23,23,23,24,23,22)
        month = month - 1
        if day > d[month]:
            return z[month]
        else :
            return z[month-1]
 
def zodiac_info(date):
    a = date.split('.')
    year = int(a[2])
    month = int(a[1])
    day = int(a[0])
    return zodiac(month, day),chineese_zodiac(year)

'''
водолей — «Aquarius» (20.01 — 18.02),
рыбы — «Pisces» (19.02 — 20.03),
овен — «Aries» (21.03 — 19.04),
телец — «Taurus» (20.04 — 20.05),
близнецы — «Gemini» (21.05 — 21.06),
рак — «Crayfish» (22.06 — 22.07),
лев — «Leo» (23.07 — 22.08),
дева — «Virgo» (23.08 — 22.09),
весы — «Libra» (23.09 — 22.10),
скорпион — «Scorpio» (23.10 — 22.11),
стрелец — «Sagittarius» (23.11 — 21.12),
козерог — «Capricorn» (22.12 — 19.01).
'''