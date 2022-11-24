# Aditya Kumar
# ITP116, 10:00-10:50a.m.
# Final Project
# Description: Space Invaders Spinoff
# Uses Turtle graphics to create a Space-Invaders type game
# in which the user controls a shape to try to reach goals
# while avoiding the randomly spawning enemies

import turtle
import random
import sys
import time


# Global function to calculate "safe points"
# Used to teleport obstacles and goals away from player
def safe_points(x, y, error):
    # Define an x-coordinate in this area
    potentialx = random.randint(-280, 280)
    # Check if the x-coordinate is too close to the user
    while (potentialx < (x + error)) and (potentialx > (x - error)):
        # If the x-coordinate is too close, redefine the point
        potentialx = random.randint(-280, 280)

    # Define a y-coordinate in this area
    potentialy = random.randint(-280, 280)
    # Check if the y-coordinate is too close to the user
    while (potentialy < (y + error)) and (potentialy > (y - error)):
        # If the y-coordinate is too close, redefine the point
        potentialy = random.randint(-280, 280)

    # Return potential coordinates
    return potentialx, potentialy


# Defines a class for the display/screen
class Display():
    # Initializes the object
    def __init__(self):
        # Uses turtle to draw
        self.draw = turtle.Turtle()
        # Draw instantaneously
        self.draw.speed(0)
        # Keep track of lives, current level, and game status
        self.lives = 3
        self.level = 1
        self.playing = False

    # Writes title on screen
    def title(self):
        # Go to the correct location
        self.draw.penup()
        self.draw.goto(-240, 0)
        # Draw title
        self.draw.write("Space Invaders\n   Spinoff", font = ("Courier", 45, "bold"))
        # Go to second location
        self.draw.penup()
        self.draw.goto(-205, -100)
        # Write message
        self.draw.write("Press space to start", font = ("Courier", 25, "normal"))

    # Ends the game
    def end(self):
        # Go to correct location
        self.draw.goto(-165, 0)
        # Write message
        self.draw.write("Game Over", font = ("Courier", 45, "bold"))
        # Go to second location
        self.draw.penup()
        self.draw.goto(-195, -100)
        # Write message
        self.draw.write("Press space to exit", font=("Courier", 25, "normal"))

    # Clears the screen
    def clear(self):
        self.draw.clear()

    # Changes status to playing
    def set_playing(self):
        self.playing = True

    # Changes status to not playing
    def not_playing(self):
        self.playing = False

    # Gets game status
    def check_playing(self):
        if self.playing:
            return True
        else:
            return False

    # Draws game map
    def draw_map(self):
        # Makes border thick
        self.draw.pensize(6)
        # Goes to left corner
        self.draw.penup()
        self.draw.goto(-300, -300)
        self.draw.pendown()
        # Loops four times to make square
        for x in range(4):
            # Draws line
            self.draw.fd(600)
            # Rotates
            self.draw.lt(90)
        # Hides turtle
        self.draw.ht()

    # Displays information on state of game
    def show_info(self):
        # Saves text as a variable
        text = "Lives Remaining: " + str(self.lives) + "\t      Current Level: " + str(self.level)
        # Goes to location
        self.draw.penup()
        self.draw.goto(-300, 305)
        # Writes message
        self.draw.write(text, font = ("Courier", 16, "normal"))

    # Updates level count
    def add_level(self):
        self.level += 1

    # Updates lives count
    def lose_life(self):
        self.lives -= 1

    # Checks if game is over
    def check_game_over(self):
        if self.lives <= 0:
            return True
        else:
            return False

    # Undoes last drawing by turtle
    def undo(self):
        self.draw.undo()

    # Returns level number
    def get_level(self):
        return self.level


# Class for shapes
class Shape(turtle.Turtle):
    # Initialize with starting coordinates and type of shape
    def __init__(self, x, y, shapeType, color):
        # Create shape
        turtle.Turtle.__init__(self, shape = shapeType)
        # Set color
        self.color(color)
        # Make shape instantaneously move to given location
        self.penup()
        self.speed(0)
        self.goto(x, y)


# Inherit from shape class for user's shape
class User(Shape):
    # Initialize
    def __init__ (self, x, y, shapeType, color):
        Shape.__init__(self, x, y, shapeType, color)

    # Movement
    def move(self, speed):
        # Set forward speed
        self.fd(speed)

        # Right border detection
        if self.xcor() > 288:
            # Set the x-coordinate to be inside the square
            self.setx(286)
            # Make the user face the opposite direction
            self.rt(180)
        # Upper border detection
        if self.ycor() > 288:
            # Set the y-coordinate to be inside the square
            self.sety(286)
            # Make the user face the opposite direction
            self.rt(180)
        # Left border detection
        if self.xcor() < -288:
            # Set the x-coordinate to be inside the square
            self.setx(-286)
            # Make the user face the opposite direction
            self.rt(180)
        # Lower border detection
        if self.ycor() < -288:
            # Set the y-coordinate to be inside the square
            self.sety(-286)
            # Make the user face the opposite direction
            self.rt(180)

    # Face up
    def face_up(self):
        self.setheading(90)

    # Face left
    def face_left(self):
        self.setheading(180)

    # Face down
    def face_down(self):
        self.setheading(270)

    # Face right
    def face_right(self):
        self.setheading(0)

    # Check collision, incorporating an error if needed
    def check_collision(self, obstacle, error):
        # Check coordinates
        return (self.ycor() > (obstacle.ycor() - error)) and (self.ycor() < (obstacle.ycor() + error)) and \
                (self.xcor() > (obstacle.xcor() - error)) and (self.xcor() < (obstacle.xcor() + error))


