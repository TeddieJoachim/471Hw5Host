#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <float.h>
#include "vector.h"
#include "boids.h"


// ONLY INCLUDE THIS HEADER IF COMPILED WITH EMCC
#ifdef __EMSCRIPTEN__
#include <emscripten/emscripten.h>
#else
#define EMSCRIPTEN_KEEPALIVE
#endif

// Necessary preprocessor directives for steering away from boundaries and staying within webgl clipping plane
#define NUM_DIM 2
#define WORLD_MIN -1.0f // thresholds for detecting collision with boundary, based on webgl vals [-1,1]
#define WORLD_MAX 1.0f
#define BOUNDARY_PROXIMITY_THRESHOLD 0.5f
#define BOUNDARY_WEIGHT 2.0f // gently steer us away from boundaries

#define INITIAL_VELOCITY 0.3f // start in a random val on range [-IV, IV]


Parameters params;

EMSCRIPTEN_KEEPALIVE
void setParameters(int numBirds, int foodFlag, float foodX, float foodY, double alpha, double gamma1, double gamma2, double kappa, double rho, double delta) 
{
  params.numBirds = numBirds;
  params.foodFlag = foodFlag;
  params.alpha = alpha;
  params.gamma1 = gamma1; // leader food desire
  params.gamma2 = gamma2; // leader charisma
  params.kappa = kappa; // cohesion weight
  params.rho = rho; // repulsion weight
  params.delta = delta; // numerical tolerance (avoid division by 0)
  params.foodX = foodX;
  params.foodY = foodY;
}

Boid* themBoids = NULL; // totally safe, production level code. the array of Boid structs
float* boidSharedPositions = NULL; // shared heap memory between WebGl and this program

// rand() returns a "random" float from 0 to some big fuckin number. if we want to clamp it between 
// min and max we need to do some arithmetic
float randomInRange(float min, float max) 
{
  float intervalSize = max - min;
  float normalized = (float)rand() / (float)RAND_MAX; // [0.0, 1.0]
  float scaled = normalized * intervalSize; // [0.0, max-min (20)]

  return scaled + min; // shift so that 0.0 -> min (-10)
}

// MALLOCS Boids and their fields as well as shared boidPositions, and assigns initial values to random coordinates.
EMSCRIPTEN_KEEPALIVE
void initializeBoids()
{
  int bI = 0;

  srand((unsigned int)time(NULL)); // seeds rand, have to cast the current time (time(NULL)) to unsigned int
  themBoids = malloc(params.numBirds * sizeof(Boid));
  boidSharedPositions = malloc(params.numBirds * NUM_DIM * sizeof(float));
  
  if (themBoids == NULL || boidSharedPositions == NULL) 
  {
    if (themBoids) free(themBoids);
    if (boidSharedPositions) free(boidSharedPositions);
    return;
  }

  while (bI < params.numBirds)
  {
    themBoids[bI].myIdx = bI;
    themBoids[bI].position = malloc(NUM_DIM * sizeof(float));
    themBoids[bI].velocity = malloc(NUM_DIM * sizeof(float));
    themBoids[bI].acceleration = malloc(NUM_DIM * sizeof(float));

    if (themBoids[bI].position == NULL || themBoids[bI].velocity == NULL || themBoids[bI].acceleration == NULL) 
    {
      if (themBoids[bI].position) free(themBoids[bI].position);
      if (themBoids[bI].velocity) free(themBoids[bI].velocity);
      if (themBoids[bI].acceleration) free(themBoids[bI].acceleration);
      return;
    }
    // for each x,y,z in the case of 3dim boids, set the initial values of position and velocity
    for (int idx = 0; idx < NUM_DIM; idx++)
    {
      themBoids[bI].position[idx] = randomInRange(WORLD_MIN, WORLD_MAX);
      themBoids[bI].velocity[idx] = randomInRange(-INITIAL_VELOCITY, INITIAL_VELOCITY);
      themBoids[bI].acceleration[idx] = 0;
      // for this boid, write its position values to the shared heap memory as they are initialized
      boidSharedPositions[(bI * NUM_DIM) + idx] = themBoids[bI].position[idx];
    }

    bI++;
  }
}


