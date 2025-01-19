import hashlib
import math
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import string

def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
def pass_generator(input_str):
    str1 = 'RADCO-molmal'
    bytes1 = str1.encode()
    res1 = []
    for i, ch in enumerate(input_str.encode()):
        res1.append(
            ch ^ bytes1[i%len(bytes1)]
            )
    
    res_str1 = bytes(res1)
    res_str1 = res_str1.decode('utf-8', errors='ignore')

    res_str2 = ""
    str2 = "r@Dco^1403!"
    for i, ch in enumerate(res_str1):
        new_ch = ord(ch) + ord(str2[i%len(str2)])
        new_ch = chr(new_ch%255)
        res_str2 = res_str2 + ch
    return res_str2
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
def remove_specific_metadata(file_path, key):
    # خواندن کل داده‌های فایل
    with open(file_path, 'rb') as file:
        separator = b"\n--METADATA--\n"
        data = file.read()

    # بررسی وجود متادیتا در فایل
    if separator in data:
        # جدا کردن بخش داده اصلی و متا
        main_data, metadata = data.split(separator, 1)
        metadata_str = metadata.decode('utf-8')

        # پردازش متاها به صورت خط به خط و حذف کلید مشخص‌شده
        new_metadata = []
        for line in metadata_str.splitlines():
            if not line.startswith(f"{key}: "):  # اگر کلید مطابقت ندارد، نگه داشته می‌شود
                new_metadata.append(line)

        # ایجاد متای جدید بدون کلید مشخص‌شده
        updated_metadata = "\n".join(new_metadata).encode('utf-8')

        # بازنویسی فایل با داده اصلی و متاهای به‌روز شده (بدون کلید مشخص‌شده)
        with open(file_path, 'wb') as file:
            file.write(main_data)
            if updated_metadata:
                file.write(separator + updated_metadata)  # فقط در صورت وجود متا، اضافه می‌شود
        print(f"Metadata with key '{key}' removed successfully.")
    else:
        print("No metadata found.")
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
def encrypt_zip_file(zip_file_path, password, out_path):
    # خواندن فایل زیپ ورودی
    with open(zip_file_path, 'rb') as f:
        data = f.read()

    # تولید کلید رمزگذاری از رمز عبور
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # ذخیره داده رمزگذاری‌شده و nonce
    encrypted_zip_path = out_path + '.enc'
    with open(encrypted_zip_path, 'wb') as enc_file:
        enc_file.write(cipher.nonce)                 # nonce برای رمزگشایی ضروری است
        enc_file.write(tag)                          # tag برای احراز هویت استفاده می‌شود
        enc_file.write(ciphertext)

    print(f"Encrypted file created: {encrypted_zip_path}")
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
def decrypt_zip_file(encrypted_zip_path, password, output_zip_path):
    # خواندن فایل رمزگذاری‌شده
    with open(encrypted_zip_path, 'rb') as enc_file:
        nonce = enc_file.read(16)           # nonce ابتدا ذخیره شده است و ۱۶ بایت است
        tag = enc_file.read(16)             # tag نیز ۱۶ بایت است
        ciphertext = enc_file.read()        # باقی داده‌ها، محتوای رمزگذاری‌شده هستند

    # تولید کلید رمزگشایی از رمز عبور
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # رمزگشایی و تأیید صحت داده‌ها با استفاده از tag
    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        # ذخیره فایل زیپ رمزگشایی‌شده
        with open(output_zip_path, 'wb') as zip_file:
            zip_file.write(data)
        print(f"Decrypted zip file created: {output_zip_path}")
        return True
    except ValueError:
        print("Incorrect password or file has been tampered with!")
        return False
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

def add_metadata_to_file(file_path, metadata):
    # باز کردن فایل در حالت افزودن باینری
    with open(file_path, 'ab') as file:
        # جداکننده‌ای مشخص برای متمایز کردن متا از داده اصلی فایل
        separator = b"\n--METADATA--\n"
        file.write(separator)
        file.write(metadata.encode())  # تبدیل متا به بایت و اضافه کردن آن به انتهای فایل

#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
def get_metadata_from_file(file_path):
    with open(file_path, 'rb') as file:
        separator = b"\n--METADATA--\n"
        data = file.read()
        if separator in data:
            metadata = data.split(separator)[-1]
            return metadata.decode('utf-8')
    return None
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
def get_metadata_value(file_path, key):
    # خواندن متا از فایل
    metadata = get_metadata_from_file(file_path)
    if metadata:
        # هر خط را بررسی می‌کنیم و به دنبال کلید خاص می‌گردیم
        for line in metadata.splitlines():
            if line.startswith(f"{key}: "):
                # مقدار را بعد از کلید و دو نقطه برمی‌گردانیم
                return line.split(f"{key}: ", 1)[1]
    return None
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
def write_header(file_path, key, value):
    """
    نوشتن هدر خاص به ابتدای فایل.
    """
    # قالب هدر: key: value
    header_data = f"{key}: {value}\n"
    separator = "--HEADER_END--\n"

    with open(file_path, 'rb') as file:
        original_data = file.read()

    with open(file_path, 'wb') as file:
        # نوشتن هدر، جداکننده و داده اصلی
        file.write(header_data.encode())
        file.write(separator.encode())
        file.write(original_data)

    print(f"Header with key '{key}' written successfully.")


def read_header(file_path, key):
    """
    خواندن مقدار یک هدر خاص بر اساس کلید.
    """
    separator = "--HEADER_END--\n"

    with open(file_path, 'rb') as file:
        header_data = b""
        while not header_data.endswith(separator.encode()):
            header_data += file.read(1)

        # هدر را بدون جداکننده استخراج می‌کنیم
        header_text = header_data.decode().split(separator)[0]

        # هر خط از هدر را بررسی می‌کنیم
        for line in header_text.splitlines():
            if line.startswith(f"{key}: "):
                return line.split(f"{key}: ", 1)[1]  # مقدار بعد از کلید برمی‌گردد

    print(f"Header with key '{key}' not found.")
    return None


if True:
    hash_str = calculate_file_hash(r'C:\Users\milad\Desktop\UPDATE\update.zip')
    print(hash_str)
    password = pass_generator(hash_str)
    encrypt_zip_file(r'C:\Users\milad\Desktop\UPDATE\update.zip', password, r'C:\Users\milad\Downloads\update')
    #add_metadata_to_file('update.enc', f'code: {hash_str}')
    #write_header('update.enc', key='code', value = hash_str)

if False:
    hash_str2 = get_metadata_value('update.enc','code')
    #hash_str2 = read_header('update.enc', key='code')
    password2 = pass_generator(hash_str2)
    remove_specific_metadata('update.enc', 'code')
    status = decrypt_zip_file('update.enc', password, 'rez2.zip')
    if status:
        print('file is valid')


