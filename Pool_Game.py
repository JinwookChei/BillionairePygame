import pygame
import sys
import math
import Physics
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

###물리 참고 https://en.wikipedia.org/wiki/Elastic_collision

# 화면 크기 설정
pygame.init()
screen_width = 1600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PoolGame")

# 인터페이스 설정
font = pygame.font.Font(None, 36)

# 그림 설정
image_path = resource_path("./image/Board1.png")
image = pygame.image.load(image_path)
image = pygame.transform.scale(image, (900, 450))  # 원하는 크기로 조정

image_Cue_Path = resource_path("./image/Cue.png")
image_Cue = pygame.image.load(image_Cue_Path)
image_Cue = pygame.transform.scale(image_Cue,(300,10))

image_Ball1_Path = resource_path("./image/Ball1.png")
image_Ball2_Path = resource_path("./image/Ball2.png")
image_Ball3_Path = resource_path("./image/Ball3.png")
image_Ball4_Path = resource_path("./image/Ball4.png")
image_Ball5_Path = resource_path("./image/Ball5.png")
image_Ball6_Path = resource_path("./image/Ball6.png")
image_Ball7_Path = resource_path("./image/Ball7.png")
image_Ball8_Path = resource_path("./image/Ball8.png")
image_Ball9_Path = resource_path("./image/Ball9.png")
image_Ball10_Path = resource_path("./image/Ball10.png")
image_Ball11_Path = resource_path("./image/Ball11.png")
image_Ball12_Path = resource_path("./image/Ball12.png")
image_Ball13_Path = resource_path("./image/Ball13.png")
image_Ball14_Path = resource_path("./image/Ball14.png")
image_Ball15_Path = resource_path("./image/Ball15.png")
image_WhiteBall_Path = resource_path("./image/ball_16.png")

image_Ball1 = pygame.image.load(image_Ball1_Path)
image_Ball1 = pygame.transform.scale(image_Ball1,(20,20))

image_Ball2 = pygame.image.load(image_Ball2_Path)
image_Ball2 = pygame.transform.scale(image_Ball2,(20,20))

image_Ball3 = pygame.image.load(image_Ball3_Path)
image_Ball3 = pygame.transform.scale(image_Ball3,(20,20))

image_Ball4 = pygame.image.load(image_Ball4_Path)
image_Ball4 = pygame.transform.scale(image_Ball4,(20,20))

image_Ball5 = pygame.image.load(image_Ball5_Path)
image_Ball5 = pygame.transform.scale(image_Ball5,(20,20))

image_Ball6 = pygame.image.load(image_Ball6_Path)
image_Ball6 = pygame.transform.scale(image_Ball6,(20,20))

image_Ball7 = pygame.image.load(image_Ball7_Path)
image_Ball7 = pygame.transform.scale(image_Ball7,(20,20))

image_Ball8 = pygame.image.load(image_Ball8_Path)
image_Ball8 = pygame.transform.scale(image_Ball8,(20,20))

image_Ball9 = pygame.image.load(image_Ball9_Path)
image_Ball9 = pygame.transform.scale(image_Ball9,(20,20))

image_Ball10 = pygame.image.load(image_Ball10_Path)
image_Ball10 = pygame.transform.scale(image_Ball10,(20,20))

image_Ball11 = pygame.image.load(image_Ball11_Path)
image_Ball11 = pygame.transform.scale(image_Ball11,(20,20))

image_Ball12 = pygame.image.load(image_Ball12_Path)
image_Ball12 = pygame.transform.scale(image_Ball12,(20,20))

image_Ball13 = pygame.image.load(image_Ball13_Path)
image_Ball13 = pygame.transform.scale(image_Ball13,(20,20))

image_Ball14 = pygame.image.load(image_Ball14_Path)
image_Ball14 = pygame.transform.scale(image_Ball14,(20,20))

image_Ball15 = pygame.image.load(image_Ball15_Path)
image_Ball15 = pygame.transform.scale(image_Ball15,(20,20))

image_WhiteBall = pygame.image.load(image_WhiteBall_Path)
image_WhiteBall = pygame.transform.scale(image_WhiteBall,(20,20))

