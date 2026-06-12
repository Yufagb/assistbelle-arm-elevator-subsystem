#ifndef ENCODER_DRIVER_H
#define ENCODER_DRIVER_H

// Driver for motor encoder.

// Base libraries
#include "base_libs.h"

// Node config
#include "node_config.h"

// PCNT Unit
#include "driver/pulse_cnt.h"


// PCNT Configs
#define PCNT_HIGH_LIMIT 10000
#define PCNT_LOW_LIMIT  -10000

#define SAMPLE_RATE (((float)1)/((float)FILTER_FREQUENCY))
#define MS_PER_LOOP (int)(1000/FILTER_FREQUENCY)

#define COUNTS_TO_RAD (float)((2.0F*M_PI)/(ENCODER_PPR*GEAR_REDUCTION))


// Helper struct
typedef struct
{
    SystemState* system_state;
    pcnt_unit_handle_t pcnt_unit_h;
} encoder_task_pointers_t;


void encoder_init(encoder_task_pointers_t* ptrs){

    // Initialize encoder

    // Configure GPIO


    // configure GPIO input + pullups
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << ENCODER_A_PIN) | (1ULL << ENCODER_B_PIN),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    gpio_config(&io_conf);



    pcnt_unit_config_t unit_config = {
        .low_limit = PCNT_LOW_LIMIT,
        .high_limit = PCNT_HIGH_LIMIT,
        .flags.accum_count = true
    };

    // Create PCNT unit on handle
     pcnt_new_unit(&unit_config, &(ptrs->pcnt_unit_h));

     

    // Set glitch filter
    pcnt_glitch_filter_config_t filter_config = {
        .max_glitch_ns = 10000,
    };

     pcnt_unit_set_glitch_filter(ptrs->pcnt_unit_h, &filter_config);
     

    // Configure channels
    pcnt_chan_config_t chan_a_config = {
        .edge_gpio_num = ENCODER_A_PIN,
        .level_gpio_num = ENCODER_B_PIN,
    };

    pcnt_channel_handle_t pcnt_chan_a = NULL;
    pcnt_new_channel(ptrs->pcnt_unit_h, &chan_a_config, &pcnt_chan_a);
    
    pcnt_channel_handle_t pcnt_chan_b = NULL;
    pcnt_chan_config_t chan_b_config = {
        .edge_gpio_num = ENCODER_B_PIN,
        .level_gpio_num = ENCODER_A_PIN,
    };
    pcnt_new_channel(ptrs->pcnt_unit_h, &chan_b_config, &pcnt_chan_b);
    

    // Set edge and level actions
        pcnt_channel_set_edge_action(pcnt_chan_a, PCNT_CHANNEL_EDGE_ACTION_INCREASE, PCNT_CHANNEL_EDGE_ACTION_DECREASE);
        pcnt_channel_set_level_action(pcnt_chan_a, PCNT_CHANNEL_LEVEL_ACTION_KEEP, PCNT_CHANNEL_LEVEL_ACTION_INVERSE);
        pcnt_channel_set_edge_action(pcnt_chan_b, PCNT_CHANNEL_EDGE_ACTION_DECREASE, PCNT_CHANNEL_EDGE_ACTION_INCREASE);
        pcnt_channel_set_level_action(pcnt_chan_b, PCNT_CHANNEL_LEVEL_ACTION_KEEP, PCNT_CHANNEL_LEVEL_ACTION_INVERSE);

    
    // Install watchpoints for count rollover
    int watch_points[] = {PCNT_LOW_LIMIT, 0, PCNT_HIGH_LIMIT};
    for (size_t i = 0; i < sizeof(watch_points)/sizeof(watch_points[0]); ++i) {
        pcnt_unit_add_watch_point(ptrs->pcnt_unit_h, watch_points[i]);
    }
     

    // Start unit
     pcnt_unit_enable(ptrs->pcnt_unit_h);
     pcnt_unit_clear_count(ptrs->pcnt_unit_h);
     pcnt_unit_start(ptrs->pcnt_unit_h);

}

void encoder_task(void* data){

    // Get pointers
    encoder_task_pointers_t* ptrs = (encoder_task_pointers_t*)data;

    // Process variable pointer
    SystemState* pv = (SystemState*)ptrs->system_state;
    

    // Define constants with arithmetic as variables so macros aren't recalculated each time
    const float counts_to_rad = COUNTS_TO_RAD;
    const float sample_rate = SAMPLE_RATE;
    const float ms_per_loop = MS_PER_LOOP;
    const float alpha = VELOCITY_FILTER_CONSTANT;

    // Initialize count
    int count = 0;
    int previous_count = 0;
    int count_delta = 0;
    float counts_per_second = 0.0F;

    // Loop counter and timer
    int loops_since_last_change = 0;
    float dt = 0.0F;

    // Velocity filter
    float decay = 0.001F;

    float prev_position = 0.0F;
    float position = 0.0F;
    float raw_velocity = 0.0F;
    float velocity = 0.0F;

    // Task timing
    TickType_t xLastWakeTime;
    xLastWakeTime = xTaskGetTickCount();
    while (1) {
        
        // Read count
        pcnt_unit_get_count((ptrs->pcnt_unit_h), &count);
    
        #ifdef ENCODER_FLIP
            count *= -1.0F;
        #endif

        // Calculate angular position
        position = ((float)count)*counts_to_rad;
        
        

        // Calculate delta
        count_delta = count - previous_count;
        previous_count = count;

        if(count_delta != 0){
            // Motor moved between loops.

            // dt is by default loop time times number of loops since last change
            dt = loops_since_last_change * sample_rate;

            // If it's zero (plus leeway for fp precision) it's the sample rate
            if(dt < 1e-6f) dt = sample_rate;

            // Calculate counts per second
            counts_per_second = ((float)count_delta)/dt;

            // Calculate raw velocity
            raw_velocity = counts_per_second*counts_to_rad;

            // Filter
            velocity = alpha*velocity + (1.0F-alpha)*raw_velocity;

            // Since we moved, reset loops since last movement
            loops_since_last_change = 0;
        }else{
            // No movement between loops
            loops_since_last_change++;

            // Exponential decay
            velocity *= expf(-decay*sample_rate);

            // Filter
            velocity = alpha*velocity + (1.0F-alpha)*raw_velocity;

        }
        

        // Hybrid velocity filter 


        // rad/s
        raw_velocity = (position-prev_position)*((float)(FILTER_FREQUENCY));

        prev_position = position;

        // Velocity first order filter
        velocity = alpha*velocity + (1.0F-alpha)*raw_velocity;
        
        // Update global variables
        
        if(xSemaphoreTake(pv_semaphore, pdMS_TO_TICKS(ms_per_loop/2.0F))){
            // Try to update position and velocity.
            // If pv is blocked for more than filter cycle time, discard old measurement and measure again
            
            pv->position = position;
            


            pv->velocity = velocity;
            //pv->velocity = raw_velocity;
            xSemaphoreGive(pv_semaphore);
        }

        // Fixed time task
        vTaskDelayUntil(&xLastWakeTime,pdMS_TO_TICKS(ms_per_loop));
    }
}



#endif //ENCODER_DRIVER_H