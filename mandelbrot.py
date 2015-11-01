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

cursor1x = 0
cursor1y = 0
cursorenabled = False
cursor2x = 0
cursor2y = 0

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

blocksize = 64

ibound = round(896/blocksize)
jbound = round(512/blocksize)

surface.lock()

reset = False

while running:
	
	for ebuddy in pygame.event.get():
		if ebuddy.type == pygame.KEYDOWN:
			if ebuddy.key ==pygame.K_ESCAPE:
				running = False
			elif ebuddy.key == pygame.K_BACKSPACE:
				minx = -2.5
				miny = -1.0
				width = 3.5
				height = 2.0
				reset = True
			elif ebuddy.key == pygame.K_SPACE:
				ratio = width/height
				if ratio<7/4:
					width = height*(7/4)
					reset = True
				elif ratio>7/4:
					height = (4/7)*width
					reset = True
			elif ebuddy.key == pygame.K_MINUS:
				minx = minx - width/2
				miny = miny - height/2
				width = width*2
				height = height*2
				reset = True
			elif ebuddy.key == pygame.K_MINUS:
				minx = minx - width/2
				miny = miny - height/2
				width = width*2
				height = height*2
				reset = True
			elif ebuddy.key == pygame.K_PLUS:
				minx = minx + width/4
				miny = miny + height/4
				width = width/2
				height = height/2
				reset = True
			if reset:
				reset = False
				blocksize = 64
				ibound = round(896/blocksize)
				jbound = round(512/blocksize)
				imajor = 0
				jmajor = 0
		elif ebuddy.type == pygame.QUIT:
			running = False
		elif ebuddy.type == pygame.MOUSEBUTTONUP:
			if ebuddy.button == 1:
				cursorenabled = True
				(cursor1x,cursor1y) = ebuddy.pos
			if ebuddy.button == 3 and cursorenabled:
				cursorenabled = False
				(cursor2x,cursor2y) = ebuddy.pos
				(rx1,ry1) = getcoords(cursor1x,cursor1y)
				(rx2,ry2) = getcoords(cursor2x,cursor2y)
				minx = min(rx1,rx2)
				miny = min(ry1,ry2)
				width = abs(rx1-rx2)
				height = abs(ry1-ry2)
				blocksize = 64
				ibound = round(896/blocksize)
				jbound = round(512/blocksize)
				imajor = 0
				jmajor = 0
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
				if cursorenabled:
					disps.set_at((cursor1x,cursor1y),(255,0,0))
				pygame.display.update()
				surface.lock()
	else:
		clock.tick(30)
		disps.blit(intermediate,(0,0),None,0)
		if cursorenabled:
			disps.set_at((cursor1x,cursor1y),(255,0,0))
		pygame.display.update()
pygame.quit()
quit()