# Inherit for shape from obstacle class
class Obstacle(Shape):
    # Initialize with more parameters to control size and speed
    def __init__(self, x, y, shapeType, color, stretch, speed):
        Shape.__init__(self, x, y, shapeType, color)
        # Can face a random direction
        self.setheading(random.randint(0, 360))
        # Set stretch and speed
        self.stretch = stretch
        self.speed = speed
        # Stretch the shape by the given amount
        self.shapesize(stretch_wid=self.stretch, stretch_len=self.stretch, outline=None)

    # Movement for the obstacle
    def move(self):
        # Set speed
        self.fd(self.speed)

        # For collisions, incorporate size of obstacle for check
        check = 300 - (10 * self.stretch)
        # Right border detection
        if self.xcor() > check:
            # Set the x-coordinate to be inside the box
            self.setx(check)
            # Make the obstacle turn a random amount
            self.rt(random.randint(45, 215))
        # Upper border detection
        if self.ycor() > check:
            # Set the y-coordinate to be inside the box
            self.sety(check)
            # Make the obstacle turn a random amount
            self.rt(random.randint(45, 215))
        # Left border detection
        if self.xcor() < (-1 * check):
            # Set the x-coordinate to be inside the box
            self.setx(-1 * check)
            # Make the obstacle turn a random amount
            self.rt(random.randint(45, 215))
        # Lower border detection
        if self.ycor() < (-1 * check):
            # Set the y-coordinate to be inside the box
            self.sety(-1 * check)
            # Make the obstacle turn a random amount
            self.rt(random.randint(45, 215))

    # Get size
    def get_size(self):
        return self.stretch

    # Method to have obstacle teleport away from player
    def teleport_away(self, userx, usery):
        # Use safe point function
        self.potentialx, self.potentialy = safe_points(userx, usery, 20)
        # Teleport to these points
        self.goto(self.potentialx, self.potentialy)
        # Set direction randomly
        self.setheading(random.randint(0, 360))


# A class for the goal that inherits from shape
class Goal(Shape):
    # Initialization
    def __init__(self, x, y, shapeType, color):
        Shape.__init__(self, x, y, shapeType, color)
        # Shorten it
        self.shapesize(stretch_wid=0.75, stretch_len=0.75, outline=None)

    # Teleport the goal
    def teleport(self, userx, usery):
        # Use safe points function
        self.potentialx, self.potentialy = safe_points(userx, usery, 80)
        # Set coordinates
        self.goto(self.potentialx, self.potentialy)



# Defines main function
def main():
    # Use tracer method to ensure graphics only updated manually
    turtle.tracer(0)

    # Create display object
    d = Display()

    # Create border/map
    d.draw_map()

    # Proceed with game once user presses space
    while not d.check_playing():
        # Show title
        d.title()
        # Wait for space key
        turtle.onkey(d.set_playing, "space")
        # Listen for user input
        turtle.listen()

    # Clear title
    d.clear()
    # Redraw borders
    d.draw_map()
    # Show level and lives
    d.show_info()

    # Create user and goal
    u = User(0, 0, "square", "black")
    g = Goal(-250, 250, "circle", "green")

    # Store a list of enemies
    enemies = []
    # Add one obstacle
    enemies.append(Obstacle(-200, 200, "triangle", "red", 1, 3))

    # Listen for user inputs for direction
    turtle.onkey(u.face_up, "Up")
    turtle.onkey(u.face_down, "Down")
    turtle.onkey(u.face_left, "Left")
    turtle.onkey(u.face_right, "Right")
    turtle.listen()

    # Loop for main gameplay
    while True:
        # Update graphics
        turtle.update()

        # Use sleep to allow time for user to react
        time.sleep(0.02)

        # User speed
        u.move(4)

        # Loop through every enemy
        for enemy in enemies:
            # Move enemy
            enemy.move()

            # Check for collision with user
            if u.check_collision(enemy, 15 * enemy.get_size()):
                # Lower life count
                d.lose_life()
                # Undo stats to reload updated ones
                d.undo()
                d.show_info()
                # Relocate enemy
                enemy.teleport_away(u.xcor(), u.ycor())

                # Check if game is over
                if d.check_game_over():
                    # Change status
                    d.not_playing()
                    # Loop until player presses space
                    while not d.check_playing():
                        # Show that game is over
                        d.end()
                        # Change status to leave loop once user presses space
                        turtle.onkey(d.set_playing, "space")
                        # Listen for user input
                        turtle.listen()
                    # Exit program
                    sys.exit()

        # Check if user touches goal
        if u.check_collision(g, 16):
            # Add to level count
            d.add_level()
            # Update stats
            d.undo()
            d.show_info()
            # Relocate goal
            g.teleport(u.xcor(), u.ycor())

            # Find new coordinates for new enemy
            newx, newy = safe_points(u.xcor(), u.ycor(), 80)
            # Check to see if the level is a multiple of five
            if d.get_level() % 5 == 0:
                # Spawn the bigger, faster triangle
                enemies.append(Obstacle(newx, newy, "triangle", "dark red", 1.5, 5))
            else:
                # Spawn the normal triangle
                enemies.append(Obstacle(newx, newy, "triangle", "red", 1, 3))



# Calls main function
main()