Font_bold = pygame.font.Font(None, 50)
Font = pygame.font.Font(None, 36)


# Turn Condition
Turning = False
Condition_Turn = 1
Previous_Turn = 2
Current_Turn = 1
BallsMoving = False
GameClear_Condition = 0


class Player:
    def __init__(self, PlayerID):    
        self.PlayerID = PlayerID
        self.Goal_Balls = []
        self.Remaining_points = 7


    def DisPlay_Situation(self, Pos_x, Pos_y):
        for i in range(len(self.Goal_Balls)):
            Pos_x += 30
            screen.blit(self.Goal_Balls[i].image, (Pos_x, Pos_y))



class Cue:
    Cue_Coord = [0,0]
    Mouse_Coord = [0,0]
    click_condition = 0
    Cue_count = 0
    CuePower_MAX = 20
    def __init__(self, x, y):
        self.Coord = [x,y]


class Ball:
    Coord = [0, 0]
    Velocity = [0, 0]
    Radius = 10
    Angular_rotation = 0
    friction = 0.998
    IsStop = True
    IsGoal = False
    Ball_ID = 0
    Collision_ON = True

    Color = (255, 255, 255)

    def __init__(self, x, y, image, PlayerNum):
        self.Coord = [x,y]
        self.image = image
        self.Ball_ID = PlayerNum

    def move(self):
        self.Coord[0] = self.Coord[0] + self.Velocity[0]
        self.Coord[1] = self.Coord[1] + self.Velocity[1]

        self.Velocity[0] *= self.friction
        self.Velocity[1] *= self.friction

        if(abs(self.Velocity[0]) < 0.1 and abs(self.Velocity[1]) < 0.1):
            self.Velocity = [0.0, 0.0]
            self.IsStop = True
        else:
            self.IsStop = False
    
    def IsCollision(self, r1, Coord1, r2, Coord2):
        distance = math.sqrt((Coord1[0] - Coord2[0]) ** 2 + (Coord1[1] - Coord2[1]) ** 2)
        if distance < r1 + r2:
            return True
        else:
            return False
    
    def CollisionToBall(self, OtherBall):
        if(self.IsCollision(self.Radius, self.Coord, OtherBall.Radius, OtherBall.Coord) == True and self.Collision_ON == True):
            AfterElastic_v = Physics.ElasticCollision_2D(30, self.Coord, self.Velocity, 30, OtherBall.Coord, OtherBall.Velocity)

            self.Velocity[0] = AfterElastic_v[0]
            self.Velocity[1] = AfterElastic_v[1]
            
            OtherBall.Velocity[0] = AfterElastic_v[2]
            OtherBall.Velocity[1] = AfterElastic_v[3]

            #오버랩 버그 발생 경우 코드!! 예외처리
            if(Physics.CircleIOU(self.Radius, [self.Coord[0] + self.Velocity[0], self.Coord[1] + self.Velocity[1]], OtherBall.Radius,[OtherBall.Coord[0]+OtherBall.Velocity[0], OtherBall.Coord[1]+ OtherBall.Velocity[1]]) > 0):
                # OtherBall.Coord[0] +=OtherBall.Radius/5
                # OtherBall.Coord[1] +=OtherBall.Radius/5
                self.Coord[0] += self.Velocity[0] *3
                self.Coord[1] += self.Velocity[1] *3

                OtherBall.Coord[0] +=OtherBall.Velocity[0] *3
                OtherBall.Coord[1] +=OtherBall.Velocity[1] *3

                 
            
    def CollisionToWall_X(self):
        self.Velocity[0] = -self.Velocity[0]

    def CollisionToWall_Y(self):
        self.Velocity[1] = -self.Velocity[1]
    
    def Goal(self):
        if(Physics.CircleIOU(self.Radius, self.Coord, 25, [331,224]) > 300):
            self.IsGoal = True
        
        elif(Physics.CircleIOU(self.Radius, self.Coord, 25, [726,217]) > 300):
            self.IsGoal = True

        elif(Physics.CircleIOU(self.Radius, self.Coord, 25, [1121,224]) > 300):
            self.IsGoal = True

        elif(Physics.CircleIOU(self.Radius, self.Coord, 25, [331,578]) > 300):
            self.IsGoal = True

        elif(Physics.CircleIOU(self.Radius, self.Coord, 25, [726,585]) > 300):
            self.IsGoal = True

        elif(Physics.CircleIOU(self.Radius, self.Coord, 25, [1121,578]) > 300):
            self.IsGoal = True


