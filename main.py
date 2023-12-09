# Import necessary libraries
import cv2
import mediapipe as mp
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluPerspective
import math

# Initialize Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize Pygame
pygame.init()

# Set up the display and OpenGL context
display = (640, 480)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption('Pygame')

# Set up the perspective projection matrix
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

# Set up the initial camera position
glTranslatef(0.0, 0.0, -5)

# Define the cube vertices
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

# Define the cube edges
edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

# Define additional lines for top and bottom faces
top_bottom_lines = (
    (0, 2),
    (1, 3),
    (4, 6),
    (5, 7)
)

# Colors
white = (1, 1, 1)
red = (1, 0, 0)
blue = (0, 0, 1)

# Light settings
light_position = (5, 5, 5, 1)
light_ambient = (0.2, 0.2, 0.2, 1)
light_diffuse = (0.8, 0.8, 0.8, 1)
light_specular = (1, 1, 1, 1)

# Set up lighting
glLightfv(GL_LIGHT0, GL_POSITION, light_position)
glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)

# Material settings
material_ambient = (0.7, 0.7, 0.7, 1)
material_diffuse = (0.8, 0.8, 0.8, 1)
material_specular = (1, 1, 1, 1)
material_shininess = 50

# Enable smooth shading
glShadeModel(GL_SMOOTH)

# Set material properties
glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, material_ambient)
glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_diffuse)
glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, material_specular)
glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, material_shininess)

# Enable depth testing and lighting
glEnable(GL_DEPTH_TEST)
glEnable(GL_COLOR_MATERIAL)

# Define functions for drawing geometric shapes

def Sphere(radius=1, resolution=20):
    # Draw a sphere
    glColor3fv((0.5, 0.8, 1.0))
    # Lines along longitude
    for i in range(resolution):
        theta0 = 2 * math.pi * (i / float(resolution))
        x0 = radius * math.cos(theta0)
        y0 = radius * math.sin(theta0)
        theta1 = 2 * math.pi * ((i + 1) / float(resolution))
        x1 = radius * math.cos(theta1)
        y1 = radius * math.sin(theta1)
        glBegin(GL_LINES)
        for j in range(resolution):
            phi = math.pi * (-0.5 + (j / float(resolution)))
            z0 = radius * math.sin(phi)
            r0 = radius * math.cos(phi)
            glVertex3f(x0 * r0, y0 * r0, z0)
            glVertex3f(x1 * r0, y1 * r0, z0)
        glEnd()
    # Lines along latitude
    for i in range(resolution):
        phi0 = math.pi * (-0.5 + (i / float(resolution)))
        z0 = radius * math.sin(phi0)
        r0 = radius * math.cos(phi0)
        phi1 = math.pi * (-0.5 + ((i + 1) / float(resolution)))
        z1 = radius * math.sin(phi1)
        r1 = radius * math.cos(phi1)
        glBegin(GL_LINES)
        for j in range(resolution + 1):
            theta = 2 * math.pi * (j / float(resolution))
            x0 = radius * math.cos(theta)
            y0 = radius * math.sin(theta)
            glVertex3f(x0 * r0, y0 * r0, z0)
            glVertex3f(x0 * r1, y0 * r1, z1)
        glEnd()

def distance_between_points(point1, point2):
    # Calculate the distance between two 3D points
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2) ** 0.5

def Cone(radius=1, height=2, resolution=20):
    # Draw a cone
    glBegin(GL_LINES)
    glColor3fv((0.5, 0.8, 1.0))
    for i in range(resolution):
        angle0 = (i / float(resolution)) * (2 * math.pi)
        x0 = radius * math.cos(angle0)
        y0 = 0
        z0 = radius * math.sin(angle0)
        angle1 = (i + 1) / float(resolution) * (2 * math.pi)
        x1 = radius * math.cos(angle1)
        y1 = 0
        z1 = radius * math.sin(angle1)
        glVertex3f(x0, y0, z0)
        glVertex3f(x1, y1, z1)
        # Connect the lines to the tip of the cone
        glVertex3f(x0, y0, z0)
        glVertex3f(0, height, 0)
    glEnd()

