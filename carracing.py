import pygame
import random

# Pygame başlatma
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gerçekçi Araba Yarışı")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)  # Gri lastikler için
DARK_GRAY = (105, 105, 105)  # Lastikler için

# Araba özellikleri
car_width = 70
car_height = 120
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 10
car_velocity = 5

# Lastikler
tire_radius = 20
tire_offset_x = 15
tire_offset_y = 10
tire_angle = 0  # Lastiğin dönme açısı

# Engeller
obstacle_width = 60
obstacle_height = 100
obstacle_velocity = 5
obstacles = []

# Skor
score = 0
font = pygame.font.SysFont("Arial", 30)

# Araba çizme fonksiyonu
def draw_car(x, y):
    global tire_angle

    # Araba gövdesi
    pygame.draw.rect(screen, RED, (x, y, car_width, car_height))
    
    # Lastikler (3D benzeri)
    draw_tire(x + tire_offset_x, y + car_height - 10, tire_radius, tire_angle)  # Sol lastik
    draw_tire(x + car_width - tire_offset_x - 10, y + car_height - 10, tire_radius, tire_angle)  # Sağ lastik

    # Farlar
    pygame.draw.circle(screen, YELLOW, (x + car_width - 10, y + 20), 8)  # Sağ far
    pygame.draw.circle(screen, YELLOW, (x + 10, y + 20), 8)  # Sol far

# Lastik çizme fonksiyonu (3D benzeri etki)
def draw_tire(x, y, radius, angle):
    tire_width = radius // 2  # Lastik için bir genişlik belirleyelim
    # Tire'yi biraz perspektife sokarak oval şekil gibi çizebiliriz
    pygame.draw.ellipse(screen, GRAY, (x - tire_width, y - radius + tire_width, radius * 2, radius))  # Yatay oval lastik
    
    # Lastiğin ortasına bir çarpı yerleştirerek dönen bir etki yaratabiliriz
    pygame.draw.line(screen, DARK_GRAY, (x, y - radius), (x, y + radius), 4)
    pygame.draw.line(screen, DARK_GRAY, (x - radius, y), (x + radius, y), 4)

# Araba hareket fonksiyonu
def move_car(x, direction):
    if direction == "left" and x > 0:
        x -= car_velocity
    elif direction == "right" and x < WIDTH - car_width:
        x += car_velocity
    return x

# Engellerin hareketi
def move_obstacles():
    global obstacles, score
    for obstacle in obstacles:
        obstacle[1] += obstacle_velocity
        if obstacle[1] > HEIGHT:
            obstacles.remove(obstacle)
            score += 1

# Yeni engel oluşturma
def create_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    obstacles.append([x, -obstacle_height])

# Oyun döngüsü
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(30)  # FPS

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

    # Ekranı temizle
    screen.fill(WHITE)

    # Yolu çiz (orta çizgi)
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 5, 0, 10, HEIGHT))
    
    # Araba çizimi
    draw_car(car_x, car_y)

    # Engelleri çiz
    for obstacle in obstacles:
        pygame.draw.rect(screen, GREEN, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

    # Skor yazısı
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))

    # Oyun bitti durumu (arabaya çarpma)
    for obstacle in obstacles:
        if (obstacle[0] < car_x + car_width and obstacle[0] + obstacle_width > car_x):
            if (obstacle[1] + obstacle_height > car_y):
                running = False

    # Lastiği döndürme etkisi
    tire_angle += 5  # Lastiği döndürme

    pygame.display.update()

# Pygame'i sonlandır
pygame.quit()
