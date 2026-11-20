# SIMATS Online Programming Lab — Assignment 2
## Python Programming: Control Flow, Strings and Functions

**Student:** Naresh Vijay R | **Register No.:** 1972260060D  
**CO Coverage:** CO2 | **Total Marks:** 50 | **Nature:** Individual | **Duration:** 1 Week

---

## Q1 — Decisions with Many Boundaries (6 Marks)

### Eight boundary-focused households

| Units | Ration card | Member >80 | Decision |
|---:|---|---|---|
| 100 | No | No | Full subsidy |
| 100 | Yes | No | Full subsidy |
| 101 | Yes | No | Partial subsidy |
| 101 | No | No | No subsidy |
| 200 | Yes | No | Partial subsidy |
| 200 | No | No | No subsidy |
| 201 | No | Yes | Special senior-age subsidy |
| 201 | Yes | No | No subsidy |

The policy is evaluated in priority order: up to 100 units receives full subsidy; 101–200 receives partial subsidy only with a ration card; above 200 receives the special senior-age subsidy only if a household member is over 80.

Independent if statements each run when their condition is true. Overlapping predicates can therefore produce two decisions. For example, units <= 100 and units <= 200 with a ration card both match an 80-unit household with a ration card. An if–elif–else chain stops after the first true branch, selecting one branch. The source includes an intentionally buggy independent-if version, a corrected independent-if version with disjoint ranges, and an if–elif–else version.

Nested conditions are clearest: first select the unit band, then check the ration card or age within that band. Python 3.10+ match-case guards can express the same ranges. A lookup table of upper limits and decisions can be useful when thresholds change frequently, but the special eligibility conditions still need band-specific checks.

## Q2 — Loops that Count Attempts (4 Marks)

The while solution maintains a counter of wrong, nonblank OTP entries. A blank entry uses continue before incrementing the counter. A correct OTP uses break. The loop else clause locks the account after normal exhaustion (three wrong entries). Pass is a no-operation placeholder and is not necessary for the core algorithm.

A plain for range(3) loop would count blank entries as iterations. The provided for implementation uses an inner while loop to re-prompt until a nonblank entry arrives. While is more natural because the number of counted attempts depends on valid user entries, not raw input events.

Incrementing before checking for blank input is a bug because blanks consume attempts. After three failures, a correct security answer increases the attempt limit to five; an incorrect answer locks the account. A recursive retry function takes O(a) time and O(a) stack space for a attempts; an iterative loop uses O(1) auxiliary space.

## Q3 — Vehicle Registration Number Validator (6 Marks)

Normalisation removes spaces and hyphens and converts letters to uppercase. Inputs such as tn 09 ab 1234, TN-09-AB-1234 and Tn09Ab1234 all normalise to TN09AB1234 and format for the receipt as **TN 09 AB 1234**.

The compact format contains two state letters, two district digits, one or two series letters, and four final digits. Validation uses only the permitted string operations and no regular expressions.

Strings are immutable, so characters cannot be changed in place. text.upper() returns a new uppercase string and leaves text unchanged. Slicing returns a new string: value[0:2] returns indexes 0 and 1; value[-4:] returns the final four characters.

## Q4 — Building Long Text: + or join()? (6 Marks)

The source implements repeated +=, list accumulation followed by join, and f-string line generation followed by join. All three produce identical output. time.perf_counter() measures the elapsed time for 100,000 records.

One measured run produced:

| Method | Elapsed time |
|---|---:|
| Repeated += | 0.0126 s |
| List + join | 0.0140 s |
| F-string lines + join | 0.0146 s |

Each method produced 2,977,785 characters. This does not prove += is universally faster: CPython can optimise some concatenation patterns, and timings vary by interpreter, machine and memory state. Benchmark the actual workload. Join remains a clear way to collect fragments and assemble once. Repeated concatenation can require new immutable string objects and copying; for output too large for memory, stream lines directly to a file.

## Q5 — Functions, Parameters and Scope (7 Marks)

In def add_item(item, order=[]), the list is created once when the function is defined. Calls omitting order share the same list. The correct pattern uses None as the default and creates a fresh list inside the function.

Positional arguments are concise when order is obvious; keyword arguments improve clarity; default parameters make common values optional. Multiple values can be returned as a tuple and unpacked by the caller.

A local name belongs to a function call. A global name is defined at module level; rebinding it inside a function requires global. A nonlocal name belongs to an enclosing function; nonlocal allows a nested function to rebind it. The source demonstrates global daily totals and a nonlocal closure counter.

## Q6 — Recursion and Its Limits (8 Marks)

Let W(n) count ways to climb n steps using 1- or 2-step moves. Base cases: W(0)=1 and W(n)=0 for n<0. Recursive case: W(n)=W(n-1)+W(n-2).

Plain recursion repeats the same subproblems and grows exponentially (O(2^n) upper-bound description). lru_cache memoisation stores results, reducing the work to O(n) time and O(n) cache space.

Memoisation does not remove recursive call depth. The recursive n=1000 call may raise RecursionError under Python's default recursion limit. The source catches this and runs an iterative alternative, which takes O(n) time and O(1) auxiliary space and is preferable for deployment at 1,000 steps.

## Q7 — Day-4 Design Challenge (13 Marks)

**A. Diagnose:** Q4 statement generation is selected. Repeatedly extending a large immutable string may cause repeated allocation and copying.

**B. Objective:** Generate identical statement text while reducing avoidable copying and supporting more than 100,000 records.

**C. Revised design:** Build each formatted line independently and join all fragments once. The source implements build_statement_revised().

**D. Prediction:** Join should scale predictably; both old and revised methods must produce identical output. Complexity is O(N) in total output characters, plus O(N) storage for the final result.

**E. Validation:** The source compares outputs and uses an assertion to verify equality. It measures elapsed time using perf_counter. Re-run locally if your instructor requires machine-specific timing evidence.

**F. Defence:** The join-based solution matches the immutable-string model, is readable and testable. If the output becomes too large for memory, stream each line to a file rather than creating one giant string.

## Conclusion

The assignment demonstrates mutually exclusive decision logic, correct retry counting, string normalisation, performance measurement, safe default arguments, variable scope, recursion and memoisation. Q7 validates the redesigned statement builder by checking output equivalence and measuring performance.

**Before submission:** execute the source, review each answer, and add any instructor-required screenshots or locally measured evidence.
