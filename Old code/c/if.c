#include <stdio.h>

int main(){
	float f;
	
	printf("Type in the number you want to examine:\n");
	scanf("%f", &f);
	if (f < 0)
	printf("%f is negative.\n", f);
	else if (f > 0)
	printf("%f is positive.\n", f);
	else
	printf("%f is still zero.\n", f);
	return 0;
}
