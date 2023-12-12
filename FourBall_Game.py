import pygame
import sys
import math
import Physics
import random
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
pygame.display.set_caption("FourBallGame")

# 인터페이스 설정
font = pygame.font.Font(None, 36)

# 그림 설정
image_path = resource_path("./image/Board2.png")
image = pygame.image.load(image_path)
image = pygame.transform.scale(image, (900, 450))  # 원하는 크기로 조정

image_Cue_Path = resource_path("./image/Cue.png")
image_Cue = pygame.image.load(image_Cue_Path)
image_Cue = pygame.transform.scale(image_Cue,(300,10))

image_BallRed_Path = resource_path("./image/BallRed.png")
image_BallOrange_Path = resource_path("./image/BallOrange.png")
image_BallWhite_Path = resource_path("./image/BallWhite.png")


image_BallOrnage = pygame.image.load(image_BallOrange_Path)
image_BallOrange = pygame.transform.scale(image_BallOrnage,(26,26))

image_BallWhite = pygame.image.load(image_BallWhite_Path)
image_BallWhite = pygame.transform.scale(image_BallWhite,(26,26))

image_BallRed = pygame.image.load(image_BallRed_Path)
image_BallRed = pygame.transform.scale(image_BallRed,(26,26))



Font_bold = pygame.font.Font(None, 50)
Font = pygame.font.Font(None, 36)


GameTurn = 1
Turning = False

def TurnChange():
    global GameTurn
    if GameTurn == 1:
        GameTurn = 2
    else:
        GameTurn = 1
    

class Player:
    def __init__(self, PlayerID):    
        self.PlayerID = PlayerID
        self.MaxRemaining_points = 70
        self.Remaining_points = 70
    
    def MinusPoint(self):
        self.Remaining_points -=10
        if self.Remaining_points < 0:
            self.Remaining_points = 0
    
    def PlusPoint(self):
        self.Remaining_points +=10
        if self.Remaining_points > self.MaxRemaining_points:
            self.Remaining_points = self.MaxRemaining_points



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
    Radius = 13
    Angular_rotation = 0
    friction = 0.998
    IsStop = True
    IsHit = False
    CountCollisionToWall = 0
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
    
    def IsCollision(self, r, Coord):
        if(Physics.CollisionDetect(self.Coord, self.Radius, Coord, r)):
            return True
    
    def CollisionToBall(self, OtherBall):
        if(self.IsCollision(OtherBall.Radius, OtherBall.Coord) == True and self.Collision_ON == True):
            AfterElastic_v = Physics.ElasticCollision_2D(30, self.Coord, self.Velocity, 30, OtherBall.Coord, OtherBall.Velocity)

            self.Velocity[0] = AfterElastic_v[0]
            self.Velocity[1] = AfterElastic_v[1]
            
            OtherBall.Velocity[0] = AfterElastic_v[2]
            OtherBall.Velocity[1] = AfterElastic_v[3]

            #오버랩 버그 발생 경우 코드!! 예외처리
            if(Physics.CircleIOU(self.Radius, [self.Coord[0] + self.Velocity[0], self.Coord[1] + self.Velocity[1]], OtherBall.Radius,[OtherBall.Coord[0]+OtherBall.Velocity[0], OtherBall.Coord[1]+ OtherBall.Velocity[1]]) > 0):
                self.Coord[0] += self.Velocity[0]*2
                self.Coord[1] += self.Velocity[1]*2
                OtherBall.Coord[0] += OtherBall.Velocity[0]*2
                OtherBall.Coord[1] += OtherBall.Velocity[1]*2
                
            
    def CollisionToWall_X(self):
        self.Velocity[0] = -self.Velocity[0]
        self.CountCollisionToWall +=1

    def CollisionToWall_Y(self):
        self.Velocity[1] = -self.Velocity[1]
        self.CountCollisionToWall +=1

    def CollisionToWall(self):
        # X축벽 충돌
        if(self.Coord[0] < 327):
            self.Coord[0] = 327
            self.CollisionToWall_X()
            

        elif(self.Coord[0] > 1124):
            self.Coord[0] = 1124
            self.CollisionToWall_X()
        
        # y축벽 충돌
        if(self.Coord[1] < 223):
            self.Coord[1] = 223
            self.CollisionToWall_Y()
            

        elif(self.Coord[1] > 576):
            self.Coord[1] = 576
            self.CollisionToWall_Y()
    


class RedBall(Ball):
    def __init__(self, x, y, image, PlayerNum):
        super().__init__(x, y, image, PlayerNum)
        self.Color = (255,255,255)

class OrangeBall(Ball):
    def __init__(self, x, y, image, PlayerNum):
        super().__init__(x,y, image, PlayerNum)
        self.Color = (255,0,0)

class WhiteBall(Ball):
    def __init__(self, x, y, image, PlayerNum):
        super().__init__(x,y, image, PlayerNum)
        self.Color = (255,0,0)


PlayerWhite = Player("Player White")
PlayerOrange = Player("Player Orange")


