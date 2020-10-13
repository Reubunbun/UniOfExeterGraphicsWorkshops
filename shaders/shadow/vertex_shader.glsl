#version 130	

in vec3 position;

in vec3 color;
in vec2 texCoord;

out vec3 fragment_color;
out vec3 position_view_space;
out vec2 fragment_texCoord;
out mat4 S;

uniform mat4 PVM;
uniform mat4 VM;
uniform mat3 VMiT;
uniform int mode;

uniform mat4 Ps;
uniform mat4 Vs;
uniform mat4 Vic;
uniform mat4 x;

void main(){
  gl_Position = PVM * vec4(position, 1.0f);
  position_view_space = vec3(VM*vec4(position, 1.0f));
  fragment_texCoord = texCoord;
  fragment_color = color;

	S = x * Ps * Vs * Vic;
}