def draw_cube():
    # Draw a cube
    glColor3fv((0.5, 0.8, 1.0))
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_axes(length=0.3, position=(-2.3, -1.8, 0), rotation_y=0):
    # Draw axes
    glPushMatrix()
    glTranslatef(*position)
    glRotatef(rotation_y, 0, 1, 0)  # Rotate only the axes, not the cube
    glScalef(length, length, length)
    glBegin(GL_LINES)
    # X-axis arrow
    glColor3fv(red)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(0.9, 0.1, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(0.9, -0.1, 0)
    # Y-axis arrow
    glColor3fv(blue)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(0.1, 0.9, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(-0.1, 0.9, 0)
    # Z-axis arrow (green)
    glColor3fv((0, 1, 0))  # Make Z-axis green
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 1)
    glVertex3f(0, 0, 1)
    glVertex3f(0.1, 0.1, 0.9)
    glVertex3f(0, 0, 1)
    glVertex3f(-0.1, -0.1, 0.9)
    glEnd()
    glPopMatrix()

def load_render_data(file_path):
    # Load 3d data from an .obj file
    render_vertices = []
    render_faces = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                # Parse vertex data
                vertex = list(map(float, line[2:].split()))
                render_vertices.append(vertex)
            elif line.startswith('f '):
                # Parse face data
                face_indices = []
                for vertex_info in line[2:].split():
                    # Split the vertex information and take only the vertex index
                    vertex_index = int(vertex_info.split('/')[0])
                    face_indices.append(vertex_index)
                render_faces.append(face_indices)
    return render_vertices, render_faces

# Load render data
render_vertices, render_faces = load_render_data('diamond.obj')

# Define a function to draw a render
def draw_render():
    glBegin(GL_LINES)
    for face in render_faces:
        for i in range(len(face)):
            if face[i] - 1 >= len(render_vertices):
                return
            else:
                glVertex3fv(render_vertices[face[i] - 1])
                next_index = (i + 1) % len(face)
                glVertex3fv(render_vertices[face[next_index] - 1])
    glEnd()

# Function to draw a stylized hand skeleton
def draw_hand_skeleton(hand_landmarks):
    if hand_landmarks:
        # Set color to a cool shade
        glColor3fv((0.5, 0.8, 1.0))
        # Draw hand landmarks as points
        glPointSize(3.0)
        glBegin(GL_POINTS)
        for landmark in hand_landmarks.landmark:
            x, y, z = landmark.x, landmark.y, landmark.z
            # Apply translation and rotation to adjust the hand landmarks
            x, y, z = -x, -y, -z  # Reverse X, Y, and Z to correct the orientation
            x += 0.5  # Adjust the X coordinate to center the hand in the view
            glVertex3f(x, y, z)
        glEnd()
        # Draw hand skeleton lines with a cool effect
        glLineWidth(2.0)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_LINES)
        for connection in mp_hands.HAND_CONNECTIONS:
            x1, y1, z1 = hand_landmarks.landmark[connection[0]].x, hand_landmarks.landmark[connection[0]].y, hand_landmarks.landmark[connection[0]].z
            x2, y2, z2 = hand_landmarks.landmark[connection[1]].x, hand_landmarks.landmark[connection[1]].y, hand_landmarks.landmark[connection[1]].z
            # Apply translation and rotation to adjust the hand skeleton lines
            x1, y1, x2, y2 = -x1, -y1, -x2, -y2  # Reverse X and Y to correct the orientation
            x1 += 0.5  # Adjust the X coordinate to center the hand in the view
            x2 += 0.5  # Adjust the X coordinate to center the hand in the view
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
        glEnd()
        glDisable(GL_BLEND)
        glDisable(GL_LINE_SMOOTH)

# Dictionary of shapes
shapes = {
    1: draw_cube,
    2: Sphere,
    3: Cone,
    4: draw_render,  # Add the 3d file to the dictionary
}

selected_shape = 1  # Initial shape (cube)

# Load a 3D .obj file
render_vertices = []
render_edges = []
with open("diamond.obj", "r") as obj_file:
    for line in obj_file:
        if line.startswith("v "):
            # Vertex
            vertex = [float(coord) for coord in line.strip().split()[1:]]
            render_vertices.append(vertex)
        elif line.startswith("l "):
            # Line (edge)
            edge = [int(index) - 1 for index in line.strip().split()[1:]]
            render_edges.append(edge)

