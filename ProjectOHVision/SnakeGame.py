import mediapipe as mp
import cv2
import numpy as np
import time
import random

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
score = 0

x_enemy = random.randint(50, 600)
y_enemy = random.randint(50, 400)

snake = []
snake_length = 1

# Warna ular
snake_colors = [(128, 0, 128), (255, 255, 0)]

# Ukuran umpan
umpan_radius = 15

obstacles = []  # List untuk menyimpan posisi obstacle
obstacle_width = 30
obstacle_height = 30
obstacle_count = 3  # Jumlah obstacle awal

game_over_time = None  # Variabel untuk menyimpan waktu game over

def enemy(image):
    global score, x_enemy, y_enemy
    cv2.circle(image, (x_enemy, y_enemy), umpan_radius, (0, 200, 0), 5)

def generate_new_enemy_position():
    global x_enemy, y_enemy
    while True:
        new_x_enemy = random.randint(50, 600)
        new_y_enemy = random.randint(50, 400)
        overlapping = False

        # Periksa tumpang tindih dengan rintangan
        for obstacle_pos in obstacles:
            x_obstacle, y_obstacle = obstacle_pos
            if (new_x_enemy >= x_obstacle - umpan_radius and new_x_enemy <= x_obstacle + obstacle_width + umpan_radius and
                new_y_enemy >= y_obstacle - umpan_radius and new_y_enemy <= y_obstacle + obstacle_height + umpan_radius):
                overlapping = True
                break

        if not overlapping:
            x_enemy, y_enemy = new_x_enemy, new_y_enemy
            break

def create_obstacles():
    global obstacles, obstacle_count
    obstacles = []  # Mengosongkan daftar obstacle
    for _ in range(obstacle_count):
        x = random.randint(50, 600)
        y = random.randint(50, 400)
        while (abs(x - x_enemy) < umpan_radius and abs(y - y_enemy) < umpan_radius):
            x = random.randint(50, 600)
            y = random.randint(50, 400)
        obstacles.append((x, y))

def draw_obstacles(image):
    global obstacles
    for obstacle_pos in obstacles:
        x, y = obstacle_pos
        cv2.rectangle(image, (x, y), (x + obstacle_width, y + obstacle_height), (0, 0, 255), -1)

def draw_snake(image):
    global snake
    for i, segment in enumerate(snake):
        color = snake_colors[i % len(snake_colors)]  # Mengambil warna berdasarkan indeks
        cv2.circle(image, (segment[0], segment[1]), 10, color, -1)

def move_snake(x, y):
    global snake, snake_length
    snake.append([x, y])
    if len(snake) > snake_length:
        del snake[0]

def reset_game():
    global score, snake, snake_length, game_over_time, obstacle_count

    score = 0
    snake = []
    snake_length = 1
    game_over_time = None
    obstacle_count = 3  # Reset the obstacle count
    create_obstacles()  # Create the initial set of obstacles again

def tampilkan_peraturan():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Peraturan Game')

    font = pygame.font.Font(None, 36)
    text = font.render("Peraturan Game:", True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 100))

    peraturan = [
        "1. Tekan 'Q' untuk keluar dari permainan.",
        "2. Dapatkan poin dengan menyentuh umpan berwarna hijau.",
        "3. Hindari rintangan merah atau game over.",
    ]

    y_offset = 200
    for line in peraturan:
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, y_offset))
        screen.blit(text, text_rect)
        y_offset += 50

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

video = cv2.VideoCapture(1)

# Tambahkan kode berikut untuk mengatur resolusi tampilan kamera
video.set(3, 1280)  # Lebar frame
video.set(4, 720)   # Tinggi frame

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        _, frame = video.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        imageHeight, imageWidth, _ = image.shape

        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 0, 255)
        text = cv2.putText(image, "Score", (480, 30), font, 1, color, 4, cv2.LINE_AA)
        text = cv2.putText(image, str(score), (590, 30), font, 1, color, 4, cv2.LINE_AA)

        enemy(image)
        draw_obstacles(image)

        # Menambahkan keterangan
        cv2.putText(image, "Persegi merah adalah obstacle", (10, 30), font, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(image, "Lingkaran hijau adalah umpan", (10, 60), font, 0.7, (0, 200, 0), 2, cv2.LINE_AA)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
                                                                 circle_radius=2))

                # Mengambil koordinat ujung jari telunjuk
                index_fingertip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                pixel_x = int(index_fingertip.x * imageWidth)
                pixel_y = int(index_fingertip.y * imageHeight)

                # Mengecek apakah ujung jari menyentuh musuh (skor bertambah)
                if abs(pixel_x - x_enemy) < umpan_radius and abs(pixel_y - y_enemy) < umpan_radius:
                    score += 1
                    generate_new_enemy_position()  # Mendapatkan posisi umpan yang tidak tumpang tindih
                    enemy(image)
                    snake_length += 1

                    # Menambah satu obstacle baru
                    obstacle_count += 1
                    create_obstacles()

                # Mengecek apakah ular menabrak rintangan (game over)
                for obstacle_pos in obstacles:
                    x_obstacle, y_obstacle = obstacle_pos
                    if (x_obstacle <= pixel_x <= x_obstacle + obstacle_width and
                        y_obstacle <= pixel_y <= y_obstacle + obstacle_height):
                        if game_over_time is None:
                            game_over_time = time.time()  # Menyimpan waktu game over
                        cv2.putText(image, "Game Over", (250, 250), font, 1, (0, 0, 255), 3, cv2.LINE_AA)
                        cv2.imshow('Hand Tracking Game', image)
                        cv2.waitKey(2000)  # Menunggu 2 detik sebelum keluar
                        reset_game()  # Reset permainan
                        create_obstacles()  # Membuat obstacle awal

                # Menggerakkan ular (menambah panjang)
                move_snake(pixel_x, pixel_y)

        # Menggambar ular dengan variasi warna
        draw_snake(image)

        cv2.imshow('Hand Tracking Game', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
tampilkan_peraturan()
