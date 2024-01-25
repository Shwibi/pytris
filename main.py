from settings import *
import sys
from tetris import Tetris, Text
import pathlib

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.canHold = False
        self.hold = False
        self.dynamic_anim_time_interval = ANIM_TIME_INTERVAL
        self.dynamic_fast_anim_time_interval = FAST_ANIM_TIME_INTERVAL
        self.level = 1

        self.set_timer()
        pass

    def reset(self):
        self.dynamic_anim_time_interval = ANIM_TIME_INTERVAL
        self.dynamic_fast_anim_time_interval = FAST_ANIM_TIME_INTERVAL
        self.canHold = False
        self.hold = False
        self.level = 1
        pass

    def load_images(self):
        image_dict = {}
        for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png'):
            if item.is_file():
                image = pg.image.load(item).convert_alpha()
                image = pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                image_dict[item.as_posix()] = image
        # files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        # images = [pg.image.load(file).convert_alpha() for file in files]
        # images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        # print(image_dict)
        return image_dict

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, self.dynamic_anim_time_interval)
        pg.time.set_timer(self.fast_user_event, self.dynamic_fast_anim_time_interval)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)
        pass

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()
        pass

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
                pass
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
                pass
            elif event.type == pg.KEYUP:
                self.tetris.control_up(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
                pass
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True
                pass
            elif event.type == self.tetris.left_user_event:
                self.tetris.tetromino.move(direction='left')
                pass
            elif event.type == self.tetris.right_user_event:
                self.tetris.tetromino.move(direction='right')
                pass
            pass
        pass

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            pass
        pass

if __name__ == '__main__':
    app = App()
    app.run()