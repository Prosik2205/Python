#include "stdafx.h"

#define ENVTYPE 0
#define NACTIONS 3
#define NSTATES 2

#define NSTEPS 200
#define NREPLICAS 1000

#define REWARD 1//+1
#define PENALTY 0//-1

// ----------------------------------------------------------------------------
// global parameters and values

int t; // current time step
int T = NSTEPS; // number of time steps = number of interactions between agent and
environment
int n = NREPLICAS; // number of replicas
int nA = NACTIONS; // number of actions
int nS = NSTATES; // number of states

// ----------------------------------------------------------------------------
// environment

int env = ENVTYPE; // type of environment:

// env = 0 -> se (stationary environment)
// env = 1 -> ce (commutative environment)

float sePa[NACTIONS]; // se: probabilities of rewards for each action

int ceState; // ce: current state of commutative environment
float cePa[NSTATES][NACTIONS]; // ce: probabilities of reward for each action
for each state of environment
float cePs[NSTATES][NSTATES]; // ce: probabilities of transition from one state to
another
// ----------------------------------------------------------------------------
// agent
int agt; // type of agent:
// agt = 0 -> random agent
// agt = 1 -> perfect agent
int action=0; // current action = {0, ... ,(nA-1)}
int response; // current response of environment = {-1;+1}
int paction; // action of perfect agent
// ----------------------------------------------------------------------------
// results for current replica
float sumR; // total reward over time sumR(t)
float avrR; // average reward over time avrR(t) = sumR(t)/t
// ----------------------------------------------------------------------------
// tabulated results
float _sumR[NSTEPS][NREPLICAS];
float _avrR[NSTEPS][NREPLICAS];
// ----------------------------------------------------------------------------
// final simulation results
float sumRm[NSTEPS]; // mean values of sumR(t)
float sumRv[NSTEPS]; // corresponding variances
float avrRm[NSTEPS]; // mean values of avrR(t)
float avrRv[NSTEPS]; // corresponding variances
// ----------------------------------------------------------------------------
// files for parameters and results
char * par_file_name = "d:\\temp2\\lab1.parameters.dat";
FILE * par_file;
char * RA_res_file_name = "d:\\temp2\\lab1.RA.results.dat";
FILE * RA_res_file;
char * PA_res_file_name = "d:\\temp2\\lab1.PA.results.dat";
FILE * PA_res_file;
// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------
// uniform discrete probability distribution
int uRand (int x)
{
int _rnum = (int) ((float)x * (float)rand() / (float)RAND_MAX);
return _rnum;
}
// ----------------------------------------------------------------------------
// discrete probability distribution specified by probabilities from <_array>
int dRand (float* _array, int size)
{
int _rnum = size-1;
float _left = 0;

float _right = _array[0];
float ftmp = (float)rand() / (float)RAND_MAX;
for (int i=0; i < size-1; i++)
{
if ((ftmp >= _left) && (ftmp < _right)) {_rnum = i; break;}
_left = _right;
_right += _array[i+1];
}
return _rnum;
}
// ----------------------------------------------------------------------------
// initialization of stationary environment
void seInit (void)
{
for (int i=0; i < nA; i++)
sePa[i] = (float)rand() / (float)RAND_MAX;
//sePa[0] = 0.8f; sePa[1] = 0.2f;
}
// ----------------------------------------------------------------------------
// response of stationary environment
int seResponse (void)
{
int _r;
float rnum = (float)rand() / (float)RAND_MAX;
if (rnum < sePa[action]) _r = REWARD;
else _r = PENALTY;
return _r;
}
// ----------------------------------------------------------------------------
// initialization of commutative environment
void ceInit (void)
{
int i,j;
float _sum1, _sum2;
// probabilities of rewards
for (i=0; i < nS; i++)
for (j=0; j < nA; j++)
cePa[i][j] = (float)rand() / (float)RAND_MAX;
// probabilities of state transition
for (i=0; i < nS; i++)
{
_sum1 = 0;
_sum2 = 0;
for (j=0; j < nS; j++)
{
cePs[i][j] = (float)rand() / (float)RAND_MAX;
_sum1 += cePs[i][j];
}
for (j=0; j < nS-1; j++)
{
cePs[i][j] = cePs[i][j] / _sum1;

_sum2 += cePs[i][j];
}
cePs[i][nS-1] = 1.0f - _sum2;
}
// initial state
ceState = uRand(nS);
}
// ----------------------------------------------------------------------------
// response of commutative environment
int ceResponse (void)
{
int _r;
// get response in current state
float rnum = (float)rand() / (float)RAND_MAX;
if (rnum < cePa[ceState][action]) _r = REWARD;
else _r = PENALTY;
// commutate states
ceState = dRand(cePs[ceState],nS);
return _r;
}
// ----------------------------------------------------------------------------
// environment
int environment (int _en)
{
int _r = 0;
switch (_en)
{
case 0: _r = seResponse(); break;
case 1: _r = ceResponse(); break;
default: printf("lab1 error: wrong env code specified\n");
}
return _r;
}
// ----------------------------------------------------------------------------
// save parameters in file
void saveParameters (void)
{
int i,j;
if ((par_file = fopen(par_file_name,"w")) == NULL) {
fprintf(stderr, "Cannot open file <%s> for parameters of experiment.\
n", par_file_name);
}
fprintf(par_file,"T = %d\n", T);
fprintf(par_file,"n = %d\n", n);
fprintf(par_file,"env = %d\n", env);
fprintf(par_file,"nA = %d\n", nA);
if (env) fprintf(par_file,"nS = %d\n", nS);

fprintf(par_file,"====================\n");
switch (env)
{
case 0: // se (stationary environment)
for (i=0; i < nA; i++)
fprintf(par_file,"p(a%d) = %f\n", i, sePa[i]);
break;
case 1: // ce (commutative environment)
// probabilities of rewards
for (i=0; i < nS; i++)
{
for (j=0; j < nA; j++)
fprintf(par_file,"p(s%d,a%d) = %f\n", i, j, cePa[i]
[j]);
if (i < nS-1) fprintf(par_file,"--------------------\n");
}
fprintf(par_file,"\n====================\n");
// probabilities of state transition
for (i=0; i < nS; i++)
{
for (j=0; j < nS; j++)
fprintf(par_file,"p(s%d,s%d) = %f\n", i, j, cePs[i]
[j]);
fprintf(par_file,"--------------------\n");
}
break;
default: printf("lab1 error: wrong env model code specified\n");
}
fclose(par_file);
}
// ----------------------------------------------------------------------------
// save results of random agent
void saveResultsRA (void)
{
int i;
if ((RA_res_file = fopen(RA_res_file_name,"w")) == NULL)
fprintf(stderr, "Cannot open file <%s> for experimental results.\n",
RA_res_file_name);
for (i=0; i < T; i++)
fprintf(RA_res_file,"%f,%f\n", avrRm[i], avrRv[i]);
fclose(RA_res_file);
}
// ----------------------------------------------------------------------------
// save results of perfect agent

