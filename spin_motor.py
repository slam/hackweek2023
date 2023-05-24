#!/usr/bin/env python3

import sys
import time
import timeit
import RPi.GPIO as GPIO

# Set the pin number (BCM mode)
PIN = 11

def main(duration_ms, run_forever=False):
    # Set GPIO mode to BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Set up the specified pin as an output
    GPIO.setup(PIN, GPIO.OUT)

    if not run_forever:
        # Calculate number of pulses
        num_pulses = int(duration_ms) // 1
    pulse_interval = 0.001  # 1 ms

    # Initialize timer
    timer = timeit.default_timer
    start_time = timer()

    try:
        # Blinking loop with time compensation
        count = 0
        while run_forever or count < num_pulses:
            next_loop_time = start_time + pulse_interval * (count + 1)
            GPIO.output(PIN, GPIO.HIGH)
            on_time = timer()
            while timer() < on_time + pulse_interval / 2:
                pass
            GPIO.output(PIN, GPIO.LOW)
            while timer() < next_loop_time:
                pass
            count += 1
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Clean up GPIO
        GPIO.cleanup()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} DURATION_MS [forever]")
    else:
        duration = sys.argv[1]
        forever = len(sys.argv) > 2 and sys.argv[2].lower() == 'forever'
        main(duration, run_forever=forever)
