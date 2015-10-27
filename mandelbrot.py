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

minx = -2.5
miny = -1
width = 3.5
height = 2

def getcoords(i,j):
	a = (i / 896.0)*width+minx
	b = ((512-j)/512)*height+miny
	return (a,b)

running = True

disps = pygame.display.get_surface()
surface = pygame.Surface((896,512),0)
intermediate = pygame.Surface((896,512),0)

imajor = 0
jmajor = 0

blocksize = 64;

ibound = round(896/blocksize)
jbound = round(512/blocksize)

surface.lock()

while running:
	
	for ebuddy in pygame.event.get():
		if ebuddy.type == pygame.key:
			if ebuddy.key ==pygame.K_ESCAPE:
				running = False
		elif ebuddy.type == pygame.QUIT:
			running = False
	if blocksize >= 1:
		if blocksize != 64 and imajor%2==0 and jmajor%2 ==0:
			skip = True
		else:
			skip = False
		
		if not skip:
			i = blocksize*imajor
			j = blocksize*jmajor
			(x,y) = getcoords(i,j)
			count = mandelbrot(x,y)
			colour = round(count/4)
			if colour < 0:
				colour = 0
			if colour > 255:
				colour = 255
			colour = 255 - colour
			fcol = (colour,colour,colour)
			for a in range(blocksize):
				for b in range(blocksize):
					surface.set_at((i+a,j+b),fcol)
					#pygame.gfxdraw.pixel(surface,i+a,j+b,fcol)
		imajor+=1
		if imajor>=ibound:
			imajor = 0
			jmajor+=1
			if jmajor>=jbound:
				jmajor = 0
				print('%s done.'%(blocksize))
				blocksize = blocksize>>1
				if blocksize == 0:
					surface.unlock()
					intermediate.blit(surface,(0,0),None,0)
					disps.blit(intermediate,(0,0),None,0)
					pygame.display.update()
					continue
				ibound = round(896/blocksize)
				jbound = round(512/blocksize)
				surface.unlock()
				intermediate.blit(surface,(0,0),None,0)
				disps.blit(intermediate,(0,0),None,0)
				pygame.display.update()
				surface.lock()
	else:
		clock.tick(30)
		pygame.display.update()
pygame.quit()
quit()
