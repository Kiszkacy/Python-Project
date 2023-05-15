#version 330

// input color
in vec4 color;

// output color
out vec4 px_color;

void main() {

    // fill pixel with color
    px_color = vec4(color);
}