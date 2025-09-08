import pygame
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Game Window Settings
WIDTH, HEIGHT = 600, 700
LANE_WIDTH = WIDTH // 6  # 6 lanes
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game 🚗💨")

# Colors
WHITE = (255, 255, 255)
ROAD_COLOR = (50, 50, 50)
CAR_COLOR = (0, 255, 0)  # Green Car
OBSTACLE_COLOR = (255, 0, 0)  # Red Obstacles
LINE_COLOR = (255, 255, 255)  # Lane dividers

# Car Properties
car_width, car_height = 50, 80
lane_positions = [LANE_WIDTH * i + (LANE_WIDTH - car_width) // 2 for i in range(6)]
car_x = lane_positions[2]  # Start in middle lane
car_y = HEIGHT - 120
car_speed = 7  # Controls obstacle speed
current_lane = 2  # Middle lane index (0-5)

# Obstacle Properties
obstacle_width, obstacle_height = 50, 80
obstacles = []

# Data Logging
race_data = {"Time": [], "Speed": [], "Crashes": 0}
start_time = time.time()

# Game Control
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)  # Clear screen
    pygame.draw.rect(screen, ROAD_COLOR, (0, 0, WIDTH, HEIGHT))  # Draw road

    # Draw Lane Dividers
    for i in range(1, 6):  # 5 lane dividers for 6 lanes
        pygame.draw.line(screen, LINE_COLOR, (LANE_WIDTH * i, 0), (LANE_WIDTH * i, HEIGHT), 3)

    # Move Obstacles
    for obs in obstacles:
        obs["y"] += car_speed  # Obstacle speed now depends on car speed
        pygame.draw.rect(screen, OBSTACLE_COLOR, (obs["x"], obs["y"], obstacle_width, obstacle_height))

    # Add New Obstacles Randomly
    if random.randint(1, 100) < 5:  # 5% chance per frame
        obstacles.append({"x": random.choice(lane_positions), "y": -obstacle_height})

    # Remove Passed Obstacles
    obstacles = [obs for obs in obstacles if obs["y"] < HEIGHT]

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Smooth Lane Switching
    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and current_lane > 0:
        current_lane -= 1  # Move left
        time.sleep(0.2)  # Prevent instant lane-switching
    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and current_lane < 5:
        current_lane += 1  # Move right
        time.sleep(0.2)

    # Speed Control
    if keys[pygame.K_UP]:
        car_speed = min(car_speed + 0.1, 15)  # Increase speed (max 15)
    if keys[pygame.K_DOWN]:
        car_speed = max(car_speed - 0.1, 3)  # Decrease speed (min 3)

    # Update Car Position Based on Lane
    car_x = lane_positions[current_lane]

    # Draw Player Car
    pygame.draw.rect(screen, CAR_COLOR, (car_x, car_y, car_width, car_height))

    # Display Speed
    font = pygame.font.SysFont(None, 55)
    speed_text = font.render(f"Speed: {car_speed:.1f}", True, (0, 0, 0))
    screen.blit(speed_text, (10, 10))

    # 🔥 **Fixed Collision Detection!**
    for obs in obstacles:
        if (
                car_x < obs["x"] + obstacle_width  # Obstacle's right side past car's left
                and car_x + car_width > obs["x"]  # Car's right side past obstacle's left
                and car_y < obs["y"] + obstacle_height  # Obstacle's bottom past car's top
                and car_y + car_height > obs["y"]  # Car's bottom past obstacle's top
        ):
            print("💥 CRASH!")
            race_data["Crashes"] += 1
            running = False

    # Log Data
    race_data["Time"].append(time.time() - start_time)
    race_data["Speed"].append(car_speed)

    # Refresh Screen
    pygame.display.update()
    clock.tick(60)  # Fixed frame rate for smooth gameplay

# Save Data for Analysis
df = pd.DataFrame(race_data)
df.to_csv("race_performance.csv", index=False)
print("🚗 Race Data Saved!")

# Analyze Race Performance
plt.figure(figsize=(8, 4))
plt.plot(df["Time"], df["Speed"], label="Speed Over Time", color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Speed")
plt.title("Race Performance Analysis")
plt.legend()
plt.show()

pygame.quit()
