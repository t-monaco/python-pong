from .paddle import Paddle
from .ball import Ball
import pygame
import random
pygame.init()


class GameInformation:
    def __init__(self, left_score, right_score):
        self.left_score = left_score
        self.right_score = right_score


class Game:
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, window: pygame.Surface, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height

        self.left_paddle = Paddle(
            10, self.window_height // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(
            self.window_width - 10 - Paddle.WIDTH, self.window_height // 2 - Paddle.HEIGHT // 2)
        self.ball = Ball(window_height // 2, window_height // 2)

        self.left_score = 0
        self.right_score = 0
        self.window = window

    def _draw_scores(self):
        left_score = self.SCORE_FONT.render(
            f'{self.left_score}', 1, self.WHITE)
        right_score = self.SCORE_FONT.render(
            f'{self.right_score}', 1, self.WHITE)
        self.window.blit(
            left_score, ((1/4) * self.window_width - left_score.get_width() // 2, 20))
        self.window.blit(
            right_score, ((3/4) * self.window_width - right_score.get_width() // 2, 20))

    def _draw_divider(self):
        """Draw the middle line that divides the field."""
        for i in range(10, self.window_height, self.window_height//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.window, self.WHITE,
                             (self.window_width//2 - 5), i, 10, self.window_height//20)

    def _handle_collision(self):
        """
            Handle situation when the ball hits the celling, the floor, or any of the walls
        """

        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        # Change ball's direction when hitting with the celling or the floor
        if ball.y + ball.RADIUS <= 0 or ball.y - ball.RADIUS >= self.window_height:
            ball.y_vel *= -1

        # Handle ball hitting the left wall
        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.HEIGHT and ball.x - Ball.RADIUS <= left_paddle.x + Paddle.WIDTH:
                self._handle_bounce_in_paddle(left_paddle)

        # Handle ball hitting the right wall
        else:
            if ball.y <= right_paddle.y and ball.y >= right_paddle.y + Paddle.HEIGHT and ball.x + Ball.RADIUS >= right_paddle.x:
                self._handle_bounce_in_paddle(right_paddle)

    def _handle_bounce_in_paddle(self, paddle: Paddle):
        middle_y = paddle.y + Paddle.HEIGHT / 2
        difference_in_y = middle_y - self.ball.y
        reduction_factor = (Paddle.HEIGHT / 2) / self.ball.MAX_VEL
        y_vel = difference_in_y / reduction_factor
        self.ball.y_vel = -1 * y_vel

    def draw(self):
        self.window.fill(self.BLACK)
        self._draw_divider()
        self._draw_scores()

        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.window)

        self.ball.draw(self.window)

    def move_paddle(self, left=True, up=True):
        """
        Move the left or right paddle.

        :returns: boolean indicating if paddle movement is valid. 
                  Movement is invalid if it causes paddle to go 
                  off the screen
        """
        if left:
            if up and self.left_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.right_paddle.move(up)

        return True

    def loop(self):
        """
        Executes a single game loop.

        :returns: GameInformation instance stating score 
                  and hits of each paddle.
        """
        self.ball.move()
        self._handle_collision()

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.left_score += 1

        game_info = GameInformation(self.left_score, self.right_score)

        return game_info

    def reset(self):
        """Reset the entire game."""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
