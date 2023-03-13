import machine
import utime
from machine import Pin


ADC_READS = 3
LED_BLINK_MS = 200
THRESHOLD_MV = 500
INCREMENT_MV = 25
PIEZO_1_PIN = Pin(2, Pin.IN)
PIEZO_2_PIN = Pin(3, Pin.IN)
LED_PIN = Pin(21, Pin.OUT, Pin.PULL_DOWN)
# Thumbwheel switch, Omron A7D
SW1 = Pin(10, Pin.IN, Pin.PULL_DOWN)
SW2 = Pin(9, Pin.IN, Pin.PULL_DOWN)
SW4 = Pin(8, Pin.IN, Pin.PULL_DOWN)
SW8 = Pin(20, Pin.IN, Pin.PULL_DOWN)


def run(threshold_mV=THRESHOLD_MV):
    _led_off()
    while True:
        p1 = _piezo_mV(PIEZO_1_PIN)
        p2 = _piezo_mV(PIEZO_2_PIN)
        curr_threshold_mV = _threshold(threshold_mV, _thumbwheel_value())
        if p1 > curr_threshold_mV or p2 > curr_threshold_mV:
            print(f"{p1:4.0f}, {p2:4.0f}, {curr_threshold_mV:d}")
            _flash_led()


def _piezo_mV(pin):
    adc = machine.ADC(pin)
    sum = 0
    for x in range(0, ADC_READS):
        sum += adc.read_uv()
    return (sum / ADC_READS / 1000)


def _threshold(threshold_mV, switch_value):
    return threshold_mV + (switch_value * INCREMENT_MV)


def _thumbwheel_value():
    return SW1.value() + (SW2.value() << 1) + (SW4.value() << 2) + (SW8.value() << 3)


def _flash_led():
    _led_on()
    utime.sleep_ms(LED_BLINK_MS)
    _led_off()


def _led_off():
    LED_PIN.value(0)


def _led_on():
    LED_PIN.value(1)
