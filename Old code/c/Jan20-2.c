#include <stdio.h>

int sigma(int *p, int size){
    int sum = 0;
    int i;
    for(i=0;i<size;i++){
        sum = sum + *p++;
    }
    return sum;
}

int main(){
    int size;
    printf("Enter the size of the array: ");
    scanf("%d", &size);
    
    int arr[size];
    printf("Enter the elements of the array: ");
    for(int i=0; i<size; i++){
        scanf("%d", &arr[i]);
    }
    
    int *q;
    q = arr;
    printf("The result is: %d\n", sigma(q, size));
    return 0;
}
