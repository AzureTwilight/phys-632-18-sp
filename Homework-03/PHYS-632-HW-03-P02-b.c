/* ############################ */
/* ## PHYS 632 (Spring 2018) ## */
/* ## HW 03 Problem 02       ## */
/* ## Part b) Ext. Trap.     ## */
/* ############################ */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>


float expFloat(float x){
  return exp(-x);
}

int main(){
  float h, a, b, Inum, err;
  float Iexact = 1 - 1./M_E;
  int N, i, j;
  FILE* fp;

  a = 0.0; b = 1.0;

  fp = fopen("p2-ptb-data.txt", "w");
  fprintf(fp, "N\t&h\t&Inum\t&err\\\\\n");
  printf("Exact value is %.4f\n", Iexact);

  for (i=0;i<10;i++){ // loop for different step

  	N=pow(2,i) + 1; // number of nodes
	h = (b - a) / (N - 1);

	Inum = 0;
	Inum += (a + b) / 2;
	for (j=2; j<N;j++){
	  Inum += expFloat(a + h * (j - 1));
	}
	Inum *= h;

	err = fabsf((Inum - Iexact)/Iexact) * 100.;

  	printf("Inum for %d intervals is %.4f with relative error = %4.2f%%\n", N -1, Inum, err);
	fprintf(fp, "%d\t&%.4f\t&%.4f\t&%.4f\\\\\n", N - 1, h, Inum, err/100.);
  }
  
  fclose(fp);
	
  
}
