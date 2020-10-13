#version 130

in vec3 fragment_texCoord;
in vec3 position_view_space;
in vec3 normal_view_space;

out vec4 final_color;

uniform samplerCube sampler_cube;	// the cube map texture
uniform mat4 VT;

void main(void) {

	vec3 camera_direction = -normalize(position_view_space);           // incident vector from viewpoint
	vec3 reflect = reflect(camera_direction, normal_view_space);       // reflect around the normal
	vec3 world_coord = vec3(VT*vec4(reflect, 1.0f));                   // back to world coordinates
	vec3 flipped = vec3(-world_coord.x, world_coord.y, world_coord.z); // flip x values

	// sample from the cube map texture
	final_color = textureCube(sampler_cube, flipped);
}
