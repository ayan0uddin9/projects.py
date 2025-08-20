# print("🌡 Temperature Converter")

# celsius = float(input("Enter temperature in Celsius: "))
# fahrenheit = (celsius * 9/5) + 32

# print(f"{celsius}°C is equal to {fahrenheit}°F")

# Enhanced version

def convert_temperature():
    print("\n🌡 Welcome to the Temperature Converter!")
    while True:
        print("\nChoose conversion:")
        print("1. Celsius → Fahrenheit")
        print("2. Fahrenheit → Celsius")
        print("3. Celsius → Kelvin")
        print("4. Kelvin → Celsius")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")
        
        if choice == "5":
            print("Thanks for using the converter!")
            break

        try:
            temp = float(input("Enter the temperature value: "))
        except ValueError:
            print("⚠ Please enter a valid number.")
            continue
        if choice == "1":
            result = (temp * 9/5) + 32
            print(f"{temp:.2f}°C = {result:.2f}°F")
        elif choice == "2":
            result = (temp - 32) * 5/9
            print(f"{temp:.2f}°F = {result:.2f}°C")
        elif choice == "3":
            result = temp + 273.15
            print(f"{temp:.2f} = {result:.2f} K")
        elif choice == "4":
            result = temp - 273.15
            print(f"{temp:.2f} K = {result:.2f}°C")
        else:
            print("Invalid choice, please select from 1 to 5.")

convert_temperature()