class WhiteBall(Ball):
    def __init__(self, x, y, image, PlayerNum):
        super().__init__(x, y, image, PlayerNum)
        self.Color = (255,255,255)


class Blackball(Ball):
    def __init__(self, x, y, image, PlayerNum):
        super().__init__(x,y, image, PlayerNum)
        self.Color = (0,0,0)    

class ColorBall(Ball):
    def __init__(self, x, y, image, PlayerNum):
        super().__init__(x,y, image, PlayerNum)
        self.Color = (255,0,0)



class BlackHoll():
    Coord = [0, 0]
    Radius = 15
    def __init__(self, x,y):
        self.Coord = [x,y]


Player1 = Player("Player 1")
Player2 = Player("Player 2")

CueStand = Cue(0,0)
CueBall = WhiteBall(500, 400, image_WhiteBall, 0)
EightBall = Blackball(940, 400, image_Ball8, 3)

ColorBall1 = ColorBall(900, 400, image_Ball1, 1)
ColorBall2 = ColorBall(920, 388, image_Ball2, 1)
ColorBall3 = ColorBall(940, 425, image_Ball3, 1)
ColorBall4 = ColorBall(960, 363, image_Ball4, 1)
ColorBall5 = ColorBall(960, 413, image_Ball5, 1)
ColorBall6 = ColorBall(980, 450, image_Ball6, 1)
ColorBall7 = ColorBall(980, 375, image_Ball7, 1)
ColorBall9 = ColorBall(920, 412, image_Ball9, 2)
ColorBall10 = ColorBall(940, 375, image_Ball10, 2)
ColorBall11 = ColorBall(960, 438, image_Ball11, 2)
ColorBall12 = ColorBall(960, 388, image_Ball12, 2)
ColorBall13 = ColorBall(980, 350, image_Ball13, 2)
ColorBall14 = ColorBall(980, 400, image_Ball14, 2)
ColorBall15 = ColorBall(980, 425, image_Ball15, 2)


ColorBallList = [ColorBall1,ColorBall2,ColorBall3,ColorBall4,ColorBall5,ColorBall6,ColorBall7,ColorBall9,ColorBall10,ColorBall11,ColorBall12,ColorBall13,ColorBall14, ColorBall15, EightBall]


