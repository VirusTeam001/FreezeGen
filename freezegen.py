import subprocess
import sys
import os
import socket
import ipaddress
import ctypes
import uuid
import random
import string
import struct
from PIL import Image, ImageDraw
import qrcode
from faker import Faker

fake = Faker()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_cmd_window_title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def gradient_text(text, start_color, end_color):
    def interpolate(start, end, step, max_steps):
        return start + (end - start) * step // max_steps

    def color_text(text, color):
        return f"\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m"

    gradient_text = ""
    max_steps = len(text)
    for i, char in enumerate(text):
        interpolated_color = (
            interpolate(start_color[0], end_color[0], i, max_steps),
            interpolate(start_color[1], end_color[1], i, max_steps),
            interpolate(start_color[2], end_color[2], i, max_steps)
        )
        gradient_text += color_text(char, interpolated_color)

    return gradient_text

def gradient_print(text, start_color, end_color):
    print(gradient_text(text, start_color, end_color))

def gradient_input(prompt, start_color, end_color):
    gradient_prompt = gradient_text(prompt, start_color, end_color)
    return input(gradient_prompt)


def print_menu(start_color, end_color):
    clear_screen()

    title = """
d88888b d8888b. d88888b d88888b d88888D d88888b   d888b  d88888b d8b   db   ┌───────────────────────────────────┐
88'     88  `8D 88'     88'     YP  d8' 88'      88' Y8b 88'     888o  88   │ ● Developer --> @abrikoSSoftware  │
88ooo   88oobY' 88ooooo 88ooooo    d8'  88ooooo  88      88ooooo 88V8o 88   │ ● Telegram  --> @abrikoSSoftware  │
88~~~   88`8b   88~~~~~ 88~~~~~   d8'   88~~~~~  88  ooo 88~~~~~ 88 V8o88   │ ● Интерфейс --> 0                 │
88      88 `88. 88.     88.      d8' db 88.      88. ~8~ 88.     88  V888   │             v0.3                  │
YP      88   YD Y88888P Y88888P d88888P Y88888P   Y888P  Y88888P VP   V8P   └───────────────────────────────────┘ 
"""
    menu = """
   ╔═══════════════════════════════════════════════════════════════════════════════════╗ 
   ║  1. Генерация Пароля             10. Генерация IMEI                               ║
   ║  2. Генерация QR-кода            11. Генерация VIN номера                         ║
   ║  3. Генерация IP4-адреса         12. Генерация Информации о своём ПК              ║
   ║  4. Генерация Email              13. Генерация Карт                               ║
   ║  5. Генерация UUID               14. Генерация Mullvad keys                       ║
   ║  6. Генерация MAC-адреса         15. Генерация IP6-адреса                         ║
   ║  7. Генерация Номера             16. Генерация DNS                                ║
   ║  8. Генерация SSN                17. Генерация токена тг ботов                    ║
   ║  9. Генерация Даты Рождения      18. Генерация дискорд токена                     ║
   ╟───────────────────────────────────────────────────────────────────────────────────╢
   ║                               777. Выход                                          ║                             
   ╚═══════════════════════════════════════════════════════════════════════════════════╝

"""

    set_cmd_window_title("FreezeGen @abrikoSSoftware")
    gradient_print(title, start_color, end_color)
    gradient_print(menu, start_color, end_color)

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def generate_uuid():
    return str(uuid.uuid4())

def generate_random_date(start_year=1900, end_year=2024):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return year, month, day

def generate_phone_number():
    country_code = random.randint(1, 999)
    area_code = random.randint(100, 999)
    subscriber_number = random.randint(1000000, 9999999)
    return f"+{country_code} ({area_code}) {subscriber_number}"

def generate_ip_address():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def generate_mac_address():
    mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    return ":".join(map(lambda x: f"{x:02x}", mac))

