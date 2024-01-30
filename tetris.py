from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)
        pass

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02), 
                            text='TETRIS', fgcolor='white',
                            size=TILE_SIZE * 1.65)
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.22), 
                            text='next', fgcolor='orange',
                            size=TILE_SIZE * 1.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.67), 
                            text='score', fgcolor='orange',
                            size=TILE_SIZE * 1.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.8), 
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.44),
                            text='held', fgcolor='white',
                            size=TILE_SIZE*0.7)
        pass

class Tetris:
    def __init__(self, app):
        pg.mixer.music.load(MUSIC_PATH + '/bg.wav')
        pg.mixer.music.play(-1)
        self.is_muted = False
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        pg.time.wait(DELAY_BETWEEN_TETROMINOS)
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.hold_tetromino = Tetromino(self, on_hold=True, current=False)
        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = POINTS_PER_LINES

        self.left_user_event = pg.USEREVENT + 2
        self.right_user_event = pg.USEREVENT + 3

        self.left_right_hold_interval = LEFT_RIGHT_HOLD_INTERVAL

        self.projection_tetromino = Tetromino(self, current=False, on_hold=False, is_projection=True)

        self.can_hard_skip = True

        self.is_left_held_down = False
        self.is_right_held_down = False
        self.is_holdkey_held_down = False
        pass

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        if self.score >= 5000:
            self.app.canHold = True
            increase_by = math.floor(self.score / SPEED_UP_EVERY) + 1
            self.app.level = increase_by
            if increase_by > 0:
                pg.time.set_timer(self.app.user_event, 0)
                self.app.dynamic_anim_time_interval = LEVEL_SPEED[self.app.level]
                self.left_right_hold_interval = math.floor(LEVEL_SPEED[self.app.level] / LR_HI_FACTOR)
                self.app.set_timer()
            # self.app.dynamic_anim_time_interval = self.app.dynamic_anim_time_interval / SPEED_FACTOR
            # print(self.app.dynamic_anim_time_interval)
        self.full_lines = 0

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                break_Sound = pg.mixer.Sound(MUSIC_PATH + '/explode.wav')
                break_Sound.play()
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

                self.full_lines += 1

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]
    
    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(GAME_END_TIME_INTERVAL)
            return True

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.app.reset()
                self.__init__(self.app)
                pass
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                pg.time.wait(INTERVAL_BETWEEN_TETROMINOS)
                self.tetromino, self.next_tetromino = self.next_tetromino, Tetromino(self, current=False)
                self.tetromino.current = True
                # self.tetromino.on_hold = False
                self.tetromino.redraw(small=False)
                # self.next_tetromino = Tetromino(self, current=False)

                pass
            pass
        pass

    def get_final_position(self):
        final_positions = [block.pos for block in self.tetromino.blocks]
        all_positions = []
        for i in range(0, 30):
            # print(i)
            rel_to = [block.pos for block in self.tetromino.blocks] if i == 0 else all_positions[i-1]
            new_block_positions = self.tetromino.get_next_block_pos(move_direction=MOVE_DIRECTIONS['down'], relative_to=rel_to)
            # print(new_block_positions)
            all_positions.append(new_block_positions)
            if self.tetromino.is_collide(new_block_positions):
                final_positions = all_positions[i - 1]
                # print(i - 1)
                break
            pass
        return final_positions
    
    def hard_skip(self):
        # pass
        if self.can_hard_skip:
            final_positions = self.get_final_position()
            if final_positions in [[block.pos for block in self.tetromino.blocks], [block.pos + MOVE_DIRECTIONS['down'] for block in self.tetromino.blocks]]:
                return
            else:
                for i, block in enumerate(self.tetromino.blocks):
                    block.pos = final_positions[i]
                    pass
                pass
        

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.app.hold = True
            self.is_left_held_down = True
            self.control_up(pg.K_RIGHT, holdstate=True)
            self.tetromino.move(direction='left')
            pg.time.set_timer(self.left_user_event, self.left_right_hold_interval)
        elif pressed_key == pg.K_RIGHT:
            self.app.hold = True
            self.is_right_held_down = True
            self.control_up(pg.K_LEFT, holdstate=True)
            self.tetromino.move(direction='right')
            pg.time.set_timer(self.right_user_event, self.left_right_hold_interval)
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True
        elif pressed_key == pg.K_c:
            self.swap_held()
        elif pressed_key == pg.K_SPACE:
            self.hard_skip()
        elif pressed_key == pg.K_z:
            self.is_holdkey_held_down = True
            if self.app.canHold:
                self.app.hold = True
                pass
            pass
        elif pressed_key == pg.K_m:
            if self.is_muted:
                # Unmute
                pg.mixer.music.unpause()
                self.is_muted = False
                pass
            else:
                pg.mixer.music.pause()
                self.is_muted = True
                pass
        pass

    def swap_held(self):

        if not self.tetromino.has_swapped:
            self.tetromino, self.hold_tetromino = self.hold_tetromino, self.tetromino
            
            self.tetromino.has_swapped = True

            self.tetromino.on_hold = False
            self.tetromino.current = True
            self.hold_tetromino.on_hold = True
            self.hold_tetromino.current = False
            self.tetromino.blocks[0].pos = INIT_POS_OFFSET
            for i, block in enumerate(self.tetromino.blocks):
                block.pos = TETROMINOS[self.tetromino.shape][i] + self.tetromino.blocks[0].pos
            self.tetromino.redraw()
            self.hold_tetromino.redraw(small=True)
            pass

    def control_up(self, pressed_key, holdstate=False):
        if pressed_key == pg.K_LEFT:
            pg.time.set_timer(self.left_user_event, 0)
            if not holdstate:
                self.is_left_held_down = False

        elif pressed_key == pg.K_RIGHT:
            pg.time.set_timer(self.right_user_event, 0)
            if not holdstate:
                self.is_right_held_down = False
        elif pressed_key == pg.K_z:
            self.is_holdkey_held_down = False
            self.app.hold = False
        elif pressed_key == pg.K_DOWN:
            self.speed_up = False
        if not self.is_left_held_down and not self.is_right_held_down and not self.is_holdkey_held_down:
            self.app.hold = holdstate
    

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                # pg.draw.rect(self.app.screen, (85, 85, 85),
                #              (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                pg.draw.circle(self.app.screen, GRID_DOT_COLOR,
                             (x * TILE_SIZE, y * TILE_SIZE), GRID_DOT_SIZE)
    
    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.projection_tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()
        pass

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)
        pass