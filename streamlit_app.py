import pygame
import random
import sys

# -------------------------------
# 초기화
# -------------------------------
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sea Level Rising - TOFU Game")

# -------------------------------
# 색상
# -------------------------------
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
LIGHTBLUE = (150, 200, 255)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)

# -------------------------------
# 캐릭터 설정
# -------------------------------
player_width, player_height = 40, 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 100
player_speed = 5
y_velocity = 0
gravity = 0.5
jump_power = -10

# -------------------------------
# 블록 설정
# -------------------------------
blocks = [pygame.Rect(WIDTH//2 - 50, HEIGHT-50, 100, 20)]
block_speed = 2
block_width, block_height = 100, 20

# -------------------------------
# 해수면 설정
# -------------------------------
sea_level = HEIGHT - 30
sea_rise_speed = 0.02  # 초당 상승량

# -------------------------------
# 점수 / 레벨
# -------------------------------
score = 0
level = 1

# -------------------------------
# 시계
# -------------------------------
clock = pygame.time.Clock()

# -------------------------------
# 폰트
# -------------------------------
font = pygame.font.SysFont(None, 30)

# -------------------------------
# 게임 루프
# -------------------------------
running = True
while running:
    dt = clock.tick(60) / 1000  # 초 단위

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------------------------------
    # 키 입력
    # -------------------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # -------------------------------
    # 중력
    # -------------------------------
    y_velocity += gravity
    player_y += y_velocity

    # -------------------------------
    # 블록 충돌
    # -------------------------------
    on_block = False
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for block in blocks:
        if player_rect.colliderect(block) and y_velocity >= 0:
            player_y = block.top - player_height
            y_velocity = jump_power  # 자동 점프
            on_block = True
            score += 1

    # -------------------------------
    # 새로운 블록 생성
    # -------------------------------
    if blocks[-1].y < HEIGHT - 150:
        new_block_x = random.randint(0, WIDTH - block_width)
        new_block = pygame.Rect(new_block_x, HEIGHT, block_width, block_height)
        blocks.append(new_block)

    # -------------------------------
    # 블록 이동 (위로)
    # -------------------------------
    for block in blocks:
        block.y -= block_speed
    blocks = [b for b in blocks if b.y > -50]

    # -------------------------------
    # 해수면 상승
    # -------------------------------
    sea_level -= sea_rise_speed * 60  # 프레임 단위로 조금씩 상승

    # -------------------------------
    # 게임 종료
    # -------------------------------
    if player_y + player_height > sea_level:
        print("Game Over! 바닷물에 잠겼습니다.")
        running = False

    # -------------------------------
    # 레벨 상승
    # -------------------------------
    if score >= level * 10:
        level += 1
        block_speed += 0.5
        sea_rise_speed += 0.005

    # -------------------------------
    # 화면 그리기
    # -------------------------------
    screen.fill(WHITE)

    # 해수면
    pygame.draw.rect(screen, BLUE, (0, sea_level, WIDTH, HEIGHT - sea_level))

    # 블록
    for block in blocks:
        pygame.draw.rect(screen, LIGHTBLUE, block)

    # 캐릭터
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

    # 점수 / 레벨 표시
    score_text = font.render(f"점수: {score}  레벨: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
