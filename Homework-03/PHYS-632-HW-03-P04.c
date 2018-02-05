/* ############################ */
/* ## PHYS 632 (Spring 2018) ## */
/* ## HW 03 Problem 04       ## */
/* ## Sample Mean MC         ## */
/* ############################ */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

float uniRand(){
  return (float) rand() / (float) RAND_MAX;
}

int main(){

  FILE* fp;
  float h, a, b, Inum,f, err, totArea;
  int n, i, j,k, nSucc;
  float Iexact = 155 / 6.0;

  int seed = time(NULL);
  srand(seed);

  fp = fopen("p04-data.txt", "w");

  for (i = 1; i < 18; i++){
	n = pow(2,i);
	Inum = 0;

	for (j = 0; j < n; j++){
	  f = 0;
	  for (k = 0; k < 10; k++) f += uniRand();
	  Inum += pow(f,2);
	}

	Inum /= n;
	err = fabsf(Inum - Iexact);
	printf("Inum for n = %d is %.4f with absolute error = %.4f\n", n, Inum, err);
	fprintf(fp,"%d\t%.6f\n", n, err);
  }

  fclose(fp);
  return 1;
}