def generate_credit_card_info(card_type):
    if card_type == 1:
        card_number = '4' + ''.join(random.choices(string.digits, k=15))
        card_name = "Украинская"
        fake_locale = 'uk_UA'
    elif card_type == 2:
        card_number = '5' + ''.join(random.choices(string.digits, k=15))
        card_name = "Русская"
        fake_locale = 'ru_RU'
    elif card_type == 3:
        card_number = '6' + ''.join(random.choices(string.digits, k=15))
        card_name = "Казахстанская"
        fake_locale = 'ru_RU'
    elif card_type == 4:
        card_number = '7' + ''.join(random.choices(string.digits, k=15))
        card_name = "Белорусская"
        fake_locale = 'ru_RU'
    elif card_type == 5:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Американская"
        fake_locale = 'en_US'
    elif card_type == 6:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Французская"
        fake_locale = 'fr_FR'
    elif card_type == 7:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Турецкая"
        fake_locale = 'tr_TR'
    elif card_type == 8:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Эстонская"
        fake_locale = 'et_EE'
    elif card_type == 9:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Латвийская"
        fake_locale = 'lv_LV'
    elif card_type == 10:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Литовская"
        fake_locale = 'lt_LT'
    elif card_type == 11:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Немецкая"
        fake_locale = 'de_DE'
    elif card_type == 12:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Испанская"
        fake_locale = 'es_ES'
    elif card_type == 13:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Итальянская"
        fake_locale = 'it_IT'
    elif card_type == 14:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Польская"
        fake_locale = 'pl_PL'
    elif card_type == 15:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Швейцарская"
        fake_locale = 'de_CH'
    elif card_type == 16:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Шведская"
        fake_locale = 'sv_SE'
    elif card_type == 17:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Финская"
        fake_locale = 'fi_FI'
    elif card_type == 18:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Датская"
        fake_locale = 'da_DK'
    elif card_type == 19:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Норвежская"
        fake_locale = 'no_NO'
    elif card_type == 20:
        card_number = ''.join(random.choices(string.digits, k=16))
        card_name = "Австралийская"
        fake_locale = 'en_AU'
    else:
        return "Неверный тип карты"

    fake = Faker(fake_locale)
    card_holder = fake.name()
    card_expiry = fake.credit_card_expire()
    card_cvv = ''.join(random.choices(string.digits, k=3))

    return {
        "card_name": card_name,
        "card_number": card_number,
        "card_holder": card_holder,
        "card_expiry": card_expiry,
        "card_cvv": card_cvv
    }

def generate_qr_code(data, start_color, end_color, filename="qrcode.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    gradient = Image.new('RGBA', img.size)
    draw = ImageDraw.Draw(gradient)
    
    for y in range(gradient.size[1]):
        color = [
            int(start_color[i] + (end_color[i] - start_color[i]) * y / gradient.size[1])
            for i in range(3)
        ]
        draw.line([(0, y), (gradient.size[0], y)], fill=tuple(color) + (255,))

    background = gradient
    img = Image.alpha_composite(background, img)

    img = add_rounded_corners(img, 20)

    img.save(filename)
    return filename

def add_rounded_corners(img, radius):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    alpha = Image.new('L', img.size, 255)
    w, h = img.size

    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))

    img.putalpha(alpha)
    return img

def generate_email():
    domains = ["gmail.com", "yahoo.com", "hotmail.com"]
    username_length = random.randint(5, 10)
    username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(username_length))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def generate_ipv6_address():
    return str(ipaddress.IPv6Address(random.getrandbits(128)))

def generate_ssn():
    ssn = [random.randint(100, 999), random.randint(10, 99), random.randint(1000, 9999)]
    return f"{ssn[0]}-{ssn[1]}-{ssn[2]}"

def generate_imei():
    tac = f"{random.randint(100000, 999999):06d}"
    sn = f"{random.randint(100000, 999999):06d}"
    cd = f"{random.randint(10, 99):02d}"
    return f"{tac}-{sn}-{cd}-{''.join(random.choice(string.digits) for _ in range(1))}"

def generate_vin():
    wmi = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    vds = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    check_digit = random.choice(string.digits + "X")
    vis = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{wmi}{vds}{check_digit}{vis}"

