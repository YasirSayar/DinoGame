import pygame
import random

# Ekran boyutları
WIDTH = 1920
HEIGHT = 1080 

# Oyuncu ve engel boyutları
PLAYER_WIDTH = 95
PLAYER_HEIGHT = 95
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 70

# Engelin hızı
OBSTACLE_SPEED = 600  # Piksel/saniye

# İkinci engel boyutları ve hızı
OBSTACLE2_WIDTH = 10
OBSTACLE2_HEIGHT = 10
OBSTACLE2_SPEED = 1000  # Piksel/saniye

# Pygame başlatılıyor
pygame.init()

# Pencere oluşturuluyor
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1920x1080 Pencere")

# Font yükleniyor
font2 = pygame.font.SysFont(None, 40)
font1 = pygame.font.Font("ARCADECLASSIC.TTF", 100)
font = pygame.font.Font("Nunito.ttf", 40)

# Arka plan görüntüsü yükleniyor
background_image = pygame.image.load("arkaplan.png").convert()
background_x = 0

# Oyuncu animasyon karesi yükleniyor
player_frames = []
for i in range(6):  # 6 kareli bir animasyon
    frame = pygame.image.load(f"oyuncu_{i}.png").convert_alpha()
    player_frames.append(frame)

# Zıplama animasyon karesi yükleniyor
jump_frames = []
for i in range(4):  # 4 kareli bir animasyon
    frame = pygame.image.load(f"ziplama_{i}.png").convert_alpha()
    jump_frames.append(frame)

# Oyuncu animasyonu
player_index = 0
player_image = player_frames[player_index]
player_pos = pygame.Rect(250, 850, PLAYER_WIDTH, PLAYER_HEIGHT)

# Zıplama animasyonu
jump_index = 0
jumping = False
jump_height = 475  # Zıplama yüksekliği (pixel)
jump_speed = 500  # Zıplama hızı (pixel/saniye)
jump_duration = jump_height / jump_speed  # Zıplama süresi (saniye)
jump_timer = 0.0
jump_animation_speed = 18  # Zıplama animasyon hızı (kareler/saniye)
jump_animation_delay = 1.0 / jump_animation_speed
jump_animation_timer = 0.0  # Zıplama animasyon zamanlayıcısı

# Karakter animasyon hızı ve başlangıç zamanı
player_animation_speed = 24  # Başlangıç hızı (kareler/saniye)
player_animation_timer = 0.0
player_animation_delay = 1.0 / player_animation_speed

# Arka plan hızı ve başlangıç zamanı
background_speed = 600  # Başlangıç hızı (pixeller/saniye)
background_timer = 0.0
background_delay = 1.0 / background_speed

# Oyun süresi
game_time = 0.0

# Engel resmini yükleme
obstacle_image = pygame.image.load("engel.png").convert_alpha()

# İkinci engel resmini yükleme
obstacle2_image = pygame.image.load("engel2.png").convert_alpha()

# Engeller
obstacles = []
obstacles2 = []

def create_obstacle():
    obstacle_y = 900
    obstacle_x = WIDTH  # Engelin başlangıç noktası

    if len(obstacles) == 0:
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        obstacles.append(obstacle_rect)
    else:
        last_obstacle = obstacles[-1]
        min_distance = 450
        max_distance = 900
        random_distance = random.randint(min_distance, max_distance)
        obstacle_x = last_obstacle.x + last_obstacle.width + random_distance
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        obstacles.append(obstacle_rect)

def create_obstacle2():
    obstacle_y = 650
    obstacle_x = WIDTH  # Engelin başlangıç noktası

    if len(obstacles2) == 0:
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, OBSTACLE2_WIDTH, OBSTACLE2_HEIGHT)
        obstacles2.append(obstacle_rect)
    else:
        last_obstacle = obstacles2[-1]
        min_distance = 5000
        max_distance = 6000
        random_distance = random.randint(min_distance, max_distance)
        obstacle_x = last_obstacle.x + last_obstacle.width + random_distance
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, OBSTACLE2_WIDTH, OBSTACLE2_HEIGHT)
        obstacles2.append(obstacle_rect)

# İlk engel oluşturma
create_obstacle()

def check_collision():
    for obstacle in obstacles:
        if player_pos.colliderect(obstacle):
            return True
    for obstacle2 in obstacles2:
        if player_pos.colliderect(obstacle2):
            return True

    return False

# Skor değişkenleri
score = 0
score_delay = 1.0  # Skor artış hızı (saniyede)
score_timer = 0.0

# Oyun durumu
game_over = False

# Start menüsü
show_start_menu = True

# Start menüsü görüntüsü yükleniyor
start_menu_image = pygame.image.load("start_menu.png").convert()

