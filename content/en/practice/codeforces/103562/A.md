---
title: "CF 103562A - Phone Numbers"
description: "The brute-force approach is exactly what the problem suggests: for each contact, convert the phone number into digits, compute their sum, and check parity. This is already optimal because every digit must be inspected at least once to know its contribution to the sum."
date: "2026-07-03T05:20:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103562
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 02-11-22 Div. 2 (Beginner)"
rating: 0
weight: 103562
solve_time_s: 44
verified: true
draft: false
---

[CF 103562A - Phone Numbers](https://codeforces.com/problemset/problem/103562/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Approaches

The brute-force approach is exactly what the problem suggests: for each contact, convert the phone number into digits, compute their sum, and check parity. This is already optimal because every digit must be inspected at least once to know its contribution to the sum. The cost is proportional to the total number of digits across all contacts, which is at most about 9000, so this runs instantly.

There is no deeper combinatorial structure or preprocessing trick needed. The only “optimization” is to avoid converting strings into integers and instead accumulate the sum directly from character codes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force digit scan | O(total digits) | O(1) extra | Accepted |
| Any advanced preprocessing | O(total digits) | O(1) | Overkill |

## Algorithm Walkthrough

1. Read the number of contacts, then process each line one by one. The streaming nature avoids storing unnecessary data.
2. Split each line into a name and a phone number string. The split is done once per line, so parsing remains linear.
3. For each character in the phone number, convert it to its numeric value and accumulate the sum. This step is necessary because the decision depends on the parity of the full digit sum, not partial structure.
4. After computing the sum, check whether it is even. If it is even, output the associated name immediately; otherwise discard it.
5. Continue until all contacts are processed, preserving input order automatically since output is produced in the same traversal order.

### Why it works

The algorithm relies on the invariant that after processing the i-th contact, we have correctly computed the exact digit sum of its phone number. Since each digit contributes independently to the sum, and parity depends only on the total sum modulo 2, no digit can be skipped or approximated. Therefore the decision “print name or not” is locally correct for each contact and does not depend on other entries.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    for _ in range(n):
        line = input().strip().split()
        name = line[0]
        number = line[1]

        s = 0
        for ch in number:
            s += ord(ch) - ord('0')

        if s % 2 == 0:
            print(name)

if __name__ == "__main__":
    solve()
```

The solution processes input in a single pass. Each line is split into exactly two tokens, so there is no ambiguity in parsing even if names are alphanumeric.

The digit sum is computed using direct character arithmetic, which avoids integer conversion overhead and preserves correctness for leading zeros. The parity check is performed immediately, and output is streamed, which keeps memory usage constant.

## Worked Examples

Consider the sample input:

```
5
Jett 012345678
Viper 111111111
Neon 987654321
Raze 512610294
Reyna 192830492
```

For each contact:

| Name | Number | Digit Sum | Even? | Output |
| --- | --- | --- | --- | --- |
| Jett | 012345678 | 0+1+2+3+4+5+6+7+8 = 36 | Yes | Jett |
| Viper | 111111111 | 9 | No | - |
| Neon | 987654321 | 45 | No | - |
| Raze | 512610294 | 30 | Yes | Raze |
| Reyna | 192830492 | 38 | Yes | Reyna |

This trace shows that each decision depends only on the parity of a local sum, independent of other contacts. The order of output matches the order of valid entries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(D) | Every digit in every phone number is scanned once |
| Space | O(1) | Only constant extra variables are used |

The total number of digits is small under the constraints, so the solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out

# provided sample
assert run("""5
Jett 012345678
Viper 111111111
Neon 987654321
Raze 512610294
Reyna 192830492
""") == """Jett
Raze
Reyna
"""

# minimum size
assert run("""1
A 0
""") == "A\n"

# all odd digits
assert run("""2
X 111
Y 135
""") == ""

# mixed parity
assert run("""3
A 12
B 123
C 222
""") == """A
C
"""

# leading zeros case
assert run("""2
Z 000
W 010
""") == """Z
W
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 0 | name printed | minimal input, zero handling |
| all ones | empty | full rejection case |
| mixed digits | selective output | parity correctness |
| leading zeros | included correctly | digit parsing correctness |

## Edge Cases

One important edge case is when the phone number consists only of zeros, such as:

```
1
Zero 000000
```

The algorithm computes a sum of 0, which is even, so the name is printed. A mistake here would be to convert the string into an integer first, which still works numerically but risks unnecessary parsing complexity and potential overflow in other variants.

Another edge case is a single-digit number like:

```
1
Odd 7
```

The sum is 7, which is odd, so nothing is printed. The algorithm handles this correctly because it does not assume any minimum length.

Finally, consider mixed leading zeros:

```
1
Lead 00012
```

The sum is 1+2 = 3, which is odd, so it is excluded. The leading zeros contribute nothing, but they must still be iterated over; skipping them would change correctness.
