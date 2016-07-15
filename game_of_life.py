
from sdl2 import *
import ctypes
import random 


PIXEL_WIDTH = 4
PIXEL_HEIGHT = 4

SPACE_WIDTH = 100
SPACE_HEIGHT = 100


population = {(i,j): 0 for i in range(SPACE_WIDTH) for j in range(SPACE_HEIGHT)}
next_pop = dict(population)


neighbors = [(-1,-1), (-1,0), (-1,1), (0,-1),(0,1), (1,-1), (1,0), (1,1)];
alive_neighbors = lambda (x,y), pop: sum(1 for (x2, y2) in neighbors if pop[(x+x2, y+y2)])


def next_generation(coords, pop):
	if coords[0] == 0 or coords[0] == SPACE_WIDTH-1 or coords[1] == SPACE_HEIGHT-1 or coords[1] == 0: return
	if pop[coords] and not (2 <= alive_neighbors(coords, pop) <= 3):
		return 0

	elif alive_neighbors(coords, pop) == 3:
		return 1

	else: 
		return pop[coords]
	
def sdl_events(): 
	event = SDL_Event()
	while SDL_PollEvent(ctypes.byref(event)):
		if event.type == SDL_QUIT:
			return 1
		if event.type == SDL_KEYDOWN:
			if event.key.keysym.sym ==  SDLK_ESCAPE:
				return 1

	return 0


def seed(pop):
	for coord in pop:
		if random.random() < 0.07: ## 7% probability of alive (~70 in 1000)
			pop[coord] = 1

SDL_Init(SDL_INIT_VIDEO)
window = SDL_CreateWindow("Game of Life", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, SPACE_WIDTH * PIXEL_WIDTH, SPACE_HEIGHT * PIXEL_HEIGHT, 0)
surf = SDL_GetWindowSurface(window)

black = SDL_MapRGB(surf.contents.format, 0, 0, 0)
white = SDL_MapRGB(surf.contents.format, 255, 255, 255)

seed(population)

while True:

	for coord in population:
		next_pop[coord] = next_generation(coord, population)
		if next_pop[coord] != population[coord]:
			rect = SDL_Rect(x=coord[0] * PIXEL_WIDTH, y=coord[1]*PIXEL_HEIGHT, w=PIXEL_WIDTH, h=PIXEL_HEIGHT)
			SDL_FillRect(surf,rect, white if population[coord] else black)

	population = next_pop
	next_pop = dict()
	SDL_UpdateWindowSurface(window)

	if sdl_events(): break
	SDL_Delay(100)



SDL_DestroyWindow(window)
SDL_Quit()


