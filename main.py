import pygame, sys, random

WIDTH, HEIGHT = 800, 500

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
grey = (175, 175, 175)

paddle_width, paddle_height = 10, 80
paddle_speed = 10
right_paddle = pygame.Rect(int(WIDTH * 0.98 - paddle_width // 2), HEIGHT // 2 - paddle_height // 2, paddle_width,
                           paddle_height)
left_paddle = pygame.Rect(int(WIDTH * 0.02 - paddle_width // 2), HEIGHT // 2 - paddle_height // 2, paddle_width,
                          paddle_height)
ball_size = 20
ball_speed = 10
ball_x_direction = random.choice((1, -1))
ball_x_velocity, ball_y_velocity = 0, 0
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)


def reset_pos():
    global ball_x_direction, ball_x_velocity, ball_y_velocity
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_x_direction  *= -1
    ball_y_direction = random.choice((1, -1))
    angle = random.randrange(2, 9) * .1
    ball_x_speed = int(ball_speed * angle)
    ball_y_speed = ball_speed - ball_x_speed
    ball_x_velocity = ball_x_speed * ball_x_direction
    ball_y_velocity = ball_y_speed * ball_y_direction


def redraw():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, grey, right_paddle)
    pygame.draw.rect(screen, grey, left_paddle)
    pygame.draw.ellipse(screen, grey, ball)
    pygame.draw.line(screen, grey, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    pygame.display.update()


def inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += paddle_speed
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed


def logic():

    global ball_x_velocity, ball_y_velocity
    ball.x += ball_x_velocity
    ball.y += ball_y_velocity
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_y_velocity *= -1
    if ball.left <= 0 or ball.right >= WIDTH:
        reset_pos()

    if right_paddle.colliderect(ball):
        if abs(right_paddle.left - ball.right) <= 10 and ball_x_velocity > 0:
            ball.right = right_paddle.left
            ball_x_velocity *= -1
        if abs(right_paddle.top - ball.bottom) <= 10:
            ball.bottom = right_paddle.top
            ball_y_velocity = abs(ball_y_velocity) * -1
        if abs(right_paddle.bottom - ball.top) <= 10:
            ball.top = right_paddle.bottom
            ball_y_velocity = abs(ball_y_velocity)

    if left_paddle.colliderect(ball):
        if abs(left_paddle.right - ball.left) <= 10 and ball_x_velocity < 0:
            ball.left = left_paddle.right
            ball_x_velocity *= -1
        if abs(left_paddle.top - ball.bottom) <= 10:
            ball.bottom = left_paddle.top
            ball_y_velocity = abs(ball_y_velocity) * -1
        if abs(left_paddle.bottom - ball.top) <= 10:
            ball.top = left_paddle.bottom
            ball_y_velocity = abs(ball_y_velocity)


def main():
    reset_pos()
    while True:
        clock.tick(60)

        redraw()
        inputs()
        logic()


if __name__ == '__main__':
    main()
