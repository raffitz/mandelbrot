import math
import pygame
import pygame.gfxdraw


# The basis of it all, the Mandelbrot iterations:
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

# Initializing pygame and opening a window:
fullscreen = False

pygame.init()

pxwidth = 896
pxheight = 512

gameDisp = pygame.display.set_mode((pxwidth,pxheight),pygame.RESIZABLE)

pygame.display.set_caption('Mandelbrot')

# Setting up the timer for after the calculations:
clock = pygame.time.Clock()

# Aspect ratio and window coordinates stuff:
stdratio = 7/4

stdminx = -2.5
stdminy = -1
stdwidth = 3.5
stdheight = 2

minx = stdminx
miny = stdminy
width = stdwidth
height = stdheight

# Cursor position and status:
cursor1x = 0
cursor1y = 0
cursorenabled = False
cursor2x = 0
cursor2y = 0

# Converting from pixel coordinates to the complex plane coordinates:
def getcoords(i,j):
	a = (i / pxwidth)*width+minx
	b = ((pxheight-j)/pxheight)*height+miny
	return (a,b)

# Cycle condition:
running = True

# Surface stuff: (I think the intermediate surface might be superfluous right now)
disps = pygame.display.get_surface()
surface = pygame.Surface((pxwidth,pxheight),0)
intermediate = pygame.Surface((pxwidth,pxheight),0)

# Block set up:
imajor = 0
jmajor = 0

blocksize = 64

ibound = math.ceil(pxwidth/blocksize)
jbound = math.ceil(pxheight/blocksize)

# Locking the surface for ease of access when writing pixel data:
surface.lock()


