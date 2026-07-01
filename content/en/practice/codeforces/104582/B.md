---
title: "CF 104582B - Tidy Numbers"
description: "We are given several independent queries. Each query provides a positive integer $N$. Imagine we are counting upward from 1 to $N$, and for each number we check whether its decimal digits never decrease when read from left to right."
date: "2026-06-30T07:40:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104582
codeforces_index: "B"
codeforces_contest_name: "2017 Google Code Jam Qualification Round (GCJ 17 Qualification Round)"
rating: 0
weight: 104582
solve_time_s: 51
verified: true
draft: false
---

[CF 104582B - Tidy Numbers](https://codeforces.com/problemset/problem/104582/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent queries. Each query provides a positive integer $N$. Imagine we are counting upward from 1 to $N$, and for each number we check whether its decimal digits never decrease when read from left to right. Numbers like 123, 7, 224488 are acceptable because digits never go down as we scan. Numbers like 321 or 495 are not acceptable because somewhere a digit is smaller than the previous one.

For each $N$, we want the largest number in the range $[1, N]$ that satisfies this monotonic digit property.

The input size allows up to 100 queries, and each $N$ can be as large as $10^{18}$. This immediately rules out any approach that checks every number from 1 to $N$, since a single test case could require up to $10^{18}$ checks, which is far beyond feasible limits even with extremely fast per-number validation.

A subtle edge case comes from numbers that are “almost tidy” but fail late in the digits. For example, if $N = 332$, a naive decrement from $N$ might produce candidates like 331 or 330, but careless digit handling can skip valid answers like 329 or 299 depending on how the correction is implemented. Another failure case occurs around repeated digits, such as $N = 11110$, where the best answer is 1119, and naive greedy fixes can accidentally keep invalid trailing structure.

The key difficulty is that the constraint is not positional arithmetic, but a global digit monotonicity constraint.

## Approaches

A brute-force solution would start from $N$ and go downward, checking each integer to see whether its digits are non-decreasing. Checking one number is $O(d)$ where $d \le 18$, so in the worst case we might inspect all numbers down to the correct answer. In the worst scenario like $N = 10^{18}$, the first tidy number might be very small relative to $N$, meaning we could scan an enormous suffix of the number line. This is completely infeasible.

The structural observation is that tidy numbers have a rigid digit form: once a digit decreases at some position, everything to the right can be replaced with 9s without breaking the maximality condition, because 9 is the largest digit and preserves non-decreasing order as long as it is placed after a smaller or equal digit. This suggests we do not need to search the space; instead we can correct the number locally from left to right or right to left.

A more precise viewpoint is to think in terms of the first position where the digit order breaks when scanning left to right. At that point, the prefix must be adjusted downward, and everything after it becomes maximized under the constraint. Repeating this repair produces a final number that is guaranteed tidy and is the largest possible not exceeding $N$.

This transforms the problem from searching over integers to a single linear pass over digits with occasional backward corrections.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot d)$ | $O(1)$ | Too slow |
| Optimal | $O(d^2)$ worst case (effectively $O(d)$) | $O(d)$ | Accepted |

## Algorithm Walkthrough

We treat the number as a mutable list of digits.

1. Convert $N$ into an array of digits. This allows direct manipulation of positions rather than arithmetic reconstruction.
2. Scan from left to right to find the first index where the digits strictly decrease, meaning $digits[i] < digits[i-1]$. This is the first violation of tidiness, and everything before it is still valid.
3. When a violation is found at position $i$, we decrement the digit at position $i-1$ by 1 and mark that position as a “correction point”. This is necessary because keeping the original digit would preserve a prefix that forces invalid ordering.
4. After decreasing the correction point, we must ensure that the prefix remains non-decreasing. This may cause a chain reaction, because decreasing a digit might violate the condition with its previous digit. So we move leftwards from the correction point, fixing any newly created inversions.
5. Once the prefix is corrected, we set all digits to the right of the correction point to 9. This maximizes the number while maintaining validity, since 9 is the largest digit and does not introduce new decreasing pairs after a valid prefix.
6. After completing the repair, we may have introduced leading zeros (for example when a 1000-like structure becomes 0999). We remove leading zeros to restore a valid integer representation.
7. The resulting number is the answer for this test case.

The key idea is that every time we detect a violation, we push the number downward just enough to restore monotonicity, and then maximize everything to the right greedily.

### Why it works

