import pygame
import random
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sea Level Rising - TOFU Style")

# 색상
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)    # 플레이어
BLUE = (50, 150, 255)    # 해수면
ICE = (200, 240, 255)    # 얼음 블록

# 플레이어 설정
player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 60, 50, 20)
player_speed = 7

# 얼음 블록 설정
blocks = []
block_width, block_height = 30, 30
block_speed = 5
spawn_delay = 30  # 블록 생성 주기
frame_count = 0

# 점수 및 해수면
score = 0
sea_level = HEIGHT - 20   # 처음 해수면 위치 (아래쪽)
sea_rise = 0              # 해수면 상승량
font = pygame.font.SysFont("arial", 24)

clock = pygame.time.Clock()

def draw():
    screen.fill(WHITE)

    # 해수면
    pygame.draw.rect(screen, BLUE, (0, sea_level, WIDTH, HEIGHT - sea_level))

    # 플레이어
    pygame.draw.rect(screen, GREEN, player)

    # 얼음 블록
    for block in blocks:
        pygame.draw.rect(screen, ICE, block)

    # 점수
    text = font.render(f"점수: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # 블록 생성
    frame_count += 1
    if frame_count % spawn_delay == 0:
        x = random.randint(0, WIDTH - block_width)
        blocks.append(pygame.Rect(x, 0, block_width, block_height))

    # 블록 이동
    for block in blocks:
        block.y += block_speed

    # 충돌 체크
    for block in blocks[:]:
        if block.colliderect(player):
            score += 1
            blocks.remove(block)  # 얼음 받으면 점수
        elif block.y > HEIGHT:
            sea_rise += 20       # 얼음 놓치면 해수면 상승
            blocks.remove(block)

    # 해수면 상승 처리
    sea_level -= sea_rise // 100  # 일정 점수 놓칠 때마다 상승
    if sea_level <= player.y:
        print("Game Over! 해수면에 잠겼습니다.")
        pygame.quit()
        sys.exit()

    draw()
    clock.tick(60)
