from input import get_radius, get_celsius, get_number
from output import print_area, print_fahrenheit, print_prime_check
from domains.math_operations import calculate_circle_area, celsius_to_fahrenheit, is_prime

def main():
    print("--- 1. Circle Area ---")
    radius = get_radius()
    area = calculate_circle_area(radius)
    print_area(area)

    print("\n--- 2. Temperature Conversion ---")
    celsius = get_celsius()
    fahrenheit = celsius_to_fahrenheit(celsius)
    print_fahrenheit(celsius, fahrenheit)

    print("\n--- 3. Prime Number Check ---")
    num = get_number()
    check = is_prime(num)
    print_prime_check(num, check)

if __name__ == "__main__":
    main()
