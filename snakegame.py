import pygame
import random
import time

# initializing pygame
pygame.init()

# Colors
white = (255, 255, 255)  # rgb format
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)

# Creating window
screen_width = 1200  # Increased screen width
screen_height = 800  # Increased screen height
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Coders Home")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])
    return screen_text.get_width()  # Return width of the rendered text for centering

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def generate_equation(difficulty):
    if difficulty == 'beginner':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        if random.choice([True, False]):
            equation = f"{num1} + {num2}"
            answer = num1 + num2
        else:
            equation = f"{num1} - {num2}"
            answer = num1 - num2
    elif difficulty == 'novice':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 9)
        if random.choice([True, False]):
            equation = f"{num1} * {num2}"
            answer = num1 * num2
        else:
            while True:
                num1 = random.randint(1, 90)
                num2 = random.randint(1, 10)
                if num1 % num2 == 0:
                    break
            equation = f"{num1} / {num2}"
            answer = num1 // num2
    else:  # professional
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        num3 = random.randint(1, 10)
        operations = ['+', '-', '*', '/']
        random.shuffle(operations)
        equation = f"{num1} {operations[0]} {num2} {operations[1]} {num3}"
        answer = eval(equation)
    return equation, answer

def generate_food(answer, difficulty, is_positive, equation):
    food_items = []
    remaining = answer
    if difficulty == 'beginner' and '-' in equation:
        # Generate positive and negative food items for subtraction
        for _ in range(4):
            value = random.randint(1, 10)
            food_x = random.randint(20, screen_width - 30)
            food_y = random.randint(60, screen_height - 30)
            food_items.append((food_x, food_y, value))
            remaining -= value
        for _ in range(4):
            value = random.randint(-10, -1)
            food_x = random.randint(20, screen_width - 30)
            food_y = random.randint(60, screen_height - 30)
            food_items.append((food_x, food_y, value))
            remaining -= value
    else:
        for _ in range(8):
            if type(answer) is int:
                value = random.randint(1, max(remaining, 1)) if is_positive else random.randint(-10, -1)
            else:
                value = round(random.uniform(0.1, max(remaining, 0.1)), 1) if is_positive else round(random.uniform(-10, -0.1), 1)
            remaining -= value
            food_x = random.randint(20, screen_width - 30)
            food_y = random.randint(60, screen_height - 30)
            food_items.append((food_x, food_y, value))
    # Ensure the last food item balances the equation
    food_x = random.randint(20, screen_width - 30)
    food_y = random.randint(60, screen_height - 30)
    food_items.append((food_x, food_y, remaining))
    return food_items

def start_screen():
    start_game = False
    difficulty = 'beginner'
    while not start_game:
        gameWindow.fill(white)
        text_screen("Select Level: B-Beginner    N-Novice    P-Professional", black, 50, 350)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    difficulty = 'beginner'
                    start_game = True
                elif event.key == pygame.K_n:
                    difficulty = 'novice'
                    start_game = True
                elif event.key == pygame.K_p:
                    difficulty = 'professional'
                    start_game = True

    return difficulty

# Game Loop
def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    difficulty = start_screen()
    equation, answer = generate_equation(difficulty)
    is_positive = '+' in equation or '*' in equation
    food_items = generate_food(answer, difficulty, is_positive, equation)
    score = 0
    correct_equations = 0
    init_velocity = 3
    snake_size = 30
    fps = 60  # fps = frames per second
    start_time = time.time()
    time_limit = 60  # Increased time limit to 60 seconds

    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Continue", red, 100, 350)
            text_screen(f"Equation: {equation}", red, 100, 400)
            text_screen(f"Correct Answer: {answer}", red, 100, 450)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Wrap the snake around the screen
            if snake_x < 0:
                snake_x = screen_width
            elif snake_x > screen_width:
                snake_x = 0
            if snake_y < 50:
                snake_y = screen_height
            elif snake_y > screen_height:
                snake_y = 50

            for food in food_items:
                food_x, food_y, food_value = food
                if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                    score += food_value
                    food_items.remove(food)
                    if len(food_items) == 0 or score == answer:
                        if score == answer:
                            equation, answer = generate_equation(difficulty)
                            is_positive = '+' in equation or '*' in equation
                            snk_length += 5  # Increase snake length only if the answer is correct
                            correct_equations += 1
                            start_time = time.time()  # Reset the timer when the equation changes
                        food_items = generate_food(answer, difficulty, is_positive, equation)
                        score = 0  # Reset score for the next equation

                    new_food_value = random.randint(1, 10) if is_positive else random.randint(-10, -1)
                    food_x = random.randint(20, screen_width - 30)
                    food_y = random.randint(60, screen_height - 30)
                    food_items.append((food_x, food_y, new_food_value))
                    break

            gameWindow.fill(white)
            mode_text_width = text_screen(f"Mode: {difficulty.capitalize()}", red, 50, 5)
            equation_text_width = text_screen(f"Equation: {equation}", red, screen_width - 350, 5)
            
            # Center score and correct equations
            score_text = font.render(f"Score: {score}", True, red)
            correct_eq_text = font.render(f"Correct Equations: {correct_equations}", True, red)
            score_width = score_text.get_width()
            correct_eq_width = correct_eq_text.get_width()
            
            # Center texts
            text_screen(f"Score: {score}", red, (screen_width - score_width) // 2, 50)
            text_screen(f"Correct Equations: {correct_equations}", red, (screen_width - correct_eq_width) // 2, 100)

            for food_x, food_y, food_value in food_items:
                pygame.draw.rect(gameWindow, green if food_value >= 0 else red, [food_x, food_y, snake_size, snake_size])
                text_screen(f"{food_value}", black, food_x + 5, food_y + 5)
            pygame.draw.line(gameWindow, red, (0, 40), (1200, 40), 5)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            # Check for time limit
            elapsed_time = time.time() - start_time
            remaining_time = time_limit - int(elapsed_time)
            text_screen(f"Time: {remaining_time}", red, screen_width - 250, 100)
            if remaining_time <= 0:
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

gameloop()