def generate_dns_name():
    return fake.domain_name()

def generate_mullvad_key():
    return ''.join(random.choices(string.digits, k=16))

def save_mullvad_keys(num_keys):
    with open('mullvad_keys.txt', 'w') as f:
        for _ in range(num_keys):
            f.write(generate_mullvad_key() + '\n')

def generate_discord_token():
    def random_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    prefix = random_string(24)
    secret = random_string(8)
    hash_part = random_string(27)

    return f"{prefix}.{secret}.{hash_part}"

def generate_telegram_token():
    def random_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    bot_id = ''.join(random.choices(string.digits, k=9))
    token_part = random_string(32)

    return f"{bot_id}:{token_part}"

def generate_pc_info():
    username = fake.user_name()
    
    os_platform = random.choice(["Windows", "MacOS", "Linux"])
    if os_platform == "Windows":
        os_version = random.choice(["Windows 10", "Windows 11"])
    elif os_platform == "MacOS":
        os_version = random.choice(["macOS Catalina", "macOS Big Sur", "macOS Monterey"])
    else:
        os_version = random.choice(["Ubuntu 20.04 LTS", "Fedora 35", "Manjaro 21.2"])

    system_type = random.choice(["32-битная", "64-битная"])
    processor_brand = random.choice(["Intel", "AMD", "Apple"])
    
    if processor_brand == "Intel":
        processor_model = random.choice(["Intel Core i7-10700K", "Intel Core i9-11900K", "Intel Core i5-11600K"])
    elif processor_brand == "AMD":
        processor_model = random.choice(["AMD Ryzen 9 5900X", "AMD Ryzen 7 5800X", "AMD Ryzen 5 5600X"])
    else:
        processor_model = random.choice(["Apple M1", "Apple M1 Pro", "Apple M1 Max"])
    
    ram_size = random.randint(4, 64)
    gpu_brand = random.choice(["NVIDIA", "AMD", "Intel"])
    
    if gpu_brand == "NVIDIA":
        gpu_model = random.choice(["NVIDIA GeForce RTX 3080", "NVIDIA GeForce RTX 3070", "NVIDIA GeForce RTX 3060"])
    elif gpu_brand == "AMD":
        gpu_model = random.choice(["AMD Radeon RX 6800 XT", "AMD Radeon RX 6700 XT", "AMD Radeon RX 6600 XT"])
    else:
        gpu_model = random.choice(["Intel Iris Xe Graphics G7", "Intel Iris Xe Graphics G4", "Intel UHD Graphics 750"])
    
    storage_size = random.randint(256, 4096)
    screen_resolution = random.choice(["1920x1080", "2560x1440", "3840x2160"])
    case_type = random.choice(["ATX", "Micro-ATX", "Mini-ITX"])
    
    pc_info = f"""
╔════════════════════════════════════════════════════╗
║                Информация о ПК                     ║
╚════════════════════════════════════════════════════╝
  Юзернейм: {username:<20}                          
  ОС: {os_platform:<20}
  Версия ОС: {os_version:<20}            
  Системный тип: {system_type:<20}                    
  Процессор: {processor_brand} {processor_model:<20}
  Оперативная память: {ram_size}GB                  
  Графический процессор: {gpu_brand} {gpu_model:<20}
  Хранилище данных: {storage_size}GB                
  Разрешение экрана: {screen_resolution}            
  Тип корпуса: {case_type:<20}                       
"""
    return pc_info

