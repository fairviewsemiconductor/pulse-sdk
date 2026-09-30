#include "../include/pulse.h"
#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("--- C Smoke Test ---\n");
    pulseInit();
    void* ptr = NULL;
    pulseMallocGallium(&ptr, 1024);
    pulseMemcpyHtoD(ptr, NULL, 1024, NULL);
    pulseLaunchMEU(NULL, NULL, NULL);
    pulseStreamSynchronize(NULL);
    free(ptr);
    printf("C API Test Passed\n");
    return 0;
}
