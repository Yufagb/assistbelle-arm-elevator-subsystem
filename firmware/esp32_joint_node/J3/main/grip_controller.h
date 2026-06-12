#ifndef GRIP_CONTROLLER_H
#define GRIP_CONTROLLER_H

#include "base_libs.h"

#include "node_config.h"

// Driver for servomotor-drive gripper

#include "driver/ledc.h"


// LEDC Setup

// 50 Hz for hobby servos
#define SERVO_FREQ          50

#define SERVO_TIMER_BIT     LEDC_TIMER_16_BIT  // 16-bit enough resolution
#define SERVO_TIMER_MODE    LEDC_LOW_SPEED_MODE
#define LEDC_CHANNEL        LEDC_CHANNEL_0
#define LEDC_TIMER          LEDC_TIMER_0

#define SERVO_MIN_US        1000
#define SERVO_MAX_US        2000


esp_err_t gripper_init(void)
{
    // Configure timer
    ledc_timer_config_t timer_conf = {
        .speed_mode       = SERVO_TIMER_MODE,
        .timer_num        = LEDC_TIMER,
        .duty_resolution  = SERVO_TIMER_BIT,
        .freq_hz          = SERVO_FREQ,
        .clk_cfg          = LEDC_AUTO_CLK
    };
    ESP_ERROR_CHECK( ledc_timer_config(&timer_conf) );

    // Configure channel
    ledc_channel_config_t channel_conf = {
        .gpio_num       = GRIPPER_PIN,
        .channel        = LEDC_CHANNEL,
        .speed_mode     = SERVO_TIMER_MODE,
        .timer_sel      = LEDC_TIMER,
        .duty           = 0,
        .hpoint         = 0
    };
    ESP_ERROR_CHECK( ledc_channel_config(&channel_conf) );

    return ESP_OK;
}

esp_err_t gripper_write(float pct)
{
    if (pct < 0) pct = 0;
    if (pct > 100) pct = 100;

    // Map 0–100% → min_us–max_us
    uint32_t pulse_us = SERVO_MIN_US +
        (uint32_t)((pct / 100.0f) * (SERVO_MAX_US - SERVO_MIN_US));

    // Convert microseconds to LEDC duty
    uint32_t max_duty = (1 << SERVO_TIMER_BIT) - 1;
    uint32_t period_us = 1000000UL / SERVO_FREQ;

    uint32_t duty = (pulse_us * max_duty) / period_us;

    return ledc_set_duty(SERVO_TIMER_MODE, LEDC_CHANNEL, duty) ||
           ledc_update_duty(SERVO_TIMER_MODE, LEDC_CHANNEL);
}

#endif //GRIP_CONTROLLER_H