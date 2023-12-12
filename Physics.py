import math


#두 원의 겹치는 영역 넓이 구하기
def CircleIOU(r1, Coord1, r2, Coord2):
    PI = math.acos(-1)
    res = 0.0
    d = math.sqrt((Coord1[0]-Coord2[0])*(Coord1[0]-Coord2[0]) + (Coord1[1]-Coord2[1])*(Coord1[1]-Coord2[1]))

    if(r1+r2<=d):
        res = 0
    elif(abs(r1-r2)>=d):
        res = PI*min(r1*r1,r2*r2) 
    else:
        theta1 = math.acos((d * d + r1 * r1 - r2 * r2) / (d * r1 * 2.0)) * 2.0
        theta2 = math.acos((d * d + r2 * r2 - r1 * r1) / (d * r2 * 2.0)) * 2.0

        res = (theta1 * r1 * r1 + theta2 * r2 * r2 - r1 * r1 * math.sin(theta1) - r2 * r2 * math.sin(theta2)) * 0.5
    
    return res


## 두 원의 CollisionDetect
def CollisionDetect(Coord1, r1, Coord2, r2):
    distance = math.sqrt((Coord1[0] - Coord2[0]) ** 2 + (Coord1[1] - Coord2[1]) ** 2)
    if distance < r1 + r2:
        return True
    else:
        return False


#두 공의 탄성충돌

# 1차원 탄성 충돌
# m=질량 u=충돌전속도 v=충돌후속도
# 질량이 다를때

def ElasticCollision_1D(M1, U1, M2, U2):
    V1 = (M1 - M2)/(M1+M2)*U1 + 2*M2/(M1+M2)*U2
    V2 = 2*M1/(M1+M2)*U1 + (M2-M1)/(M1+M2)*U2
    
    return [V1,V2]



# 2차원 탄성 충돌
def ElasticCollision_2D(M1, Coord1, Velocity1, M2, Coord2, Velocity2):
    Delta_x = Coord2[0] - Coord1[0]
    Delta_y = Coord2[1] - Coord1[1]
    Delta_vx = Velocity2[0] - Velocity1[0]
    Delta_vy = Velocity2[1] - Velocity1[1]
    
    Delta_magnitude = math.sqrt(Delta_x**2 + Delta_y**2)
    Normal_x = Delta_x / Delta_magnitude
    Normal_y = Delta_y / Delta_magnitude
    
    Vrel = Delta_vx * Normal_x + Delta_vy * Normal_y
    
    V1x = Velocity1[0] + ((2 * M2) / (M1 + M2)) * Vrel * Normal_x
    V1y = Velocity1[1] + ((2 * M2) / (M1 + M2)) * Vrel * Normal_y
    V2x = Velocity2[0] - ((2 * M1) / (M1 + M2)) * Vrel * Normal_x
    V2y = Velocity2[1] - ((2 * M1) / (M1 + M2)) * Vrel * Normal_y
    
    return [V1x, V1y, V2x, V2y]