# Main loop:
while running:
	# Event handling:
	for ebuddy in pygame.event.get():
		if ebuddy.type == pygame.KEYDOWN:
			reset = False
			if ebuddy.key ==pygame.K_ESCAPE:
				# If you escape, you escape
				running = False
			elif ebuddy.key == pygame.K_BACKSPACE:
				# Resetting the view
				minx = stdminx
				miny = stdminy
				width = stdwidth
				height = stdheight
				reset = True
			elif ebuddy.key == pygame.K_SPACE:
				# Fixing aspect ratio
				ratio = width/height
				if ratio<stdratio:
					width = height*stdratio
					reset = True
				elif ratio>stdratio:
					height = stdratio*width
					reset = True
			elif ebuddy.key == pygame.K_MINUS:
				# Zooming out
				minx = minx - width/2
				miny = miny - height/2
				width = width*2
				height = height*2
				reset = True
			elif ebuddy.key == pygame.K_PLUS:
				# Zooming in
				minx = minx + width/4
				miny = miny + height/4
				width = width/2
				height = height/2
				reset = True
			elif ebuddy.key == pygame.K_F11:
				# Toggling fullscreen
				reset = True
				if fullscreen:
					fullscreen = False

					gameDisp = pygame.display.set_mode((896,512),pygame.RESIZABLE)
				else:
					fullscreen = True
					modes = pygame.display.list_modes()
					gameDisp = pygame.display.set_mode(modes[0],pygame.FULLSCREEN)
				disps = pygame.display.get_surface()
				pxwidth,pxheight = disps.get_size()
				
				surface = pygame.Surface((pxwidth,pxheight),0)
				intermediate = pygame.Surface((pxwidth,pxheight),0)
				
				stdratio = pxwidth / pxheight
				ratio = 3.5/2
				if ratio<stdratio:
					stdheight = 2
					stdwidth = 2*stdratio
					stdminy = -1
					stdminx = (-2.5/3.5)*stdwidth
				elif ratio>stdratio:
					stdwidth = 3.5
					stdheight = stdratio*3.5
					stdminx = -2.5
					stdminy = (-0.5)*stdheight
			if reset:
				# Stop current render and restart based on new coordinates
				reset = False
				blocksize = 64
				ibound = math.ceil(pxwidth/blocksize)
				jbound = math.ceil(pxheight/blocksize)
				imajor = 0
				jmajor = 0
		elif ebuddy.type == pygame.QUIT:
			# If you wanna exit the window, we'll let'ya
			running = False
		elif ebuddy.type == pygame.MOUSEBUTTONUP:
			if ebuddy.button == 1:
				# Left mouse click sets up the cursor
				cursorenabled = True
				(cursor1x,cursor1y) = ebuddy.pos
			if ebuddy.button == 3 and cursorenabled:
				# If cursor is set up, right mouse click zooms on area delimited by the cursor and the mouse
				cursorenabled = False
				(cursor2x,cursor2y) = ebuddy.pos
				(rx1,ry1) = getcoords(cursor1x,cursor1y)
				(rx2,ry2) = getcoords(cursor2x,cursor2y)
				minx = min(rx1,rx2)
				miny = min(ry1,ry2)
				width = abs(rx1-rx2)
				height = abs(ry1-ry2)
				blocksize = 64
				ibound = math.ceil(pxwidth/blocksize)
				jbound = math.ceil(pxheight/blocksize)
				imajor = 0
				jmajor = 0
		elif ebuddy.type == pygame.VIDEORESIZE:
			# The window is resizeable. If it is, in fact resized, it needs to be handled
			pxwidth = ebuddy.w	# New width
			pxheight = ebuddy.h	# New height
			
			# Deleting current surfaces and reinstating them with their new sizes:
			surface.unlock()
			del surface
			del intermediate
			
			surface = pygame.Surface((pxwidth,pxheight),0)
			intermediate = pygame.Surface((pxwidth,pxheight),0)
			gameDisp = pygame.display.set_mode((pxwidth,pxheight),pygame.RESIZABLE)
			disps = pygame.display.get_surface()
			surface.lock()
			
			# Debug message:
			#print('resize: %s %s'%(pxwidth,pxheight))
			
			# Restarting render:
			blocksize = 64
			ibound = math.ceil(pxwidth/blocksize)
			jbound = math.ceil(pxheight/blocksize)
			imajor = 0
			jmajor = 0
			
			# Redefining default coordinates:
			stdratio = pxwidth / pxheight
			ratio = 3.5/2
			if ratio<stdratio:
				stdheight = 2
				stdwidth = 2*stdratio
				stdminy = -1
				stdminx = (-2.5/3.5)*stdwidth
			elif ratio>stdratio:
				stdwidth = 3.5
				stdheight = stdratio*3.5
				stdminx = -2.5
				stdminy = (-0.5)*stdheight
			
	if blocksize >= 1:
		# While the render isn't complete, we have to work on it.
		
		# This skips the portion of the block that was completed with the previous blocksize
		if blocksize != 64 and imajor%2==0 and jmajor%2 ==0:
			skip = True
		else:
			skip = False
		
		if not skip:
			# Calculating the actual coordinates:
			i = blocksize*imajor
			j = blocksize*jmajor
			(x,y) = getcoords(i,j)
			
			# Running the Mandelbrot iterations and attributing it a colour:
			count = mandelbrot(x,y)
			colour = round(count/4)
			if colour < 0:
				colour = 0
			if colour > 255:
				colour = 255
			colour = 255 - colour
			fcol = (colour,colour,colour)
			
			# For all picels in this block, paint them that same colour:
			for a in range(blocksize):
				# If the window size isn't divisible by the block size, we have got to make sure we don't paint pixels outside the window
				if i+a > pxwidth:
					break
				for b in range(blocksize):
					if j+b > pxheight:
						break
					surface.set_at((i+a,j+b),fcol)
					#pygame.gfxdraw.pixel(surface,i+a,j+b,fcol)
		
		# Incrementing the position:
		imajor+=1
		if imajor>=ibound:
			imajor = 0
			jmajor+=1
			if jmajor>=jbound:
				jmajor = 0
				# If we reached the end of the columns, we have got to start working on the next blocksize (or stop working altogether)
				
				# Debug print
				# print('%s done.'%(blocksize))
				
				# Decrease blocksize:
				blocksize = blocksize>>1
				if blocksize == 0:
					# Yay, the render is complete!
					surface.unlock()
					intermediate.blit(surface,(0,0),None,0)
					disps.blit(intermediate,(0,0),None,0)
					pygame.display.update()
					continue
				
				# The render is still not complete:
				ibound = math.ceil(pxwidth/blocksize)
				jbound = math.ceil(pxheight/blocksize)
				
				# We can show what's already done, though:
				surface.unlock()
				intermediate.blit(surface,(0,0),None,0)
				surface.lock()
				disps.blit(intermediate,(0,0),None,0)
				
				#If the cursor is enabled, we show it
				if cursorenabled:
					disps.set_at((cursor1x,cursor1y),(255,0,0))
				pygame.display.update()
	else:
		# Framerate limiting (we're showing a static render, it's not as if we need to keep refreshing the picture)
		clock.tick(30)
		
		# Showing the completed render:
		disps.blit(intermediate,(0,0),None,0)
		
		# Adding the cursor on top of that:
		if cursorenabled:
			disps.set_at((cursor1x,cursor1y),(255,0,0))
			
		# Updating the window:
		pygame.display.update()

# We got out of that vicious cycle, gotta get going:
pygame.quit()
quit()
