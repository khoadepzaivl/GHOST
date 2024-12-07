import pygame
import math
import random
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GHOST")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Tốc độ khung hình
clock = pygame.time.Clock()
FPS = 60

# vịt
tank_width = 100
tank_height = 80
tank_speed = 5
recoil_strength = 5  # Tăng cường giật lùi

# Đạn
bullet_width = 25
bullet_height = 35
bullet_speed = 7

# Kẻ địch
enemy_width = 50
enemy_height = 50
enemy_speed = 1.5

# Hình ảnh
start_screen_image = pygame.image.load("Project python/image/start.png")
start_screen_image = pygame.transform.scale(start_screen_image, (screen_width, screen_height))

background_image = pygame.image.load("Project python/image/background1.gif")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

enemy_image = pygame.image.load("Project python/image/ghost.gif")
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

tank_image = pygame.image.load("Project python/image/tank.png")
tank_image = pygame.transform.scale(tank_image, (tank_width, tank_height))

bullet_image = pygame.image.load("Project python/image/fireball.png")
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))

# Nhạc nền
pygame.mixer.music.load("Project python/music/soundbackground.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)


def set_custom_cursor():
    cursor_image = pygame.image.load("Project python/image/mouse2.png")  # Đường dẫn tới hình ảnh con trỏ
    cursor_image = pygame.transform.scale(cursor_image, (32, 32))  # Điều chỉnh kích thước nếu cần
    pygame.mouse.set_visible(False)  # Ẩn con trỏ mặc định
    return cursor_image


def show_start_screen():
    screen.blit(start_screen_image, (0, 0))  # Hiển thị màn hình start
    pygame.display.flip()


def draw_tank(x, y):
    screen.blit(tank_image, (x, y, tank_width, tank_height))


def draw_bullet(bullet):
    screen.blit(bullet_image, (bullet[0], bullet[1], bullet_width, bullet_height))


def draw_enemy(enemy):
    screen.blit(enemy_image, (enemy[0], enemy[1]))


def draw_score(score):
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def calculate_angle(tank_x, tank_y, mouse_x, mouse_y):
    return math.atan2(mouse_y - tank_y, mouse_x - tank_x)


def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)


def ask_to_play_again():
    font = pygame.font.SysFont("Arial", 24)
    text = font.render("Do you want to play again? (Y/N)", True, RED)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # 'Y' for Yes
                    return True
                elif event.key == pygame.K_n:  # 'N' for No
                    return False


def reset_game():
    global tank_x, tank_y, bullets, enemies, score, tank_recoil
    tank_x = screen_width // 2 - tank_width // 2
    tank_y = screen_height // 2 - tank_height // 2
    bullets = []
    enemies = []
    score = 0
    tank_recoil = 0


def main():
    global tank_x, tank_y, bullets, enemies, score, tank_recoil

    tank_x = screen_width // 2 - tank_width // 2
    tank_y = screen_height // 2 - tank_height // 2
    bullets = []
    enemies = []
    score = 0
    tank_recoil = 0

    cursor_image = set_custom_cursor()  # Thiết lập con trỏ tùy chỉnh

    running = True
    game_over = False

    show_start_screen()

    # Chờ người chơi nhấn chuột để bắt đầu game
    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_game = True

    while running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        draw_tank(tank_x, tank_y)
        for bullet in bullets:
            draw_bullet(bullet)
        for enemy in enemies:
            draw_enemy(enemy)

        draw_score(score)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        angle = calculate_angle(tank_x + tank_width // 2, tank_y + tank_height // 2, mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            shoot_sound = pygame.mixer.Sound("Project python/music/soundgun.mp3")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                shoot_sound.play()
                if tank_recoil == 0:
                    bullet_x = tank_x + tank_width // 2 - bullet_width // 2
                    bullet_y = tank_y
                    bullets.append([bullet_x, bullet_y, angle])
                    tank_recoil = recoil_strength

        if game_over:
            font = pygame.font.SysFont("Arial", 48)
            lose_text = font.render("You Lose!", True, RED)
            screen.blit(lose_text, (screen_width // 2 - lose_text.get_width() // 2, screen_height // 2 - lose_text.get_height() // 2))
            gameover_music = pygame.mixer.Sound("Project python/music/gameover.mp3")
            gameover_music.play()
            play_again = ask_to_play_again()

            if play_again:
                reset_game()
                game_over = False
            else:
                running = False

        else:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and tank_x > 0:
                tank_x -= tank_speed
            if keys[pygame.K_RIGHT] and tank_x < screen_width - tank_width:
                tank_x += tank_speed
            if keys[pygame.K_UP] and tank_y > 0:
                tank_y -= tank_speed
            if keys[pygame.K_DOWN] and tank_y < screen_height - tank_height:
                tank_y += tank_speed

            if tank_recoil > 0:
                recoil_x = -recoil_strength * math.cos(angle)
                recoil_y = -recoil_strength * math.sin(angle)

                tank_x += recoil_x
                tank_y += recoil_y

                tank_x = max(0, min(tank_x, screen_width - tank_width))
                tank_y = max(0, min(tank_y, screen_height - tank_height))

                tank_recoil -= 1

            for bullet in bullets[:]:
                bullet[0] += bullet_speed * math.cos(bullet[2])
                bullet[1] += bullet_speed * math.sin(bullet[2])

                if bullet[1] < 0 or bullet[0] < 0 or bullet[0] > screen_width or bullet[1] > screen_height:
                    bullets.remove(bullet)

            for enemy in enemies:
                angle_to_tank = calculate_angle(enemy[0] + enemy_width // 2, enemy[1] + enemy_height // 2, tank_x + tank_width // 2, tank_y + tank_height // 2)
                enemy[0] += enemy_speed * math.cos(angle_to_tank)
                enemy[1] += enemy_speed * math.sin(angle_to_tank)

                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
                #tank_rect = pygame.Rect(tank_x, tank_y, tank_width, tank_height)
                if check_collision(tank_rect, enemy_rect):
                    game_over = True

            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
                for enemy in enemies[:]:
                    enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
                    if check_collision(bullet_rect, enemy_rect):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 10

            if len(enemies) < 5:
                if pygame.time.get_ticks() % 100 == 0:
                    enemy_x = random.randint(0, screen_width - enemy_width)
                    enemy_y = random.randint(0, screen_height - enemy_height)
                    enemies.append([enemy_x, enemy_y])

        # Vẽ con trỏ tùy chỉnh lên màn hình
        screen.blit(cursor_image, (mouse_x, mouse_y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
