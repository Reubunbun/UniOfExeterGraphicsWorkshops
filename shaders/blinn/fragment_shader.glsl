# version 130

in vec3 fragment_color;      
in vec3 position_view_space;
in vec3 normal_view_space;


out vec3 final_color;

uniform int mode;

// material uniforms
uniform vec3 Ka;
uniform vec3 Kd;
uniform vec3 Ks;
uniform float Ns;

// light source
uniform vec3 light;
uniform vec3 Ia;
uniform vec3 Id;
uniform vec3 Is;

void main() {
  // calculate vectors used for shading calculations
  vec3 camera_direction = -normalize(position_view_space);
  vec3 light_direction = normalize(light-position_view_space);
  vec3 halfway = normalize(light_direction+camera_direction);

  // calculate light components
  vec3 ambient = Ia*Ka;
  vec3 diffuse = Id*Kd*max(0.0f,dot(light_direction, normal_view_space));
  vec3 specular = Is*Ks*pow(max(0.0f, dot(halfway, normal_view_space)), 4*Ns);

  // calculate the attenuation function
  float dist = length(light - position_view_space);
  float attenuation =  min(1.0/(dist*dist*0.005) + 1.0/(dist*0.05), 1.0);

  // combine the shading components
  final_color = ambient + attenuation*(diffuse + specular);
}
