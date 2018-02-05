/* ############################ */
/* ## PHYS 632 (Spring 2018) ## */
/* ## HW 03 Problem 02       ## */
/* ## Part c) Romberg Int.   ## */
/* ############################ */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define ROW 9

float expFloat(float x){
  return exp(-x);
}

int initRn(float Rn[ROW][ROW]){
  int i,j;
  for(i=0; i<ROW; i++){
	for(j=0; j<ROW; j++){
	  Rn[i][j] = 0;
	}
  }
  return 1;
}


int main(){
  float h, a, b, Inum, err;
  float Rn[ROW][ROW], tmpf;
  float Iexact = 1 - 1./M_E;
  int N;
  int i, j, k;
  FILE* fp;

  a = 0.0; b = 1.0;

  /* fp = fopen("p2-ptc-data.txt", "w"); */
  printf("Exact value is %.4f\n", Iexact);

  initRn(Rn);

  // Step 1
   h = b - a;
  Rn[0][0] =  0.5 * (expFloat(a) + expFloat(b));
  printf("%.4f\n", Rn[0][0]);
 
  for (i=1;i<ROW;i++){ // loop for different step
	h /= 2;

	tmpf = 0;
	for (j = 0; j < pow(2,i-1); j++){
	  tmpf += expFloat(a + h * (2 * j + 1));
	}
	tmpf *= h;
	Rn[i][0] = tmpf + .5 * Rn[i-1][0];
	printf("%.4f", Rn[i][0]);

	for (j = 1; j<i+1; j++){
	  Rn[i][j] = Rn[i][j-1] + (Rn[i][j-1] - Rn[i-1][j-1]) / (pow(4,j) - 1.0);
	  printf("\t%.4f", Rn[i][j]);
	}
	printf("\n");
  }
  
}
