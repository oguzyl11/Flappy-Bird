import pygame
import random
import sys
import math

# Oyun penceresi boyutları
WINDOW_WIDTH = 800  # Genişliği artırdık
WINDOW_HEIGHT = 600

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)

class Bird:
    def __init__(self):
        self.x = 200  # Başlangıç pozisyonunu sağa kaydırdık
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.3  # Yerçekimini azalttık
        self.lift = -8  # Sıçrama gücünü azalttık
        self.size = 30  # Kuşun boyutunu artırdık
        self.angle = 0
        self.forward_speed = 1  # Başlangıç hızını düşürdük
        self.speed_increase = 0.05  # Hız artışını azalttık

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.x += self.forward_speed
        
        # Kuşun açısını hıza göre ayarla
        self.angle = min(max(self.velocity * 2, -45), 45)

        # Yerçekimi sınırlaması
        if self.y > WINDOW_HEIGHT - self.size:
            self.y = WINDOW_HEIGHT - self.size
            self.velocity = 0
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def increase_speed(self):
        self.forward_speed += self.speed_increase

    def flap(self):
        self.velocity = self.lift

    def draw(self, screen):
        # Kuşun gövdesi (daire)
        pygame.draw.circle(screen, GREEN, (self.x, int(self.y)), self.size)
        
        # Kuşun başı (küçük daire)
        head_x = self.x + self.size * 0.7
        head_y = self.y - self.size * 0.3
        pygame.draw.circle(screen, DARK_GREEN, (int(head_x), int(head_y)), self.size // 2)
        
        # Kuşun gagası (üçgen)
        beak_length = self.size
        beak_x = head_x + self.size // 2
        beak_y = head_y
        points = [
            (beak_x, beak_y),
            (beak_x + beak_length, beak_y - beak_length // 3),
            (beak_x + beak_length, beak_y + beak_length // 3)
        ]
        pygame.draw.polygon(screen, DARK_GREEN, points)
        
        # Kuşun kanatları
        wing_length = self.size * 1.5
        wing_x = self.x - self.size // 2
        wing_y = self.y
        
        # Sol kanat
        left_wing_points = [
            (wing_x, wing_y),
            (wing_x - wing_length * math.cos(math.radians(45 + self.angle)), 
             wing_y - wing_length * math.sin(math.radians(45 + self.angle))),
            (wing_x - wing_length * math.cos(math.radians(90 + self.angle)), 
             wing_y - wing_length * math.sin(math.radians(90 + self.angle)))
        ]
        pygame.draw.polygon(screen, DARK_GREEN, left_wing_points)
        
        # Sağ kanat
        right_wing_points = [
            (wing_x, wing_y),
            (wing_x - wing_length * math.cos(math.radians(45 - self.angle)), 
             wing_y + wing_length * math.sin(math.radians(45 - self.angle))),
            (wing_x - wing_length * math.cos(math.radians(90 - self.angle)), 
             wing_y + wing_length * math.sin(math.radians(90 - self.angle)))
        ]
        pygame.draw.polygon(screen, DARK_GREEN, right_wing_points)

class Pipe:
    def __init__(self, gap_size=200):  # Delik boyutunu artırdık
        self.gap = gap_size
        self.top = random.randint(100, WINDOW_HEIGHT - self.gap - 100)  # Boruların yüksekliğini ayarladık
        self.bottom = self.top + self.gap
        self.x = WINDOW_WIDTH
        self.width = 80  # Boru genişliğini artırdık
        self.speed = 3
        self.passed = False

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top))
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom, self.width, WINDOW_HEIGHT - self.bottom))

    def collide(self, bird):
        if (bird.x + bird.size > self.x and bird.x - bird.size < self.x + self.width):
            if (bird.y - bird.size < self.top or bird.y + bird.size > self.bottom):
                return True
        return False

def load_high_score():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    except:
        return 0

def save_high_score(score):
    with open('highscore.txt', 'w') as file:
        file.write(str(score))

def show_start_screen(screen, font):
    screen.fill(WHITE)
    title = font.render("Flappy Bird", True, BLACK)
    start_text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, WINDOW_HEIGHT//3))
    screen.blit(start_text, (WINDOW_WIDTH//2 - start_text.get_width()//2, WINDOW_HEIGHT//2))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = []
    score = 0
    high_score = load_high_score()
    font = pygame.font.Font(None, 48)  # Font boyutunu artırdık
    gap_size = 200  # Başlangıç delik boyutu

    # Başlangıç ekranını göster
    show_start_screen(screen, font)

    # İlk boruyu oluştur
    pipes.append(Pipe(gap_size))
    pipe_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Boru oluşturma
        pipe_timer += 1
        if pipe_timer > 150:  # Boru oluşturma süresini artırdık
            pipes.append(Pipe(gap_size))
            pipe_timer = 0

        # Oyun güncelleme
        bird.update()
        for pipe in pipes:
            pipe.update()
            if pipe.collide(bird):
                if score > high_score:
                    save_high_score(score)
                pygame.quit()
                sys.exit()
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                score += 1
                bird.increase_speed()
                gap_size = max(120, gap_size - 2)  # Minimum delik boyutunu artırdık

        # Ekranı temizle
        screen.fill(WHITE)

        # Çizimler
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Skorları göster
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        screen.blit(high_score_text, (20, 70))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 