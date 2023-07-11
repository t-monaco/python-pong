from pong import Game
import pygame


class PongGame:
    FPS = 60

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.game = Game(window, window_width, window_height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle

    def run_game(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(self.FPS)
            game_info = self.game.loop()

            # Quit the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.game.draw()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and self.left_paddle.y - self.left_paddle.VEL >= 0:
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.VEL <= self.window_height:
                self.game.move_paddle(left=True, up=False)


if __name__ == '__main__':
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pong = PongGame(win, width, height)
    pong.run_game()
