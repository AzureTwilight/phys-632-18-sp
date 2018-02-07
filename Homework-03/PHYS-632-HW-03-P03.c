/* ############################ */
/* ## PHYS 632 (Spring 2018) ## */
/* ## HW 03 Problem 03       ## */
/* ## Romberg Int.           ## */
/* ############################ */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define RN_SIZE 30

float targetFunc(float x){
  return pow(sin(x),2);
}

int initRn(float Rn[RN_SIZE][RN_SIZE]){
  int i,j;
  for(i=0; i<RN_SIZE; i++){
	for(j=0; j<RN_SIZE; j++){
	  Rn[i][j] = 0;
	}
  }
  return 1;
}


int main(){
  float h, a, b, Inum, err;
  float Rn[RN_SIZE][RN_SIZE], tmpf;
  float Iexact = 2 * M_PI;
  int N;
  int i, j, k;
  int SUCC_FLG = 0;
  FILE* fp;
  float eps;
  int order = 3;
  int rowMin;

  if (order == 3){
	rowMin = 3;
	eps = 1e-5;
  }else{
	rowMin = 4;
	eps = 1e-6;
  }



  a = 0.0; b = 4 * M_PI;

  /* fp = fopen("p2-ptc-data.txt", "w"); */
  printf("Exact value is %.4f\n", Iexact);

  initRn(Rn);

  // Step 1
  h = b - a;
  Rn[0][0] =  0.5 * (targetFunc(a) + targetFunc(b));
  printf("%.4f\n", Rn[0][0]);
 
  i = 1;
  while (!SUCC_FLG){
	h /= 2;

	tmpf = 0;
	for (j = 0; j < pow(2,i-1); j++){
	  tmpf += targetFunc(a + h * (2 * j + 1));
	}
	tmpf *= h;
	Rn[i][0] = tmpf + .5 * Rn[i-1][0];
	printf("%.4f", Rn[i][0]);

	for (j = 1; j<i+1; j++){
	  Rn[i][j] = Rn[i][j-1] + (Rn[i][j-1] - Rn[i-1][j-1]) / (pow(4,j) - 1.0);
	  printf("\t%.4f", Rn[i][j]);
	}

	err = fabsf(Rn[i][i] - Rn[i-1][i-1]);
	printf("\t (err = %.4e)\n", err);
	if (err < eps && i > rowMin + 1) SUCC_FLG = 1;
	i++;
  }

  if (Rn[i-1][i-1] == Rn[i-2][i-2]) printf("equal\n");
  
  return 1;
}