White_Ball = WhiteBall(450,400, image_BallWhite, 1)
Orange_Ball = OrangeBall(1000,400, image_BallOrange, 2)

RedBall_PawnRandX = random.randrange(350, 1100)
RedBall_PawnRandY = random.randrange(230, 570)
Red_Ball_1 = RedBall(RedBall_PawnRandX, RedBall_PawnRandY, image_BallRed, 3)

RedBall_PawnRandX = random.randrange(350, 1100)
RedBall_PawnRandY = random.randrange(230, 570)
Red_Ball_2 = RedBall(RedBall_PawnRandX, RedBall_PawnRandY, image_BallRed, 3)

BallList = [White_Ball, Orange_Ball, Red_Ball_1, Red_Ball_2]

CueStand = Cue(0,0)


# 게임 루프
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(image, (275, 175))

    #플레이어 턴 선택
    if(Turning != True):
        if(GameTurn == 1):
            WhitePlayer_ID = Font_bold.render(PlayerWhite.PlayerID, True, (255, 255, 0))
            OrangePlayer_ID = Font_bold.render(PlayerOrange.PlayerID, True, (255, 255, 255))    
        elif(GameTurn == 2):
            WhitePlayer_ID = Font_bold.render(PlayerWhite.PlayerID, True, (255, 255, 255))
            OrangePlayer_ID = Font_bold.render(PlayerOrange.PlayerID, True, (255, 255, 0))
    elif(Turning == True):
        WhitePlayer_ID = Font_bold.render(PlayerWhite.PlayerID, True, (255, 0, 0))
        OrangePlayer_ID = Font_bold.render(PlayerOrange.PlayerID, True, (255, 0, 0)) 

    screen.blit(WhitePlayer_ID, (1270, 200))
    screen.blit(OrangePlayer_ID, (1270, 450))


    WhitePlayer_Score = font.render("Remaining Points : " + str(PlayerWhite.Remaining_points), True, (255, 255, 255))
    OrangePlayer_Score = font.render("Remaining Points : " + str(PlayerOrange.Remaining_points), True, (255, 255, 255))
    screen.blit(WhitePlayer_Score, (1250, 250))
    screen.blit(OrangePlayer_Score, (1250, 500))


    CueStand.Mouse_Coord= pygame.mouse.get_pos()

    if(PlayerWhite.Remaining_points == 0 or PlayerOrange.Remaining_points == 0):
        running = False


    if(GameTurn == 1):
        i = White_Ball
    elif(GameTurn == 2):
        i = Orange_Ball



    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and Turning == False:
            CueStand.click_condition = 1
        elif event.type == pygame.MOUSEBUTTONUP and Turning == False:
            CueStand.click_condition = 2
            CueStand.Cue_count = 0
            
            Cue_Power = [(i.Coord[0] - CueStand.Cue_Coord[0])/50, (i.Coord[1] - CueStand.Cue_Coord[1])/50]
            if abs(Cue_Power[0]) > CueStand.CuePower_MAX:
                Cue_Power[0] = Cue_Power[0] / abs(Cue_Power[0]) * CueStand.CuePower_MAX
            if abs(Cue_Power[1]) > CueStand.CuePower_MAX:
                Cue_Power[1] = Cue_Power[0] / abs(Cue_Power[0]) * CueStand.CuePower_MAX

            i.Velocity = Cue_Power

        if event.type == pygame.QUIT:
            running = False

    if(CueStand.click_condition == 1):
        # 큐가 하얀 공 방향을 가리키도록 회전
        angle = math.degrees(math.atan2(i.Coord[1] - CueStand.Mouse_Coord[1], i.Coord[0] - CueStand.Mouse_Coord[0]))
        rotated_image_Cue = pygame.transform.rotate(image_Cue, -angle)
        cue_rect = rotated_image_Cue.get_rect(center=CueStand.Mouse_Coord)

        # 큐 이미지를 그리기 전에 회전시킨 이미지를 사용
        screen.blit(rotated_image_Cue, cue_rect)
        CueStand.Cue_Coord[0] = CueStand.Mouse_Coord[0] + 150*math.cos(math.atan2(i.Coord[1] - CueStand.Mouse_Coord[1], i.Coord[0] - CueStand.Mouse_Coord[0]))
        CueStand.Cue_Coord[1] = CueStand.Mouse_Coord[1] + 150*math.sin(math.atan2(i.Coord[1] - CueStand.Mouse_Coord[1], i.Coord[0] - CueStand.Mouse_Coord[0]))

        # 큐 조준선
        Distance_x = (i.Coord[0] - CueStand.Cue_Coord[0]) *2
        Distance_y = (i.Coord[1] - CueStand.Cue_Coord[1]) *2
        pygame.draw.line(screen, [255, 255, 0], i.Coord, [i.Coord[0]+Distance_x, i.Coord[1]+Distance_y], 3)

    elif(CueStand.click_condition == 2):
        cue_rect = rotated_image_Cue.get_rect(center=i.Coord)
        CueStand.Cue_count += 1
        

        if(CueStand.Cue_count == 5):
            CueStand.click_condition = 0
            
            
            

        # 큐 이미지를 그리기 전에 회전시킨 이미지를 사용
        screen.blit(rotated_image_Cue, cue_rect)

    else:
        # MOVE!!
        White_Ball.move()
        Orange_Ball.move()  
        Red_Ball_1.move()
        Red_Ball_2.move()
        if CueStand.Cue_count == 5:
            Turning = True