// decrements acceleration in direction of walls when applicable
void avoidBoundaries(Boid* thisBoid)
{
  float distToMax, distToMin;
  for (int coordIdx = 0; coordIdx < NUM_DIM; coordIdx++)
  {
    distToMax = WORLD_MAX - thisBoid->position[coordIdx];
    distToMin = thisBoid->position[coordIdx] - WORLD_MIN;

    // if we are within a threshold (about to hit wall) decelerate in that direction proportionally to how close we are
    // so the larger distToMax is, the smaller the steering force. (THRESHOLD - distToMax) = how far we are into the threshold
    // we then divide how far we've encroached by the threshold to get a value between 0 and 1 
    // (if we are 0.5 into the boundary, we get 1.0, if 0.25 we get 0.5, makes it easy to tune with boundary weight)
    if (distToMax < BOUNDARY_PROXIMITY_THRESHOLD)
    {
      thisBoid->acceleration[coordIdx] -= BOUNDARY_WEIGHT * (BOUNDARY_PROXIMITY_THRESHOLD - distToMax) / BOUNDARY_PROXIMITY_THRESHOLD;
    }
    else if (distToMin < BOUNDARY_PROXIMITY_THRESHOLD)
    {
      thisBoid->acceleration[coordIdx] += BOUNDARY_WEIGHT * (BOUNDARY_PROXIMITY_THRESHOLD - distToMin) / BOUNDARY_PROXIMITY_THRESHOLD;
    }
  }
}

// Don't let birds leave boundaries. If hit, set to boundary and ensure they aren't travelling out by zeroing that coordIdx
void clampAtBoundaries(Boid* thisBoid, int coordIdx)
{
  if (thisBoid->position[coordIdx] > WORLD_MAX)
  {
    thisBoid->position[coordIdx] = WORLD_MAX;
    if (thisBoid->velocity[coordIdx] > 0.0f) 
    {
      thisBoid->velocity[coordIdx] = 0.0f;
    }
  }
  else if (thisBoid->position[coordIdx] < WORLD_MIN)
  {
    thisBoid->position[coordIdx] = WORLD_MIN;

    if (thisBoid->velocity[coordIdx] < 0.0f) 
    {
      thisBoid->velocity[coordIdx] = 0.0f;
    }
  }
}


// These functions are the forcing terms defined in problem assignment. 
// My current idea is to calculate these on a bird to bird basis, so rather than a 
// massive N x 2 matrix, these calculate each birds entry in that matrix.
void foodForce(float* targetVec, const float* leaderPos) 
{
  float foodX = params.foodX;
  float foodY = params.foodY;
  float foodPos[NUM_DIM] = {foodX, foodY};
  vectorSubtract(targetVec, &foodPos[0], leaderPos, NUM_DIM);
  vectorScalar(targetVec, params.gamma1, NUM_DIM);
}

void leaderForce(float* targetVec, const float* leaderPos, const float* myPos)
{
  vectorSubtract(targetVec, leaderPos, myPos, NUM_DIM);
  vectorScalar(targetVec, params.gamma2, NUM_DIM);
}

void cohesionForce(float* targetVec, const float* myPos, const float* avgPos)
{
  vectorSubtract(targetVec, avgPos, myPos, NUM_DIM);
  vectorScalar(targetVec, params.kappa, NUM_DIM);
}

void repulsionForces(float repulsionVecs[5][NUM_DIM], const float* myPos, const float neighbors[5][NUM_DIM])
{
  float numerator, denominator;

  for (int nI = 0; nI < 5; nI++) 
  {
    for (int cI = 0; cI < NUM_DIM; cI++)
    {
      numerator = params.rho * (myPos[cI] - neighbors[nI][cI]);
      denominator = ((myPos[cI] - neighbors[nI][cI]) * (myPos[cI] - neighbors[nI][cI])) + params.delta;
      repulsionVecs[nI][cI] = numerator / denominator;
    }
  }
}
// End forcing terms


