---
title: "CF 411A - Password Check"
description: "We are asked to check whether a password string is \"complex enough\" based on four criteria. The password is a sequence of up to 100 characters containing uppercase letters, lowercase letters, digits, and a few special characters."
date: "2026-06-07T02:15:35+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 411
codeforces_index: "A"
codeforces_contest_name: "Coder-Strike 2014 - Qualification Round"
rating: 800
weight: 411
solve_time_s: 254
verified: true
draft: false
---

[CF 411A - Password Check](https://codeforces.com/problemset/problem/411/A)

**Rating:** 800  
**Tags:** *special, implementation  
**Solve time:** 4m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to check whether a password string is "complex enough" based on four criteria. The password is a sequence of up to 100 characters containing uppercase letters, lowercase letters, digits, and a few special characters. A password is acceptable if it is at least five characters long, contains at least one uppercase letter, at least one lowercase letter, and at least one digit.

The input consists of a single line with the password. The output is a single message: "Correct" if the password meets all requirements, and "Too weak" otherwise.

The constraints are very small. A maximum of 100 characters means we can afford to examine each character individually multiple times without worrying about performance. This rules out any concern for optimizing to sub-linear scans.

The subtlety is in checking all four conditions carefully. A naive approach that only checks for length or only checks for letters without considering digits could produce wrong results. For instance, the input `Abc!` is too short, even though it contains both cases and a special character. The input `abcdef` is long and contains lowercase letters, but it lacks uppercase letters and digits, so it should be rejected. This shows that partial compliance is not enough, and all four conditions must be verified.

## Approaches

The brute-force approach is straightforward: we check each condition independently. First, we measure the password length. Next, we scan the string to see if it contains at least one uppercase letter, at least one lowercase letter, and at least one digit. This can be done with four separate scans over the string, or with a single pass tracking all four flags. Since the password length is capped at 100, four scans would perform at most 400 character examinations, which is negligible.

The key insight that simplifies the implementation is that we can check all character-type requirements in a single pass. We maintain three boolean flags, one for uppercase, one for lowercase, and one for digits. As we iterate through the string, we update these flags accordingly. If all flags are set by the end of the pass and the length is sufficient, the password is valid. This avoids multiple iterations and is conceptually simpler.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (multiple passes) | O(n) | O(1) | Accepted |
| Optimal (single pass) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the password string. The first thing to check is the length. If it is less than 5 characters, immediately return "Too weak" because no further checks can make the password valid.
2. Initialize three boolean variables: `has_upper`, `has_lower`, and `has_digit`. These will track whether the password contains at least one character of each required type.
3. Iterate over each character of the password. If the character is an uppercase letter, set `has_upper` to `True`. If it is a lowercase letter, set `has_lower` to `True`. If it is a digit, set `has_digit` to `True`.
4. After the loop, check all four conditions: length, `has_upper`, `has_lower`, and `has_digit`. If all are satisfied, print "Correct". Otherwise, print "Too weak".

Why it works: The algorithm maintains three boolean flags that represent the presence of required character types. Iterating through the string ensures that each character is evaluated exactly once. By combining this with the length check, we guarantee that no password can be falsely accepted, and all valid passwords are correctly recognized.

## Python Solution

```python
import sys
input = sys.stdin.readline

password = input().strip()

if len(password) < 5:
    print("Too weak")
else:
    has_upper = False
    has_lower = False
    has_digit = False
    
    for ch in password:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True
    
    if has_upper and has_lower and has_digit:
        print("Correct")
    else:
        print("Too weak")
```

The solution starts by trimming whitespace to handle any accidental leading or trailing spaces. Length is checked first to quickly reject obviously short passwords. Three flags track character types. Using `isupper()`, `islower()`, and `isdigit()` avoids manually comparing character ranges, which is safer and more readable. Finally, the result is determined by evaluating all four conditions in a single logical expression.

## Worked Examples

**Sample Input 1**: `abacaba`

| Character | has_upper | has_lower | has_digit |
| --- | --- | --- | --- |
| a | False | True | False |
| b | False | True | False |
| a | False | True | False |
| c | False | True | False |
| a | False | True | False |
| b | False | True | False |
| a | False | True | False |

Length = 7, has_upper = False, has_lower = True, has_digit = False → Output: Too weak

**Custom Input 2**: `A1b2C`

| Character | has_upper | has_lower | has_digit |
| --- | --- | --- | --- |
| A | True | False | False |
| 1 | True | False | True |
| b | True | True | True |
| 2 | True | True | True |
| C | True | True | True |

Length = 5, all flags True → Output: Correct

The tables show that the algorithm tracks all required flags correctly through the iteration and only accepts passwords that satisfy all conditions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through the string of length n (≤100) |
| Space | O(1) | Only three boolean flags used, no additional structures |

The time complexity is linear, but since n ≤ 100, this is effectively constant. Space usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    password = input().strip()
    if len(password) < 5:
        print("Too weak")
    else:
        has_upper = has_lower = has_digit = False
        for ch in password:
            if ch.isupper():
                has_upper = True
            elif ch.islower():
                has_lower = True
            elif ch.isdigit():
                has_digit = True
        if has_upper and has_lower and has_digit:
            print("Correct")
        else:
            print("Too weak")
    return output.getvalue().strip()

# Provided sample
assert run("abacaba") == "Too weak", "sample 1"

# Custom cases
assert run("A1b2C") == "Correct", "mixed chars, exact length"
assert run("abc") == "Too weak", "too short"
assert run("ABCDE") == "Too weak", "uppercase only"
assert run("abcde123") == "Too weak", "missing uppercase"
assert run("Ab1!") == "Too weak", "exact 4 chars, fails length"
assert run("Abcdef1") == "Correct", "long enough, meets all"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| A1b2C | Correct | All criteria satisfied, minimal length 5 |
| abc | Too weak | Short length, missing uppercase and digit |
| ABCDE | Too weak | Uppercase only, missing lowercase and digit |
| abcde123 | Too weak | Missing uppercase |
| Ab1! | Too weak | Length < 5 |
| Abcdef1 | Correct | Longer password, all conditions met |

## Edge Cases

The edge cases mainly involve borderline lengths and combinations of character types. For `Ab1!`, the algorithm first checks length, immediately rejecting it without needing to check the character types, demonstrating short-circuit evaluation. For a password like `ABCDE`, the algorithm tracks uppercase correctly but finds lowercase and digit flags remain false, ensuring it outputs "Too weak". This confirms that the approach handles both length and character-type boundaries without off-by-one errors or missed conditions.
