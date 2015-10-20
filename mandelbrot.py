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

imajor = 0
jmajor = 0

ibound = 56
jbound = 32
irange = round(896/ibound)
jrange = round(512/jbound)

# If you change ibound or jbound, the banlist ought to be cleared!

banlist = [(44, 3), (43, 4), (44, 4), (42, 6), (43, 6), (44, 6), (45, 6), (46, 6), (39, 7), (40, 7), (41, 7), (42, 7), (43, 7), (44, 7), (45, 7), (46, 7), (47, 7), (48, 7), (37, 8), (38, 8), (39, 8), (40, 8), (41, 8), (42, 8), (43, 8), (44, 8), (45, 8), (46, 8), (47, 8), (48, 8), (49, 8), (50, 8), (36, 9), (37, 9), (38, 9), (39, 9), (40, 9), (41, 9), (42, 9), (43, 9), (44, 9), (45, 9), (46, 9), (47, 9), (48, 9), (49, 9), (50, 9), (51, 9), (35, 10), (36, 10), (37, 10), (38, 10), (39, 10), (40, 10), (41, 10), (42, 10), (43, 10), (44, 10), (45, 10), (46, 10), (47, 10), (48, 10), (49, 10), (50, 10), (51, 10), (52, 10), (35, 11), (36, 11), (37, 11), (38, 11), (39, 11), (40, 11), (41, 11), (42, 11), (43, 11), (44, 11), (45, 11), (46, 11), (47, 11), (48, 11), (49, 11), (50, 11), (51, 11), (52, 11), (34, 12), (35, 12), (36, 12), (37, 12), (38, 12), (39, 12), (40, 12), (41, 12), (42, 12), (43, 12), (44, 12), (45, 12), (46, 12), (47, 12), (48, 12), (49, 12), (50, 12), (51, 12), (52, 12), (25, 13), (26, 13), (27, 13), (28, 13), (29, 13), (30, 13), (34, 13), (35, 13), (36, 13), (37, 13), (38, 13), (39, 13), (40, 13), (41, 13), (42, 13), (43, 13), (44, 13), (45, 13), (46, 13), (47, 13), (48, 13), (49, 13), (50, 13), (51, 13), (52, 13), (24, 14), (25, 14), (26, 14), (27, 14), (28, 14), (29, 14), (30, 14), (31, 14), (33, 14), (34, 14), (35, 14), (36, 14), (37, 14), (38, 14), (39, 14), (40, 14), (41, 14), (42, 14), (43, 14), (44, 14), (45, 14), (46, 14), (47, 14), (48, 14), (49, 14), (50, 14), (51, 14), (24, 15), (25, 15), (26, 15), (27, 15), (28, 15), (29, 15), (30, 15), (31, 15), (33, 15), (34, 15), (35, 15), (36, 15), (37, 15), (38, 15), (39, 15), (40, 15), (41, 15), (42, 15), (43, 15), (44, 15), (45, 15), (46, 15), (47, 15), (48, 15), (49, 15), (50, 15), (24, 16), (25, 16), (26, 16), (27, 16), (28, 16), (29, 16), (30, 16), (31, 16), (33, 16), (34, 16), (35, 16), (36, 16), (37, 16), (38, 16), (39, 16), (40, 16), (41, 16), (42, 16), (43, 16), (44, 16), (45, 16), (46, 16), (47, 16), (48, 16), (49, 16), (50, 16), (24, 17), (25, 17), (26, 17), (27, 17), (28, 17), (29, 17), (30, 17), (31, 17), (33, 17), (34, 17), (35, 17), (36, 17), (37, 17), (38, 17), (39, 17), (40, 17), (41, 17), (42, 17), (43, 17), (44, 17), (45, 17), (46, 17), (47, 17), (48, 17), (49, 17), (50, 17), (51, 17), (25, 18), (26, 18), (27, 18), (28, 18), (29, 18), (30, 18), (34, 18), (35, 18), (36, 18), (37, 18), (38, 18), (39, 18), (40, 18), (41, 18), (42, 18), (43, 18), (44, 18), (45, 18), (46, 18), (47, 18), (48, 18), (49, 18), (50, 18), (51, 18), (52, 18), (34, 19), (35, 19), (36, 19), (37, 19), (38, 19), (39, 19), (40, 19), (41, 19), (42, 19), (43, 19), (44, 19), (45, 19), (46, 19), (47, 19), (48, 19), (49, 19), (50, 19), (51, 19), (52, 19), (35, 20), (36, 20), (37, 20), (38, 20), (39, 20), (40, 20), (41, 20), (42, 20), (43, 20), (44, 20), (45, 20), (46, 20), (47, 20), (48, 20), (49, 20), (50, 20), (51, 20), (52, 20), (35, 21), (36, 21), (37, 21), (38, 21), (39, 21), (40, 21), (41, 21), (42, 21), (43, 21), (44, 21), (45, 21), (46, 21), (47, 21), (48, 21), (49, 21), (50, 21), (51, 21), (52, 21), (36, 22), (37, 22), (38, 22), (39, 22), (40, 22), (41, 22), (42, 22), (43, 22), (44, 22), (45, 22), (46, 22), (47, 22), (48, 22), (49, 22), (50, 22), (51, 22), (37, 23), (38, 23), (39, 23), (40, 23), (41, 23), (42, 23), (43, 23), (44, 23), (45, 23), (46, 23), (47, 23), (48, 23), (49, 23), (50, 23), (39, 24), (40, 24), (41, 24), (42, 24), (43, 24), (44, 24), (45, 24), (46, 24), (47, 24), (48, 24), (49, 24), (41, 25), (42, 25), (43, 25), (44, 25), (45, 25), (46, 25), (43, 27), (44, 27), (44, 28)]

while running:
	clock.tick(30)
	for ebuddy in pygame.event.get():
		if hasattr(ebuddy, 'key'):
			if ebuddy.key ==pygame.K_ESCAPE:
				running = False
		elif ebuddy.type == pygame.QUIT:
			running = False
	
	if (imajor,jmajor) not in banlist:
		ban = True
		for iminor in range(irange):
			for jminor in range(jrange):
				i = irange*imajor + iminor
				j = jrange*jmajor + jminor
				(x,y) = getcoords(i,j)
				count = mandelbrot(x,y)
				if count < 1023:
					ban = False
				colour = round(count/4)
				if colour < 0:
					colour = 0
				if colour > 255:
					colour = 255
				colour = 255 - colour
				fcol = (colour,colour,colour)
				pygame.gfxdraw.pixel(surface,i,j,fcol)
		if ban:
			banlist.append((imajor,jmajor))
	imajor+=1
	if imajor>=ibound:
		imajor = 0
		jmajor+=1
		if jmajor>=jbound:
			jmajor = 0
	pygame.display.update()
pygame.quit()
print('%s'% banlist)
quit()