# 게임 루프
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(image, (275, 175))

    #플레이어 턴 선택
    if(Condition_Turn == 1):
        Current_Turn = 1
        Player1_ID = Font_bold.render(Player1.PlayerID, True, (255, 255, 0))
        Player2_ID = Font_bold.render(Player2.PlayerID, True, (255, 255, 255))
        
    elif(Condition_Turn == 2):
        Current_Turn = 2
        Player1_ID = Font_bold.render(Player1.PlayerID, True, (255, 255, 255))
        Player2_ID = Font_bold.render(Player2.PlayerID, True, (255, 255, 0))
        
    elif(Condition_Turn == 0):
        Player1_ID = Font_bold.render(Player1.PlayerID, True, (255, 0, 0))
        Player2_ID = Font_bold.render(Player2.PlayerID, True, (255, 0, 0))

    screen.blit(Player1_ID, (1300, 200))
    screen.blit(Player2_ID, (1300, 450))

    if(Player1.Remaining_points != 0):
        Player1_Score = font.render("Remaining Score : " + str(Player1.Remaining_points), True, (255, 255, 255))
    elif(Player1.Remaining_points == 0):
        Player1_Score = font.render("Place the black ball !!", True, (0, 255, 0))
    if(Player2.Remaining_points != 0): 
        Player2_Score = font.render("Remaining Score : " + str(Player2.Remaining_points), True, (255, 255, 255))
    elif(Player2.Remaining_points == 0):
        Player2_Score = font.render("Place the black ball !! : " , True, (0, 255, 0))

    screen.blit(Player1_Score, (1250, 250))
    screen.blit(Player2_Score, (1250, 500))

    Player1.DisPlay_Situation(1250, 300)
    Player2.DisPlay_Situation(1250, 550)

    CueStand.Mouse_Coord= pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and Turning == False:
            CueStand.click_condition = 1
        elif event.type == pygame.MOUSEBUTTONUP and Turning == False:
            CueStand.click_condition = 2
            CueStand.Cue_count = 0

            Cue_Power = [(CueBall.Coord[0] - CueStand.Cue_Coord[0])/30, (CueBall.Coord[1] - CueStand.Cue_Coord[1])/30]
            if abs(Cue_Power[0]) > CueStand.CuePower_MAX:
                Cue_Power[0] = Cue_Power[0] / abs(Cue_Power[0]) * CueStand.CuePower_MAX
            if abs(Cue_Power[1]) > CueStand.CuePower_MAX:
                Cue_Power[1] = Cue_Power[0] / abs(Cue_Power[0]) * CueStand.CuePower_MAX
            print(Cue_Power)

            CueBall.Velocity = Cue_Power

        if event.type == pygame.QUIT:
            running = False

    if(CueStand.click_condition == 1 and Turning == False):
        # 큐가 하얀 공 방향을 가리키도록 회전
        angle = math.degrees(math.atan2(CueBall.Coord[1] - CueStand.Mouse_Coord[1], CueBall.Coord[0] - CueStand.Mouse_Coord[0]))
        rotated_image_Cue = pygame.transform.rotate(image_Cue, -angle)
        cue_rect = rotated_image_Cue.get_rect(center=CueStand.Mouse_Coord)

        # 큐 이미지를 그리기 전에 회전시킨 이미지를 사용
        screen.blit(rotated_image_Cue, cue_rect)
        CueStand.Cue_Coord[0] = CueStand.Mouse_Coord[0] + 150*math.cos(math.atan2(CueBall.Coord[1] - CueStand.Mouse_Coord[1], CueBall.Coord[0] - CueStand.Mouse_Coord[0]))
        CueStand.Cue_Coord[1] = CueStand.Mouse_Coord[1] + 150*math.sin(math.atan2(CueBall.Coord[1] - CueStand.Mouse_Coord[1], CueBall.Coord[0] - CueStand.Mouse_Coord[0]))

        # 큐 조준선
        Distance_x = (CueBall.Coord[0] - CueStand.Cue_Coord[0]) *2
        Distance_y = (CueBall.Coord[1] - CueStand.Cue_Coord[1]) *2
        pygame.draw.line(screen, [255, 255, 0], CueBall.Coord, [CueBall.Coord[0]+Distance_x, CueBall.Coord[1]+Distance_y], 3)

    elif(CueStand.click_condition == 2 and Turning == False):
        CueBall.IsGoal = False
        CueBall.Collision_ON = True
        cue_rect = rotated_image_Cue.get_rect(center=CueBall.Coord)
        CueStand.Cue_count += 1
        if(CueStand.Cue_count == 5):
            CueStand.click_condition = 0

        
        Previous_Turn = Condition_Turn

        # 큐 이미지를 그리기 전에 회전시킨 이미지를 사용
        screen.blit(rotated_image_Cue, cue_rect)

    else:
        # MOVE!!
        Turning = True

        CueBall.move()
        for i in ColorBallList:
            i.move()

        # GOAL!!
        CueBall.Goal()
        if(CueBall.IsGoal == True):
            CueBall = WhiteBall(CueStand.Mouse_Coord[0],CueStand.Mouse_Coord[1], image_WhiteBall, 0)
            CueBall.IsGoal = True
            CueBall.Collision_ON = False


        for i in ColorBallList:
            i.Goal()
            if(i.IsGoal == True):
                ColorBallList.remove(i)
                if(i.Ball_ID == 1):
                    Player1.Remaining_points -= 1
                    Player1.Goal_Balls.append(i)
                    if( Current_Turn == 1):
                        Previous_Turn = 2
                elif(i.Ball_ID == 2):
                    Player2.Remaining_points -= 1
                    Player2.Goal_Balls.append(i)
                    if( Current_Turn == 2):
                        Previous_Turn = 1
                elif(i.Ball_ID == 3):
                    if( Current_Turn == 1 and Player1.Remaining_points == 0):
                        GameClear_Condition = 1
                        running = False

                    elif( Current_Turn == 2 and Player2.Remaining_points == 0):
                        GameClear_Condition = 2
                        running = False

                    elif( Current_Turn == 1 and Player1.Remaining_points != 0):
                        GameClear_Condition = 3
                        running = False

                    elif( Current_Turn == 2 and Player2.Remaining_points != 0):
                        GameClear_Condition = 4
                        running = False

        
        # x축벽 충돌
        if(CueBall.Coord[0] < 327):
            CueBall.Coord[0] = 327
            CueBall.CollisionToWall_X()

        elif(CueBall.Coord[0] > 1124):
            CueBall.Coord[0] = 1124
            CueBall.CollisionToWall_X()

        # y축벽 충돌
        if(CueBall.Coord[1] < 223):
            CueBall.Coord[1] = 223
            CueBall.CollisionToWall_Y()
        elif(CueBall.Coord[1] > 576):
            CueBall.Coord[1] = 576
            CueBall.CollisionToWall_Y()

