import sys
import math
import random
import string
from datetime import datetime

# ---------- Input Utilities ----------
def _raw(prompt: str) -> str:
    """Basic input wrapper. Allows quitting with q/quit/exit at sub-prompts."""
    value = input(f"{prompt} (q to quit): ")
    if value.lower() in ("q", "quit", "exit"):
        sys.exit()
    return value

def _yn(prompt: str) -> bool:
    """Prompt the user for yes/no input until valid."""
    while True:
        val = _raw(f"{prompt} (y/n)").strip().lower()
        if val in ("y", "n"):
            return val == "y"
        print("Please enter y or n.")

def _num(prompt: str, caster=float, min_value=None):
    """Prompt for a number, re-asking until valid. Enforce minimum if set."""
    while True:
        try:
            val = caster(_raw(prompt))
            if min_value is not None and val < min_value:
                print(f"Must be >= {min_value}.")
                continue
            return val
        except ValueError:
            print("Please enter a numeric value.")


# ---------- Core Functions ----------
def SecurePasswordGenerator():
    """Factory returning a password generator function."""
    def generate_password(length=12, use_upper=True, use_lower=True,
                          use_digits=True, use_special=True):
        """Generate a secure password based on user settings."""
        if length < 8:
            raise ValueError("Password length should be at least 8 characters.")

        # Select available character sets based on user choices
        lowercase = string.ascii_lowercase if use_lower else ""
        uppercase = string.ascii_uppercase if use_upper else ""
        digits = string.digits if use_digits else ""
        special = string.punctuation if use_special else ""

        if not (lowercase or uppercase or digits or special):
            raise ValueError("At least one character set must be selected.")

        all_chars = lowercase + uppercase + digits + special

        # Ensure one of each selected type is included
        password = []
        if use_lower:
            password.append(random.choice(string.ascii_lowercase))
        if use_upper:
            password.append(random.choice(string.ascii_uppercase))
        if use_digits:
            password.append(random.choice(string.digits))
        if use_special:
            password.append(random.choice(string.punctuation))

        # Fill the rest randomly
        while len(password) < length:
            password.append(random.choice(all_chars))

        random.shuffle(password)
        return "".join(password)

    return generate_password

def CalculateAFormalPercentage():
    """Factory returning a percentage calculator function."""
    def calculate_percentage(part, whole, decimals=2):
        """Return (part/whole * 100), rounded to the specified decimals."""
        if whole == 0:
            return 0
        return round((part / whole) * 100, decimals)
    return calculate_percentage

def HowManyDaysUntilJulyFour():
    """Factory returning a function that calculates days until July 4, 2025."""
    def days_until_july_four():
        """Return non-negative integer days until July 4, 2025."""
        today = datetime.now()
        target = datetime(2025, 7, 4)
        days = (target - today).days
        return days if days > 0 else 0
    return days_until_july_four

def LegOfTriangle():
    """Factory returning a Law of Cosines function."""
    def calculate_leg(a, b, angle_degrees):
        """Return side c given sides a, b and included angle."""
        angle_radians = math.radians(angle_degrees)
        return math.sqrt(a**2 + b**2 - (2 * a * b * math.cos(angle_radians)))
    return calculate_leg

def VolRightCircularCylinder():
    """Factory returning a volume calculator for right circular cylinder."""
    def volume_cylinder(radius, height):
        """Return volume; both radius and height must be non-negative."""
        if radius < 0 or height < 0:
            raise ValueError("Radius and height must be non-negative.")
        return math.pi * (radius ** 2) * height
    return volume_cylinder

def ProgramsExit():
    """Factory returning an exit function."""
    def exit_program():
        """Exit program immediately."""
        sys.exit()
    return exit_program


# ---------- Menu Option Handlers ----------
def _handle_password(password_gen):
    """Handle password generation option (a)."""
    length = _num("Length (>=8)", int, 8)
    use_upper = _yn("Include uppercase?")
    use_lower = _yn("Include lowercase?")
    use_digits = _yn("Include digits?")
    use_special = _yn("Include special characters?")
    # Ensure at least one set is selected
    while not (use_upper or use_lower or use_digits or use_special):
        print("Select at least one character set.")
        use_upper = _yn("Include uppercase?")
        use_lower = _yn("Include lowercase?")
        use_digits = _yn("Include digits?")
        use_special = _yn("Include special characters?")
    print(password_gen(length, use_upper, use_lower, use_digits, use_special))

def _handle_percentage(percentage_calc):
    """Handle percentage calculation option (b)."""
    part = _num("Numerator")
    whole = _num("Denominator")
    decimals = _num("Decimals", int)
    print(f"{percentage_calc(part, whole, decimals)} %")

def _handle_days(days_until):
    """Handle option (c): days until July 4, 2025."""
    print(f"{days_until()} days")

def _handle_cosine(cosine_calc):
    """Handle option (d): calculate triangle side using cosine rule."""
    a = _num("Side a")
    b = _num("Side b")
    angle = _num("Angle (degrees)")
    print(cosine_calc(a, b, angle))

def _handle_cylinder(cylinder_vol):
    """Handle option (e): volume of a right circular cylinder."""
    radius = _num("Radius")
    height = _num("Height")
    print(cylinder_vol(radius, height))


# ---------- Main Menu ----------
def menu():
    """Main program loop. Quit only with option (f) or sub-prompt 'q'."""
    password_gen = SecurePasswordGenerator()
    percentage_calc = CalculateAFormalPercentage()
    days_until = HowManyDaysUntilJulyFour()
    cosine_calc = LegOfTriangle()
    cylinder_vol = VolRightCircularCylinder()
    exit_program = ProgramsExit()

    while True:
        print(
            "\n(a) Password Generator"
            "\n(b) Calculate and Format Percentage"
            "\n(c) Days until July 4, 2025"
            "\n(d) Calculate Leg of Triangle"
            "\n(e) Right Cylinder Volume"
            "\n(f) Exit"
        )
        choice = input("Choice: ").lower()

        if choice == "a":
            _handle_password(password_gen)
        elif choice == "b":
            _handle_percentage(percentage_calc)
        elif choice == "c":
            _handle_days(days_until)
        elif choice == "d":
            _handle_cosine(cosine_calc)
        elif choice == "e":
            _handle_cylinder(cylinder_vol)
        elif choice == "f":
            exit_program()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()
