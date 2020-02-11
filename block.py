import pygame

pygame.init()
font = pygame.font.Font('font.TTF', 10)
"""实现方块类"""
class Block():

    def __init__(self, type, num, position):
        self.type = type
        self.state = 'hidden'
        self.others = []
        self.num = num
        self.bomb_num = 0
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 25, 25)

    def add_others(self, block_list, map_size):  # map_size 地图长宽元组  block_list 地图方块列表
        if self.num == 1:
            self.others.append(block_list[1])
            self.others.append(block_list[map_size[1]])
            self.others.append(block_list[map_size[1] + 1])
        elif self.num == map_size[1]:
            self.others.append(block_list[map_size[1] - 2])
            self.others.append(block_list[2 * map_size[1] - 1])
            self.others.append(block_list[2 * map_size[1] - 2])
        elif self.num == (map_size[0] - 1) * map_size[1] + 1:
            self.others.append(block_list[(map_size[0] - 1) * map_size[1]+1])
            self.others.append(block_list[(map_size[0] - 2) * map_size[1] + 1])
            self.others.append(block_list[(map_size[0] - 2) * map_size[1]])
        elif self.num == map_size[0] * map_size[1]:
            self.others.append(block_list[map_size[0] * map_size[1]-2])
            self.others.append(block_list[(map_size[0] - 1) * map_size[1] - 1])
            self.others.append(block_list[(map_size[0] - 1) * map_size[1] - 2])
        elif 1 < self.num < map_size[1]:
            self.others.append(block_list[self.num])
            self.others.append(block_list[self.num-2])
            self.others.append(block_list[self.num + map_size[1] - 1])
            self.others.append(block_list[self.num + map_size[1] - 2])
            self.others.append(block_list[self.num + map_size[1]])
        elif map_size[1] * (map_size[0] - 1) + 1 < self.num < map_size[1] * map_size[0]:
            self.others.append(block_list[self.num])
            self.others.append(block_list[self.num-2])
            self.others.append(block_list[self.num - map_size[1] - 1])
            self.others.append(block_list[self.num - map_size[1] - 2])
            self.others.append(block_list[self.num - map_size[1]])
        elif (map_size[1] < self.num < (map_size[0]-1) * map_size[1]-1) and (self.num not in [map_size[1] + 1 + a*map_size[1] for a in range(map_size[0] - 2)] and self.num not in [map_size[1] + a*map_size[1] for a in range(map_size[0] - 2)]):
            self.others.append(block_list[self.num])
            self.others.append(block_list[self.num - 2])
            self.others.append(block_list[self.num - map_size[1]])
            self.others.append(block_list[self.num - map_size[1] - 1])
            self.others.append(block_list[self.num - map_size[1] - 2])
            self.others.append(block_list[self.num + map_size[1]])
            self.others.append(block_list[self.num + map_size[1] - 1])
            self.others.append(block_list[self.num + map_size[1] - 2])

        elif self.num in [map_size[1] + 1 + a*map_size[1] for a in range(map_size[0] - 2)] or self.num in [map_size[1] + (a+1)*map_size[1] for a in range(map_size[0] - 2)]:

            if self.num in [map_size[1] + 1 + a*map_size[1] for a in range(map_size[0] - 2)]:

                self.others.append(block_list[self.num])
                self.others.append(block_list[self.num + map_size[1] - 1])
                self.others.append(block_list[self.num + map_size[1]])
                self.others.append(block_list[self.num - map_size[1] - 1])
                self.others.append(block_list[self.num - map_size[1]])
            elif self.num in [map_size[1] + (a+1)*map_size[1] for a in range(map_size[0] - 2)]:
                self.others.append(block_list[self.num - 2])
                self.others.append(block_list[self.num + map_size[1] - 1])
                self.others.append(block_list[self.num + map_size[1] - 2])
                self.others.append(block_list[self.num - map_size[1] - 1])
                self.others.append(block_list[self.num - map_size[1] - 2])
        self.others = list(set(self.others))

    def count_bombs(self):
        for block in self.others:
            if block.type == 'bomb':
                self.bomb_num += 1

    def draw(self, screen):
        if self.state == 'hidden':
            pygame.draw.rect(screen, (30, 160, 190), self.rect)
        elif self.state == 'shown':
            for other in self.others:
                if other.type == 'ground':
                    num = 0
                    for a in other.others:
                        if a.type is not 'ground':
                            num += 1
                        if num >= 3:
                            break

                    if num < 3:
                        other.state = 'shown'

            if self.type is not 'bomb' and self.bomb_num != 0:
                pygame.draw.rect(screen, (200, 180, 150), self.rect)
                text = font.render(str(self.bomb_num), True, (10, 1, 0))
                text_rect = text.get_rect()
                text_rect.center = (self.position[0]+12.5, self.position[1]+12.5)
                screen.blit(text, text_rect)
            elif self.type is not 'bomb' and self.bomb_num == 0:
                pygame.draw.rect(screen, (200, 180, 150), self.rect)
            else:
                pygame.draw.rect(screen, (250, 0, 0), self.rect)
        elif self.state == 'select':
            pygame.draw.rect(screen, (200, 120, 250), self.rect)
