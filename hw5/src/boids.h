#ifndef BOIDS_H
#define BOIDS_H

typedef struct Boid {
  int myIdx;
  float* acceleration;
  float* position;
  float* velocity;
} Boid;

typedef struct Parameters {
  int numBirds;
  int foodFlag;
  double alpha;
  double gamma1;
  double gamma2;
  double kappa;
  double rho;
  double delta;
} Parameters;

// Sets parameters as passed in from user
void setParameters(int numBirds, int foodFlag, double alpha, double gamma1, double gamma2, double kappa, double rho, double delta);
// MALLOCS Boids and their fields as well as shared boidPositions, and assigns initial values. Sets positions to random coordinates.
void initializeBoids();

// Will call RK4 to update bird velocities
void advanceBoids(float delT);

// returns base pointer to shared heap memory with WebAssembly
float* getBoidPositions();

int getDim();
void freeBoids();

#endif