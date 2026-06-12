// main.c

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <math.h>           // roundf(), lroundf()
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"
#include "driver/twai.h"
#include "esp_rom_sys.h"
#include "esp_task_wdt.h"

// —————————————————————————————————————————————————————
// TB6600 DIP-switch configuration
// —————————————————————————————————————————————————————
#define DIP_S1 1
#define DIP_S2 1
#define DIP_S3 0

#define DIP_S4 0
#define DIP_S5 0
#define DIP_S6 0

static uint32_t calculate_microstep(void) {
    if      (DIP_S1 && DIP_S2 && !DIP_S3) return 1;
    else if (DIP_S1 && !DIP_S2 && DIP_S3) return 2;
    else if (!DIP_S1 && DIP_S2 && DIP_S3) return 2;
    else if (DIP_S1 && !DIP_S2 && !DIP_S3) return 4;
    else if (!DIP_S1 && DIP_S2 && !DIP_S3) return 8;
    else if (!DIP_S1 && !DIP_S2 && DIP_S3) return 16;
    else                                    return 32;
}

static float calculate_current(void) {
    if      (DIP_S4 && DIP_S5 && DIP_S6)  return 0.5f;
    else if (DIP_S4 && !DIP_S5 && DIP_S6) return 1.0f;
    else if (DIP_S4 && DIP_S5 && !DIP_S6) return 1.5f;
    else if (DIP_S4 && !DIP_S5 && !DIP_S6) return 2.0f;
    else if (!DIP_S4 && DIP_S5 && DIP_S6) return 2.5f;
    else if (!DIP_S4 && !DIP_S5 && DIP_S6) return 2.8f;
    else if (!DIP_S4 && DIP_S5 && !DIP_S6) return 3.0f;
    else                                    return 3.5f;
}

// —————————————————————————————————————————————————————
// TB6600 driver pins
// —————————————————————————————————————————————————————
#define ENA_PIN 19
#define DIR_PIN 18
#define PUL_PIN  5

// —————————————————————————————————————————————————————
// CAN (TWAI) pins & config @500 kbps
// —————————————————————————————————————————————————————
#define CAN_TX_GPIO 22
#define CAN_RX_GPIO 21

static const twai_general_config_t can_g_config = {
    .tx_io           = CAN_TX_GPIO,
    .rx_io           = CAN_RX_GPIO,
    .mode            = TWAI_MODE_NORMAL,
    .clkout_io       = TWAI_IO_UNUSED,
    .bus_off_io      = TWAI_IO_UNUSED,
    .tx_queue_len    = 5,
    .rx_queue_len    = 5,
    .alerts_enabled  = TWAI_ALERT_NONE,
    .clkout_divider  = 0,
};
static const twai_timing_config_t can_t_config = TWAI_TIMING_CONFIG_500KBITS();
static const twai_filter_config_t can_f_config = TWAI_FILTER_CONFIG_ACCEPT_ALL();

// —————————————————————————————————————————————————————
// Motor & tornillo T8
// —————————————————————————————————————————————————————
#define FULL_STEPS_PER_REV 200u
#define SCREW_LEAD_MM        8u
#define SPEED_HZ           500u  // pulsos/s

static uint32_t g_pulses_per_mm = 1;

// ¡Con signo y VOLATILE para lecturas mientras se mueve!
static volatile int32_t g_current_position_steps = 0;

// Cola para objetivos (int32_t)
static QueueHandle_t motion_q;

// —————————————————————————————————————————————————————
// Utils
// —————————————————————————————————————————————————————
static inline void pack_f32_le(uint8_t out[4], float f) {
    union { float f; uint8_t b[4]; } u;
    u.f = f;
    out[0] = u.b[0]; out[1] = u.b[1]; out[2] = u.b[2]; out[3] = u.b[3];
}

