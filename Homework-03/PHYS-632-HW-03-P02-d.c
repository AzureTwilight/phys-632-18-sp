/* ############################ */
/* ## PHYS 632 (Spring 2018) ## */
/* ## HW 03 Problem 02       ## */
/* ## Part d) Hit/Miss MC    ## */
/* ############################ */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

float expFloat(float x){
  return exp(-x);
}

float uniRand(){
  return (float) rand() / (float) RAND_MAX;
}

int main(){

  float h, a, b, Inum, err, totArea;
  float Iexact = 1 - 1./M_E;
  float x,y;
  int n, i, j, nSucc;
  int nList[10] = {10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000};

  int seed = time(NULL);
  srand(seed);

  FILE* fp = fopen("p2-ptd-data.txt", "w");
  fprintf(fp, "N\t& h\t& Inum\t& err \\\n");


  a = 0.0; b = 1.0;
  totArea = (b - a) * 1;
  
  for (i = 0; i < 10; i++){
	n = nList[i];
	nSucc = 0;
	for (j = 0; j < n; j++){
	  x = a + (b - a) * (uniRand());
	  y = uniRand();

	  if (y < expFloat(x)){
		nSucc++;
	  }

	  Inum = totArea * nSucc / (float) n;
	  
	}
	err = fabsf((Inum - Iexact)/Iexact) * 100.;
	printf("Inum for n = %d is %.4f with relative error = %4.2f%%\n", n, Inum, err);
	fprintf(fp, "%d\t& %.4f\t& %.4f\\\\\n", n, Inum, err);
  }

  fclose(fp);
  return 0;
}
