#ifndef MOTOR_DRIVER_H
#define MOTOR_DRIVER_H

// Driver for DRV8871 H-bridge.

// Base libraries
#include "base_libs.h"

// Node config
#include "node_config.h"


// MCPWM driver
#include "driver/mcpwm.h"


#ifdef ILIM_CONNECTED
// If ILIM resistor is connected, set DAC to output a fixed voltage to set current limit

    // DAC libraries
    #include "driver/dac_oneshot.h"
    
    // Full scale current limit. Max. 3.6
    #define I_FS 3.5F

    
    // Driver constants
    #define VRREF 1.232F //V
    #define VILIM 64.0F //V
    #define ARREF VILIM
    #define RREF ILIM_RESISTOR

    // I FS = ARREF * (VRREF - VDAC)/(VRREF * RREF)
    #define VDAC (-(I_FS*VRREF*RREF - ARREF*VRREF)/ARREF)

    // DAC handle
    #define DAC_CHANNEL DAC_CHAN_0
    dac_oneshot_handle_t dac = NULL;

    // DAC setup function
    esp_err_t setup_dac(dac_oneshot_handle_t* dac){
        esp_err_t error = ESP_OK;
        dac_oneshot_config_t config = {};
        config.chan_id = DAC_CHANNEL;
        error = dac_oneshot_new_channel(&config, dac);
        if(error != ESP_OK) return error;
        error = dac_oneshot_output_voltage(*dac, ((uint8_t)(VDAC)) );
        return error;
    }

#endif


// Motor direction struct
typedef enum {
    DIR_FORWARD = 0,
    DIR_BACKWARD,
    DIR_BRAKE,
    DIR_COAST
} motor_dir_t;


// MCPWM config
    #define PWM_FREQ_HZ        20000   // 20 kHz PWM
    #define MCPWM_UNIT_USED    MCPWM_UNIT_0
    #define MCPWM_TIMER_USED   MCPWM_TIMER_0
    #define MCPWM_OP_A         MCPWM0A
    #define MCPWM_OP_B         MCPWM0B


// ===== Initialize driver =====
esp_err_t driver_init(void)
{   esp_err_t error = ESP_OK;

    
    // Initialize MCPWM GPIOs
    error = mcpwm_gpio_init(MCPWM_UNIT_USED, MCPWM0A, DRV_IN1);
    error = mcpwm_gpio_init(MCPWM_UNIT_USED, MCPWM0B, DRV_IN2);
    if(error != ESP_OK) return error;

    // Configure MCPWM
    mcpwm_config_t pwm_config = {
        .frequency = PWM_FREQ_HZ,       // frequency
        .cmpr_a = 0.0,                  // duty cycle of operator A
        .cmpr_b = 0.0,                  // duty cycle of operator B
        .duty_mode = MCPWM_DUTY_MODE_0, // active high
        .counter_mode = MCPWM_UP_COUNTER, // up counter
    };

    error = mcpwm_init(MCPWM_UNIT_USED, MCPWM_TIMER_USED, &pwm_config);

    // Brake motor at first
    mcpwm_set_signal_high(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_A);
    mcpwm_set_signal_high(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_B);

    // If ILIM connected, setup DAC and output fixed voltage
    #ifdef ILIM_CONNECTED
        if(error != ESP_OK) return error;
        error = setup_dac(&dac);
    #endif

    return error;
}


void driver_write(float normalized_effort)
{
    // Writes to driver via MCPWM peripheral
    
    // Direction
    motor_dir_t dir;
    if(normalized_effort > 0) {
        dir = DIR_FORWARD;
    }else if(normalized_effort < 0){
        dir = DIR_BACKWARD;
    }else{
            // Brake for direct position control
            dir = DIR_BRAKE;     

            // Coast for velocity control
            //dir = DIR_COAST;
        }

    // Saturation
    if (normalized_effort < -100.0F) normalized_effort = -100.0F;
    if (normalized_effort > 100.0F) normalized_effort = 100.0F;
    
    switch (dir) {
        case DIR_FORWARD:
            // A = PWM, B = Low
            mcpwm_set_signal_low(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_B); 
            mcpwm_set_duty(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_A, fabsf(normalized_effort));
            mcpwm_set_duty_type(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_A, MCPWM_DUTY_MODE_0);
            break;

        case DIR_BACKWARD:
            // B = PWM, A = Low
            mcpwm_set_signal_low(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_A);
            mcpwm_set_duty(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_B, fabsf(normalized_effort));
            mcpwm_set_duty_type(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_B, MCPWM_DUTY_MODE_0);
            break;

        case DIR_BRAKE:
            // Both high (brake)
            mcpwm_set_signal_high(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_A);
            mcpwm_set_signal_high(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_B);
            break;

        case DIR_COAST:
        default:
            // Both low (coast)
            mcpwm_set_signal_low(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_A);
            mcpwm_set_signal_low(MCPWM_UNIT_USED, MCPWM_TIMER_USED, MCPWM_GEN_B);
            break;
    }
}



void motor_driver_task(void* data){
    
    // Write control effor to driver at high frequency
    float* u = (float*)data;
    
    
    while (true){

        driver_write(*u);
        vTaskDelay(pdMS_TO_TICKS(1));

    }
    

}

#endif //MOTOR_DRIVER_H