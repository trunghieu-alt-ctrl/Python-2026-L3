def calculate_circle_area(radius):
    return 3.14 * (radius ** 2)

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
