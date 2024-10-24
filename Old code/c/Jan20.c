#include <stdio.h>

int arr1[10] = {1,2,3,4,5,6,7,8,9,10};
int arr2[10] = {2,3,4,5,6,7,8,9,10,11};

int sigma(int *p){
	int i;
	int sum = 0;
	for(i=0;i<10;i++){
		sum = sum + *p++;
	}
	return sum;
}

int main(){
	int *q;
	q = arr1;
	printf("Result1 is: %d\n", sigma(q));
	q = arr2;
	printf("Result2 is: %d\n", sigma(q));
	return 0;
}