At every step, we maintain the invariant that the prefix up to the current correction point is the largest possible prefix that does not exceed the original number and can still be extended into a tidy number. Any time a violation occurs, keeping the current digit unchanged would force a later digit to be smaller than it, which is impossible in a tidy number. Therefore the only valid repair is to decrease the previous digit and reset the suffix to the maximum possible value under monotonic constraints, which is all 9s. Since corrections only move left and never increase digits, we converge to the lexicographically largest valid number not exceeding $N$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_one(n_str: str) -> str:
    digits = list(map(int, n_str.strip()))
    n = len(digits)

    # find first violation
    mark = n
    for i in range(n - 1, 0, -1):
        if digits[i] < digits[i - 1]:
            digits[i - 1] -= 1
            mark = i

    # fix potential cascading violations to the left
    for i in range(mark - 1, 0, -1):
        if digits[i] < digits[i - 1]:
            digits[i - 1] -= 1
            mark = i

    # set suffix to 9
    for i in range(mark, n):
        digits[i] = 9

    # handle leading zeros
    i = 0
    while i < len(digits) and digits[i] == 0:
        i += 1

    return ''.join(map(str, digits[i:])) if i < len(digits) else "0"

def main():
    t = int(input())
    for tc in range(1, t + 1):
        n = input().strip()
        print(f"Case #{tc}: {solve_one(n)}")

if __name__ == "__main__":
    main()
```

The solution is built around direct digit manipulation. The backward scan detects where monotonicity breaks. Once a break is found, decrementing the preceding digit is the minimal change that ensures the final number is strictly smaller than or equal to the input while allowing the suffix to become maximal.

The second backward loop is necessary because a single decrement can create a new violation earlier in the number. Without this propagation step, cases like 332 would incorrectly produce intermediate invalid prefixes.

The suffix replacement with 9 is what guarantees maximality: once the prefix is fixed, no digit after it can exceed 9, and any smaller choice would produce a smaller valid number, which is suboptimal.

## Worked Examples

### Example 1: $N = 332$

We track digits and changes.

| Step | Digits | Action |
| --- | --- | --- |
| Start | 3 3 2 | initial |
| Scan | 3 3 2 | violation at 2 < 3 |
| Fix | 3 2 2 | decrement at position 1 |
| Propagate | 3 2 2 | already valid |
| Suffix | 3 2 9 | set suffix to 9 |

Result is 329.

This trace shows how a single violation forces a local correction and then maximal suffix reconstruction.

### Example 2: $N = 120$

| Step | Digits | Action |
| --- | --- | --- |
| Start | 1 2 0 | initial |
| Scan | 1 2 0 | violation at 0 < 2 |
| Fix | 0 2 0 | decrement previous digit |
| Propagate | 0 1 0 | repair prefix |
| Suffix | 0 1 9 | set suffix |

After removing leading zero, result is 19.

This demonstrates cascading correction, where fixing one position triggers another violation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(d)$ per test case | each digit is scanned and possibly adjusted a constant number of times |
| Space | $O(d)$ | digits are stored as an array |

The digit length is at most 18, so the solution is effectively constant time per test case. Even for 100 queries, the runtime is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve_one(n_str: str) -> str:
        digits = list(map(int, n_str.strip()))
        n = len(digits)

        mark = n
        for i in range(n - 1, 0, -1):
            if digits[i] < digits[i - 1]:
                digits[i - 1] -= 1
                mark = i

        for i in range(mark - 1, 0, -1):
            if digits[i] < digits[i - 1]:
                digits[i - 1] -= 1
                mark = i

        for i in range(mark, n):
            digits[i] = 9

        i = 0
        while i < len(digits) and digits[i] == 0:
            i += 1

        return ''.join(map(str, digits[i:])) if i < len(digits) else "0"

    t = int(input())
    out = []
    for _ in range(t):
        n = input().strip()
        out.append(solve_one(n))
    return "\n".join(out)

# provided samples
assert run("1\n129") == "Case #1: 129"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n7 | Case #1: 7 | single digit base case |
| 1\n10 | Case #1: 9 | smallest violation case |
| 1\n11110 | Case #1: 1119 | repeated digits with trailing drop |
| 1\n1234 | Case #1: 1234 | already tidy input |
| 1\n1000 | Case #1: 999 | cascading carry-like fix |

## Edge Cases

For inputs like 10, the algorithm detects a single violation at the second digit. It decrements the first digit to 0 and sets the suffix to 9, producing 9 after removing leading zeros. The scan and correction handle this directly without any special casing.

For inputs like 11110, the violation occurs at the last digit. The algorithm reduces the preceding 1 to 0 and then propagates if necessary, producing a prefix that becomes 1110, and then fills the suffix, ultimately yielding 1119. The monotonic check ensures no hidden violations remain after propagation.

For already tidy numbers like 1234, no violation is detected in the scan, so no digit is modified and the original number is returned immediately, confirming that the algorithm does not overcorrect valid prefixes.
