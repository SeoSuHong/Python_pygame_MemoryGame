import pygame

pygame.init() # 초기화
screen_width = 1280 # 가로 크기
screen_height = 720 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height)) # 화면 구성
pygame.display.set_caption("Memory Game") # 제목

# 게임 루프
running = True # 게임이 실행 중인가?
while running:
    # 이벤트 루프
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트인가?
            running = False # 게임이 더 이상 실행중이 아님

# 게임 종료
pygame.quit()