void getNeighbors(Boid* me, float neighbors[5][NUM_DIM])
{
  float distances[params.numBirds];
  float minDistances[5] = {FLT_MAX, FLT_MAX, FLT_MAX, FLT_MAX, FLT_MAX};
  float differenceInPos[NUM_DIM];

  // get distance to every bird
  for (int bI = 0; bI < params.numBirds; bI++)
  {
    if (themBoids[bI].myIdx != me->myIdx) 
    {
      vectorSubtract(differenceInPos, me->position, themBoids[bI].position, NUM_DIM);
      distances[bI] = vecMagnitude(differenceInPos, NUM_DIM);
    }
    else distances[bI] = 0;
  }
  // now select the 5 smallest distances (excluding yourself) as neighbors
  // for every distance, check if any of our 5 neighbors can be replaced
  for (int dI = 0; dI < params.numBirds; dI++) // for every bird/distance
  {
    if (dI == me->myIdx) continue; // skip yourself
    for (int nI = 0; nI < 5; nI++) // for every neighbor
    {
      if (distances[dI] < minDistances[nI]) // if distance to this bird is less than a previous min
      {
        // we should shift our minDistances to make room for the new min
        // have a new incoming min -> copy the last distance into the second to last,
        // then set last neighbor to be second to last neighbor, and repeat.
        // when you perform the shift in minDistances, update the neighbors as well
        // eg minDist = {2, 4, 6, 8, 10}
        // new min = 1, say nI = 0 -> 
        // {2, 4, 6, 8, 8} -> {2, 4, 6, 6, 8} -> {2, 4, 4, 6, 8} -> {2, 2, 4, 6, 8} -> {1, 2, 4, 6, 8}
        for (int shift = 4; shift > nI; shift--) 
        {
          minDistances[shift] = minDistances[shift-1];
          for (int cI = 0; cI < NUM_DIM; cI++)
          {
            neighbors[shift][cI] = neighbors[shift - 1][cI];
          }
        }
        minDistances[nI] = distances[dI];
        for (int cI = 0; cI < NUM_DIM; cI++) // write this birds coordinates into this neighbors
        {
          neighbors[nI][cI] = themBoids[dI].position[cI];
        }
        break; // found a new neighbor
      }
    }
  }

}

void getFlockAvg(float* flockAverage)
{
  zeroVec(flockAverage, NUM_DIM);
  
  for (int bI = 0; bI < params.numBirds; bI++)
  {
    vectorAdd(flockAverage, themBoids[bI].position, flockAverage, NUM_DIM);
  }
  vectorScalar(flockAverage, 1.0/params.numBirds, NUM_DIM);
}

void applyForcing()
{
  float getFood[NUM_DIM];
  float followLead[NUM_DIM];
  float cohesion[NUM_DIM];
  float repulsion[5][NUM_DIM];
  float neighborPositions[5][NUM_DIM];
  float flockAverage[NUM_DIM];
  Boid* currBird; 
  Boid* leaderBird;

  leaderBird = &themBoids[0];
  getFlockAvg(flockAverage);
  for (int bI = 0; bI < params.numBirds; bI++)
  {
    currBird = &themBoids[bI];
    getNeighbors(currBird, neighborPositions);
    if (currBird->myIdx == 0 && params.foodFlag) // I am leader and food flag is high
    {
      // vector steering us towards food written into getFood
      foodForce(getFood, leaderBird->position);
    }
    else // I am not the leader 
    {
      // vectors steering us in the forcing directions
      leaderForce(followLead, leaderBird->position, currBird->position);
      cohesionForce(cohesion, currBird->position, flockAverage);
      repulsionForces(repulsion, currBird->position, neighborPositions);
    }
    
  }
}

// What WebGl context calls, updates our simulation internally using RK4, then updates shared memory
EMSCRIPTEN_KEEPALIVE
void RK4(float t, float delT)
{
  // in our case, B' = F -> bird velocities (position') = forcing terms
  // B(t0) = random initial positions 
  // t_0 assumed to be 0 -> t_i = h*i
  // so our RK4 will calculate from i = 0 to n-1 (passed as arguments)

  
  
}








/* Functions that will never change that WebGl context needs exposed. */
EMSCRIPTEN_KEEPALIVE
float* getBoidPositions()
{
  return &boidSharedPositions[0];
}

EMSCRIPTEN_KEEPALIVE
int getDim()
{
  return NUM_DIM;
}

EMSCRIPTEN_KEEPALIVE
void freeBoids()
{
  int idx = 0;

  while (idx < params.numBirds) // dont free when killed, translate to ground?
  {
    free(themBoids[idx].position);
    free(themBoids[idx].velocity);
    free(themBoids[idx].acceleration);
    idx++;
  }
  
  free(themBoids);
  free(boidSharedPositions);
}