// —————————————————————————————————————————————————————
// Stepper helpers
// —————————————————————————————————————————————————————
static void stepper_init(void) {
    gpio_reset_pin(ENA_PIN);
    gpio_set_direction(ENA_PIN, GPIO_MODE_OUTPUT);
    gpio_set_level(ENA_PIN, 0);  // habilita driver

    gpio_reset_pin(DIR_PIN);
    gpio_set_direction(DIR_PIN, GPIO_MODE_OUTPUT);

    gpio_reset_pin(PUL_PIN);
    gpio_set_direction(PUL_PIN, GPIO_MODE_OUTPUT);
}

static void pulse_once(uint32_t period_us) {
    uint32_t half = period_us / 2;
    gpio_set_level(PUL_PIN, 1);
    esp_rom_delay_us(half);
    gpio_set_level(PUL_PIN, 0);
    esp_rom_delay_us(half);
}

// AHORA actualiza posición en TIEMPO REAL (por pulso)
static void move_steps_chunked(uint32_t steps, bool forward) {
    const uint32_t CHUNK  = 200;
    const uint32_t period = 1000000U / SPEED_HZ;
    const int32_t  inc    = forward ? 1 : -1;

    esp_task_wdt_add(NULL);
    gpio_set_level(DIR_PIN, forward ? 1 : 0);

    for (uint32_t done = 0; done < steps; done += CHUNK) {
        uint32_t this_chunk = (steps - done > CHUNK) ? CHUNK : (steps - done);

        for (uint32_t i = 0; i < this_chunk; ++i) {
            pulse_once(period);
            // Actualización inmediata de la posición:
            g_current_position_steps += inc;
        }

        esp_task_wdt_reset();
        vTaskDelay(1);

        printf("[DBG] chunk %lu/%lu dir=%u pos=%ld steps\n",
               (unsigned long)(done + this_chunk),
               (unsigned long)steps,
               (unsigned)forward,
               (long)g_current_position_steps);
    }
    esp_task_wdt_reset();
    esp_task_wdt_delete(NULL);
}

// Movimiento a posición ABSOLUTA (con signo)
static void move_to_position(int32_t target_steps) {
    int32_t current = g_current_position_steps;    // lectura atómica en Xtensa
    if (target_steps == current) return;

    bool forward = (target_steps > current);
    uint32_t delta = (uint32_t)(forward ? (target_steps - current)
                                        : (current - target_steps));

    printf("[DBG] move_to: %ld→%ld (Δ=%lu) dir=%u\n",
           (long)current, (long)target_steps,
           (unsigned long)delta, (unsigned)forward);

    move_steps_chunked(delta, forward);

    // Al terminar, nos aseguramos de aterrizar EXACTO en el objetivo:
    g_current_position_steps = target_steps;

    float pos_mm = (float)g_current_position_steps / (float)g_pulses_per_mm;
    printf("Reached %ld steps (%.3f mm)\n",
           (long)g_current_position_steps, pos_mm);
}

// —————————————————————————————————————————————————————
static void motion_task(void *arg) {
    printf("[TASK] motion_task start on core %u\n", xPortGetCoreID());
    int32_t req_steps;
    while (xQueueReceive(motion_q, &req_steps, portMAX_DELAY) == pdTRUE) {
        printf("[TASK] target %ld steps\n", (long)req_steps);
        move_to_position(req_steps);
    }
}

