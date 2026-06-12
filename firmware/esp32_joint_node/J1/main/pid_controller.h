#ifndef PID_CONTROLLER
#define PID_CONTROLLER

// Base libraries
#include "base_libs.h"

// Node config
#include "node_config.h"


// PID controller
bool get_pv(SystemState* local_pv, SystemState* global_pv){
    // Transfers global process variable to task memory
    if(xSemaphoreTake(pv_semaphore, 0)){
        // Try to get pv with no delay. If blocked, return false.
        *local_pv = *global_pv;
        xSemaphoreGive(pv_semaphore);
        return true;
    }else return false;
}

bool get_sp(SystemState* local_sp, SystemState* global_sp){
    // Transfers global process variable to task memory
    if(xSemaphoreTake(sp_semaphore, 0)){
        // Try to get sp with no delay. If blocked, return false.
        *local_sp = *global_sp;
        xSemaphoreGive(sp_semaphore);
        return true;
    }else return false;
}

void pid_controller_task(void* data){
    // Joint velocity PID controller

    // Define constants with arithmetic as variables so macros aren't recalculated each time
    const float kp = CONTROLLER_GAIN_KP;
    const float ki = CONTROLLER_GAIN_KI;
    const float kd = CONTROLLER_GAIN_KD;
    const float controller_frequency = CONTROLLER_FREQUENCY;
    const float ms_per_loop = MS_PER_LOOP;

    // Get pointers to sp, pv and u
    StatePointers* ptrs = (StatePointers*)data;
    SystemState* global_pv = ptrs->pv;
    SystemState* global_sp = ptrs->sp;
    float* u = ptrs->u;

    // Locally stored setpoint
    SystemState local_sp = {};
    local_sp.position = 0.0F;
    local_sp.velocity = 0.0F;

    // Locally stored process variables
    SystemState local_pv = {};
    local_sp.position = 0.0F;
    local_sp.velocity = 0.0F;


    float e = 0.0F;
    float pe = 0.0F;
    float de = 0.0F;
    float ie = 0.0F;

    // Task timing
    TickType_t xLastWakeTime;
    xLastWakeTime = xTaskGetTickCount();

    while (true)
    {
        // Try to get pv and sp

        if(!get_pv(&local_pv, global_pv) || !get_sp(&local_sp, global_sp)) {
            // If not available, wait until next loop
            vTaskDelay(pdMS_TO_TICKS(ms_per_loop));
            continue;
        }

        // Calculate error
        e = local_sp.velocity - local_pv.velocity;
        // Calculate derivative of eror
        de = (e-pe)*((float)controller_frequency);
        // Calculate integral of error
        ie += e/((float)controller_frequency);
        // Anti-Windup by clamping
        if(ie < -CONTROLLER_INTEGRATOR_LIMIT) ie = -CONTROLLER_INTEGRATOR_LIMIT;
        if(ie > CONTROLLER_INTEGRATOR_LIMIT) ie = CONTROLLER_INTEGRATOR_LIMIT;
        

        // Calculate control effort
        float u_unsat = kp*e + ki*ie + kd*de;

        // Saturate
        if(u_unsat > 100.0F){
            *u = 100.0F;
        }else if(u_unsat < -100.0F){
            *u = -100.0F;
        }else{ 
            *u = u_unsat;
        }

        // Fixed time task
        vTaskDelayUntil(&xLastWakeTime,pdMS_TO_TICKS(ms_per_loop));

    }
    
}



#endif //PID_CONTROLLER