from BaseModel import BaseModel
from matutils import poseMatrix
# imports all openGL functions
from OpenGL.GL import *
import numpy as np
from mesh import Mesh
from material import Material
from texture import Texture


class Sphere(Mesh):
    def __init__(self, nvert=10, nhoriz=20):
        n = nvert * nhoriz + 2
        vertex_colors = np.zeros((n, 3), 'f')
        # texture coordinates
        textureCoords = np.zeros((n, 2), 'f')

        circles, vertices = self.generate_points(nvert, nhoriz)
        vertices = np.array(vertices, dtype='f')
        faces = self.generate_faces(circles)
        indices = np.array(faces, dtype=np.uint32)

        Mesh.__init__(self,
                      vertices=vertices,
                      faces=indices,
                      textureCoords=textureCoords,
                      material=Material(Ka=[0.5,0.5,0.5], Kd=[0.6,0.6,0.9], Ks=[1.,1.,0.9], Ns=15.0)
                      )

    def generate_points(self, horizontal, vertical):
        '''
        Generates a list of vertices for a sphere of given number of horizontal and vertical points you wish to have.
        :param horizontal: How many horizontal segments the sphere will have
        :param vertical: How many vertical segments the sphere will have
        :return points: A list of all the vertices that the sphere will have
        :return circles: A list of the vertices separated by which vertical segment you are on
        '''

        currentPoint = [0, 1, 0]
        # A list that will contain separate lists of each circle as you move down the sphere
        circles = []
        # A list that will contain vertices of a circle at a given y coordinate
        yCircles = []
        for i in range(vertical - 1):
            # Rotate around the z axis for every vertical point over pi radians
            rotation = self.rotZ(np.pi / vertical)
            currentPoint = np.matmul(rotation, currentPoint)
            yCircles.append(currentPoint)
            for j in range(horizontal):
                # Rotate around the y axis for every horizontal point over 2 pi radians
                rotation = self.rotY(2 * np.pi / horizontal)
                currentPoint = np.matmul(rotation, currentPoint)
                # Don't append to the list if we are at the last point
                if j != horizontal - 1:
                    yCircles.append(currentPoint)
            circles.append(yCircles)
            yCircles = []

        # The very top point of the cirlce
        points = [[0, 1, 0]]
        # Create the raw list of vertices
        for circle in circles:
            for point in circle:
                points.append(point)

        # Append the very bottom point of the circle
        circles.append([0, -1, 0])
        points.append([0, -1, 0])

        return circles, points

    def generate_faces(self, points):
        '''
        Creates a list of all faces in a sphere, given we have the vertices
        :param points: A list of all the points on the sphere
        :return: A list of all the faces on the sphere
        '''

        faces = []
        for i in range(len(points)):
            width = len(points[0])
            # Calculate the index of the first point on the current circle
            currentCircle = (i - 1) * width
            # Calculate teh index of the first point on the next circle
            nextCircle = i * width
            # Create the faces for the top fan
            if i == 0:
                for j in range(1, len(points[0]) + 1):
                    if j != len(points[0]):
                        faces.append([0, j, j + 1])
                    else:
                        faces.append([0, j, 1])
            # Create the faces of the bottom fan
            elif i == len(points) - 1:
                for j in range(1, len(points[0]) + 1):
                    if j != len(points[0]):
                        faces.append([currentCircle + j, nextCircle + 1, currentCircle + j + 1])
                    else:
                        faces.append([currentCircle + j, nextCircle + 1, currentCircle + 1])
            # Create all other faces
            else:
                for j in range(1, len(points[i]) + 1):

                    if j != len(points[i]):
                        faces.append([currentCircle + j, nextCircle + j, nextCircle + j + 1])
                        faces.append([currentCircle + j, nextCircle + j + 1, currentCircle + j + 1])
                    else:
                        faces.append([currentCircle + j, nextCircle + j, nextCircle + 1])
                        faces.append([currentCircle + j, nextCircle + 1, currentCircle + 1])

        return faces

    def rotZ(self, ang):
        '''
        :param ang: The angle to rotate by
        :return: The rotation matrix around the z axis
        '''

        rotation = np.identity(3, dtype='f')
        rotation[0][0] = np.cos(ang)
        rotation[0][1] = np.sin(ang)
        rotation[1][0] = -1 * np.sin(ang)
        rotation[1][1] = np.cos(ang)

        return rotation

    def rotY(self, ang):
        '''
        :param ang: The angle to rotate by
        :return: The rotation matrix around the y axis
        '''
        rotation = np.identity(3, dtype='f')
        rotation[0][0] = np.cos(ang)
        rotation[0][2] = np.sin(ang)
        rotation[2][0] = -1 * np.sin(ang)
        rotation[2][2] = np.cos(ang)

        return rotation