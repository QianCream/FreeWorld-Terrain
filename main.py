import random
import math
import pygame

class TerrainGenerator:
    def __init__(self) :
        self.__map_height = 512
        self.__map_width = 20
        self.map = [[0 for i in range(self.__map_width)] for i in range(self.__map_height)]

        self.__terrain_height = int(self.__map_height / 2 + 20)
        self.seed = 0
        self.terrain_type = self.__getRandom(2)
        self.terrain_type_list = []

        self.sea_level = int(self.__map_height / 2 - 15)
        self.sand_level = int(self.__map_height / 2 - 12)

    # 获取随机值的私有方法
    def __getRandom(self ,max_value):
        return int(math.ceil((math.ceil(random.random() * 10)) / (10 / max_value)))

    def __generateLand(self, new_map, change_height, change_frequency, generate_soil, new_terrain_height):
        for i in range(self.__map_width):
            terrain_change = self.__getRandom(change_frequency)
            if terrain_change == 1:
                new_terrain_height += self.__getRandom(change_height)
            elif terrain_change == 2:
                new_terrain_height -= self.__getRandom(change_height)

            for j in range(new_terrain_height):
                new_map[self.__map_height - 1 - j][i] = 1

            if generate_soil:
                soil_height = self.__getRandom(3)
                for j in range(soil_height):
                    new_map[self.__map_height - new_terrain_height - j - 1][i] = 2

                new_map[self.__map_height - new_terrain_height - soil_height - 1][i] = 3

        return new_map, new_terrain_height

    def __generateHardStone(self,new_map):
        for i in range(self.__map_width):
            for j in range(5):
                if self.__getRandom(j + 1) == 1:
                    new_map[self.__map_height - j - 1][i] = 4

        return new_map

    # 地形生成的私有方法
    def __terrainGenerator(self, new_terrain_height, terrain_type):
        self.new_terrain_height = new_terrain_height
        new_map = [[0 for i in range(self.__map_width)] for i in range(self.__map_height)]

        if new_terrain_height < self.sea_level:
            terrain_type = 3

        if new_terrain_height < self.sand_level and new_terrain_height >= self.sea_level:
            terrain_type = 4

        elif self.__getRandom(6) == 1:
            terrain_type = self.__getRandom(2)

        # 平原
        if terrain_type == 1:
            new_map, new_terrain_height = self.__generateLand(new_map, 1, 10, True, new_terrain_height)

        # 山脉
        if terrain_type == 2:
            new_map, new_terrain_height = self.__generateLand(new_map, 3, 3, False, new_terrain_height)

        # 海
        if terrain_type == 3:
            change_height = 1
            change_frequency = 5

            for i in range(self.__map_width):
                terrain_change = self.__getRandom(change_frequency)
                if terrain_change == 1:
                    new_terrain_height += self.__getRandom(change_height)
                elif terrain_change == 2:
                    new_terrain_height -= self.__getRandom(change_height)

                for j in range(new_terrain_height):
                    new_map[self.__map_height - 1 - j][i] = 1

                for j in range(3):
                    new_map[self.__map_height - new_terrain_height - j - 1][i] = 5

                for j in range(self.__map_height - new_terrain_height - self.__map_height + self.sea_level - 3):
                    new_map[self.__map_height - new_terrain_height - j - 4][i] = 6

        # 海滩
        if terrain_type == 4:
            change_height = 1
            change_frequency = 6

            for i in range(self.__map_width):
                terrain_change = self.__getRandom(change_frequency)
                if terrain_change == 1:
                    new_terrain_height += self.__getRandom(change_height)
                elif terrain_change == 2:
                    new_terrain_height -= self.__getRandom(change_height)

                for j in range(new_terrain_height):
                    new_map[self.__map_height - 1 - j][i] = 1

                for j in range(3):
                    new_map[self.__map_height - new_terrain_height - j - 1][i] = 5

        new_map = self.__generateHardStone(new_map)

        return new_terrain_height, new_map, terrain_type

    # 第一次地形生成的方法
    def firstTerrainGenerator(self):
        self.__terrain_height, self.map, self.terrain_type = self.__terrainGenerator(self.__terrain_height, self.terrain_type)
        self.terrain_type_list.append(self.terrain_type)

    # 完整地形生成的方法
    def wholeTerrainGenerator(self, number):
        for i in range(number):
            self.__terrain_height, temp_map, self.terrain_type = self.__terrainGenerator(self.__terrain_height , self.terrain_type)
            self.terrain_type_list.append(self.terrain_type)

            for i in range(self.__map_height):
                self.map[i] = self.map[i] + temp_map[i]

    # 设置随机种子的方法
    def setSeed(self, seed):
        self.seed = seed
        random.seed(self.seed)

terrain_generator = TerrainGenerator()

def TerrainPygamePrinter(map, number, x):
    pygame.init()
    screen = pygame.display.set_mode((20 * number * x, 512 * x))
    pygame.display.set_caption("Terrain Generator")

    colour_map = {
        0 : (50,233,233), # 空气
        1 : (192,192,192), # 石头
        2 : (48,5,52), # 泥土
        3 : (0,255,0), # 草
        4 : (0,0,0), # 坚硬石
        5 : (240,240,128), # 沙子
        6 : (0,128,255) # 水
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        for i in range(len(map)):
            for j in range(len(map[i])):
                pygame.draw.rect(screen, colour_map[map[i][j]], (j * x, i * x, x, x))

        for i in range(len(terrain_generator.terrain_type_list)):
            if terrain_generator.terrain_type_list[i] == 1:
                pygame.draw.rect(screen,(0,255,0),((0 + i * 20,0),(20,20)))
            elif terrain_generator.terrain_type_list[i] == 2:
                pygame.draw.rect(screen, (192,192,192), ((0 + i * 20,0),(20,20)))
            elif terrain_generator.terrain_type_list[i] == 3:
                pygame.draw.rect(screen, (0,128,255), ((0 + i * 20,0),(20,20)))
            elif terrain_generator.terrain_type_list[i] == 4:
                pygame.draw.rect(screen, (240,240,128), ((0 + i * 20,0),(20,20)))

        for i in range(number - 1):
            pygame.draw.rect(screen, (255, 255, 255), ((0 + (i + 1) * 20, 0), (1, 512)))

        pygame.display.update()

if __name__ == '__main__':
    seed = int(input("请输入随机种子："))
    terrain_generator.setSeed(seed)
    terrain_generator.firstTerrainGenerator()
    terrain_generator.wholeTerrainGenerator(50)
    TerrainPygamePrinter(terrain_generator.map, 50, 1)
