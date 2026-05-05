#!/usr/bin/env python3

from gpiozero import PWMOutputDevice


class DCMotor:
    """DC Motor driver class driven by PWM (gpiozero version)"""

    def __init__(self, forPin, bacPin):
        # PWM devices (values range 0.0 → 1.0)
        self._forPWM = PWMOutputDevice(forPin)
        self._bacPWM = PWMOutputDevice(bacPin)

        self._maxSpeed = 100.0
        self._minSpeed = 0.0

        self.stop()

    def forward(self, speed=None):
        """Run motor forward"""
        if speed is None:
            speed = self._minSpeed
        self.run(abs(speed))

    def reverse(self, speed=None):
        """Run motor backward"""
        if speed is None:
            speed = self._minSpeed
        self.run(-abs(speed))

    def stop(self):
        """Stop the motor"""
        self._forPWM.value = 0.0
        self._bacPWM.value = 0.0

    def run(self, speed=None):
        """Run motor with signed speed (-100 to 100)"""
        if speed is None:
            speed = self._minSpeed

        # Clamp speed
        speed = max(-self._maxSpeed, min(self._maxSpeed, speed))

        # Normalize to 0.0–1.0 for gpiozero
        norm_speed = abs(speed) / self._maxSpeed

        if speed < 0:
            self._forPWM.value = 0.0
            self._bacPWM.value = norm_speed
        else:
            self._forPWM.value = norm_speed
            self._bacPWM.value = 0.0