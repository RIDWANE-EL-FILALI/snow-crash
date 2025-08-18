#include <stdio.h>

int main(void) {
    FILE *fp = fopen("token", "r");
    if (!fp) return 1;

    int c;
    int i = 0;
    while ((c = fgetc(fp)) != EOF) {
        putchar(c - i);
        i++;
    }
    fclose(fp);
    return 0;
}
