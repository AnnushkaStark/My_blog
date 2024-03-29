import string
from .ban_words import BAN_WORDS
import os
from PIL import Image
from django.core.exceptions import ValidationError


def valid_name(first_name):
    """
    Проверка валидности имени пользователя
    """
    if first_name.isalnum() and 3 <= len(first_name) <= 20:
        return "is_valid"
    return "invalid first_name"


def valid_email(email):
    """
    Проверка валидности
    электронной почты
    """
    uncorrect_chars = "йёукенгшщзхъэждлорпавыфячсмитьбюЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ"
    incorrect_chars = [  # Символы которые
        " ",
        ":",  # нельзя использовать в электронной почте
        ";",
        "<",
        ">",
        "{",
        "}",
        "[",
        "]",
        "?",
        ",",
        "/",
        "\\",
        "!",
        "|",
        "&",
        "(",
        ")",
        "#",
        "*",
        "+",
        "=",
    ]
    counter = 0
    incorrect_counter = 0
    test_mail = email.split("@")
    test_mail_2 = test_mail[-1]
    test_mail_2 = test_mail_2.replace(".", "")
    test_mail_2 = test_mail_2.replace("-", "")
    test_mail_2 = test_mail_2.replace("_", "")
    for char in email:
        if char in incorrect_chars or char in uncorrect_chars:
            incorrect_counter += 1
    if incorrect_counter == 0:
        counter += 1
    if "." in test_mail[-1]:
        counter += 1
    if email[0].isalpha():
        counter += 1
    if 7 <= len(email) <= 20:
        counter += 1
    if "@" in email and email.count("@") == 1:
        counter += 1
    if "." in email and email.index(".") > email.index("@"):
        counter += 1
    if (
        ".." not in email
        and "..." not in email
        and "..." not in email
        and "...." not in email
        and "....." not in email
        and "......" not in email
        and "........" not in email
        and "........." not in email
        and ".........." not in email
        and "..........." not in email
        and "............" not in email
        and "............." not in email
        and "..............." not in email
        and ".............." not in email
        and "................" not in email
        and "................." not in email
        and ".................." not in email
        and "..................." not in email
    ):
        counter += 1
    if email[0] != "." and email[-1] != ".":
        counter += 1
    if test_mail_2.isalnum():
        counter += 1
    if counter == 9:
        return "is_valid"
    else:
        return "invalid_email"


def valid_password(password):
    """
    Проверка валидности пароля
    """
    uppercase = "QWERTYUIOPASDFGHJKLZXCVBNM"
    lowercase = "qwertyuioplkjhgfdsazxcvbnm"
    digits = "1234567890"
    chars = "!@#$%^&*()[]}{:;?/.><,"
    uncorrect_chars = "йёукенгшщзхъэждлорпавыфячсмитьбюЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ"
    counter_upper = 0
    counter_lower = 0
    counter_digits = 0
    counter_chars = 0
    counter_uncorrect_chars = 0
    for char in password:
        if char in uppercase:
            counter_upper += 1
        if char in lowercase:
            counter_lower += 1
        if char in digits:
            counter_digits += 1
        if char in chars:
            counter_chars += 1
        if char in uncorrect_chars:
            counter_uncorrect_chars += 1
    if (
        counter_chars >= 1
        and counter_digits >= 1
        and counter_lower >= 1
        and counter_upper >= 1
        and counter_uncorrect_chars == 0
        and len(password) >= 6
        and len(password) <= 64
    ):
        return "is_valid"
    return "Invalid_password"


def valid_text(text):
    """
    Функция фильтрации бранных
    в текста
    """
    flag = True
    clean_text = set(text.translate(str.maketrans("", "", string.punctuation)).split())
    for word in clean_text:
        if word.lower() in BAN_WORDS:
            flag = False
            break

    if flag:
        return "is_valid"
    return "Invalid_text"


def valid_image(file):
    """
    Функция валидации изображения
    """
    try:
        Image.open(file)
        return "is_valid"
    except IOError:
        return "invalid_file"
    

def valid_file_size(file):
    """
    Функция валидации размера 
    изображения в МБ
    """
    if file:
        if file.size > 10485760:
            raise ValidationError("Файл , больше 10 ти мб не может быть загружен")
        return file