void saveResultsPA (void)
{
int i;
if ((PA_res_file = fopen(PA_res_file_name,"w")) == NULL)
fprintf(stderr, "Cannot open file <%s> for experimental results.\n",
PA_res_file_name);
for (i=0; i < T; i++)
fprintf(PA_res_file,"%f,%f\n", avrRm[i], avrRv[i]);
fclose(PA_res_file);
}
// ----------------------------------------------------------------------------
// return index of maximal value in <_array>
int argmax(float* _array, int size)
{
int _arg = uRand(size);
float _max = _array[_arg];
for (int i=0; i < size; i++)
if (_array[i] > _max) {_max = _array[i]; _arg = i;}
return _arg;
}
// ----------------------------------------------------------------------------
// init agent
void initAgent (int _ag)
{
switch (_ag)
{
case 0: break;
case 1: break;
default: printf("lab1 error: wrong agent code specified\n");
}
}
// ----------------------------------------------------------------------------
// random agent
int randomAgent (void)
{
return uRand(nA);
}
// ----------------------------------------------------------------------------
// perfect agent
int perfectAgent (void)
{
if (env) paction = argmax(cePa[ceState],nA);
else paction = argmax(sePa,nA);
return paction;
}
// ----------------------------------------------------------------------------
// agent

int agent (int _ag)
{
int _a = 0;
switch (_ag)
{
case 0: _a = randomAgent(); break;
case 1: _a = perfectAgent(); break;
default: printf("lab1 error: wrong agent code specified\n");
}
return _a;
}
// ----------------------------------------------------------------------------
// simulation
void simulation (int _i)
{
initAgent(agt);
sumR = 0.0f;
avrR = 0.0f;
for (t=0; t < T; t++) {
// get action of agent
action = agent(agt);
// get response of environment
response = environment(env);
// calculate cumulative results
sumR = sumR + (float)response;
avrR = sumR / ((float)t + 1);
// save results
_sumR[t][_i] = sumR;
_avrR[t][_i] = avrR;
}
}
// ----------------------------------------------------------------------------
// get mean values of simulation results
void getMeanValues (void)
{
for (t=0; t < T; t++)
{
float tmps1 = 0.0f;
float tmps2 = 0.0f;
for (int i=0; i < n; i++)
{
tmps1 += _sumR[t][i];
tmps2 += _avrR[t][i];
}
sumRm[t] = (float)tmps1 / (float)n;
avrRm[t] = (float)tmps2 / (float)n;
}
}
// ----------------------------------------------------------------------------

// get variances of simulation results
void getVarianceValues (void)
{
for (t=0; t < T; t++)
{
float tmps1 = 0.0f;
float tmps2 = 0.0f;
for (int i=0; i < n; i++)
{
tmps1 += (sumRm[t] - _sumR[t][i]) * (sumRm[t] - _sumR[t][i]);
tmps2 += (avrRm[t] - _avrR[t][i]) * (avrRm[t] - _avrR[t][i]);
}
sumRv[t] = (float)tmps1 / (float)(n-1);
avrRv[t] = (float)tmps2 / (float)(n-1);
//sumRv[t] = (float)tmps1 / (float)n;
//avrRv[t] = (float)tmps2 / (float)n;
}
}
// ----------------------------------------------------------------------------
// main
int main(int argc, char* argv[])
{
int i;
// init random-number generator
srand((unsigned)time(NULL));
// init environment
if (env == 0) seInit();
else ceInit();
// save parameters of experiment
saveParameters();
// run experiment for random agent
agt = 0;
for (i=0; i < n; i++) simulation(i);
getMeanValues();
getVarianceValues();
saveResultsRA();
// run experiment for perfect agent
agt = 1;
for (i=0; i < n; i++) simulation(i);
getMeanValues();
getVarianceValues();
saveResultsPA();
return 0;
}