current_scale = 1.0  # Initial scale value
current_hand_position = (0, 0, 0)  # Initial hand position
last_hand_position = (0, 0, 0)  # Previous hand position for smoothing
rotation_matrix = pygame.math.Vector3()  # Initialize rotation matrix
damping_factor = 0.2  # Damping factor for smooth transitions
calibration_complete = False  # Flag to indicate if calibration is complete
selected_shape = 1  # Initial shape (cube)
calibration_offset = (0, 0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_shape = 1
            elif event.key == pygame.K_2:
                selected_shape = 2
            elif event.key == pygame.K_3:
                selected_shape = 3
            elif event.key == pygame.K_4:
                selected_shape = 4  # Switch to render

    # Capture a single frame
    ret, frame = cap.read()

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe Hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) <= 2:
        if len(results.multi_hand_landmarks) == 1:
            hand1 = results.multi_hand_landmarks[0]
            index_tip_hand1 = hand1.landmark[8]

            # If calibration is not complete and hand is near the center, set the calibration offset
            if not calibration_complete and (
                0.3 <= index_tip_hand1.x <= 0.7 and 0.3 <= index_tip_hand1.y <= 0.7
            ):
                calibration_offset = (
                    index_tip_hand1.x - current_hand_position[0],
                    index_tip_hand1.y - current_hand_position[1],
                    index_tip_hand1.z - current_hand_position[2],
                )
                calibration_complete = True

            # Update the current hand position with smoothing
            current_hand_position = (
                (1 - damping_factor) * current_hand_position[0] + damping_factor * (index_tip_hand1.x - calibration_offset[0]),
                (1 - damping_factor) * current_hand_position[1] + damping_factor * (index_tip_hand1.y - calibration_offset[1]),
                (1 - damping_factor) * current_hand_position[2] + damping_factor * (index_tip_hand1.z - calibration_offset[2]),
            )

            # Clear the screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Draw axes
            draw_axes()

            # Draw the selected shape based on hand position
            glPushMatrix()
            glColor3fv((0.5, 0.8, 1.0))
            draw_hand_skeleton(hand1)
            glTranslatef(*current_hand_position)
            glRotatef(rotation_matrix.y, 0, 1, 0)
            glScalef(current_scale, current_scale, current_scale)
            shapes[selected_shape]()
            glPopMatrix()

        elif len(results.multi_hand_landmarks) == 2:
            hand1, hand2 = results.multi_hand_landmarks
            index_tip_hand1 = hand1.landmark[8]
            index_tip_hand2 = hand2.landmark[8]

            # Calculate the average distance between index finger tips
            distance = (distance_between_points(index_tip_hand1, index_tip_hand2) +
                        distance_between_points(hand1.landmark[0], hand2.landmark[0])) / 2

            # Update the current scale and hand position based on hand positions with smoothing
            current_scale = (1 - damping_factor) * current_scale + damping_factor * distance
            last_hand_position = current_hand_position
            current_hand_position = (
                (1 - damping_factor) * (-(index_tip_hand1.x + index_tip_hand2.x) / 2) + damping_factor * last_hand_position[0],
                (1 - damping_factor) * (-(index_tip_hand1.y + index_tip_hand2.y) / 2) + damping_factor * last_hand_position[1],
                (1 - damping_factor) * ((index_tip_hand1.z + index_tip_hand2.z) / 2) + damping_factor * last_hand_position[2],
            )

            # Update the rotation matrix based on the vertical movement of two hands
            rotation_matrix.y = (index_tip_hand2.y - index_tip_hand1.y) * 100

            # Clear the screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Draw axes
            draw_axes(rotation_y=rotation_matrix.y)

            glPushMatrix()
            glColor3fv((0.5, 0.8, 1.0))
            draw_hand_skeleton(hand1)
            draw_hand_skeleton(hand2)
            glTranslatef(*current_hand_position)
            glRotatef(rotation_matrix.y, 0, 1, 0)
            glScalef(current_scale, current_scale, current_scale)
            shapes[selected_shape]()
            glPopMatrix()

    else:
        # If no hands are detected, smoothly transition back to the center
        target_position = (0, 0, 0)
        current_hand_position = tuple(
            (1 - damping_factor) * current + damping_factor * target
            for current, target in zip(current_hand_position, target_position)
        )

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_axes(rotation_y=rotation_matrix.y)

        glPushMatrix()
        glTranslatef(*current_hand_position)
        glRotatef(rotation_matrix.y, 0, 1, 0)
        glScalef(current_scale, current_scale, current_scale)
        shapes[selected_shape]()
        glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)