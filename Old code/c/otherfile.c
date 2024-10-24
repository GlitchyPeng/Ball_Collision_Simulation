#include <stdio.h>

void bubbleSort(int arr[], int n);

int main(){
    int size;
    printf("Enter the size of the array: ");
    scanf("%d", &size);
    
    int arr[size];
    printf("Enter the elements of the array: ");
    for(int i=0; i<size; i++){
        scanf("%d", &arr[i]);
    }
    
    bubbleSort(arr,size);
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }

    printf("\n"); 
    return 0;
}
