#include <stdio.h>
#include <math.h>
#define ZERO 10e-5

int main(){
	float f1, f2;

	printf("Type in the two numbers you want to examine:\n");
	scanf("%f %f", &f1, &f2);
	
	float delta = fabsf(f1 - f2);	
	
	if (delta <= ZERO)
		printf("%f and %f are equal.\n", f1, f2);
	else
		printf("%f and %f are not equal.\n", f1, f2);
	return 0;
}
