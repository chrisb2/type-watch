import machine
import utime
from machine import Pin


ADC_READS = 3
KEY_DELAY_MS = 100
LED_BLINK_MS = 200
THRESHOLD_MV = 170
PIEZO_1_PIN = Pin(2, Pin.IN)
PIEZO_2_PIN = Pin(3, Pin.IN)
LED_PIN = Pin(21, Pin.OUT, Pin.PULL_DOWN)

current_threshold_mV = THRESHOLD_MV


def run(threshold_mV=THRESHOLD_MV):
    _led_off()
    _set_threshold(threshold_mV)
    while True:
        p1 = _piezo_mV(PIEZO_1_PIN)
        p2 = _piezo_mV(PIEZO_2_PIN)
        if p1 > current_threshold_mV or p2 > current_threshold_mV:
            print(f"{p1:4.0f}, {p2:4.0f}")
            _flash_led()


def _piezo_mV(pin):
    adc = machine.ADC(pin)
    sum = 0
    for x in range(0, ADC_READS):
        sum += adc.read_uv()
    return (sum / ADC_READS / 1000)


def _flash_led():
    _led_on()
    utime.sleep_ms(LED_BLINK_MS)
    _led_off()


def _led_off():
    LED_PIN.value(0)


def _led_on():
    LED_PIN.value(1)


def _set_threshold(threshold_mV):
    global current_threshold_mV
    current_threshold_mV = threshold_mV
