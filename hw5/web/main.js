// import a renderer object
import { Renderer } from "./renderer.js";
let Module; // C functions will be called through module._(a c func name)
let animationId = null;
let simulationRunning = false;

// grab webgl rendering context
const canvas = document.getElementById("gameCanvas");
const gl = canvas.getContext("webgl2");

if (!gl) {
  console.error("Ruh roh couldn't load webgl2");
}

// async needed so that javascript doesn't just mosey along and do other stuff
async function startGame() {
  Module = await createWASMModule(); // load C module
  const params = getParams();
  validateParams(params);
  Module._setParameters(
    params.numBirds,
    params.isPred ? 1: 0,
    params.foodMoves ? 1 : 0,
    params.foodFlag ? 1 : 0,
    params.foodX,
    params.foodY,
    params.alpha,
    params.gamma1,
    params.gamma2,
    params.kappa,
    params.rho,
    params.delta
  );
  Module._printParameters();

  document.getElementById("stopButton").addEventListener("click", stopGame);

  document.querySelectorAll("#controls input").forEach(input => {input.addEventListener("change", restartGame);});

  restartGame();
}

startGame();


function runGame(Module, params) {
  const numBoids = params.numBirds;
  const boidDim = Module._getDim();
  const numPositions = numBoids * boidDim;
  // Module.HEAPU8.buffer is the heap memory of WebAssembly. 
  // Module._getBoidPos returns the address we begin reading  
  // we read numPositions (bytes * sizeof(float)) = 4 bytes * numFloats
  const sharedHeapCoords = new Float32Array(Module.HEAPU8.buffer, Module._getBoidPositions(), numPositions);
  if (sharedHeapCoords == null) {
    console.log("Likely malloc failure.");
    return;
  }
  const renderer = new Renderer(canvas, boidDim);

  const delTime = 0.01; 
  let simulationTime = 0;

  function gameLoop() {
    Module._RK4(simulationTime, delTime) // step simulation
    
    // increment clock time (even though our ODE is not really time dependent, I'm including it for future implememtnations)
    simulationTime += delTime; 
    
    // render using sharedHeapCoords (this is a pointer, not a copy!)
    renderer.render(sharedHeapCoords, numBoids, boidDim, params.isPred);

    // next frame
    if (simulationRunning) {
      animationId = requestAnimationFrame(gameLoop);
    }
  }


  simulationRunning = true;
  animationId = requestAnimationFrame(gameLoop);
}


function getParams() {
  return {
    foodFlag: document.getElementById("foodFlag").checked,
    isPred: document.getElementById("isPred").checked,
    foodMoves: document.getElementById("foodMoves").checked,
    alpha: Number(document.getElementById("alpha").value),
    foodX: Number(document.getElementById("foodX").value),
    foodY: Number(document.getElementById("foodY").value),
    gamma1: Number(document.getElementById("gamma1").value),
    gamma2: Number(document.getElementById("gamma2").value),
    kappa: Number(document.getElementById("kappa").value),
    rho: Number(document.getElementById("rho").value),
    delta: Number(document.getElementById("delta").value),
    numBirds: Number(document.getElementById("numBirds").value)
  };
}

function validateParams(params) {
  if (!Number.isFinite(params.alpha) ||
    !Number.isFinite(params.gamma1) ||
    !Number.isFinite(params.gamma2) ||
    !Number.isFinite(params.kappa) ||
    !Number.isFinite(params.rho) ||
    !Number.isFinite(params.delta)) {
  throw new Error("One or more parameters are invalid.");
  }

  if (params.delta <= 0) {
    throw new Error("Delta must be positive.");
  }

  if (params.foodX < -1.0 || params.foodX > 1.0) {
    throw new Error("Coordinates of feeder must be in [-1.0, 1.0]");
  }

  if (params.foodY < -1.0 || params.foodY > 1.0) {
    throw new Error("Coordinates of feeder must be in [-1.0, 1.0]");
  }

  if (!Number.isInteger(params.numBirds) || params.numBirds < 10) {
    throw new Error("Number of birds must be an integer >= 10.");
  }
}

function stopGame() {
  if (animationId !== null) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }

  if (simulationRunning) {
    simulationRunning = false;
    //Module._stopDiagnostics();
    //downloadDiagnostics(Module);
    Module._freeBoids();
  }
}

function downloadDiagnostics(Module) {
  const contents = Module.FS.readFile("/forces.csv", {
    encoding: "utf8"
  });

  const blob = new Blob([contents], { type: "text/csv" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "forces.csv";
  link.click();

  URL.revokeObjectURL(url);
}

function restartGame() {
  // stop the old simulation if one is running
  stopGame();

  try {
    const params = getParams();
    validateParams(params);

  Module._setParameters(
    params.numBirds,
    params.isPred ? 1: 0,
    params.foodMoves ? 1 : 0,
    params.foodFlag ? 1 : 0,
    params.foodX,
    params.foodY,
    params.alpha,
    params.gamma1,
    params.gamma2,
    params.kappa,
    params.rho,
    params.delta
  );

  Module._initializeBoids();

  runGame(Module, params);

  } catch (error) {
    console.error("Could not restart simulation:", error);
  }
}