import pygame
import random

# Pygame başlatma
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinamik Araba Yarışı")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (105, 105, 105)
BLUE = (30, 144, 255)

# Araba özellikleri
car_width = 70
car_height = 120
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 10
car_velocity = 7

# Engeller
obstacle_width = 60
obstacle_height = 100
obstacle_velocity = 7
obstacles = []

# Skor
score = 0
font = pygame.font.SysFont("Arial", 30)

# Arka plan şeritleri
road_lines = [HEIGHT // 6 * i for i in range(6)]

# Araba çizme fonksiyonu
def draw_car(x, y):
    pygame.draw.rect(screen, RED, (x, y, car_width, car_height), border_radius=15)
    # Farlar
    pygame.draw.circle(screen, YELLOW, (x + 15, y + 20), 10)
    pygame.draw.circle(screen, YELLOW, (x + car_width - 15, y + 20), 10)
    # Çerçeve
    pygame.draw.rect(screen, BLACK, (x + 10, y + 30, car_width - 20, car_height - 40))

# Yolu çizme fonksiyonu
def draw_road():
    screen.fill((50, 50, 50))  # Asfalt renkli arka plan
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 150, 0, 300, HEIGHT))  # Genişletilmiş yol
    for i in range(len(road_lines)):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, road_lines[i], 10, 40))
        road_lines[i] += obstacle_velocity // 2
        if road_lines[i] > HEIGHT:
            road_lines[i] = -40

# Araba hareket fonksiyonu
def move_car(x, direction):
    if direction == "left" and x > WIDTH // 2 - 150:  # Geniş yol için sınır değişikliği
        x -= car_velocity
    elif direction == "right" and x < WIDTH // 2 + 150 - car_width:  # Geniş yol için sınır değişikliği
        x += car_velocity
    return x

# Engelleri hareket ettirme ve çarpışma kontrolü
def move_obstacles():
    global obstacles, score, running, game_over
    for obstacle in obstacles:
        obstacle[1] += obstacle_velocity
        if obstacle[1] > HEIGHT:
            obstacles.remove(obstacle)
            score += 1
        # Çarpışma kontrolü
        if (obstacle[0] < car_x + car_width and obstacle[0] + obstacle_width > car_x and
                obstacle[1] + obstacle_height > car_y):
            game_over = True

# Yeni engel oluşturma
def create_obstacle():
    x = random.randint(WIDTH // 2 - 150, WIDTH // 2 + 150 - obstacle_width)  # Genişletilmiş yol alanı
    obstacles.append([x, -obstacle_height])

# Oyun bitiş ekranı
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Oyun Bitti!", True, WHITE)
    retry_text = font.render("Tekrar Dene", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    retry_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, GREEN, retry_button)
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and retry_button.collidepoint(event.pos):
                return

# Oyun döngüsü
running = True
clock = pygame.time.Clock()
game_over = False

while running:
    clock.tick(30)  # FPS

    if game_over:
        game_over_screen()
        # Oyun sıfırlama
        car_x = WIDTH // 2 - car_width // 2
        obstacles = []
        score = 0
        game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Klavye tuşlarına göre araba hareketi
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x = move_car(car_x, "left")
    if keys[pygame.K_RIGHT]:
        car_x = move_car(car_x, "right")

    # Yeni engel oluşturma
    if random.randint(1, 100) <= 5:
        create_obstacle()

    # Engelleri hareket ettir
    move_obstacles()

    # Ekranı temizle ve yolu çiz
    draw_road()

    # Arabayı çiz
    draw_car(car_x, car_y)

    # Engelleri çiz
    for obstacle in obstacles:
        pygame.draw.rect(screen, GREEN, (obstacle[0], obstacle[1], obstacle_width, obstacle_height), border_radius=5)

    # Skor yazısı
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

# Pygame'i sonlandır
pygame.quit()
