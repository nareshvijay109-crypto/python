"""SIMATS Online Programming Lab — Assignment 2.
Student: Naresh Vijay R | Register No.: 1972260060D
Run: python assignment2_solution.py
"""
from functools import lru_cache
from time import perf_counter


# Q1: Electricity subsidy decisions

def subsidy_separate_ifs_buggy(units, has_ration_card, has_senior_over_80):
    decisions = []
    if units <= 100:
        decisions.append("FULL SUBSIDY")
    if units <= 200 and has_ration_card:  # deliberate overlap
        decisions.append("PARTIAL SUBSIDY")
    if units > 200 and has_senior_over_80:
        decisions.append("SPECIAL SENIOR-AGE REVIEW")
    if not decisions:
        decisions.append("NO SUBSIDY")
    return decisions


def subsidy_separate_ifs(units, has_ration_card, has_senior_over_80):
    decisions = []
    if units <= 100:
        decisions.append("FULL SUBSIDY")
    if 101 <= units <= 200 and has_ration_card:
        decisions.append("PARTIAL SUBSIDY")
    if 101 <= units <= 200 and not has_ration_card:
        decisions.append("NO SUBSIDY")
    if units > 200 and has_senior_over_80:
        decisions.append("SPECIAL SENIOR-AGE SUBSIDY")
    if units > 200 and not has_senior_over_80:
        decisions.append("NO SUBSIDY")
    return decisions


def subsidy_elif(units, has_ration_card, has_senior_over_80):
    if units <= 100:
        return "FULL SUBSIDY"
    elif 101 <= units <= 200:
        if has_ration_card:
            return "PARTIAL SUBSIDY"
        return "NO SUBSIDY"
    elif has_senior_over_80:
        return "SPECIAL SENIOR-AGE SUBSIDY"
    return "NO SUBSIDY"


def subsidy_match_case(units, has_ration_card, has_senior_over_80):
    match units:
        case n if n <= 100:
            return "FULL SUBSIDY"
        case n if 101 <= n <= 200 and has_ration_card:
            return "PARTIAL SUBSIDY"
        case n if 101 <= n <= 200:
            return "NO SUBSIDY"
        case n if n > 200 and has_senior_over_80:
            return "SPECIAL SENIOR-AGE SUBSIDY"
        case _:
            return "NO SUBSIDY"


def q1_demo():
    households = [
        (100, False, False), (100, True, False),
        (101, True, False), (101, False, False),
        (200, True, False), (200, False, False),
        (201, False, True), (201, True, False),
    ]
    for household in households:
        print(household, "=>", subsidy_elif(*household))
    print("Overlapping-if bug:", subsidy_separate_ifs_buggy(80, True, False))


# Q2: OTP verification

