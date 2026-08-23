#ifndef PULSE_H
#define PULSE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct pulseDevice_t pulseDevice_t;
typedef struct pulseStream_t pulseStream_t;
typedef struct pulseMemoryPool_t pulseMemoryPool_t;

int pulseInit(void);
int pulseMallocGallium(void** devPtr, size_t size);
int pulseMemcpyHtoD(void* dst, const void* src, size_t size, pulseStream_t* stream);
int pulseLaunchMEU(pulseStream_t* stream, void* func, void** args);
int pulseStreamSynchronize(pulseStream_t* stream);

#ifdef __cplusplus
}
#endif

#endif // PULSE_H
