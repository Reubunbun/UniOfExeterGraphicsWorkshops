#version 130

in vec3 position_view_space;
in vec2 fragment_texCoord;
in mat4 S;

out vec4 final_color;

uniform int mode;

uniform int has_texture;

uniform sampler2D textureObject;
uniform sampler2D sampler_shadow;

uniform vec3 Ka;
uniform vec3 Kd;
uniform vec3 Ks;
uniform float Ns;

uniform vec3 light;
uniform vec3 Ia;
uniform vec3 Id;
uniform vec3 Is;

void main() {
	// Calculate vectors used for shading calculations
  vec3 camera_direction = -normalize(position_view_space);
  vec3 light_direction = normalize(light-position_view_space);

  // Calculate the normal to the fragment using position of its neighbours
  vec3 xTangent = dFdx( position_view_space );
  vec3 yTangent = dFdy( position_view_space );
  vec3 normal_view_space = normalize( cross( xTangent, yTangent ) );

  // calculate light components
  vec4 ambient = vec4(Ia*Ka,1.0f);
  vec4 diffuse = vec4(Id*Kd*max(0.0f,dot(light_direction, normal_view_space)),1.0f);
  vec4 specular = vec4(Is*Ks*pow(max(0.0f, dot(reflect(light_direction, normal_view_space), -camera_direction)), Ns), 1.0f);

  // calculate the attenuation function
  float dist = length(light - position_view_space);
  float attenuation =  min(1.0/(dist*dist*0.005) + 1.0/(dist*0.05), 1.0);

  vec4 texval = vec4(1.0f);

	if (has_texture == 1){
		texval = texture2D(textureObject, fragment_texCoord);
	}

	// Store the tempory value for the final colour
	vec4 temp = texval*ambient + attenuation*(texval*diffuse + specular);

	// Convert coordinates to light space
	vec4 position_light_space = S * vec4(position_view_space, 1.0f);

	// If the last coordinate is negative, we can ignore this point and render in the usual way as its behind the rendered view.
	if (position_light_space.w >= 0){

		// Divide by the fourth coordinate to remove the homogenous coordinate. Each coordinate is moved very slightly to improve appearance.
		vec3 position = vec3((position_light_space.x/position_light_space.w)-0.001f, (position_light_space.y/position_light_space.w)-0.001f, (position_light_space.z/position_light_space.w)-0.001f);

		// If the texture depth is smaller than position's z value, then it is occluded and we should use ambient lighting. Otherwise render the usual way.
		if (texture(sampler_shadow, position.xy).z < position.z){
			final_color = texval * ambient;
		} else {
			final_color = temp;
		}

	} else {
		final_color = temp;
	}

}
