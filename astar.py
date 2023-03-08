import random
import pygame
from queue import PriorityQueue
import level
from box import Spot,GREY,WHITE

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("\tA* Path Finding Algorithm")


# image Scailing here
SCALEVALUE = (40,40)

directoryOfImage=".//images//"

def loadImageScale(loc,scalevalue=SCALEVALUE):
	return pygame.transform.scale(pygame.image.load(directoryOfImage+loc),scalevalue)

#icon set
pygame.display.set_icon(loadImageScale("nav.png",(40,40)))

#Image Load
cafe = loadImageScale("cafeTransparent.png")
lib = loadImageScale("library.jpg")
school = loadImageScale("school.png")
postoffice = loadImageScale("postOffice.jpg")
road = loadImageScale("straightRoadTransparent.png")
mall =loadImageScale("shoppingMall.jpg")
house =loadImageScale("house.jpg")

# Heuristic value
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# Path reconstruction
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

# A* algo
def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	col = GREY
	for i in range(rows):
		pygame.draw.line(win, col, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))



def changingGrid():
	global Map,grassob
	Map = level.getlevel()
	obj = random.choice(["stone.jpg","desert.jpg","grass.jpg","snow.jpg"])
	grassob = loadImageScale(obj,(50,50))

changingGrid()

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			if Map[row.index(spot)][grid.index(row)] =="x":
				spot.make_barrier()
				spot.draw_img(grassob)
			elif Map[row.index(spot)][grid.index(row)] =="c":
				spot.draw_img(cafe)
			elif Map[row.index(spot)][grid.index(row)] =="l":
				spot.draw_img(lib)
			elif Map[row.index(spot)][grid.index(row)] =="s":
				spot.draw_img(school)
			elif Map[row.index(spot)][grid.index(row)] =="m":
				spot.draw_img(postoffice)
			elif Map[row.index(spot)][grid.index(row)] =="sm":
				spot.draw_img(mall)
			elif Map[row.index(spot)][grid.index(row)] =="h":
				spot.draw_img(house)
			else:
				spot.draw_img(road)
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 10
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				#elif spot != end and spot != start:
				#	spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

				if event.key == pygame.K_r:
					start = None
					end = None
					changingGrid()
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)