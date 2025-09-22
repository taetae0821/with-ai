import pygame
import random
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 300, 500  # 화면 크기 줄임
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sea Level Rising Game (Fast)")

# 색상
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)

# 캐릭터 설정
player = pygame.Rect(WIDTH//2 - 15, HEIGHT-70, 30, 30)  # 크기 축소
player_speed = 5
gravity = 0.5
jump_power = -10
y_velocity = 0

# 블록(해수면) 설정
blocks = [pygame.Rect(WIDTH//2 - 40, HEIGHT-40, 80, 15)]
block_speed = 3  # 위로 올라가는 속도 ↑
MAX_BLOCKS = 8   # 동시에 존재할 수 있는 최대 블록 수

clock = pygame.time.Clock()

def draw():
    screen.fill(WHITE)

    # 블록 그리기
    for block in blocks:
        pygame.draw.rect(screen, BLUE, block)

    # 캐릭터 그리기
    pygame.draw.rect(screen, GREEN, player)

    pygame.display.flip()

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # 중력 적용
    y_velocity += gravity
    player.y += y_velocity

    # 블록 위 충돌 처리
    for block in blocks:
        if player.colliderect(block) and y_velocity >= 0:
            player.bottom = block.top
            y_velocity = jump_power  # 자동 점프

    # 새로운 블록 생성
    if blocks[-1].y < HEIGHT - 120 and len(blocks) < MAX_BLOCKS:
        new_block = pygame.Rect(random.randint(40, WIDTH-120), HEIGHT, 80, 15)
        blocks.append(new_block)

    # 블록 위로 이동
    for block in blocks:
        block.y -= block_speed
    blocks = [b for b in blocks if b.y > -30]

    # 바닥에 떨어지면 게임 종료
    if player.y > HEIGHT:
        print("Game Over! 바닷물에 잠겼습니다.")
        pygame.quit()
        sys.exit()

    draw()
    clock.tick(60)  # 60 FPS 고정