def change_interface_color():
    gradient_print("Выберите цвет интерфейса:", start_color, end_color)
    gradient_print("0. Стандартный (Ладеной синий)", start_color, end_color)
    gradient_print("1. Малиново-красный", start_color, end_color)
    gradient_print("2. Изумрудно-зелёный", start_color, end_color)
    gradient_print("3. Алмазный", start_color, end_color)
    gradient_print("4. Рубиновый", start_color, end_color)
    gradient_print("5. Бриллиантовый", start_color, end_color)
    gradient_print("6. Ситаллы", start_color, end_color)
    gradient_print("7. Феникс", start_color, end_color)
    gradient_print("8. Кровавый", start_color, end_color)
    gradient_print("9. Чёрно-белое", start_color, end_color)
    gradient_print("10. Манга", start_color, end_color)
    gradient_print("11. Лаймовый", start_color, end_color)
    gradient_print("12. Рассвет", start_color, end_color)
    gradient_print("13. Firewatch", start_color, end_color)
    gradient_print("14. Вай Сити", start_color, end_color)
    gradient_print("15. Nighthawk", start_color, end_color)
    
    choice = gradient_input("Введите номер цвета: ", start_color, end_color)
    
    if choice == "1":
        return (255, 105, 180), (139, 0, 139)
    elif choice == "2":
        return (60, 179, 113), (0, 100, 0)
    elif choice == "3":
        return (0, 127, 255), (255, 255, 255)
    elif choice == "4":
        return (204, 0, 0), (255, 204, 204)
    elif choice == "5":
        return (255, 255, 0), (255, 255, 255)
    elif choice == "6":
        return (0, 204, 204), (255, 255, 255)
    elif choice == "7":
        return (255, 69, 0), (255, 165, 0)
    elif choice == "8":
        return (139, 0, 0), (255, 0, 0)
    elif choice == "9":
        return (0, 0, 0), (255, 255, 255)
    elif choice == "10":
        return (255, 182, 193), (255, 105, 180)
    elif choice == "11":
        return (50, 205, 50), (0, 255, 0)
    elif choice == "12":
        return (255, 223, 186), (255, 160, 122)
    elif choice == "13":
        return (255, 69, 0), (128, 0, 128)
    elif choice == "14":
        return (0, 255, 255), (255, 20, 147)
    elif choice == "15":
        return (25, 25, 112), (70, 130, 180)
    else:
        return (173, 216, 230), (0, 0, 255)

