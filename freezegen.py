import subprocess
import sys
import os
import ctypes
import uuid
import random
import string
from PIL import Image, ImageDraw
import qrcode
from faker import Faker

required_packages = ['Pillow', 'qrcode', 'faker']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

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
d88888b d8888b. d88888b d88888b d88888D d88888b   d888b  d88888b d8b   db   ┌─────────────────────────────────┐
88'     88  `8D 88'     88'     YP  d8' 88'      88' Y8b 88'     888o  88   │ Developer --> @abrikoSSoftware  │
88ooo   88oobY' 88ooooo 88ooooo    d8'  88ooooo  88      88ooooo 88V8o 88   │ Telegram  --> @abrikoSSoftware  │
88~~~   88`8b   88~~~~~ 88~~~~~   d8'   88~~~~~  88  ooo 88~~~~~ 88 V8o88   │ Интерфейс --> 0                 │
88      88 `88. 88.     88.      d8' db 88.      88. ~8~ 88.     88  V888   │             v0.2                │
YP      88   YD Y88888P Y88888P d88888P Y88888P   Y888P  Y88888P VP   V8P   └─────────────────────────────────┘ 
"""
    menu = """
   ╔═══════════════════════════════════════════════════════════════════════════════════╗
   ║  1. Генерация Пароля             10. Генерация IMEI                               ║
   ║  2. Генерация QR-кода            11. Генерация VIN номера                         ║
   ║  3. Генерация IP-адреса          12. Генерация Bнформации о своём ПК              ║
   ║  4. Генерация Email                                                               ║
   ║  5. Генерация UUID                                                                ║
   ║  6. Генерация MAC-адреса                                                          ║
   ║  7. Генерация Номера                                                              ║
   ║  8. Генерация SSN                                                                 ║
   ║  9. Генерация Даты Рождения                                                       ║
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

def generate_qr_code(data, filename="qrcode.png"):
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
    start_color = (173, 216, 230)
    end_color = (0, 0, 255)
    for y in range(gradient.size[1]):
        color = [
            int(start_color[i] + (end_color[i] - start_color[i]) * y / gradient.size[1])
            for i in range(3)
        ]
        draw.line([(0, y), (gradient.size[0], y)], fill=tuple(color) + (255,))

    img = Image.alpha_composite(gradient, img)

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
  {os_version:<15}            
  Систем тайп: {system_type:<20}                    
  Процессор: {processor_brand}{processor_model:<20}
  Оперативная память: {ram_size}GB                  
  Графический процессор: {gpu_brand} {gpu_model:<20}
  Хранилище данных: {storage_size}GB                
  Разрешение экрана: {screen_resolution}            
  Тип корпуса: {case_type:<20}                       
"""
    return pc_info


def change_interface_color():
    gradient_print("Выберите цвет интерфейса:", start_color, end_color)
    gradient_print("0. Стандартный (Ляденой синий)", start_color, end_color)
    gradient_print("1. Малиново-красный", start_color, end_color)
    gradient_print("2. Изумрудно-зелёный", start_color, end_color)
    gradient_print("3. Алмазный", start_color, end_color)
    gradient_print("4. Рубиновый", start_color, end_color)
    gradient_print("5. Бриллиантовый", start_color, end_color)
    gradient_print("6. Ситаллы", start_color, end_color)
    
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
    else:
        return (173, 216, 230), (0, 0, 255)


def main():
    global start_color, end_color
    start_color, end_color = (173, 216, 230), (0, 0, 255)
    set_cmd_window_title("FreezeGen @abrikoSSoftware")

    while True:
        print_menu(start_color, end_color)
        choice = gradient_input("Выберите опцию: ", start_color, end_color)

        if choice == "1":
            length = int(gradient_input("Введите длину пароля: ", start_color, end_color))
            password = generate_password(length)
            gradient_print(f"Сгенерированный пароль: {password}", start_color, end_color)
        elif choice == "2":
            data = gradient_input("Введите данные для QR-кода: ", start_color, end_color)
            filename = generate_qr_code(data)
            gradient_print(f"QR-код сохранен в файл: {filename}", start_color, end_color)
        elif choice == "3":
            ip_address = generate_ip_address()
            gradient_print(f"Сгенерированный IP-адрес: {ip_address}", start_color, end_color)
        elif choice == "4":
            email = generate_email()
            gradient_print(f"Сгенерированный Email: {email}", start_color, end_color)
        elif choice == "5":
            uuid_str = generate_uuid()
            gradient_print(f"Сгенерированный UUID: {uuid_str}", start_color, end_color)
        elif choice == "6":
            mac_address = generate_mac_address()
            gradient_print(f"Сгенерированный MAC-адрес: {mac_address}", start_color, end_color)
        elif choice == "7":
            phone_number = generate_phone_number()
            gradient_print(f"Сгенерированный номер телефона: {phone_number}", start_color, end_color)
        elif choice == "8":
            ssn = generate_ssn()
            gradient_print(f"Сгенерированный SSN: {ssn}", start_color, end_color)
        elif choice == "9":
            birth_date = generate_random_date()
            gradient_print(f"Сгенерированная дата рождения: {birth_date}", start_color, end_color)
        elif choice == "10":
            imei = generate_imei()
            gradient_print(f"Сгенерированный IMEI: {imei}", start_color, end_color)
        elif choice == "11":
            vin = generate_vin()
            gradient_print(f"Сгенерированный VIN: {vin}", start_color, end_color)
        elif choice == "12":
            pc_info = generate_pc_info()
            gradient_print(f"Сгенерированная информация о ПК: {pc_info}", start_color, end_color)
        elif choice == "777":
            break
        elif choice == "0":
            start_color, end_color = change_interface_color()
        else:
            gradient_print("Неверный выбор. Попробуйте снова.", start_color, end_color)
            continue

        gradient_input("\nНажмите Enter для продолжения...", start_color, end_color)

if __name__ == "__main__":
    fake = Faker()
    main()

