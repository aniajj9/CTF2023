#include <stdio.h>
#include<stdlib.h>
#include<time.h>

void print_flag(){
    FILE *fptr = fopen("/secured/flag.txt", "r");
    if (fptr == NULL)
    {
        printf("Error: Cannot open file!\n");
        exit(1);
    }
  
    // Read contents from file
    int c = fgetc(fptr);
    while (c != EOF)
    {
        printf ("%c", c);
        c = fgetc(fptr);
    }
  
    fclose(fptr);
}

int main() {
    srand((unsigned int) time(NULL));
    int num1 = ((float) rand() / (float)(RAND_MAX)) * 1000;
    int num2 = ((float) rand() / (float)(RAND_MAX)) * 1000;
    int expected = num1 + num2;

    printf("What is the result of %d + %d? ", num1, num2);
    fflush(stdout);
    
    int input;
    int result = scanf("%d", &input);

    if (result == EOF || input != expected) {
        puts("Wrong. Try again!");
        exit(1);
    }

    print_flag();
    return 0;
}