def main():
    global start_color, end_color
    start_color, end_color = (173, 216, 230), (0, 0, 255)
    fake = Faker()

    while True:
        print_menu(start_color, end_color)
        choice = gradient_input("Выберите опцию: ", start_color, end_color)

        if choice == "1":
            length = int(gradient_input("Введите длину пароля: ", start_color, end_color))
            password = generate_password(length)
            gradient_print(f"Сгенерированный пароль: {password}", start_color, end_color)
        elif choice == "2":
            data = gradient_input("Введите данные для QR-кода: ", start_color, end_color)
            filename = generate_qr_code(data, start_color, end_color)
            gradient_print(f"QR-код сохранен в файл: {filename}", start_color, end_color)
        elif choice == "3":
            ip_address = generate_ip_address()
            gradient_print(f"\nСгенерированный IP-адрес: {ip_address}", start_color, end_color)
        elif choice == "4":
            email = generate_email()
            gradient_print(f"\nСгенерированный Email: {email}", start_color, end_color)
        elif choice == "5":
            uuid_str = generate_uuid()
            gradient_print(f"\nСгенерированный UUID: {uuid_str}", start_color, end_color)
        elif choice == "6":
            mac_address = generate_mac_address()
            gradient_print(f"\nСгенерированный MAC-адрес: {mac_address}", start_color, end_color)
        elif choice == "7":
            phone_number = generate_phone_number()
            gradient_print(f"\nСгенерированный номер телефона: {phone_number}", start_color, end_color)
        elif choice == "8":
            ssn = generate_ssn()
            gradient_print(f"\nСгенерированный SSN: {ssn}", start_color, end_color)
        elif choice == "9":
            birth_date = generate_random_date()
            gradient_print(f"\nСгенерированная дата рождения: {birth_date}", start_color, end_color)
        elif choice == "10":
            imei = generate_imei()
            gradient_print(f"\nСгенерированный IMEI: {imei}", start_color, end_color)
        elif choice == "11":
            vin = generate_vin()
            gradient_print(f"\nСгенерированный VIN: {vin}", start_color, end_color)
        elif choice == "12":
            pc_info = generate_pc_info()
            gradient_print(f"\nСгенерированная информация о ПК: {pc_info}", start_color, end_color)
        elif choice == "0":
            start_color, end_color = change_interface_color()
        elif choice == "13":
            gradient_print("Выберите тип карты:", start_color, end_color)
            gradient_print("1. Украинская", start_color, end_color)
            gradient_print("2. Русская", start_color, end_color)
            gradient_print("3. Казахстанская", start_color, end_color)
            gradient_print("4. Белорусская", start_color, end_color)
            gradient_print("5. Американская", start_color, end_color)
            gradient_print("6. Французская", start_color, end_color)
            gradient_print("7. Турецкая", start_color, end_color)
            gradient_print("8. Эстонская", start_color, end_color)
            gradient_print("9. Латвийская", start_color, end_color)
            gradient_print("10. Литовская", start_color, end_color)
            gradient_print("11. Немецкая", start_color, end_color)
            gradient_print("12. Испанская", start_color, end_color)
            gradient_print("13. Итальянская", start_color, end_color)
            gradient_print("14. Польская", start_color, end_color)
            gradient_print("15. Шведская", start_color, end_color)
            gradient_print("16. Финская", start_color, end_color)
            gradient_print("17. Норвежская", start_color, end_color)
            gradient_print("18. Датская", start_color, end_color)
            gradient_print("19. Швейцарская", start_color, end_color)
            gradient_print("20. Австралийская", start_color, end_color)

            card_choice = gradient_input("Введите номер типа карты: ", start_color, end_color)
            card_choice = int(card_choice) if card_choice.isdigit() else None

            if card_choice and 1 <= card_choice <= 20:  # Исправил на 20
                card_info = generate_credit_card_info(card_choice)
                if isinstance(card_info, dict):
                    card_name = card_info.get("card_name", "Неизвестный")
                    card_number = card_info.get("card_number", "Неизвестный")
                    card_holder = card_info.get("card_holder", "Неизвестный")
                    card_expiry = card_info.get("card_expiry", "Неизвестный")
                    card_cvv = card_info.get("card_cvv", "Неизвестный")

                    gradient_print(f"Тип карты: {card_name}", start_color, end_color)
                    gradient_print(f"Номер карты: {card_number}", start_color, end_color)
                    gradient_print(f"Владелец карты: {card_holder}", start_color, end_color)
                    gradient_print(f"Срок действия: {card_expiry}", start_color, end_color)
                    gradient_print(f"CVV: {card_cvv}", start_color, end_color)
                else:
                    gradient_print(card_info, start_color, end_color)
            else:
                gradient_print("Неверный тип карты.", start_color, end_color)
        elif choice == "14":
                num_keys = int(gradient_input("Введите количество ключей Mullvad для генерации: ", start_color, end_color))
                save_mullvad_keys(num_keys)
                gradient_print(f"{num_keys} ключей Mullvad успешно сохранены в файл 'mullvad_keys.txt'.", start_color, end_color)
        elif choice == "16":
            dns_name = generate_dns_name()
            gradient_print(f"\nСгенерированный DNS-имя: {dns_name}", start_color, end_color)
        elif choice == "15":
            ipv6_address = generate_ipv6_address()
            gradient_print(f"Сгенерированный IPv6-адрес: {ipv6_address}", start_color, end_color)
        elif choice == "17":
            telegram_token = generate_telegram_token()
            gradient_print(f"Фейковый токен Telegram: {telegram_token}", start_color, end_color)
        elif choice == "18":
            discord_token = generate_discord_token()
            gradient_print(f"Фейковый токен Discord: {discord_token}", start_color, end_color)
        elif choice == "777":
            print("Выход...")
            break
        else:
            gradient_print("Неверный выбор, попробуйте снова.", start_color, end_color)
        
        input(gradient_text("Нажмите Enter, чтобы продолжить...", start_color, end_color))

if __name__ == "__main__":
    main()
print(Faker.locales)