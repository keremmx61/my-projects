import pygame
import random

# Pygame başlat
pygame.init()

# Renkler
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yatırımcı Simülasyonu")

# Yazı tipi
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Başlangıç sermayesi
capital = 1000

# Yatırım seçenekleri
investments = {
    "Hisse Senedi": 100,
    "Kripto Para": 200,
    "Emlak": 500
}

# Piyasa dalgalanması
def market_fluctuation():
    return random.uniform(0.8, 1.5)  # Fiyatlar %80 ile %150 arasında değişir

# Yatırım yapma fonksiyonu
def invest(investment_type, amount):
    global capital
    if investment_type in investments:
        if amount > capital:
            return "Yeterli sermayeniz yok!"
        else:
            price = investments[investment_type]
            capital -= amount
            fluctuation = market_fluctuation()
            profit_or_loss = amount * fluctuation - amount
            capital += (amount + profit_or_loss)
            return f"{investment_type} yatırımı {fluctuation*100:.2f}% değişti. {('Kar' if profit_or_loss > 0 else 'Zarar')} ettiniz!"
    else:
        return "Geçersiz yatırım türü!"

# Oyun döngüsü
def game():
    global capital
    clock = pygame.time.Clock()
    running = True
    investing = False
    investment_message = ""

    # Başlangıç ekranı
    while running:
        screen.fill(WHITE)

        # Başlangıç mesajı
        title_text = large_font.render("Yatırımcı Simülasyonu", True, BLUE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        start_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
        pygame.draw.rect(screen, GREEN, start_button)
        start_text = font.render("Oyuna Başla", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    investing = True

        pygame.display.flip()
        clock.tick(60)

        if investing:
            break

    # Yatırım yapma ekranı
    while True:
        screen.fill(WHITE)

        # Başlangıç sermayesi
        capital_text = font.render(f"Sermaye: {capital:.2f} TL", True, BLACK)
        screen.blit(capital_text, (20, 20))

        # Yatırım seçenekleri
        pygame.draw.rect(screen, BLUE, pygame.Rect(100, 100, 200, 50))
        hisse_text = font.render("Hisse Senedi (100 TL)", True, WHITE)
        screen.blit(hisse_text, (120, 110))

        pygame.draw.rect(screen, BLUE, pygame.Rect(100, 200, 200, 50))
        kripto_text = font.render("Kripto Para (200 TL)", True, WHITE)
        screen.blit(kripto_text, (120, 210))

        pygame.draw.rect(screen, BLUE, pygame.Rect(100, 300, 200, 50))
        emlak_text = font.render("Emlak (500 TL)", True, WHITE)
        screen.blit(emlak_text, (120, 310))

        # Mesaj
        if investment_message:
            message_text = font.render(investment_message, True, RED)
            screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT - 50))

        # Yatırım yapma
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(100, 100, 200, 50).collidepoint(event.pos):
                    investment_message = invest("Hisse Senedi", 100)
                elif pygame.Rect(100, 200, 200, 50).collidepoint(event.pos):
                    investment_message = invest("Kripto Para", 200)
                elif pygame.Rect(100, 300, 200, 50).collidepoint(event.pos):
                    investment_message = invest("Emlak", 500)

        pygame.display.flip()
        clock.tick(60)

# Oyunu başlat
game()
pygame.quit()
