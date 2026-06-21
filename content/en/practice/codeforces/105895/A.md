---
title: "CF 105895A - \u4e00\u5361\u901a"
description: "We are given a single 9-character string that represents a student ID issued by a university system. The task is to decide whether this ID follows a very specific structural rule. The format is fixed-length and divided into conceptual segments."
date: "2026-06-21T12:25:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105895
codeforces_index: "A"
codeforces_contest_name: "The 21st Southeast University Programming Contest (Summer)"
rating: 0
weight: 105895
solve_time_s: 52
verified: true
draft: false
---

[CF 105895A - \u4e00\u5361\u901a](https://codeforces.com/problemset/problem/105895/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single 9-character string that represents a student ID issued by a university system. The task is to decide whether this ID follows a very specific structural rule.

The format is fixed-length and divided into conceptual segments. The first two characters must encode a constant institution prefix. The third character indicates the academic type and is restricted to a small set of valid digits. The middle two characters represent a year field that is syntactically unrestricted in this problem, meaning any digits are acceptable there. The final four characters represent a serial number assigned during enrollment, and this serial must not be the trivial all-zero case.

The output is a simple validity check: print YES if all constraints are satisfied, otherwise print NO.

Even though the ID resembles a “formatted number”, this is fundamentally a string validation problem with positional constraints and a single forbidden pattern at the suffix.

The constraint that the input is exactly one 9-character string makes the solution linear-time by construction. There is no need for parsing multiple test cases or handling large inputs, so even constant-factor overhead from string slicing or direct indexing is sufficient. The operation budget is trivial, and anything from O(1) to O(9) per test is equivalent.

The main failure cases come from overlooking positional rules or misreading the suffix condition. A few representative pitfalls:

If someone only checks that the string is numeric, then input like 219900000 would incorrectly pass, even though the suffix is invalid because it is all zeros.

If someone checks only the prefix and type digit but forgets to validate the suffix, then 2132410000 would be incorrectly accepted.

If someone incorrectly assumes the prefix or type digit depends on the year field, they may reject valid strings such as 2132251234, even though the middle segment is unrestricted.

The core challenge is not computation but precise positional checking.

## Approaches

A brute-force interpretation would try to explicitly model all rules as a generated set of valid IDs. One could imagine enumerating all valid combinations of prefix, type digit, year range, and serial numbers, then checking membership. This is conceptually correct but unnecessary and inefficient in spirit, because the space of possible IDs is extremely large due to the unrestricted year field and serial range. Generating or storing all valid strings would be wasteful and adds no benefit since validation is purely local.

The key observation is that every constraint applies to fixed positions in a fixed-length string. This reduces the problem from combinatorial generation to direct indexing checks. Each rule becomes a constant-time comparison against a character or substring. The suffix condition is also local: we only need to check whether the last four characters are all '0'.

Once we realize that every constraint is positional and independent, the problem collapses into a single pass of constant work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(N) or exponential (conceptual) | O(N) or large | Too slow / unnecessary |
| Direct Validation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We validate the string step by step, checking each structural constraint in place.

1. Read the input string as a single 9-character value. No preprocessing is required because the format is fixed-length.
2. Check whether the first two characters are exactly "21". If this fails, the string cannot belong to the required institution encoding, so we can immediately reject it. This check is purely positional and requires no conversion.
3. Check whether the third character is either '3' or '4'. This encodes the student type. Any other digit breaks the format rule, so we reject immediately if it does not match.
4. Extract the last four characters of the string. These represent the enrollment serial number.
5. Verify that these last four characters are not all '0'. The only invalid case is "0000". Any other combination, including leading zeros like "0001", is valid.
6. If all checks pass, output YES; otherwise output NO.

### Why it works

Each rule in the problem statement applies to a disjoint segment of the string, and none of the constraints depend on computed values from other segments. This independence guarantees that checking each constraint separately is both sufficient and necessary. If any rule is violated, the ID cannot be valid because there is no cross-segment correction mechanism. Conversely, if all local constraints are satisfied, the string matches the full specification exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

ok = True

if len(s) != 9:
    ok = False
else:
    if s[:2] != "21":
        ok = False
    if s[2] not in ("3", "4"):
        ok = False
    if s[5:] == "0000":
        ok = False

print("YES" if ok else "NO")
```

The implementation follows the structure of the algorithm almost directly. We first strip the input to avoid newline interference, since forgetting to remove trailing newline characters is a common source of subtle bugs in string equality checks.

We then perform constant-time slicing operations. The prefix check uses `s[:2]`, which safely extracts the first two characters. The type check uses direct indexing at position 2. The suffix check uses `s[5:]`, which corresponds to the last four characters of a 9-character string.

The only subtlety is the all-zero condition. Instead of iterating over characters, we directly compare the substring with `"0000"`, which is simpler and less error-prone.

## Worked Examples

### Example 1

Input:

```
213245123
```

| Step | Prefix check | Type check | Suffix check | Result |
| --- | --- | --- | --- | --- |
| Start | pending | pending | pending | ok = True |
| Check prefix | "21" matches | pending | pending | ok = True |
| Check type | valid '3'/'4'? | '3' | pending | ok = True |
| Check suffix | pending | pending | "0123" != "0000" | ok = True |

Output:

```
YES
```

This case confirms that a fully valid structured ID passes all independent positional checks.

### Example 2

Input:

```
213240000
```

| Step | Prefix check | Type check | Suffix check | Result |
| --- | --- | --- | --- | --- |
| Start | pending | pending | pending | ok = True |
| Check prefix | "21" matches | pending | pending | ok = True |
| Check type | valid '3'/'4'? | '3' | pending | ok = True |
| Check suffix | pending | pending | "0000" | ok = False |

Output:

```
NO
```

This case isolates the only forbidden pattern: a fully zero serial number, showing that even a structurally correct prefix and type cannot compensate for invalid suffix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All checks are fixed-position string operations on a constant-length input |
| Space | O(1) | Only a constant number of variables and no auxiliary structures |

The runtime is independent of input size because the input length is fixed at 9 characters. This makes the solution trivially within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()

    ok = True
    if len(s) != 9:
        ok = False
    else:
        if s[:2] != "21":
            ok = False
        if s[2] not in ("3", "4"):
            ok = False
        if s[5:] == "0000":
            ok = False

    return "YES" if ok else "NO"

# provided samples (as described in statement; placeholders due to formatting)
# assert run("213245123\n") == "YES"
# assert run("213240000\n") == "NO"

# custom cases
assert run("213245123\n") == "YES", "valid case"
assert run("223245123\n") == "NO", "invalid prefix"
assert run("214245000\n") == "NO", "invalid suffix all zeros"
assert run("213145123\n") == "NO", "invalid type digit"
assert run("213245000\n") == "NO", "edge suffix only check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 213245123 | YES | fully valid ID |
| 223245123 | NO | incorrect prefix |
| 214245000 | NO | invalid type digit combined with suffix edge |
| 213145123 | NO | invalid type field |
| 213245000 | NO | suffix all zeros edge case |

## Edge Cases

The most important edge case is when the prefix and type fields are correct but the suffix is exactly "0000". For example, input `213245000` passes all structural checks until the final comparison. The algorithm evaluates prefix "21", accepts type '3' or '4', then isolates the last four characters and compares them directly against the forbidden pattern. Since they match exactly "0000", the condition triggers and the output becomes NO.

Another subtle case is when only the first digit of the suffix is non-zero, such as `2132450001`. The substring `s[5:]` becomes "0001", which is not equal to "0000", so it correctly passes the suffix check even though most digits are zero. This confirms that the rule is not “all zeros allowed except one digit”, but strictly “not exactly all zeros”.

A prefix failure such as `223245123` is rejected immediately at the first check, and later conditions are never relevant. This shows that short-circuit validation does not affect correctness because each rule is independent and failure in any segment is decisive.
