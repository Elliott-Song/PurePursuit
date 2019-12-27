import sys, pygame, math, time, random
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 30)
size = width, height = 1200, 675
screen = pygame.display.set_mode(size)
k = pygame.Surface((size))  # per-pixel alpha
l = pygame.Surface((size), pygame.SRCALPHA)

blue = 100, 100, 200
white = 200, 200, 200
green = 100, 200, 100
grey = 80, 80, 80
red = 200, 100, 100


origin = (width/2, height/2)
rang = 200
points = []
complexity = 150
points.append([origin[0],origin[1]])
for i in range (1, complexity):
    ex = points[i-1][0] + random.randint(-20, 100)
    wy = points[i-1][1] + random.randint(-50,50)
    points.append([ex,wy])
trail = []
trail.append([origin[0], origin[1]])

def mag(A):   #finds magnitude of a vector
    dist= math.sqrt((A[0])**2+(A[1])**2)
    return dist

def dot(A,B):   #find dot product of two vectors
    prod = A[0]*B[0] + A[1]*B[1]
    return prod

def inrange(a,b,c):  #returns true if value c is inbetween a and b
    if(a<=c<=b or b<=c<=a) :
        return 1
    return 0

#intersection returns a list of tuple coordinates of the intersection points between a line segment and a plane
def intersection (l1, l2, c, r):   #l1 and l2 are points at the ends of the line segment. c is the circle's centre and r is the radius
    l1c=(c[0]-l1[0], c[1]-l1[1])   #l1c is vector from l1 to c
    l1l2 = (l2[0]-l1[0], l2[1]-l1[1])   #l1l2 is vector from l1 to l2
    scalar = dot(l1c,l1l2)/(mag(l1l2)**2)
    proj= (l1l2[0]*scalar, l1l2[1]*scalar)   #finds l1c projected onto l1l2
    perp = (l1c[0] - proj[0], l1c[1] - proj[1])   #finds perp which is the vector from c to the closest point on the line

    inter = []   #list of points we will return
    if (mag(perp)<r): #checks if an intersection occurs
        diff = math.sqrt(r**2 - mag(perp)**2)   #finds distance between closest point and intersection points
        unit = (diff * l1l2[0]/mag(l1l2), diff * l1l2[1]/mag(l1l2))   #finds unit vector in direction of l1l2, multiplies by diff

        px = l1[0]+proj[0]+unit[0]  #finds x coordinate of FIRST potential intersection (closer to l2)
        if (inrange(l1[0],l2[0],px)):
            inter.append((px, l1[1] + proj[1] + unit[1]))  #if potential intersection is on line segment, add to list

        px = l1[0] + proj[0] - unit[0]  #finds x coordinate of SECOND potential intersection (closer to l1)
        if (inrange(l1[0],l2[0],px)):
            inter.append((px, l1[1] + proj[1] - unit[1]))  #if potential intersection is on line segment, add to list

    return inter

#pursuit returns the best angle for a vehicle to follow an efficient path
def pursuit (points, c, r):   #points is the array of coordinates to follow, c is centre of circle, r is radius
    pnt = c
    for i in range (len(points)-1, 0, -1):   #iterates through line segments, starting at furthest
        ins = intersection(points[i-1],points[i], c, r)
        if (len(ins)>0):   #if an intersection exists, set variable pnt to the further POI and stop looping
            pnt = ins[0]
            break
    vec = (c[0]-pnt[0], c[1]-pnt[1]) #vec is the direction vector to be followed
    return math.atan2(vec[1], vec[0])


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    pygame.draw.line(k, grey, (width/2,0), (width/2,height), 2)
    pygame.draw.line(k, grey, (0, height/2), (width, height / 2), 2)
    pygame.draw.ellipse(k, green, ((origin[0]-rang/2,origin[1]-rang/2), (rang, rang)), 2)

    pygame.draw.ellipse(k, blue, (points[0], (10,10)), 5)
    pygame.draw.ellipse(k, red, (points[complexity-1], (10, 10)), 5)
    for i in range(0, complexity -1):
        pygame.draw.line(k, green, points[i], points[i+1], 2)
        ins = intersection(points[i], points[i+1], origin, rang / 2)
        for j in range(0, len(ins)):
            pygame.draw.line(k, grey, origin, ins[j], 2)

    angle = pursuit(points, origin, rang/2)
    print(math.cos(angle),math.sin(angle))
    pygame.draw.line(k, red, origin, (origin[0]-50*math.cos(angle),origin[1]-50*math.sin(angle)) , 2)
    for i in range (0, complexity):
        points[i][0] += 10*math.cos(angle)
        points[i][1] += 10 * math.sin(angle)

    trail.append([origin[0], origin[1]])
    for i in range(len(trail)):
        trail[i][0] += 10 *math.cos(angle)
        trail[i][1] += 10 * math.sin(angle)
        pygame.draw.ellipse(k, red, (trail[i], (2, 2)), 1)

    screen.blit(k, (0,0))
    k.fill((0, 0, 0))


    time.sleep(0.05)
    pygame.display.update()
