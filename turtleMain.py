import turtle

def draw_line(side_length, depth):
    # Base Case: If we are at the lowest depth, just draw a straight line.
    if depth == 0:
        my_turtle.forward(side_length)
        return

    # Recursive Step: Apply the pattern rules.
    # Divide the line into three segments.
    new_length = side_length / 3

    # 1. Draw the first 1/3 segment.
    draw_line(new_length, depth - 1)

    # 2. Turn right to start the inward triangle.
    my_turtle.right(60)

    # 3. Draw the second segment (first side of the triangle).
    draw_line(new_length, depth - 1)

    # 4. Turn left to draw the second side of the triangle.
    my_turtle.left(120)

    # 5. Draw the third segment (second side of the triangle).
    draw_line(new_length, depth - 1)

    # 6. Turn right again to get back to the original direction.
    my_turtle.right(60)

    # 7. Draw the final 1/3 segment.
    draw_line(new_length, depth - 1)


# --- Main Program ---

# Get user input
try:
    num_sides = int(input("Enter the number of sides: "))
    length = int(input("Enter the side length: "))
    recursion_depth = int(input("Enter the recursion depth: "))
except ValueError:
    print("Invalid input. Please enter integers.")
    exit()

# Setup the turtle screen and turtle
screen = turtle.Screen()
screen.title("Recursive Polygon Pattern")
my_turtle = turtle.Turtle()
my_turtle.shape("turtle")
my_turtle.color("blue")
my_turtle.speed(0)  # Set speed to fastest for complex drawings

# Lift the pen and position the turtle to center the drawing
my_turtle.penup()
my_turtle.goto(-length / 2, length / 2) # Adjust starting position
my_turtle.pendown()

# Draw the complete shape
for _ in range(num_sides):
    draw_line(length, recursion_depth)
    # Turn to draw the next side of the shape
    my_turtle.right(360 / num_sides)

# Hide the turtle and keep the window open
my_turtle.hideturtle()
screen.mainloop()