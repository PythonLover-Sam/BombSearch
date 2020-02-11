import sys
from block import *
from random import choice

if __name__ == "__main__":
    pygame.init()
    global game_state, block_list, map_size, selects, total_bomb, types
    pygame.display.set_caption('Bomb Searching')
    game_state = 'play'
    map_size = (14, 9)  # 可改变的变量
    screen = pygame.display.set_mode((40 + 26 * map_size[1], 40 + 26 * map_size[0]), 0, 32)
    left_top = (20, 20)
    types = ['bomb', 'ground', 'ground', 'ground', 'ground', 'ground', 'ground', 'ground']
    block_list = []

    def game_init():
        global game_state, block_list, map_size, selects, total_bomb, types
        game_state = 'play'
        block_list = []

        x = left_top[0]
        y = left_top[1]
        for i in range(map_size[0] * map_size[1]):

            if i % (map_size[1]) == 0 or i == 0:
                x = left_top[0]
                if i != 0:
                    y += 26

            else:
                x += 26
            block_list.append(Block(choice(types), i + 1, (x, y)))

        selects = []
        total_bomb = 0
        for block in block_list:
            block.add_others(block_list, map_size)
            block.count_bombs()
            if block.type == 'bomb':
                total_bomb += 1
            print(total_bomb)

    x = left_top[0]
    y = left_top[1]
    for i in range(map_size[0] * map_size[1]):

        if i % (map_size[1]) == 0 or i == 0:
            x = left_top[0]
            if i != 0:
                y += 26

        else:
            x += 26
        block_list.append(Block(choice(types), i+1, (x, y)))

    selects = []
    total_bomb = 0
    for block in block_list:
        block.add_others(block_list, map_size)
        block.count_bombs()
        if block.type == 'bomb':
            total_bomb += 1

    while True:
        for select in selects:
            if select.state is 'shown':
                selects.remove(select)
        if game_state == 'GameOver':
            game_init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for block in block_list:
                        if block.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            block.state = 'shown'
                            print(len(selects), ' / ', total_bomb)
                            if block in selects and block.type is not 'bomb':
                                selects.remove(block)

                            if block.type == 'bomb':
                                game_state = 'GameOver'
                                print(game_state)

                if event.button == pygame.BUTTON_RIGHT:
                    for block in block_list:
                        if block.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and block.state is not 'shown':
                            block.state = 'select'
                            selects.append(block)
                            selects = list(set(selects))

        if len(selects) == total_bomb:

            check = 0
            for select in selects:
                if select.type == 'bomb':
                    check += 1
            if check == total_bomb:
                game_state = 'win'
                print(game_state)

        for block in block_list:
            block.draw(screen)

        pygame.display.update()