from settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos): # position in playfield of 10 x 20 (not relative to tetromino block)
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.hold_pos = vec(pos) + HOLD_POS_OFFSET
        self.final_pos = vec(pos)
        self.alive = True
        self.image = tetromino.image

        self.rect = self.image.get_rect()


        super().__init__(tetromino.tetris.sprite_group)

        self.is_small = False
        if (not self.tetromino.current or self.tetromino.on_hold) and not self.tetromino.is_projection:
            self.smaller_img()
            pass
        # self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        # self.image.fill('orange')
        # pg.draw.rect(self.image, 'orange', (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), border_radius=8)

        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_counter = 0
        self.hold = False
        pass

    def smaller_img(self):
        self.image = pg.transform.scale(self.image, (SMALL_TILE_SIZE, SMALL_TILE_SIZE))
        self.is_small = True
        self.set_rect_pos()
        pass

    def normal_img(self):
        self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.is_small = False
        self.set_rect_pos()
        pass


    def sfx_end_time(self):
        if self.tetromino.tetris.app.anim_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True

    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)

    def is_alive(self):
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()

    def rotate(self, pivot_pos, angle=90):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(angle)
        return rotated + pivot_pos

    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        if self.tetromino.on_hold:
            pos = self.hold_pos
        if self.tetromino.is_projection:
            pos = self.final_pos
            # print("call")
        
        if self.is_small:
            self.rect.topleft = pos * (SMALL_TILE_SIZE)
            pass
        else:
            self.rect.topleft = pos * TILE_SIZE
            pass
        pass

    def update(self):
        self.is_alive()
        self.set_rect_pos()
        pass

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (
            y < 0 or not self.tetromino.tetris.field_array[y][x]
        ):
            return False
        return True


class Tetromino:
    def __init__(self, tetris, current=True, on_hold=False, is_projection=False):
        self.tetris = tetris
        
        self.landing = False
        self.current = current
        self.on_hold = on_hold
        self.shape = random.choice(list(TETROMINOS.keys())) if not is_projection else self.tetris.tetromino.shape
        self.image = tetris.app.images[SPRITE_DIR_PATH + "/" + self.shape + '.png']
        self.is_projection = is_projection
        positions = TETROMINOS[self.shape]
        if self.is_projection:
            self.image = tetris.app.images[SPRITE_DIR_PATH + "/p.png"]
            positions = self.tetris.get_final_position()

        self.blocks = [Block(self, pos) for pos in positions]

        self.has_swapped = False
        pass


    def rotate(self, index=0):
        pivot_pos = self.blocks[index].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if self.is_collide(new_block_positions):
            new_block_positions = [block.rotate(pivot_pos, 180) for block in self.blocks]
        if self.is_collide(new_block_positions):
            new_block_positions = [block.rotate(pivot_pos, 270) for block in self.blocks]


        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
                pass
            pass
        elif index < 4:
            self.rotate(index+1)


        

    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))
    
    def get_next_block_pos(self, move_direction, relative_to=False):
        # move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        if relative_to:
            new_block_positions = [relative_to_block + move_direction for relative_to_block in relative_to]
        
        return new_block_positions

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = self.get_next_block_pos(move_direction)
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
                pass
            pass
        elif direction == 'down':
            self.landing = True

    def update(self):
        if not self.tetris.app.hold and not self.is_projection:
            self.move(direction='down') 
            pass
        elif self.is_projection:
            final_positions = self.tetris.get_final_position()
            for i, block in enumerate(self.blocks):
                block.final_pos = final_positions[i]
        pass

    def redraw(self, small=False):
        for block in self.blocks:
            if small:
                block.smaller_img()
                pass
            else:
                block.normal_img()
                pass