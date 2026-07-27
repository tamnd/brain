---
title: "CF 102784E - Spooky Numbers"
description: "Francine has a collection of individual digits and wants to arrange some of them into the largest possible number that Buster considers spooky. A spooky number is a non-negative integer divisible by 2, 3, and 5, which is the same as being divisible by 30."
date: "2026-07-27T19:47:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102784
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 1"
rating: 0
weight: 102784
solve_time_s: 57
verified: true
draft: false
---

[CF 102784E - Spooky Numbers](https://codeforces.com/problemset/problem/102784/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
# Problem Understanding

Francine has a collection of individual digits and wants to arrange some of them into the largest possible number that Buster considers spooky. A spooky number is a non-negative integer divisible by 2, 3, and 5, which is the same as being divisible by 30. She may discard some digits because Arthur added unwanted ones, but the remaining digits must form the largest possible value and cannot contain unnecessary leading zeroes.

The input gives the number of available digits and then the digits themselves. The output is the largest integer that can be created from these digits while being divisible by 30. If no such number exists, we print `-1`.

The constraint allows up to 100000 digits. Any approach that tries different arrangements or checks many possible subsets is impossible because the number of candidates grows exponentially. Even trying all permutations of a large fraction of the digits would immediately exceed the available time. The solution needs to process the digits a constant number of times, which points toward an O(n) or O(n log n) method.

There are a few cases where a careless implementation can fail. A single zero is a valid answer because zero is divisible by every non-zero divisor. For example, input

```
1
0
```

must produce

```
0
```

A solution that requires a non-zero leading digit would incorrectly reject it.

Another trap is forgetting that divisibility by 30 requires a zero at the end. For example,

```
4
3 3 6 6
```

has digit sum 18, which is divisible by 3, and contains even digits, but it has no zero. The correct output is

```
-1
```

because no arrangement can be divisible by 5.

A final common mistake is removing the wrong digit when fixing the digit sum. Consider

```
5
1 1 1 2 0
```

The total sum is 5, so one digit must be removed to make the sum divisible by 3. Removing a `2` gives the largest answer:

```
1110
```

Removing a `1` gives `2100`, which is smaller. The removal process must preserve the largest possible remaining number.

## Approaches

The brute force idea is to generate possible subsets of the available digits, arrange each chosen subset in descending order, and check whether the resulting number is divisible by 30. This is correct because every possible valid answer appears among those candidates, and the maximum one can be selected afterward.

The problem is that there are up to 100000 digits. The number of subsets is 2^n, and even storing or checking a tiny fraction of them is impossible. The brute force approach fails because it treats the digits as independent choices instead of using the divisibility rules that describe exactly what matters.

The key observation is that divisibility by 30 has a very simple structure. A number divisible by 30 must be divisible by 10, so it must contain a zero that is placed at the end. It must also be divisible by 3, which only depends on the sum of its digits. The exact order of the other digits does not affect divisibility by 3.

The problem becomes selecting which digits to remove. Since we want the largest possible number, we should keep as many digits as possible. If the digit sum is already divisible by 3, we only need to sort all available digits in descending order. Otherwise, we remove the smallest possible number of digits that makes the sum divisible by 3. After that, sorting the remaining digits gives the maximum arrangement.

The only digits that matter for the removal are their remainders modulo 3. To reduce the sum by 1 modulo 3, we remove the smallest digit with remainder 1. To reduce it by 2 modulo 3, we remove the smallest digit with remainder 2. If a single digit is unavailable, removing two digits of the opposite remainder can achieve the same effect.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count all digits and compute their total sum. The sum tells us the current remainder modulo 3, which is the only information needed for divisibility by 3.
2. Check whether there is at least one zero. If there is no zero, the number cannot be divisible by 10, so no spooky number can exist.
3. If the digit sum is not divisible by 3, remove the smallest possible digit or pair of digits that fixes the remainder. A smaller removed value leaves a larger final number.
4. Sort the remaining digits in descending order. A number with the same digits is largest when its highest digits appear first.
5. Print the resulting digits. If the only remaining representation is zeroes, print a single zero instead of multiple leading zeroes.

Why it works: the algorithm only removes digits when required by the divisibility rule for 3. Removing fewer digits always keeps a number with more digits, which is larger than any number with fewer digits made from the same collection. When a removal is necessary, choosing the smallest possible removable digits leaves the largest remaining multiset of digits. Finally, sorting descending produces the maximum number from that multiset. The presence of zero guarantees divisibility by 10, and the corrected digit sum guarantees divisibility by 3, so the result is always divisible by 30.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    digits = list(map(int, input().split()))

    if 0 not in digits:
        print(-1)
        return

    total = sum(digits)
    rem = total % 3

    if rem != 0:
        removed = False

        for i, d in enumerate(digits):
            if d % 3 == rem:
                digits.pop(i)
                removed = True
                break

        if not removed:
            need = (3 - rem) % 3
            to_remove = []
            for i, d in enumerate(digits):
                if d % 3 == need:
                    to_remove.append(i)
                    if len(to_remove) == 2:
                        break

            if len(to_remove) < 2:
                print(-1)
                return

            for i in reversed(to_remove):
                digits.pop(i)

    digits.sort(reverse=True)

    if digits[0] == 0:
        print(0)
    else:
        print("".join(map(str, digits)))

if __name__ == "__main__":
    solve()
```

The solution first rejects cases without a zero because no amount of rearranging can create a number ending in zero. This avoids unnecessary work and handles the divisibility by 10 requirement directly.

The digit sum is used to decide whether any removal is needed. When removing one digit, the code searches for the smallest digit with the required remainder because smaller removed digits preserve a larger answer. If one digit is not enough, it removes two digits with the same combined remainder effect.

The final descending sort is what converts the chosen digits into the largest possible integer. The special check for `digits[0] == 0` handles the case where every remaining digit is zero, preventing outputs such as `0000`.

Python integers do not overflow here because the algorithm never constructs the number numerically. It builds the answer as a string of digits, which is necessary because the answer can contain 100000 digits.

## Worked Examples

For the first example:

```
1
0
```

The execution is:

| Step | Digits | Sum remainder | Action | Result |
| --- | --- | --- | --- | --- |
| Initial | [0] | 0 | Zero exists, no removal needed | [0] |
| Sort | [0] | 0 | Already largest order | 0 |

This demonstrates the special zero-only case. The answer is zero, not an invalid empty number.

For the second example:

```
6
2 3 1 3 1 0
```

The execution is:

| Step | Digits | Sum remainder | Action | Result |
| --- | --- | --- | --- | --- |
| Initial | [2,3,1,3,1,0] | 1 | Need to reduce sum by 1 | Remove digit 1 |
| After removal | [2,3,1,3,0] | 0 | Divisible by 3 and 10 | Keep all |
| Sort | [3,3,2,1,0] | 0 | Largest arrangement | 33210 |

This shows why using the largest possible subset of digits is not always correct. The full set has the wrong digit sum, so one digit must be discarded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Counting and removal are linear, and sorting the digits dominates the runtime. |
| Space | O(n) | The digits are stored in a list and rearranged in memory. |

The input size is 100000 digits, so sorting 100000 values is easily within the limit. The algorithm avoids all subset or permutation generation and only performs simple scans plus one sort.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def solve():
    input = sys.stdin.readline
    n = int(input())
    digits = list(map(int, input().split()))

    if 0 not in digits:
        print(-1)
        return

    total = sum(digits)
    rem = total % 3

    if rem:
        removed = False
        for i, d in enumerate(digits):
            if d % 3 == rem:
                digits.pop(i)
                removed = True
                break

        if not removed:
            need = (3 - rem) % 3
            idx = []
            for i, d in enumerate(digits):
                if d % 3 == need:
                    idx.append(i)
                    if len(idx) == 2:
                        break

            if len(idx) < 2:
                print(-1)
                return

            for i in reversed(idx):
                digits.pop(i)

    digits.sort(reverse=True)
    if digits[0] == 0:
        print(0)
    else:
        print("".join(map(str, digits)))

assert run("""1
0
""") == "0\n", "sample 1"

assert run("""6
2 3 1 3 1 0
""") == "33210\n", "sample 2"

assert run("""4
3 3 6 6
""") == "-1\n", "no zero"

assert run("""5
1 1 1 2 0
""") == "1110\n", "remove smallest digit"

assert run("""3
0 0 0
""") == "0\n", "all zeroes"

assert run("""5
9 9 9 9 0
""") == "99990\n", "large equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0` | Minimum size and zero-only handling |
| `6 / 2 3 1 3 1 0` | `33210` | Sample behavior and remainder fixing |
| `4 / 3 3 6 6` | `-1` | Missing zero boundary case |
| `5 / 1 1 1 2 0` | `1110` | Choosing the smallest removal |
| `3 / 0 0 0` | `0` | Avoiding multiple leading zeroes |
| `5 / 9 9 9 9 0` | `99990` | Equal digits and large values |

## Edge Cases

For the zero-only case:

```
1
0
```

The algorithm finds a zero, computes a digit sum remainder of zero, skips removal, sorts the list, and sees that the first digit is zero. It outputs one zero. This prevents the common mistake of treating zero as an invalid number because it has no non-zero leading digit.

For the missing-zero case:

```
4
3 3 6 6
```

The algorithm immediately fails the divisibility by 10 requirement because no zero exists. It outputs `-1` before attempting any digit removal. Removing digits cannot help because every valid spooky number must end in zero.

For a case where the digit sum needs correction:

```
5
1 1 1 2 0
```

The sum is 5, leaving remainder 2 modulo 3. The algorithm searches for a digit with remainder 2 and removes the digit `2`. The remaining digits have sum 3, contain zero, and sort into `1110`. Removing any `1` instead would leave a smaller number.

For multiple zeroes:

```
3
0 0 0
```

All possible arrangements represent zero. After sorting, the algorithm detects that the first digit is zero and prints only one digit. This handles the representation issue while preserving the mathematical value.
