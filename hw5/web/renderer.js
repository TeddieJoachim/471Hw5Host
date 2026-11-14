import { vertexShaderDef, fragmentShaderDef } from "./shaders.js";
/*
Used webglfundamentals.org to get up and running with this.
The renderer has several responsibilites. It compiles and links shaders, creates a webgl program, and creates 
a buffer for our bird positions before binding it to a gl.ARRAY_BUFFER
*/


export class Renderer {
  constructor(canvas, boidDim) {
    this.gl = canvas.getContext("webgl2");
    const gl = this.gl;
    if (!gl) throw new Error("Renderer failed to load webgl2");

    // create the shaders, using webgl context to compile them and return a shader, then attach and link them to create a program 
    const vertexShader = this.createShader(gl, gl.VERTEX_SHADER, vertexShaderDef);
    const fragemntShader = this.createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderDef);
    this.program = this.createProgram(gl, vertexShader, fragemntShader);
    this.vao = gl.createVertexArray();
    gl.bindVertexArray(this.vao);

    // attributes get data from buffers, so we create one, then bind ARRAY_BUFFER to it so that when we write to ARRAY_BUFFER we are writing to positionBuffer
    this.positionBuffer = gl.createBuffer();
    this.colorBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);

    // we need to see where the attribute aPosition is for our program so that we can feed it
    // next line tells the vertex shader to read boidDim floats at a time from aPosition
    // then finally we enable 
    // Position attribute
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
    this.positionAttributeLocation = gl.getAttribLocation(this.program, "aPosition");
    gl.vertexAttribPointer(this.positionAttributeLocation, boidDim, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(this.positionAttributeLocation);

    // Color attribute
    gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
    this.colorAttributeLocation = gl.getAttribLocation(this.program, "aColor");
    gl.vertexAttribPointer(this.colorAttributeLocation, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(this.colorAttributeLocation);
  }

render(boidPositions, numBoids, boidDim, isPred) {
  const gl = this.gl;

  gl.clearColor(0, 0, 0, 1);
  gl.clear(gl.COLOR_BUFFER_BIT);
  gl.useProgram(this.program);
  gl.bindVertexArray(this.vao);

  const colors = new Float32Array(numBoids * 4);
  const toRender = new Float32Array(numBoids * boidDim);

  for (let idx = 0; idx < numBoids; idx++) {
    toRender[idx * boidDim] = boidPositions[idx * boidDim];
    toRender[idx * boidDim + 1] = boidPositions[idx * boidDim + 1];
    toRender[idx * boidDim + 2] = boidPositions[idx * boidDim + 2];

    if (idx === 0) {
      colors.set([0, 0, 1, 1], idx * 4);
    }
    else if (idx === numBoids - 1 && isPred) {
      colors.set([1, 0, 0, 1], idx * 4);
    }
    else {
      colors.set([0, 1, 0, 1], idx * 4);
    }
  }

  gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, toRender, gl.DYNAMIC_DRAW);

  gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, colors, gl.DYNAMIC_DRAW);

  gl.drawArrays(gl.POINTS, 0, numBoids);
}

  createShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      return shader;
    }
    else {
      console.log("createShader failure" + gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
    }
  }

  createProgram(gl, vertexShader, fragemntShader) {
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragemntShader);
    gl.linkProgram(program);
    if (gl.getProgramParameter(program, gl.LINK_STATUS)) {
      return program;
    }
    else {
      console.log("createProgram failure " + gl.getProgramInfoLog(program));
      gl.deleteProgram(program);
    }
  }
}