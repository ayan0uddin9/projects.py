# print(" Simple Calculator")

# num1 = float(input("Enter first number: "))
# op = input("Enter operation (+, -, *, /): ")
# num2 = float(input("Enter second number: "))

# if op == "+":
#     print("Result:", num1 + num2)
# elif op == "-":
#     print("Result:", num1 - num2)
# elif op == "*":
#     print("Result:", num1 * num2)
# elif op == "/":
#     if num2 != 0:
#         print("Result:", num1 / num2)
#     else:
#         print("⚠ Cannot divide by zero!")
# else:
#     print(" Invalid operation")

# Enhanced version

def calculator():
    print("\nWelcome to the Enhanced Calculator!")
    print("Available operations: +  -  *  /  **(power)  %(modulus)")
    
    while True:
        try:
            num1 = float(input("\nEnter first number: "))
            op = input("Enter operation: ")
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("⚠ Invalid input. Please enter numbers only.")
            continue

        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            result = "⚠ Cannot divide by zero!" if num2 == 0 else num1 / num2
        elif op == "**":
            result = num1 ** num2
        elif op == "%":
            result = num1 % num2
        else:
            print("Invalid operation.")
            continue
        print(f"Result: {result}")

        again = input("Do another calculation? (y/n): ").lower()
        if again != "y":
            print("Thanks for using the calculator!")
            break

calculator()



