/*
 * PFC II - Asistbelle
 *
 * Modular DC motor controller.
 */

/*
 * This is the firmware for our modular DC motor controller intended for robotics.
 * This module controls a single DC motor equipped with a quadrature encoder.
 * It communicates via CANBUS (TWAI) and implements three controllers:
 * 1. An inner PI velocity controller for joint velocity
 * 2. An outer P + ff controller for joint trajectory tracking.
 * 3. A servo controller for a servo-equipped end effector.
 * It can switch between joint trajectory tracking mode (P + ff) and differential control mode (just joint velocity)
 */

/* --------------------- Libraries ------------------ */

#include "motor_driver.h"
#include "encoder_driver.h"
#include "pid_controller.h"
#include "twai_comms.h"


/* --------------------- Global variables ------------------ */

// Global process variable struct
SystemState global_pv = {0};

// Global setpoint struct
SystemState global_sp = {0};

// Global external loop setpoint struct
SystemState global_ext_sp = {0};

// Global control mode
uint32_t control_mode = 0;

// Global control effort
float u = 0.0F;


StatePointers ext_loop_ptrs = {
    .pv = &global_pv,
    .sp = &global_ext_sp,
    .control_mode = &control_mode,
    .u = &u
};

StatePointers int_loop_ptrs = {
    .pv = &global_pv,
    .sp = &global_sp,
    .control_mode = &control_mode,
    .u = &u
};

// Global TWAI message struct
twai_message_t* state_response = NULL;

// TWAI pointers
twai_task_pointers_t twai_task_pointers = {0};

// Encoder pointers
encoder_task_pointers_t encoder_task_ptrs = {0};

// Global pcnt unit handle
pcnt_unit_handle_t pcnt_unit_h = NULL;


void app_main(void)
{
    // Create mutexes
    pv_semaphore = xSemaphoreCreateMutex();
    sp_semaphore = xSemaphoreCreateMutex();
    ext_sp_semaphore = xSemaphoreCreateMutex();



    #ifdef NODE_HAS_GRIPPER
        // Initialize gripper
        gripper_init();
        gripper_write(0.0f);
    #endif

    // Initialize TWAI
    state_response = twai_message_init(ID_STATE_RESPONSE);
    
    
    // Pack twai pointers
    twai_task_pointers.msg_ptr = state_response;
    twai_task_pointers.state_ptrs = &ext_loop_ptrs;

    twai_driver_install(&g_config, &t_config, &f_config);
    twai_start();
    // Create task on core 1
    xTaskCreatePinnedToCore(twai_task, "TWAI", TWAI_TASK_STACK_DEPTH, (void*)&twai_task_pointers, TWAI_TASK_PRIO, NULL, 1);
    ESP_LOGI(MAIN_TASK_TAG, "TWAI Started.");

    // Initialize motor driver
    driver_init();
    // Create task on core 0
    xTaskCreatePinnedToCore(motor_driver_task, "Driver", DRIVER_TASK_STACK_DEPTH, (void*)&u, DRIVER_TASK_PRIO, NULL, 0);
    ESP_LOGI(MAIN_TASK_TAG, "Motor Driver Started.");

    // Initialize encoder
    // Pack encoder pointers
    encoder_task_ptrs.pcnt_unit_h = pcnt_unit_h;
    encoder_task_ptrs.system_state = &global_pv;

    encoder_init(&encoder_task_ptrs);

    // Create task on core 0
    xTaskCreatePinnedToCore(encoder_task, "Encoder", ENCODER_TASK_STACK_DEPTH, (void*)&encoder_task_ptrs, ENCODER_TASK_PRIO, NULL, 0);
    ESP_LOGI(MAIN_TASK_TAG, "Encoder Started.");


    // Create PID velocity controller task on core 0
    xTaskCreatePinnedToCore(pid_controller_task, "PID", PID_TASK_STACK_DEPTH, (void*)&int_loop_ptrs, PID_TASK_PRIO, NULL, 0);
    ESP_LOGI(MAIN_TASK_TAG, "PID Velocity controller started");

    ESP_LOGI(MAIN_TASK_TAG, "Starting main in 2s.");
    vTaskDelay(pdTICKS_TO_MS(2000));
    ESP_LOGI(MAIN_TASK_TAG, "Controller started in trajectory tracking mode");
    


    // Outer control loop
    
    float position_goal = 0.0F;
    float velocity_goal = 0.0F;

    float position_gain = TRAJ_CONTROLLER_GAIN;//4.5F;
    float max_vel = CONTROLLER_MAX_VELOCITY;

    float current_pos = 0.0F;


    while(true){
        if(xSemaphoreTake(pv_semaphore, 0)){
            current_pos = global_pv.position;

            xSemaphoreGive(pv_semaphore);
            if(xSemaphoreTake(ext_sp_semaphore, 0) && xSemaphoreTake(sp_semaphore, 0)){
                position_goal = global_ext_sp.position;
                velocity_goal = global_ext_sp.velocity;
                xSemaphoreGive(ext_sp_semaphore);

                float e = position_goal-current_pos;
                
                // If robot in differential control mode just call velocity controller
                global_sp.velocity = velocity_goal;

                // If robot in trajectory tracking mode implement P + ff trajectory tracking controller
                if(!control_mode) global_sp.velocity += position_gain*e;

                // Saturation
                if(global_sp.velocity > max_vel) global_sp.velocity = max_vel; 
                if(global_sp.velocity < -max_vel) global_sp.velocity = -max_vel; 
            
                xSemaphoreGive(sp_semaphore);
            }
        }else continue;

        vTaskDelay(pdTICKS_TO_MS(100));
        }
    }


   


