#ifndef NODE_CONFIG_H
#define NODE_CONFIG_H

#include "base_libs.h"

// Debug tags

    #define MAIN_TASK_TAG "MAIN"
    #define TWAI_TAG "TWAI"
    #define CONTROLLER_TAG "Control"
    #define DRIVER_TAG "Driver"

// Task config
    
    // Motor driver task
        #define DRIVER_TASK_STACK_DEPTH 2048
        #define DRIVER_TASK_PRIO (configMAX_PRIORITIES-10)
        
    // Encoder task
        #define ENCODER_TASK_STACK_DEPTH 2048
        #define ENCODER_TASK_PRIO (configMAX_PRIORITIES-11)

    // PID Controller task
        #define PID_TASK_STACK_DEPTH 2048
        #define PID_TASK_PRIO (configMAX_PRIORITIES-12)

    // TWAI task
        #define TWAI_TASK_STACK_DEPTH 4096    
        #define TWAI_TASK_PRIO (configMAX_PRIORITIES-13)
    

// Motor Driver
    // Driver IN pins
    #define DRV_IN1 GPIO_NUM_32
    #define DRV_IN2 GPIO_NUM_33
    

    // If the ILIM pin of the driver is connected or not
    // Comment out if not
    #define ILIM_CONNECTED //J1 has ILIM

    // Measured value of ILIM Resistor
    #define ILIM_RESISTOR 45.44F //kOhm 



// Encoder
    // J2
    #define ENCODER_A_PIN GPIO_NUM_10
    #define ENCODER_B_PIN GPIO_NUM_13
    #define ENCODER_PPR 68.0F
    #define GEAR_REDUCTION 131.0F // Motor gearbox
    
    // Flip encoder
    //#define ENCODER_FLIP

    #define VELOCITY_FILTER_CONSTANT 0.01F
    #define FILTER_FREQUENCY 1000

// Controller
    #define CONTROLLER_FREQUENCY 500
    #define CONTROLLER_GAIN_KP 200.0F
    #define CONTROLLER_GAIN_KI 15.0F
    #define CONTROLLER_INTEGRATOR_LIMIT 90.0F
    #define CONTROLLER_GAIN_KD 0.0F
    #define CONTROLLER_MAX_VELOCITY (5.0F*M_PI)

// Trajectory controller
    #define TRAJ_CONTROLLER_GAIN 20.0F


// TWAI

    // SN65H pins
        // J2
        #define TX_GPIO_NUM GPIO_NUM_21
        #define RX_GPIO_NUM GPIO_NUM_22
        

    // TWAI Address
        //J4
        #define DEVICE_ID               0x001
        #define ID_STATE_REQUEST        0x0A1
        #define ID_STATE_BROADCAST_REQUEST 0x0A6

        #define ID_STATE_RESPONSE       0x0B1
        
        #define ID_SETPOINT_CHANGE      0x0C1
        
        #define ID_CONTROL_MODE         0x0D1



    // Gripper
        // J1 has no gripper
        // #define NODE_HAS_GRIPPER
        
        
        #ifdef NODE_HAS_GRIPPER
            // Gripper cmd
            #define ID_GRIPPER_CMD          0x0D2
            // Gripper pin
            #define GRIPPER_PIN GPIO_NUM_5
        #endif //NODE_HAS_GRIPPER


#endif // NODE_CONFIG_H