# Ana oyun döngüsü
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(300) / 1000.0  # Zamanı güncelleme

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                if show_start_menu:
                    show_start_menu = False
                elif not jumping and not game_over:
                    jumping = True
                    jump_timer = 0.0
                    jump_animation_timer = 0.0
                elif game_over:
                    # Yeniden başlatmak için değişkenleri sıfırlama
                    player_pos.y = 850
                    jump_timer = 0.0
                    jump_animation_timer = 0.0
                    game_time = 0.0
                    obstacles.clear()
                    obstacles2.clear()
                    create_obstacle()
                    score = 0
                    game_over = False

    if not game_over:
        if show_start_menu:
            # Start menüsünü göster
            screen.blit(start_menu_image, (0, 0))
        else:
            # Ekranı temizleme
            screen.fill((0, 0, 0))

            # Arka plan görüntüsünü pencereye yerleştirme
            screen.blit(background_image, (background_x, 0))
            screen.blit(background_image, (background_x + background_image.get_width(), 0))

            # Arka plan hareketi
            background_x -= background_speed * dt
            if background_x <= -background_image.get_width():
                background_x = 0

            # Oyuncu animasyonunu güncelleme
            player_animation_timer += dt
            if player_animation_timer >= player_animation_delay:
                player_index = (player_index + 1) % len(player_frames)
                player_image = player_frames[player_index]
                player_animation_timer = 0.0

            # Zıplama animasyonunu güncelleme
            if jumping:
                jump_timer += dt
                if jump_timer <= jump_duration / 2:
                    # Yükselme aşaması
                    jump_height = jump_speed * jump_timer
                    player_pos.y = 850 - jump_height
                    jump_index = 2  # Yükselme animasyonu için orta kareler kullanılır
                elif jump_timer <= jump_duration:
                    # İniş aşaması
                    jump_height = jump_speed * (jump_duration - jump_timer)
                    player_pos.y = 850 - jump_height
                    jump_index = 0  # İniş animasyonu için ilk kareler kullanılır
                else:
                    jumping = False
                    player_pos.y = 850

                # Zıplama animasyonunu güncelleme
                jump_animation_timer += dt
                if jump_animation_timer >= jump_animation_delay:
                    jump_index = (jump_index + 1) % len(jump_frames)
                    jump_animation_timer = 0.0
                player_image = jump_frames[jump_index]
            else:
                player_pos.y = 850  # Oyuncu yüksekliği varsayılan değerine geri döner

            # Engelleri güncelleme ve kontrol etme
            for obstacle in obstacles:
                obstacle.x -= OBSTACLE_SPEED * dt
                if obstacle.right < 0:
                    obstacles.remove(obstacle)

            for obstacle in obstacles2:
                obstacle.x -= OBSTACLE2_SPEED * dt
                if obstacle.right < 0:
                    obstacles2.remove(obstacle)

            # Skoru güncelleme
            score_timer += dt * 81
            if score_timer >= score_delay:
                score += 1  # Skoru 1 artır
                score_timer = 0.0

            # Yeni engel oluşturma
            if not game_over and obstacles[-1].x < WIDTH - 800:
                create_obstacle()
                if game_time > 2:
                    create_obstacle2()
            if not game_over and obstacles[-1].x < WIDTH - 800:
                create_obstacle2()

            # Skoru ekrana yazdırma
            score_text = font.render("Skor  " + str(score), True, (255, 255, 255))
            screen.blit(score_text, (20, 20))

            # Oyuncu-Engel çarpışmasını kontrol etme
            if check_collision():
                game_over = True

            # Engelleri ekrana çizme
            for obstacle in obstacles:
                screen.blit(obstacle_image, obstacle)

            for obstacle in obstacles2:
                screen.blit(obstacle2_image, obstacle)

            # Oyuncuyu ekrana çizme
            screen.blit(player_image, player_pos)

            # Oyun süresini güncelleme
            game_time += dt

            # Ekranın sağ üst köşesine süreyi yazdırma
            time_text = font.render(f"Played Time  {int(game_time)} sn", True, (255, 255, 255))
            screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

            # Oyun durumu metnini ekrana çizme
            if game_over:
                text1 = font1.render("Game Over!", True, (255, 255, 255))
                text2 = font2.render("Press SPACE to restart", True, (255, 255, 255))
                text1_rect = text1.get_rect(center=((WIDTH // 2)+15, HEIGHT // 2))
                text2_rect = text2.get_rect(center=(WIDTH // 2, (HEIGHT // 2)+50))
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)
            
            fps = int(clock.get_fps())

            # FPS değerini yazdırma
            fps_text = font.render("FPS: " + str(fps), True, (255, 255, 255))
            screen.blit(fps_text, (1750,1020))

        # Ekranı güncelleme
        pygame.display.flip()

pygame.quit()