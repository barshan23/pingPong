import pygame,random

pygame.init()

display_height = 600
display_width = 800

display = pygame.display.set_mode((display_width,display_height))

block = 10
clock = pygame.time.Clock()

def randomColor(bricks):
	color = []
	for i in bricks:
		color.append((random.randrange(30,255),random.randrange(30,255),random.randrange(30,255)))
	return color


def buildWall(level):
	bricks = []
	for i in range(level+3):
		for j in range(40):
			bricks.append(pygame.Rect((j*2*block,i*block),(2*block,block)))
	return bricks

def drawWall(bricks,color):
	for i,brick in enumerate(bricks):
		pygame.draw.rect(display, (0,0,0), [brick.left-2, brick.top-2,brick.width+4,brick.height+4])
		pygame.draw.rect(display, color[i],brick)


font = pygame.font.SysFont(None, 25)


def showMessage(msg,color):
	w,h = font.size(msg)
	textScreen = font.render(msg, True, color)
	display.blit(textScreen, [(display_width/2)-(w/2), (display_height/2)-(h/2)])

def gameLoop():
	gameOver = False
	gameExit = False
	score = 0
	while  not gameOver:
		if gameExit:
			display.fill((255,255,255))
			screen = showMessage("Score is "+str(score)+" Game Over! Press C to play again, Q to quit game",(255,0,0))
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = True
					break
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						gameExit = False
						break
					if event.key == pygame.K_q:
						gameOver = True
						continue
			continue

		bricks = buildWall(1);
		colors = randomColor(bricks)
		score = 0
		paddle_pos_x = display_width/2;
		paddle_speed = 0
		pong_pos_x = paddle_pos_x + ((block*10)/2) - block/2
		pong_pos_y = display_height - (2*block)
		pong_speed_x = 3
		pong_speed_y = 3

		while not gameExit:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						gameExit = True
						gameOver = True
						break
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_LEFT :
							paddle_speed = -3
						if event.key == pygame.K_RIGHT:
							paddle_speed = 3
					if event.type == pygame.KEYUP:
						paddle_speed = 0
				display.fill((255,255,255))
				drawWall(bricks,colors)
				paddle_pos_x += paddle_speed
				pong_pos_x -= pong_speed_x
				pong_pos_y -= pong_speed_y
				pong = pygame.draw.rect(display,(255,0,0),[pong_pos_x, pong_pos_y, block, block])
				paddle = pygame.draw.rect(display,(0,0,0),[paddle_pos_x, display_height-block, block*10, block])
				
				index = pong.collidelist(bricks)
				if index != -1:
					score += 1
					pong_speed_y = -pong_speed_y
					del bricks[index]
					del colors[index]

				if paddle_pos_x > (display_width-(block*10)) or paddle_pos_x < 0:
					paddle_speed = 0
					paddle_pos_x = 0 if (paddle_pos_x < 0) else (display_width-(block*10))
				if paddle.colliderect(pong):
					if pong_pos_x < (paddle_pos_x+(block*5)):
						pong_speed_x= (pong_speed_x) if pong_speed_x > 0 else -pong_speed_x
						pong_speed_y = -pong_speed_y
					elif pong_pos_x > (paddle_pos_x+(block*5)):
						pong_speed_x = -pong_speed_x if pong_speed_x > 0 else pong_speed_x
						pong_speed_y = -pong_speed_y

				else:
					if pong_pos_x > (display_width-block) or pong_pos_x < 0:
						pong_speed_x= -pong_speed_x
					if pong_pos_y < 0:
						pong_speed_y = -pong_speed_y
					if pong_pos_y > (display_height-block):
						gameExit = True
						break
				#print (pong_pos_x,pong_pos_y)
				pygame.display.update()
				clock.tick(100)

	pygame.quit()
	quit()
 
gameLoop()