import re

def isValidAge():
    """Prompt for age (0..120). Return int, or None if user types exit/quit."""
    while True:
        age = input("Enter your age: ").strip()
        if _exit_requested(age):
            return None
        if age.isdigit() and 0 <= int(age) <= 120:
            return int(age)
        print("Invalid age. Please enter a number between 0 and 120 (or 'exit').\n")

def firstName():
    """Prompt for first name. Letters, spaces, hyphens, apostrophes allowed. Return str or None."""
    pat = re.compile(r"[A-Za-z][A-Za-z '\-]*$")
    while True:
        fName = input("Enter your first name: ").strip()
        if _exit_requested(fName):
            return None
        if pat.fullmatch(fName):
            return fName
        print("Invalid first name. Use letters, spaces, hyphens, or apostrophes (or 'exit').\n")

def lastName():
    """Prompt for last name. Letters, spaces, hyphens, apostrophes allowed. Return str or None."""
    pat = re.compile(r"[A-Za-z][A-Za-z '\-]*$")
    while True:
        lName = input("Enter your last name: ").strip()
        if _exit_requested(lName):
            return None
        if pat.fullmatch(lName):
            return lName
        print("Invalid last name. Use letters, spaces, hyphens, or apostrophes (or 'exit').\n")

def _yes_no(value: str):
    v = value.strip().lower()
    if v in {"y", "yes"}:
        return True
    if v in {"n", "no"}:
        return False
    return None

def countryOfCitizenship():
    """Ask U.S. citizenship (Yes/No). Return True/False, or None if exit/quit."""
    while True:
        ans = input("Are you a U.S. Citizen? (Yes/No): ").strip()
        if _exit_requested(ans):
            return None
        yn = _yes_no(ans)
        if yn is not None:
            return yn
        print("Please answer Yes or No (or type 'exit' to cancel).\n")

def zipCode():
    """Prompt for ZIP (##### or #####-####). Return string or None if exit/quit."""
    pat = re.compile(r"\d{5}(-\d{4})?$")
    while True:
        zip_code = input("Enter your zip code (##### or #####-####): ").strip()
        if _exit_requested(zip_code):
            return None
        if pat.fullmatch(zip_code):
            return zip_code
        print("Invalid ZIP. Please enter 5 digits or ZIP+4 (or 'exit').\n")
 
def _ask_continue(prompt: str = "Do you want to continue with Voter Registration? (Yes/No): ") -> bool:
    while True:
        ans = input(prompt).strip()
        yn = _yes_no(ans)
        if yn is not None:
            return yn
        print("Please answer Yes or No.\n")

def _continue_or_raise(initial: bool = False) -> None:
    """Ask the standard continue question; raise if user says No."""
    if not _ask_continue():
        msg = "Thanks for trying the Voter Registration Application. Goodbye!" if initial \
              else "Registration canceled. Goodbye!"
        raise CancelRegistration(msg)

def _require(getter):
    """Call a getter (e.g., firstName). If it returns None (user exit), raise."""
    val = getter()
    if val is None:
        raise CancelRegistration()
    return val

def _exit_requested(text: str) -> bool:
    return text.strip().lower() in {"exit", "quit"}

class CancelRegistration(Exception):
    """Raised to stop the flow cleanly."""
    def __init__(self, message: str = "Registration canceled. Goodbye!"):
        super().__init__(message)
        self.message = message

stateOfResidenceHM ={
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}

def stateOfResidence():
    """Prompt for state (two-letter code). Return code or None if exit/quit."""
    while True:
        state = input("What state do you live? (Two-letter code, e.g., MD): ").strip().upper()
        if _exit_requested(state):
            return None
        if len(state) == 2 and state in stateOfResidenceHM.values():
            return state
        print("Invalid state code. Please enter a valid two-letter code (or 'exit').\n")
    
def main():
    """Run the interactive voter registration flow using the provided functions."""
    print("*" * 64)
    print("Welcome to the Python Voter Registration Application.\n")

    try:
        _continue_or_raise(initial=True)

        # Define steps: (key, getter, optional post_check callable)
        def _age_check(value: int) -> None:
            if value < 18:
                print("\nYou must be at least 18 years old to register to vote.")
                raise CancelRegistration("Thanks for trying the Voter Registration Application.")

        def _citizen_check(value: bool) -> None:
            if not value:
                print("\nOnly U.S. citizens are eligible to register to vote.")
                raise CancelRegistration("Thanks for trying the Voter Registration Application.")

        steps = [
            ("first", firstName, None),
            ("last",  lastName, None),
            ("age",   isValidAge, _age_check),
            ("citizen", countryOfCitizenship, _citizen_check),
            ("state", stateOfResidence, None),
            ("zip",   zipCode, None),
        ]

        results = {}  # collect values for summary

        # Ask the “continue?” question and then run each step uniformly
        for key, getter, post_check in steps:
            _continue_or_raise()
            value = _require(getter)
            if post_check:
                post_check(value)
            results[key] = value

        # Success summary
        print("\nThanks for registering to vote. Here is the information we received:")
        print(f"Name (first last): {results['first']} {results['last']}")
        print(f"Age: {results['age']}")
        print("U.S. Citizen: Yes")
        print(f"State: {results['state']}")
        print(f"Zipcode: {results['zip']}")
        print(
            "\nThanks for trying the Voter Registration Application. "
            "Your voter registration card should be shipped within 3 weeks."
        )
        print("*" * 64)

    except CancelRegistration as stop:
        print(stop.message)
        print("*" * 64)
        
if __name__ == "__main__":
    main()