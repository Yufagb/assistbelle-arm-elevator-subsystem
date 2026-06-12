#ifndef BASE_LIBS_H
#define BASE_LIBS_H

// Base libraries and types used by node

//  ----------------------------------------------------- C STD libraries -----------------------------------------------------
#include <math.h>

//  ----------------------------------------------------- Logging and error check -----------------------------------------------------
#include "esp_err.h"
#include "esp_log.h"

// ESP SDK Config
#include "sdkconfig.h"

//  ----------------------------------------------------- GPIO -----------------------------------------------------
#include "driver/gpio.h"


//  ----------------------------------------------------- FREERTOS -----------------------------------------------------
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"

// Semaphores
SemaphoreHandle_t pv_semaphore = NULL;
SemaphoreHandle_t sp_semaphore = NULL;
SemaphoreHandle_t ext_sp_semaphore = NULL;

// Global structs

typedef struct{
    float position;
    float velocity;
} SystemState;

// Data transfer struct


 typedef struct{
    SystemState* pv;
    SystemState* sp;
    uint32_t* control_mode;
    float* u;
 } StatePointers;



#endif //BASE_LIBS_H