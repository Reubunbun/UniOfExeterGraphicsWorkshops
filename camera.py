# import a bunch of useful matrix functions (for translation, scaling etc)
from matutils import *


class Camera:
    '''
    Base class for handling the camera.
    TODO WS2: Implement this class to allow moving the mouse
    '''

    def __init__(self):
        self.V = np.identity(4)     # Start with the identity matrix.
        self.phi = 0.               # Azimuth angle (around the y axis)
        self.psi = 0.               # Zenith angle (around the x axis)
        self.distance = 10.         # Distance of the camera to the centre point
        self.center = [0., 0., 0.]  # Position of the centre
        self.update()               # Calculate the view matrix

    def update(self):
        '''
        Function to update the camera view matrix from parameters.
        Starts by setting the point the camera looks at as the center of the coordinate system.
        This coordinate system is then moved and rotated by changing this class' attributes.
        '''
        # Calculate the translation matrix for the view center (the point we look at)
        T0 = translationMatrix(self.center)

        # Calculate the rotation matrix from the angles phi and psi angles.
        R = np.matmul( rotationMatrixX(self.psi), rotationMatrixY(self.phi) )

        # Calculate translation for the camera distance to the center point.
        T = translationMatrix( [0., 0., -self.distance] )

        # Finally we calculate the view matrix by combining the three matrices.
        self.V = np.matmul( np.matmul(T, R), T0 )