// —————————————————————————————————————————————————————
// CAN task: A5/A6 → responde B5 DLC=8 (float32LE + 04 00 00 80)
//            C5   → mover a mm (int16 BE o float32 LE)
// —————————————————————————————————————————————————————
static void can_task(void *arg) {
    printf("[TASK] can_task start on core %u\n", xPortGetCoreID());
    twai_message_t rx;

    twai_message_t tx_pos = {
        .identifier       = 0xB5,
        .extd             = 0,
        .rtr              = 0,
        .ss               = 0,
        .self             = 0,
        .data_length_code = 8
    };

    while (twai_receive(&rx, portMAX_DELAY) == ESP_OK) {
        printf("[CAN] RX id=0x%03lX dlc=%lu payload=[",
               (unsigned long)rx.identifier,
               (unsigned long)rx.data_length_code);
        for (uint32_t i = 0; i < rx.data_length_code; ++i) {
            printf("0x%02X%s", rx.data[i],
                   (i + 1 < rx.data_length_code) ? "," : "");
        }
        printf("]\n");

        // Petición de posición (responder SIEMPRE con la posición actual)
        if (rx.identifier == 0x0A5 || rx.identifier == 0xA5 ||
            rx.identifier == 0x0A6 || rx.identifier == 0xA6) {

            // Lectura "live": puede estar moviéndose
            int32_t steps_now = g_current_position_steps;
            float pos_mm = (float)steps_now / (float)g_pulses_per_mm;

            pack_f32_le(&tx_pos.data[0], pos_mm);
            tx_pos.data[4] = 0x04; tx_pos.data[5] = 0x00; tx_pos.data[6] = 0x00; tx_pos.data[7] = 0x80;

            if (twai_transmit(&tx_pos, pdMS_TO_TICKS(100)) == ESP_OK) {
                printf("[CAN] TX B5 pos=%.3f mm\n", pos_mm);
            } else {
                printf("[CAN][ERR] TX B5 failed\n");
            }
        }
        // Movimiento a posición en mm
        else if (rx.identifier == 0x0C5 || rx.identifier == 0xC5) {
            int16_t mm_signed = 0;

            if (rx.data_length_code == 4) {
                union { uint8_t b[4]; float f; } u = {0};
                for (int i = 0; i < 4; ++i) u.b[i] = rx.data[i];   // float32 LE
                mm_signed = (int16_t)lroundf(u.f);
            } else if (rx.data_length_code >= 2) {
                mm_signed = (int16_t)((rx.data[0] << 8) | rx.data[1]); // int16 BE
            } else {
                continue;
            }

            int32_t target_steps = (int32_t)mm_signed * (int32_t)g_pulses_per_mm;
            printf("[CAN] move cmd: %d mm → %ld steps\n",
                   (int)mm_signed, (long)target_steps);

            xQueueOverwrite(motion_q, &target_steps);
        }
    }
}

// —————————————————————————————————————————————————————
void app_main(void) {
    // Config
    uint32_t micro = calculate_microstep();
    float current  = calculate_current();
    g_pulses_per_mm = (FULL_STEPS_PER_REV * micro) / SCREW_LEAD_MM;
    if (g_pulses_per_mm == 0) g_pulses_per_mm = 1;

    printf("Config: 1/%lu μstep, %lu pulses/rev, %.1fA, %lu pulses/mm\n",
           (unsigned long)micro,
           (unsigned long)(FULL_STEPS_PER_REV * micro),
           current,
           (unsigned long)g_pulses_per_mm);

    // HW
    stepper_init();

    // CAN
    ESP_ERROR_CHECK(twai_driver_install(&can_g_config, &can_t_config, &can_f_config));
    ESP_ERROR_CHECK(twai_start());

    // RTOS
    motion_q = xQueueCreate(1, sizeof(int32_t));
    xTaskCreatePinnedToCore(can_task,    "can_task",    4096, NULL, 5, NULL, 0);
    xTaskCreatePinnedToCore(motion_task, "motion_task", 4096, NULL, 5, NULL, 1);

    // Pequeña calibración y anuncio de home (en formato B5)
    {
        uint32_t cal_steps = 5 * g_pulses_per_mm;
        printf("Calibrating: +5 mm then -5 mm\n");
        move_steps_chunked(cal_steps, true);
        move_steps_chunked(cal_steps, false);
        g_current_position_steps = 0;

        twai_message_t home = {
            .identifier       = 0xB5,
            .extd             = 0,
            .rtr              = 0,
            .ss               = 0,
            .self             = 0,
            .data_length_code = 8
        };
        pack_f32_le(&home.data[0], 0.0f);
        home.data[4] = 0x04; home.data[5] = 0x00; home.data[6] = 0x00; home.data[7] = 0x80;
        (void)twai_transmit(&home, pdMS_TO_TICKS(100));

        printf("Home set at 0 mm\n");
    }
}
