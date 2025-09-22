import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌊 해수면 상승 게임")

# 색상
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 캐릭터
player_width, player_height = 30, 30
player_x, player_y = WIDTH//2, HEIGHT-50
player_speed = 5

# 해수면
water_height = 0
water_speed = 0.2

# FPS
clock = pygame.time.Clock()

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # 해수면 상승
    water_height += water_speed
    water_y = HEIGHT - water_height

    # 충돌 체크
    if player_y + player_height > water_y:
        font = pygame.font.SysFont(None, 50)
        text = font.render("게임 종료! 🌊", True, RED)
        screen.blit(text, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # 화면 그리기
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, water_y, WIDTH, water_height))
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

    pygame.display.flip()
    clock.tick(60)
