#version 130

in vec3 position;	
in vec3 normal;
in vec3 color;

out vec3 fragment_color;

uniform mat4 PVM;
uniform mat4 VM;
uniform mat3 VMiT;
uniform int mode;

uniform vec3 Ka;
uniform vec3 Kd;
uniform vec3 Ks;
uniform float Ns;

uniform vec3 light;
uniform vec3 Ia;
uniform vec3 Id;
uniform vec3 Is;


void main() {
  // transform the position using PVM matrix.
  gl_Position = PVM * vec4(position, 1.0f);

  // calculate vectors used for shading calculations
  vec3 position_view_space = vec3(VM*vec4(position,1.0f));
  vec3 normal_view_space = normalize(VMiT*normal);
  vec3 camera_direction = -normalize(position_view_space);
  vec3 light_direction = normalize(light-position_view_space);

  // calculate light components
  vec3 ambient = Ia*Ka;
  vec3 diffuse = Id*Kd*max(0.0f,dot(light_direction, normal_view_space));
  vec3 specular = Is*Ks*pow(max(0.0f, dot(reflect(light_direction, normal_view_space), -camera_direction)), Ns);

  // calculate the attenuation function
  float dist = length(light - position_view_space);
  float attenuation =  min(1.0/(dist*dist*0.005) + 1.0/(dist*0.05), 1.0);

  // combine the shading components
  fragment_color = ambient + attenuation*(diffuse + specular);
}
