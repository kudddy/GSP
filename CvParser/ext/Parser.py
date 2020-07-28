import textract
import re


class HhProfileInfo:
    def __init__(self):
        pass

    def read_pdf(self, dir_path):
        txt = textract.process(dir_path, method='pdfminer').decode().replace('\xa0', ' ').replace('\x0c', '')
        txt = list(filter(lambda x: x != '', txt.split('\n')))
        return txt

    def get_vacants_ru(self, lst):
        head_hunter = False
        for line in lst:
            if "Резюме обновлено" in line:
                head_hunter = True
                break
        if head_hunter:
            postfix = ['январь', 'февраль',
                       'март', 'апрель', 'май', 'июнь', 'июль',
                       'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь', 'настоящее время'] + \
                      ['.ru', '.org', '.net', '.com', '.io', '.info', '.рф']
            key_words = ["Желаемая должность и зарплата", 'Опыт работы', 'Образование', 'Опыт вождения', 'Навыки',
                         'Дополнительная информация', 'Ключевые навыки',
                         'Повышение квалификации, курсы', 'Тесты, экзамены',
                         "Электронные сертификаты", 'Знание языков', "Рекомендации", 'Обо мне', 'Комментарии к резюме',
                         'История общения с кандидатом', 'Телефон']

            educ_flag, exp_flag, car_flag, skills_flag, my_flag = False, False, False, False, False

            cv_summary = {'Тесты, экзамены': '', 'Дополнительная информация': '', 'Ключевые навыки': '',
                          'Электронные сертификаты': '', 'Уровень образования': '', 'Опыт работы': '',
                          'Образование': '',
                          'Желаемая позиция': '', 'Зарплата': '', 'Занятость': '', 'График работы': '',
                          'Профессиональная область работы': '', 'Повышение квалификации, курсы': '',
                          'Знание языков': '',
                          'Наличие автомобиля': '', 'Навыки': [], 'Опыт вождения': '', 'Обо мне': '',
                          'Рекомендации': '',
                          'Комментарии к резюме': '', 'История общения с кандидатом': '', 'Телефон': '', 'Возраст': '',
                          'Email': '', 'Город': '', 'ФИО': '', 'Гражданство': '', 'Пол': '', 'ФИО': ''}
            counter = 0
            count = 0
            for l in lst:
                if "Желаемая должность и зарплата" in l:
                    break
                counter += 1
                if l[0].isdigit() and cv_summary['Зарплата'] == '' and ''.join(l.split()).isdigit():
                    cv_summary['Зарплата'] = int(''.join(l.split()))
                elif 'Проживает' in l:
                    cv_summary['Город'] = l[11:]
                elif 'Мужчина' in l or 'Женщина' in l:
                    cv_summary['Пол'] = l[:7]
                    cv_summary['Возраст'] = l[9:-len(l[9:].lstrip("0123456789"))]
                elif l.istitle() and re.fullmatch(r'[\w -]+', l) != None:
                    cv_summary['ФИО'] += l.strip()
                elif '(' in l:
                    cv_summary['Телефон'] = l.split('—')[0].replace('(', '').replace(')', '').replace(' ', '')
                elif '@' in l:
                    cv_summary['Email'] = l.split('—')[0].strip()
                elif 'Гражданство' in l:
                    cv_summary['Гражданство'] = l[12:].split('есть')[0].strip(' ,')
            counter += 1
            if counter >= len(lst):
                return
            cv_summary['Желаемая позиция'] = lst[counter].strip()
            counter += 1
            if counter >= len(lst):
                return
            while '•' not in lst[counter]:
                cv_summary['Профессиональная область работы'] += lst[counter].replace('.', ' ').strip() + '.'
                counter += 1
                if counter >= len(lst):
                    return
            if counter >= len(lst):
                return
            while "•" in lst[counter]:
                cv_summary['Профессиональная область работы'] += lst[counter].replace('.', ' ').strip('•') + '.'
                counter += 1
                if counter >= len(lst):
                    return
            if 'Занятость' in lst[counter]:
                cv_summary['Занятость'] = lst[counter][11:].strip()
                counter += 1
            if counter >= len(lst):
                return
            if 'График работы' in lst[counter]:
                cv_summary['График работы'] = lst[counter][15:].strip()
                counter += 1
            if counter >= len(lst):
                return
            if 'Желательное время в пути' in lst[counter]:
                pass
                counter += 1
            if counter >= len(lst):
                return
            if cv_summary['Зарплата'] == '' and ''.join(lst[counter].split()).isdigit():
                cv_summary['Зарплата'] = int(''.join(lst[counter].split()))
                counter += 1
            while counter < len(lst):
                if ('лет' in lst[counter].lower() or 'месяц' in lst[counter].lower() \
                    or 'год' in lst[counter].lower()) and len(lst[counter]) <= 18:
                    count += 1
                if lst[counter] == ("Образование") and not educ_flag:
                    key_words.remove('Образование')
                    counter += 1
                    educ_flag = True
                    if counter >= len(lst):
                        break
                    if 'Уровень' in lst[counter]:
                        counter += 1
                    if counter == len(lst):
                        return
                    if "Резюме обновлено" not in lst[counter]:
                        cv_summary['Уровень образования'] = lst[counter].strip()
                        counter += 1
                    else:
                        counter += 1
                        cv_summary['Уровень образования'] = lst[counter].strip()
                        counter += 1
                    while counter < len(lst):
                        if "Резюме обновлено" not in lst[counter]:
                            ok = False
                            for k in key_words:
                                if k in lst[counter]:
                                    ok = True
                                    break
                            if ok:
                                counter -= 1
                                break
                            cv_summary["Образование"] += " " + lst[counter].strip()
                        counter += 1
                if counter >= len(lst):
                    break
                if lst[counter].startswith("Опыт вождения") and not car_flag:
                    key_words.remove("Опыт вождения")
                    car_flag = True
                    counter += 1
                    while counter < len(lst):
                        if "Резюме обновлено" not in lst[counter]:
                            ok = False
                            for k in key_words:
                                if k in lst[counter]:
                                    ok = True
                                    break
                            if ok:
                                counter -= 1
                                break
                            if 'Имеется собственный автомобиль' in lst[counter]:
                                cv_summary['Наличие автомобиля'] = 1
                            else:
                                cv_summary['Опыт вождения'] = lst[counter][16:].split(', ')
                        counter += 1
                if counter >= len(lst):
                    break
                if lst[counter].startswith("Опыт работы") and not exp_flag:
                    key_words.remove('Опыт работы')
                    exp_flag = True
                    counter += 1
                    if counter >= len(lst):
                        break
                    while counter < len(lst) - 1:
                        if "Резюме обновлено" not in lst[counter]:
                            ok = False
                            for k in key_words:
                                if k in lst[counter]:
                                    ok = True
                                    break
                            if ok:
                                counter -= 1
                                break
                            ok = True
                        for x in postfix:
                            if x in lst[counter].lower():
                                ok = False
                                break
                        if ('лет' in lst[counter].lower() or 'месяц' in lst[counter].lower() \
                            or 'год' in lst[counter].lower() or lst[counter].isdigit()) and len(lst[counter]) <= 18:
                            ok = False
                            if not lst[counter].isdigit():
                                count += 1
                        if ok:
                            cv_summary["Опыт работы"] += lst[counter].strip() + ' '
                        counter += 1
                if counter >= len(lst):
                    break
                if lst[counter].startswith("Навыки") and not skills_flag:
                    key_words.remove("Навыки")
                    skills_flag = True
                    counter += 1
                    while counter < len(lst) - 1:
                        if "Резюме обновлено" not in lst[counter]:
                            ok = False
                            for k in key_words:
                                if k in lst[counter]:
                                    ok = True
                                    break
                            if ok:
                                counter -= 1
                                break
                            cv_summary["Навыки"] += lst[counter].strip().split('      ')
                        counter += 1
                for key_word in key_words:
                    if counter >= len(lst):
                        break
                    if lst[counter].startswith(key_word):
                        counter += 1
                        while counter < len(lst):
                            if "Резюме обновлено" not in lst[counter]:
                                ok = False
                                for k in key_words:
                                    if k in lst[counter]:
                                        ok = True
                                        break
                                if ok:
                                    counter -= 1
                                    break
                                if not lst[counter].isdigit():
                                    cv_summary[key_word] += " " + lst[counter].strip().replace(key_word, '')
                            counter += 1
                counter += 1
            cv_summary['Навыки'] = ' '.join(cv_summary['Навыки'])
            return {x: y for x, y in cv_summary.items() if y != ''}
