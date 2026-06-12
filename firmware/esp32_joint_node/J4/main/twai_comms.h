#ifndef TWAI_COMMS_H
#define TWAI_COMMS_H

// Base libraries
#include "base_libs.h"

// Node config
#include "node_config.h"

// TWAI driver
#include "driver/twai.h"

#ifdef NODE_HAS_GRIPPER
    // Gripper driver
    #include "grip_controller.h"
#endif

// TWAI pripheral config
const twai_timing_config_t t_config = TWAI_TIMING_CONFIG_500KBITS();
const twai_filter_config_t f_config = TWAI_FILTER_CONFIG_ACCEPT_ALL();
const twai_general_config_t g_config = TWAI_GENERAL_CONFIG_DEFAULT(TX_GPIO_NUM, RX_GPIO_NUM, TWAI_MODE_NORMAL);

// Helper struct

typedef struct twai_comms
{
    StatePointers* state_ptrs;
    twai_message_t* msg_ptr;
} twai_task_pointers_t;


twai_message_t* twai_message_init(uint32_t id){

    // TWAI message initializer

    // Allocate memory
    twai_message_t* msg = (twai_message_t*)calloc(1, sizeof(twai_message_t));

    // Message type and format settings
    msg->extd = 0;              // Standard Format message (11-bit ID)
    msg->rtr = 0;               // Send a data frame
    msg->ss = 0;                // Is not single shot (will retry on error or NACK)
    msg->self = 0;              // Not a self reception request
    msg->dlc_non_comp = 0;      // DLC is less than 8
    msg->data_length_code = 8;

    // Message ID
    msg->identifier = id; // ID_STATE_RESPONSE for response msg

    // Initialize payload to zero
    for(size_t i = 0;i<8;i++){
        msg->data[i] = 0;
    }
    return msg;

}

// Transfers global process variable to task memory
bool twai_get_pv(SystemState* local_pv, SystemState* global_pv){
    if(xSemaphoreTake(pv_semaphore, portMAX_DELAY)){
        // Try to get pv with no delay. If blocked, return false.
        *local_pv = *global_pv;
        xSemaphoreGive(pv_semaphore);
        return true;
    }else return false;
}


esp_err_t send_pv(SystemState* global_state, twai_message_t* msg ){
    
    //TODO: Implement multi-frame data transfer to send u
    // Recover control effort
    //float* u = state->u;

    // Local variables to store pv
    float d1 = 0.0F;
    float d2 = 0.0F;

    // Take semaphore
    if(xSemaphoreTake(pv_semaphore, portMAX_DELAY)){
        // Copy pv to local variables
        d1 = global_state->position;
        d2 = global_state->velocity;
        // Give semaphore
        xSemaphoreGive(pv_semaphore);

        // memcpy local variables to message
        xthal_memcpy(msg->data, &d1, 4);
        xthal_memcpy(msg->data+4, &d2, 4);
        
    }else return ESP_ERR_TIMEOUT;
    // Transmit
    return twai_transmit(msg, portMAX_DELAY);
}


bool change_sp(SystemState* local_sp, SystemState* global_sp){
    // Transfers global process variable to task memory
    if(xSemaphoreTake(sp_semaphore, portMAX_DELAY)){
        // Try to get sp with no delay. If blocked, return false.
        *global_sp = *local_sp;
        xSemaphoreGive(sp_semaphore);
        return true;
    }else return false;
}

// Generic frame processor
void process_frame(
    void* frame_in,
    void* items_out,
    size_t count,
    size_t size_of_element
){
    // C doesn't like void* arithmetics
    uint8_t* src = frame_in;
    uint8_t* dst = items_out;

    for (size_t i = 0; i < count; i++) {
        xthal_memcpy(
            dst + i * size_of_element,
            src + i * size_of_element,
            size_of_element
        );
    }
}



void twai_task(void *arg){
    // Recover pointers

    twai_task_pointers_t* ptrs = (twai_task_pointers_t*)arg;
    twai_message_t* state_response_msg = ptrs->msg_ptr;
    SystemState* global_pv = ptrs->state_ptrs->pv;
    SystemState* global_sp = ptrs->state_ptrs->sp;
    float* u = ptrs->state_ptrs->u;

    // Locally stores variables
    SystemState local_pv = {0};
    SystemState local_sp = {0};


    while (1) {
        twai_message_t rx_msg;
        twai_receive(&rx_msg, portMAX_DELAY);
        switch (rx_msg.identifier)
        {
        case ID_STATE_REQUEST:
            ESP_LOGI(TWAI_TAG, "Received state request.");
            twai_get_pv(&local_pv, global_pv);
            send_pv(&local_pv, state_response_msg);
            break;

        case ID_STATE_BROADCAST_REQUEST:
            ESP_LOGI(TWAI_TAG, "Received state broadcast request.");
            twai_get_pv(&local_pv, global_pv);
            send_pv(&local_pv, state_response_msg);
            break;

        case ID_SETPOINT_CHANGE:
            ESP_LOGI(TWAI_TAG, "Setpoint change request received.");
            float buffer[2] = {};
            process_frame(rx_msg.data, (void*)&buffer, 2, sizeof(float));
            local_sp.position = buffer[0];
            local_sp.velocity = buffer[1];
            if(change_sp(&local_sp, global_sp)){
                ESP_LOGI(TWAI_TAG, "Changed setpoint to (%f, %f).",buffer[0], buffer[1]);
            }
            
            break;

        case ID_CONTROL_MODE:
            ESP_LOGI(TWAI_TAG, "Control mode change request received.");
            uint32_t mode = 0;
            process_frame(rx_msg.data, (void*)&mode, 1, sizeof(uint32_t));
            if(!mode){
                ESP_LOGI(TWAI_TAG, "Changed control mode to trajectory tracking.");
                *(ptrs->state_ptrs->control_mode) = 0;
                }
            else{
                ESP_LOGI(TWAI_TAG, "Changed control mode to differential.");
                *(ptrs->state_ptrs->control_mode) = 1;
            }
            
            break;

            #ifdef NODE_HAS_GRIPPER
                case ID_GRIPPER_CMD:
                    float grip = 0.0F;
                    process_frame(rx_msg.data, (float*)&grip, 1, sizeof(float));
                    gripper_write(grip);
                    ESP_LOGI(TWAI_TAG, "Gripper state changed: %f",grip);
                
                break;
            #endif

        default:
            break;
        }

    }
        
}


#endif //TWAI_DRIVER_H