# 벽 충돌
        for i in ColorBallList:
            if(i.Coord[0] < 327):
                i.Coord[0] = 327
                i.CollisionToWall_X()
            elif(i.Coord[0] > 1124):
                i.Coord[0] = 1124
                i.CollisionToWall_X()

            if(i.Coord[1] < 223):
                i.Coord[1] = 223
                i.CollisionToWall_Y()
            elif(i.Coord[1] >= 576):
                i.Coord[1] = 576
                i.CollisionToWall_Y()

# 충돌 검사
        for i in ColorBallList:
            CueBall.CollisionToBall(i)

        for i in range(len(ColorBallList)-1):
            for j in range(i+1,len(ColorBallList)):
                ColorBallList[i].CollisionToBall(ColorBallList[j])

# 게임 턴 결정
        BallsMoving = False
        
        if CueBall.IsStop == False:
            BallsMoving = True

        for i in ColorBallList:
            if i.IsStop == False:
                BallsMoving = True

        if BallsMoving == True:
            Condition_Turn = 0

        elif CueBall.IsGoal == False and Previous_Turn == 1:
            Condition_Turn = 2
            Turning = False

        elif CueBall.IsGoal == False and Previous_Turn == 2:
            Condition_Turn = 1
            Turning = False

        elif Condition_Turn == 0 and CueBall.IsGoal == True  and Current_Turn == 1:
            Condition_Turn = 2
            Turning = False

        elif Condition_Turn == 0 and CueBall.IsGoal == True  and Current_Turn == 2:
            Condition_Turn = 1
            Turning = False
        else:
            Turning = False


# 이미지 업데이트
    pygame.draw.circle(screen, CueBall.Color, CueBall.Coord, CueBall.Radius)

    for i in ColorBallList:
        rect = image_Ball1.get_rect(center=i.Coord)
        screen.blit(i.image, rect)   
    
    pygame.display.update()



# 결과 화면을 초기화
if(GameClear_Condition == 1):
    screen.fill((0,0,0))
    game_over_text = Font_bold.render("Player1 Win!!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()

elif(GameClear_Condition == 2):
    screen.fill((0,0,0))
    game_over_text = Font_bold.render("Player2 Win!!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()

elif(GameClear_Condition == 3):
    screen.fill((0, 0, 0))  
    game_over_text = Font_bold.render("Player1 Goal eightBall!. Player2 Win!!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()

elif(GameClear_Condition == 4):
    screen.fill((0, 0, 0))
    game_over_text = Font_bold.render("Player2 Goal eightBall!. Player1 Win!!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()



# 사용자가 마우스 클릭할 때까지 대기
waiting_for_click = True
while waiting_for_click:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_for_click = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            waiting_for_click = False


# 파이게임 종료
pygame.quit()
sys.exit()
