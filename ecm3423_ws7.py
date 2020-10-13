import pygame

# import the scene class
from scene import Scene

from lightSource import LightSource

from blender import load_obj_file

from BaseModel import DrawModelFromMesh

from shaders import *

from cubeMap import *

from sphereModel import Sphere

from showTexture import *


class ExeterScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.light = LightSource(self, position=[4., 5., 3.])
        Vs = lookAt(self.light.position, np.array([0., 0., 0.], dtype='f'))

        meshes = load_obj_file('models/scene.obj')
        self.meshes = [DrawModelFromMesh(scene=self, M=scaleMatrix([0.5,0.5,0.5]), mesh=mesh, shader=ShadowShader(Vs)) for mesh in meshes]

        table = load_obj_file('models/quad_table.obj')
        self.table = [DrawModelFromMesh(scene=self, M=translationMatrix([0, -3, +0]), mesh=mesh, shader=ShadowShader(Vs)) for mesh in table]

        box = load_obj_file('models/fluid_border.obj')
        self.box = [DrawModelFromMesh(scene=self, M=translationMatrix([0,+1,0]), mesh=mesh, shader=ShadowShader(Vs)) for mesh in box]

        # The shader to apply to the model - CubeShader for reflection, ShadowShader(Vs) for shadows
        shaderMode = CubeShader()

        bunny = load_obj_file('models/bunny_world.obj')
        bunny = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, +1, 0]), scaleMatrix([0.5, 0.5, 0.5])), mesh=bunny[0], shader=shaderMode)

        sphere = Sphere()
        sphere = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, +1, 0]), scaleMatrix([0.5, 0.5, 0.5])), mesh=sphere, shader=shaderMode)

        # The model to draw in the middle - bunny or sphere
        self.modelToDraw = sphere

        self.shadow_map = ShadowMap(self)
        self.cube = CubeMap(self, name='skybox/ame_ash')

        # Helper object to show the cube map.
        '''flat_cube = CubeMap(self, name='skybox/ame_ash')
        self.flattened_cube = FlattenCubeMap(scene=self, cube=flat_cube)'''

        # Helper object to show the shadow map.
        self.show_texture = ShowTexture(self, self.shadow_map)

    def keyboard(self, event):
        '''
        Process additional keyboard events for this demo.
        '''
        Scene.keyboard(self, event)

        if event.key == pygame.K_1:
            print('--> using Flat shading without texture')
            self.modelToDraw.use_textures = False
            self.modelToDraw.bind_shader('flat')
        elif event.key == pygame.K_2:
            print('--> using gouraud')
            self.modelToDraw.use_textures = False
            self.modelToDraw.bind_shader('gouraud')
        elif event.key == pygame.K_3:
            print('--> using phong')
            self.modelToDraw.use_textures = False
            self.modelToDraw.bind_shader('phong')
        elif event.key == pygame.K_4:
            print('--> using blinn')
            self.modelToDraw.use_textures = False
            self.modelToDraw.bind_shader('blinn')
        elif event.key == pygame.K_5:
            print('--> using Flat shading with texture')
            self.modelToDraw.use_textures = True
            self.modelToDraw.bind_shader('flat')
        elif event.key == pygame.K_6:
            print('--> using Texture shading')
            self.modelToDraw.bind_shader('texture')
        elif event.key == pygame.K_7:
            print('--> using original texture')
            self.modelToDraw.shader.mode = 1
        elif event.key == pygame.K_8:
            print('--> using second texture')
            self.modelToDraw.shader.mode = 2

    def draw(self):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.camera.update()
        self.shadow_map.bind_texture()

        # then we loop over all models in the list and draw them
        for model in self.meshes:
            model.draw()
        # also all models from the table
        for model in self.table:
            model.draw()
        # and for the box
        for model in self.box:
            model.draw()

        self.cube.bind_texture()
        self.modelToDraw.draw()

        '''self.flattened_cube.draw()'''
        '''self.show_texture.draw()'''
        
        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        pygame.display.flip()

    def depth_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for model in self.table:
            model.draw()
        for model in self.box:
            model.draw()
        for model in self.meshes:
            model.draw()
        self.modelToDraw.draw()

    def draw_reflections(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.shadow_map.bind_texture()

        for model in self.meshes:
            model.draw()
        for model in self.table:
            model.draw()
        for model in self.box:
            model.draw()


if __name__ == '__main__':
    # initialises the scene object
    # scene = Scene(shaders='gouraud')
    scene = ExeterScene()

    # starts drawing the scene
    scene.run()
