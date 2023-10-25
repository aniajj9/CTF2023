#include <stdio.h>
int main(){
    char buf[5];
    char f;
    setbuf(stdout, 0);
    printf("Visit at the doctor\n");
    printf("Open your mouth and say......");
    gets(buf);

    if(f=='A'){
        system("cat ./flag");
    }
}