def verify_otp_while(correct_otp, read=input, write=print, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        entered = read("Enter OTP: ").strip()
        if entered == "":
            write("Blank entry: please try again; no attempt used.")
            continue
        if entered == correct_otp:
            write("OTP verified.")
            break
        attempts += 1
        write(f"Incorrect OTP. {max_attempts - attempts} attempt(s) left.")
    else:
        write("Account locked for 30 minutes.")
        return False
    return True


def verify_otp_for(correct_otp, read=input, write=print, max_attempts=3):
    for attempt_index in range(max_attempts):
        while True:
            entered = read("Enter OTP: ").strip()
            if entered == "":
                write("Blank entry: please try again; no attempt used.")
                continue
            break
        if entered == correct_otp:
            write("OTP verified.")
            break
        write(f"Incorrect OTP. {max_attempts - attempt_index - 1} attempt(s) left.")
    else:
        write("Account locked for 30 minutes.")
        return False
    return True


def verify_otp_with_security(correct_otp, security_answer, read=input, write=print):
    attempts, attempt_limit = 0, 3
    extra_attempts_granted = False
    while attempts < attempt_limit:
        entered = read("Enter OTP: ").strip()
        if not entered:
            write("Blank entry: no attempt used.")
            continue
        if entered == correct_otp:
            write("OTP verified.")
            return True
        attempts += 1
        write("Incorrect OTP.")
        if attempts == 3 and not extra_attempts_granted:
            answer = read("Security answer for two extra attempts: ").strip()
            if answer.casefold() == security_answer.casefold():
                attempt_limit += 2
                extra_attempts_granted = True
                write("Security answer accepted. Two extra attempts granted.")
            else:
                break
    else:
        write("Account locked for 30 minutes.")
        return False
    write("Account locked for 30 minutes.")
    return False


# Q3: Registration validation without regular expressions

def normalize_registration(raw):
    return "".join(raw.strip().upper().replace("-", "").split())


def validate_registration(raw):
    value = normalize_registration(raw)
    if len(value) not in (9, 10):
        return False, value
    if not (value[0:2].isalpha() and value[2:4].isdigit()):
        return False, value
    series_length = len(value) - 8
    if not value[4:4 + series_length].isalpha():
        return False, value
    if not value[4 + series_length:].isdigit():
        return False, value
    return True, value


def format_registration(raw):
    valid, value = validate_registration(raw)
    if not valid:
        raise ValueError("Invalid vehicle registration number")
    series_length = len(value) - 8
    return f"{value[:2]} {value[2:4]} {value[4:4 + series_length]} {value[-4:]}"


# Q4: Statement construction and benchmark

def build_with_plus(records):
    statement = ""
    for index, record in enumerate(records, start=1):
        statement += f"{index}. {record}\n"
    return statement


def build_with_join(records):
    parts = []
    for index, record in enumerate(records, start=1):
        parts.append(f"{index}. {record}\n")
    return "".join(parts)


def build_with_fstring_lines(records):
    return "".join(
        f"{index}. {record}\n"
        for index, record in enumerate(records, start=1)
    )


def benchmark_statements(count=100_000):
    records = [f"Call/SMS record {i}" for i in range(count)]
    outputs = {}
    for label, builder in (
        ("repeated +=", build_with_plus),
        ("list + join", build_with_join),
        ("f-string lines + join", build_with_fstring_lines),
    ):
        start = perf_counter()
        outputs[label] = builder(records)
        print(f"{label:24s}: {perf_counter() - start:.6f} seconds")
    assert outputs["repeated +="] == outputs["list + join"] == outputs["f-string lines + join"]


# Q5: Safe orders and scope

def add_item_buggy(item, order=[]):
    order.append(item)
    return order


def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order


def create_order(*items, customer="Walk-in", tax_rate=0.05):
    subtotal = sum(price for _, price in items)
    tax = subtotal * tax_rate
    return customer, [name for name, _ in items], round(subtotal, 2), round(tax, 2), round(subtotal + tax, 2)


canteen_total = 0


def add_to_daily_total(amount):
    global canteen_total
    canteen_total += amount
    return canteen_total


def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


# Q6: Climbing stairs

plain_calls = 0


def ways_plain(n):
    global plain_calls
    plain_calls += 1
    if n < 0:
        return 0
    if n == 0:
        return 1
    return ways_plain(n - 1) + ways_plain(n - 2)


@lru_cache(maxsize=None)
def ways_memo(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_iterative(n):
    if n < 0:
        return 0
    previous, current = 1, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def q6_demo():
    global plain_calls
    plain_calls = 0
    print("Plain recursion n=10:", ways_plain(10), "calls:", plain_calls)
    ways_memo.cache_clear()
    print("Memoised n=10:", ways_memo(10), "cache:", ways_memo.cache_info())
    ways_memo.cache_clear()
    try:
        print("Memoised n=1000:", ways_memo(1000))
    except RecursionError as error:
        print("Memoised recursion at n=1000:", error)
        print("Iterative n=1000:", ways_iterative(1000))


# Q7: Revised statement builder

def build_statement_revised(records):
    return "".join(
        f"{index}. {record}\n"
        for index, record in enumerate(records, start=1)
    )


def q7_validate():
    records = ["Call 09:00 - Rs. 2.00", "SMS 09:05 - Rs. 1.00"]
    assert build_with_join(records) == build_statement_revised(records)
    print("Q7 statement output validated.")


if __name__ == "__main__":
    q1_demo()
    print("Q2: call the OTP functions interactively.")
    for sample in ("tn 09 ab 1234", "TN-09-AB-1234", "Tn09Ab1234", "TN-09-A-1234"):
        valid, normalized = validate_registration(sample)
        print(sample, "=>", normalized, valid,
              format_registration(sample) if valid else "Invalid")
    benchmark_statements()
    print("Shared default bug:", add_item_buggy("Tea"), add_item_buggy("Coffee"))
    print("Safe orders:", add_item("Tea"), add_item("Coffee"))
    print("Order:", create_order(("Idli", 30), ("Tea", 15), customer="Naresh"))
    print("Daily total:", add_to_daily_total(45))
    counter = make_counter()
    print("Nonlocal counter:", counter(), counter())
    q6_demo()
    q7_validate()
