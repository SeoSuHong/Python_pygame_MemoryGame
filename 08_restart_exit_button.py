import pygame
from random import *

# 레벨에 맞게 설정
def setup(level):
    global display_time
    # 얼마동안 숫자를 보여줄지
    display_time = 5 - (level // 3)
    display_time = max(display_time, 3) # 1초 미만이면 1초로 처리

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
    global curr_level

    msg_curr_level = game_font.render(f"{curr_level} LEVEL", True, WHITE)
    msg_curr_level_rect = msg_curr_level.get_rect(center=((screen_width / 2), (screen_height / 2)))

    screen.blit(msg_curr_level, msg_curr_level_rect)

    # 동그라미 그리기 (장소, 색깔, 중심좌표, 반지름 길이, 선 두께)
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)

# 게임 화면 보여주기
def display_game_screen():
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> sec
        if elapsed_time > display_time:
            hidden = True

    for idx, rect in enumerate(number_buttons, start=1):
        if hidden: # 숫자 숨김 처리
            # 사각형 버튼 그리기
            pygame.draw.rect(screen, WHITE, rect)
        else:
            # 실제 숫자 텍스트
            cell_text = game_font.render(str(idx), True, WHITE) # 숫자 텍스트
            text_rect = cell_text.get_rect(center=rect.center) # rect 의 센터값
            screen.blit(cell_text, text_rect) # 숫자 텍스트의 위치를 rect의 센터값으로 정의
    
# 포지션에 해당하는 버튼 확인
def check_buttons(pos):
    global start, over, start_ticks, running, curr_level, main

    if start: # 게임이 시작했다면?
        check_number_buttons(pos)
    elif start_button.collidepoint(pos): # 시작 버튼을 누를 시
        start = True
        start_ticks = pygame.time.get_ticks() # 타이머 시작 (현재 시간을 저장)
    elif restart_button.collidepoint(pos): # 게임 끝난 후 시작 버튼을 누를 시
        running = False
        main = False
        main = True
    elif exit_button.collidepoint(pos): # 게임 끝난 후 나가기 버튼을 누를 시
        running = False
        main = False

# 클릭한 숫자의 정답처리
def check_number_buttons(pos):
    global start, hidden, curr_level

    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]: # 올바른 숫자 클릭
                print("Correct")
                del number_buttons[0] # 클릭한 숫자 삭제
                if not hidden:
                    hidden = True # 숫자 숨김 처리
            else: # 잘못된 숫자 클릭
                game_over()
            break
    
    # 모든 숫자를 다 맞췄다면? 레벨 업 하여 다시 시작화면으로 감
    if len(number_buttons) == 0:
        start = False
        hidden = False
        curr_level += 1
        setup(curr_level)

# 게임 종료 처리 and 'Game Over' 메시지
def game_over():
    global over, start, restart_button, exit_button
    start = False
    over = True

    msg_over = game_font.render("Game Over", True, WHITE)
    msg_level = game_font.render(f"Your level is {curr_level}", True, WHITE)
    msg_over_rect = msg_over.get_rect(center=((screen_width / 2), (screen_height / 2) - 120))
    msg_level_rect = msg_level.get_rect(center=((screen_width / 2), (screen_height / 2)))

    screen.fill(BLACK)
    screen.blit(msg_over, msg_over_rect)
    screen.blit(msg_level, msg_level_rect)
    screen.blit(restart_button_txt, restart_button_rect)
    screen.blit(exit_button_txt, exit_button_rect)

######################################################################

main = True # 재시작 시 전체 초기화
while main:
    pygame.init() # 초기화
    screen_width = 1280 # 가로 크기
    screen_height = 720 # 세로 크기
    screen = pygame.display.set_mode((screen_width, screen_height)) # 화면 구성
    pygame.display.set_caption("Memory Game") # 제목
    game_font = pygame.font.Font(None, 120) # 폰트 정의
    game_restart_font = pygame.font.Font(None, 90) # START, EXIT 폰트 정의

    # 색깔
    BLACK = (0, 0, 0) # RGB
    WHITE = (255, 255, 255) # RGB
    GRAY = (50, 50, 50)

    # 시작 버튼
    start_button = pygame.Rect(0, 0, 120, 120)
    start_button.center = (120, screen_height - 120)

    # 재시작 버튼
    restart_button = pygame.Rect(0, 0, 150, 100)
    restart_button.center = ((screen_width / 4), (screen_height - 120))
    restart_button_txt = game_restart_font.render("START", True, WHITE)
    restart_button_rect = restart_button_txt.get_rect(center=restart_button.center)

    # 나가기 버튼
    exit_button = pygame.Rect(0, 0, 150, 100)
    exit_button.center = ((screen_width / 4) * 3, (screen_height - 120))
    exit_button_txt = game_restart_font.render("EXIT", True, WHITE)
    exit_button_rect = exit_button_txt.get_rect(center=exit_button.center)

    number_buttons = [] # 플레이어가 눌러야 하는 버튼들
    curr_level = 1 # 현재 레벨
    display_time = None # 숫자를 보여주는 시간
    start_ticks = None # 시간 계산 (현재 시간 정보를 저장)

    # 게임 시작 여부
    start = False

    # 게임 오버 여부
    over = False

    # 숫자 숨김 여부
    hidden = False

    # 게임 시작 전에 게임 설정 함수 수행
    setup(curr_level)

    # 게임 루프
    running = True # 게임이 실행 중인가?
    while running:

        click_pos = None

        # 이벤트 루프
        for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
            if event.type == pygame.QUIT: # 창이 닫히는 이벤트인가?
                running = False # 게임이 더 이상 실행중이 아님
                main = False
                break
            elif event.type == pygame.MOUSEBUTTONUP: # 사용자가 마우스를 클릭했을 때
                click_pos = pygame.mouse.get_pos()
                print(click_pos)
        # 화면 전체를 검은색으로 칠함
        screen.fill(BLACK)

        if start: 
            display_game_screen() # 게임 화면 표시
        elif over:
            game_over()
        else:
            display_start_screen() # 시작 화면 표시

        # 사용자가 클릭한 좌표 값이 있다면 (어딘가 클릭했다면)
        if click_pos:
            check_buttons(click_pos)

        # 화면 업데이트
        pygame.display.update()

    # 게임 종료
    pygame.quit()