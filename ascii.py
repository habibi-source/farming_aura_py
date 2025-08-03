import cv2
import sys
import os
import time

# ====== KONFIGURASI ======
VIDEO_PATH = "farming_aura.mp4"  # Path video kamu
MAX_DURATION = None       # Durasi maksimum (detik), None = semua
ASCII_CHARS = "@%#*+=-:. "  # Karakter ASCII
WIDTH = 120               # Lebar output ASCII
COLOR_GREEN = "\033[1;32m"  # Warna hijau ANSI
RESET_COLOR = "\033[0m"     # Reset warna

# ====== KONVERSI FRAME KE ASCII ======
def frame_to_ascii(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * WIDTH * 0.3)  # koreksi proporsi
    resized_gray = cv2.resize(gray, (WIDTH, new_height))
    
    ascii_img = []
    for row in resized_gray:
        line = "".join([ASCII_CHARS[int(pixel) * len(ASCII_CHARS) // 256] for pixel in row])
        ascii_img.append(line)  # <-- indentasi pas di sini, 8 spasi / 1 tab dari margin kiri
    return "\n".join(ascii_img)

# ====== MAIN ======
cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS) or 25
interval = max(1, int(fps // fps))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

max_frames = total_frames
if MAX_DURATION:
    max_frames = min(total_frames, int(fps * MAX_DURATION))

ascii_frames = []
count = 0

# ====== BACA VIDEO DAN SIMPAN ASCII FRAME ======
while cap.isOpened() and len(ascii_frames) < max_frames:
    ret, frame = cap.read()
    if not ret:
        break
    if count % interval == 0:
        ascii_frames.append(frame_to_ascii(frame))
    count += 1

cap.release()

# ====== TAMPILKAN SEBAGAI ANIMASI ======
os.system('cls' if os.name == 'nt' else 'clear')
delay = 1 / fps

try:
    while True:
        for ascii_frame in ascii_frames:
            sys.stdout.write("\033c")  # clear terminal
            sys.stdout.write(COLOR_GREEN + ascii_frame + RESET_COLOR + "\n")
            sys.stdout.flush()
            time.sleep(delay)
except KeyboardInterrupt:
    print("\n\033[1;32m[+] Animasi dihentikan\033[0m")
