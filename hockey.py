import pygame
import time

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hokey Oyunu")

# Renkler
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)  # Futbol sahasının rengi
LINE_COLOR = (255, 255, 255)  # Çizgi rengi

# Paddle boyutları
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
player1 = pygame.Rect(350, 550, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(350, 30, PADDLE_WIDTH, PADDLE_HEIGHT)

# Disk (Puck) özellikleri
puck = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
puck_speed_x = 5  # Hızı artırdık
puck_speed_y = 5  # Hızı artırdık

# Skor
score1 = 0
score2 = 0

# Yazı fontu
font = pygame.font.Font(None, 50)

# Zamanlayıcı
clock = pygame.time.Clock()

# Geri sayım fonksiyonu
def countdown():
    font_big = pygame.font.Font(None, 100)
    for i in range(3, 0, -1):
        screen.fill(GREEN)  # Arka planı yeşil yap
        pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)  # Orta çizgi
        pygame.draw.rect(screen, LINE_COLOR, (50, 100, WIDTH - 100, HEIGHT - 200), 5)  # Sahayı çevreleyen çizgi
        pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 100), (WIDTH // 2, HEIGHT - 100), 5)  # Kale çizgileri
        countdown_text = font_big.render(str(i), True, WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

# Skor ekranı fonksiyonu
def score_screen(winner):
    font_big = pygame.font.Font(None, 80)
    score_text = font_big.render(f"{winner} scored!", True, WHITE)
    screen.fill(GREEN)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)  # Orta çizgi
    pygame.draw.rect(screen, LINE_COLOR, (50, 100, WIDTH - 100, HEIGHT - 200), 5)  # Sahayı çevreleyen çizgi
    pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 100), (WIDTH // 2, HEIGHT - 100), 5)  # Kale çizgileri
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)  # 3 saniye bekle

# Oyun döngüsü
while True:
    # Başlangıçta geri sayım
    countdown()

    # Oyuna başla
    puck.x = WIDTH // 2 - 15
    puck.y = HEIGHT // 2 - 15
    puck_speed_x = 5  # Hızı artırdık
    puck_speed_y = 5  # Hızı artırdık

    # Oyun döngüsü
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Klavye ile oyuncu hareketi
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player1.x -= 10
        if keys[pygame.K_RIGHT]:
            player1.x += 10
        if keys[pygame.K_a]:
            player2.x -= 10
        if keys[pygame.K_d]:
            player2.x += 10

        # Disk hareketi
        puck.x += puck_speed_x
        puck.y += puck_speed_y

        # Diskin ekrandan dışarı çıkmasını engelle
        if puck.left <= 0 or puck.right >= WIDTH:
            puck_speed_x = -puck_speed_x
        if puck.top <= 0 or puck.bottom >= HEIGHT:
            puck_speed_y = -puck_speed_y

        # Skor kontrolü
        if puck.colliderect(player1) or puck.colliderect(player2):
            puck_speed_y = -puck_speed_y

        # Skor güncellemeleri
        if puck.top <= 0:
            score1 += 1
            score_screen("Player 1")
            break  # Oyun bitti, tekrar geri sayım için dışarı çık
        if puck.bottom >= HEIGHT:
            score2 += 1
            score_screen("Player 2")
            break  # Oyun bitti, tekrar geri sayım için dışarı çık

        # Ekranı temizle ve çizimler yap
        screen.fill(GREEN)  # Arka planı yeşil yap

        # Futbol sahası çizgileri (orta çizgi, kale çizgileri, alanlar)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)  # Orta çizgi
        pygame.draw.rect(screen, LINE_COLOR, (50, 100, WIDTH - 100, HEIGHT - 200), 5)  # Sahayı çevreleyen çizgi
        pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 100), (WIDTH // 2, HEIGHT - 100), 5)  # Kale çizgileri

        # Kale alanları (futbol sahası için)
        pygame.draw.rect(screen, LINE_COLOR, (100, 100, 100, HEIGHT - 200), 5)  # Sol kale alanı
        pygame.draw.rect(screen, LINE_COLOR, (WIDTH - 200, 100, 100, HEIGHT - 200), 5)  # Sağ kale alanı

        # Oyuncu paddle'ları
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)

        # Disk (Puck) çizimi
        pygame.draw.ellipse(screen, WHITE, puck)

        # Skorları yazdır
        score_text = font.render(f"Player 1: {score1}  Player 2: {score2}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

        # Ekranı güncelle
        pygame.display.flip()

        # FPS kontrolü
        clock.tick(60)
