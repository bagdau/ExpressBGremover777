import os
from rembg import remove
from PIL import Image
import time
from concurrent.futures import ThreadPoolExecutor

input_folder = 'input'
output_folder = 'output'

start_time = time.time()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
files = files[:90]
print(f"[INFO] Найдено файлов: {len(files)}")

def process_image(file):
    input_path = os.path.join(input_folder, file)
    output_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".png")
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            output_data = remove(input_data)
        with open(output_path, 'wb') as o:
            o.write(output_data)
        print(f"[OK] {file} → обработан")
        return True
    except Exception as e:
        print(f"[ERROR] {file}: {e}")
        return False

with ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(process_image, files))

total_time = round(time.time() - start_time, 2)
print(f"\n[DONE] Успешно: {sum(results)}/{len(files)} файлов за {total_time} секунд.")
