"""
This will attempt to import RPi.GPIO. If this fails (due to not running on a GPIO-capable device),
this will import `Mock.GPIO`
"""
try:
    import RPi.GPIO as GPIO
except (ImportError, ModuleNotFoundError):
    print("Warning: Using Mock GPIO subsystem.")
    import Mock.GPIO as GPIO
