import pygame
from random import *

# 레벨에 맞게 설정
def setup(level):
    # 얼마나 많은 숫자를 보여줄 것인가?
    number_count = (level // 3) + 5
    number_count = min(number_count, 20) # 만약 20을 초과하면 20으로 처리

    # 실제 화면에 grid 형태로 숫자를 랜덤으로 배치
    shuffle_grid(number_count)

# 숫자 섞기 (이프로젝트에서 가장 중요!)
def shuffle_grid(number_count):
    rows = 5
    columns = 9

    cell_size = 130 # 각 Grid cell 별 가로, 세로 크기
    button_size = 110 # Grid cell 내에 실제로 그려질 버튼 크기
    screen_left_margin = 55 # 전체 스크린 왼쪽 여백
    screen_top_margin = 20 # 전체 스크린 위쪽 여백
    
    # [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    grid = [[0 for col in range(columns)] for row in range(rows)] # 5 X 9
    
    number = 1 # 시작 숫자를 1부터 number_count 까지
    while number <= number_count:
        row_index = randrange(0, rows) # 0, 1, 2, 3, 4 중에서 랜덤으로 뽑기
        col_index = randrange(0, columns) # 0 ~ 8 중에서 랜덤으로 뽑기
        
        if grid[row_index][col_index] == 0:
            grid[row_index][col_index] = number # 숫자 지정
            number += 1

            # 현재 Grid cell 위치 기준으로 x, y 위치를 구함
            center_x = screen_left_margin + (col_index * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_index * cell_size) + (cell_size / 2)

            # 숫자 버튼 만들기
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)
    
    # 배치된 랜덤 숫자 확인
    print(grid)
    

# 시작 화면 보여주기
def display_start_screen():
    # 동그라미 그리기 (장소, 색깔, 중심좌표, 반지름 길이, 선 두께)
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)

# 게임 화면 보여주기
def display_game_screen():
    for idx, rect in enumerate(number_buttons, start=1):
        pygame.draw.rect(screen, GRAY, rect)

        # 실제 숫자 텍스트
        cell_text = game_font.render(str(idx), True, WHITE) # 숫자 텍스트
        text_rect = cell_text.get_rect(center=rect.center) # rect 의 센터값
        screen.blit(cell_text, text_rect) # 숫자 텍스트의 위치를 rect의 센터값으로 정의
    
# 포지션에 해당하는 버튼 확인
def check_buttons(pos):
    global start
    if start_button.collidepoint(pos):
        start = True

######################################################################

pygame.init() # 초기화
screen_width = 1280 # 가로 크기
screen_height = 720 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height)) # 화면 구성
pygame.display.set_caption("Memory Game") # 제목
game_font = pygame.font.Font(None, 120) # 폰트 정의

# 시작 버튼
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)

# 색깔
BLACK = (0, 0, 0) # RGB
WHITE = (255, 255, 255) # RGB
GRAY = (50, 50, 50)

number_buttons = [] # 플레이어가 눌러야 하는 버튼들

# 게임 시작 여부
start = False

# 게임 시작 전에 게임 설정 함수 수행
setup(1)

# 게임 루프
running = True # 게임이 실행 중인가?
while running:

    click_pos = None

    # 이벤트 루프
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트인가?
            running = False # 게임이 더 이상 실행중이 아님
        elif event.type == pygame.MOUSEBUTTONUP: # 사용자가 마우스를 클릭했을 때
            click_pos = pygame.mouse.get_pos()
            print(click_pos)
    # 화면 전체를 검은색으로 칠함
    screen.fill(BLACK)

    if start: 
        display_game_screen() # 게임 화면 표시
    else:
        display_start_screen() # 시작 화면 표시

    # 사용자가 클릭한 좌표 값이 있다면 (어딘가 클릭했다면)
    if click_pos:
        check_buttons(click_pos)

    # 화면 업데이트
    pygame.display.update()

# 게임 종료
pygame.quit()