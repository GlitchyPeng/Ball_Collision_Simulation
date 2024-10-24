#include <stdio.h>

int main(){
	char a1;
	short a2;
	int a3;
	long a4;
	float a5;
	double a6;
	long double a7;
	unsigned int a8;
	printf("The size of char is %lu bytes.\n", sizeof(a1));
	printf("The size of short is %lu bytes.\n", sizeof(a2));
	printf("The size of int is %lu bytes.\n", sizeof(a3));
	printf("The size of long is %lu bytes.\n", sizeof(a4));
	printf("The size of float is %lu bytes.\n", sizeof(a5));
	printf("The size of double is %lu bytes.\n", sizeof(a6));
	printf("The size of long double is %lu bytes.\n", sizeof(a7));
	printf("The size of unsigned int is %lu bytes.\n", sizeof(a8));
	return 0;
}
