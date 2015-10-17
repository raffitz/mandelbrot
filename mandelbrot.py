import pygame
import pygame.gfxdraw

def mandelbrot(x,y):
	count = 0
	itx = 0.0
	ity = 0.0
	while itx*itx + ity*ity < 4 and count < 1023:
		newx = itx*itx - ity*ity + x
		ity = 2*itx*ity + y
		itx = newx
		count += 1
	return count

pygame.init()

gameDisp = pygame.display.set_mode((896,512))

pygame.display.set_caption('Mandelbrot')

clock = pygame.time.Clock()

mincoords = (-2.5,-1)
maxcoords = (1,1)

def getcoords(i,j):
	a = (i / 896.0)*3-2.5
	b = ((512-j)/512)*2-1
	return (a,b)

running = True

surface = pygame.display.get_surface()

i = 0
while running:
	clock.tick(30)
	for ebuddy in pygame.event.get():
		if hasattr(ebuddy, 'key'):
			if ebuddy.key ==pygame.K_ESCAPE:
				running = False
		elif ebuddy.type == pygame.QUIT:
			running = False
	

	for j in range(512):
		(x,y) = getcoords(i,j)
		count = mandelbrot(x,y)
		colour = round(count/4)
		if colour < 0:
			colour = 0
		if colour > 255:
			colour = 255
		colour = 255 - colour
		fcol = (colour,colour,colour)
		pygame.gfxdraw.pixel(surface,i,j,fcol)
	i+=1
	if i>=896:
		i = 0
	pygame.display.update()
pygame.quit()
quit()
