// Receives data in aPosition, (x,y,z), returns a gl_position.
// Runs once per vertex.
export const vertexShaderDef = `#version 300 es
  in vec3 aPosition;
  in vec4 aColor;
  out vec4 vColor;

  void main() {
    gl_Position = vec4(aPosition, 1.0);
    gl_PointSize = 12.0; // Point size in pixels (for now boids are points)
    vColor = aColor;
  }
`;

// Returns a vector of red. 
// Runs for fragments generated from rasterizing triangles between vertices
export const fragmentShaderDef = `#version 300 es
  precision highp float;
  in vec4 vColor;
  out vec4 fragColor;

  void main() {
    fragColor = vColor;
  }
`;