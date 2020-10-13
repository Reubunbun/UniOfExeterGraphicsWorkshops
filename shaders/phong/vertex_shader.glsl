#version 130

in vec3 position;
in vec3 normal;
in vec3 color;

out vec3 fragment_color;
out vec3 position_view_space;
out vec3 normal_view_space;

uniform mat4 PVM;
uniform mat4 VM;
uniform mat3 VMiT;
uniform int mode;


void main() {
    // transform the position using PVM matrix.
    gl_Position = PVM * vec4(position, 1.0f);

    // calculate vectors used for shading calculations
    position_view_space = vec3(VM*vec4(position,1.0f));
    normal_view_space = normalize(VMiT*normal);

    // pass on the color from the data array
    fragment_color = color;
}
