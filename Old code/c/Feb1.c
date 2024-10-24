#include <stdio.h>

void selectionSort(int arr[], int n){
    for (int i = 0; i < n-1; i++){
        int min_index = i;
        for (int j = i+1; j < n; j++){
            if (arr[j] < arr[min_index]) {
                min_index = j;  // Update the index of the smallest element found
            }
        }
        // Swap the found minimum element with the element at index i
        int temp = arr[i];
        arr[i] = arr[min_index];
        arr[min_index] = temp;
    }
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
    
    selectionSort(arr,size);
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }

    printf("\n"); 
    return 0;
}