# 벽 충돌
    White_Ball.CollisionToWall()
    Orange_Ball.CollisionToWall()
    Red_Ball_1.CollisionToWall()
    Red_Ball_2.CollisionToWall()

# 충돌 검사

    for i in range(len(BallList)-1):
        for j in range(i+1, len(BallList)):
            if BallList[i].IsCollision(BallList[j].Radius, BallList[j].Coord) == True :
                BallList[i].CollisionToBall(BallList[j])
                
    
    if (GameTurn == 1):
        if (White_Ball.IsCollision(Red_Ball_1.Radius, Red_Ball_1.Coord) == True):
            Red_Ball_1.IsHit = True
        if (White_Ball.IsCollision(Red_Ball_2.Radius, Red_Ball_2.Coord) == True):
            Red_Ball_2.IsHit = True
        if (White_Ball.IsCollision(Orange_Ball.Radius, Orange_Ball.Coord) == True):
            Orange_Ball.IsHit = True
    elif (GameTurn == 2):
        if (Orange_Ball.IsCollision(Red_Ball_1.Radius, Red_Ball_1.Coord) == True):
            Red_Ball_1.IsHit = True
        if (Orange_Ball.IsCollision(Red_Ball_2.Radius, Red_Ball_2.Coord) == True):
            Red_Ball_2.IsHit = True
        if (Orange_Ball.IsCollision(White_Ball.Radius, White_Ball.Coord) == True):
            White_Ball.IsHit = True



# 턴 종료
    if(White_Ball.IsStop == True and Orange_Ball.IsStop == True and Red_Ball_1.IsStop == True and Red_Ball_2.IsStop == True and Turning):

        if(GameTurn == 1):
            if(Orange_Ball.IsHit == False and Red_Ball_1.IsHit == True  and Red_Ball_2.IsHit== True and White_Ball.CountCollisionToWall < 3):
                PlayerWhite.MinusPoint()
                Turning = False
            elif(Orange_Ball.IsHit == False and Red_Ball_1.IsHit == True  and Red_Ball_2.IsHit== True and White_Ball.CountCollisionToWall >= 3):
                PlayerWhite.MinusPoint()
                PlayerWhite.MinusPoint()
                PlayerWhite.MinusPoint()
                Turning = False
            elif(Orange_Ball.IsHit == True):
                PlayerWhite.PlusPoint()
                Turning = False
                TurnChange()
            else:
                TurnChange()
                Turning = False

        elif(GameTurn == 2):
            if(White_Ball.IsHit == False and Red_Ball_1.IsHit == True  and Red_Ball_2.IsHit== True and Orange_Ball.CountCollisionToWall < 3):
                PlayerOrange.MinusPoint()
                Turning = False
            elif(White_Ball.IsHit == False and Red_Ball_1.IsHit == True  and Red_Ball_2.IsHit== True and Orange_Ball.CountCollisionToWall >= 3):
                PlayerOrange.MinusPoint()
                PlayerOrange.MinusPoint()
                PlayerOrange.MinusPoint()
                Turning = False
            elif(White_Ball.IsHit == True):
                PlayerOrange.PlusPoint()
                Turning = False
                TurnChange()
            else:
                TurnChange()
                Turning = False

        White_Ball.IsHit = 0
        White_Ball.CountCollisionToWall = 0
        Orange_Ball.IsHit = 0
        Orange_Ball.CountCollisionToWall = 0
        Red_Ball_1.IsHit = 0
        Red_Ball_1.CountCollisionToWall = 0
        Red_Ball_2.IsHit = 0
        Red_Ball_2.CountCollisionToWall = 0
        CueStand.Cue_count = 0
        

# 이미지 업데이트
    rect = image_BallOrange.get_rect(center=Orange_Ball.Coord)
    screen.blit(Orange_Ball.image, rect)
    rect = image_BallWhite.get_rect(center=White_Ball.Coord)
    screen.blit(White_Ball.image, rect)
    rect = image_BallRed.get_rect(center=Red_Ball_1.Coord)
    screen.blit(Red_Ball_1.image, rect)
    rect = image_BallRed.get_rect(center=Red_Ball_2.Coord)
    screen.blit(Red_Ball_2.image, rect)
    pygame.display.update()

# 종료 화면 출력
if(GameTurn == 1):
    screen.fill((0,0,0))
    game_over_text = Font_bold.render("PlayerWhite Win!!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()

elif(GameTurn == 2):
    screen.fill((0,0,0))
    game_over_text = Font_bold.render("PlayerOrange Win!!", True, (255, 255, 255))
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
