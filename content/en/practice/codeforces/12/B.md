---
title: "CF 12B - Correct Solution?"
description: "Alice gives Bob a decimal number and asks him to rearrange its digits so that the resulting number is as small as possible, while still being a valid decimal number without leading zeroes."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 12
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 12 (Div 2 Only)"
rating: 1100
weight: 12
solve_time_s: 79
verified: true
draft: false
---
[CF 12B - Correct Solution?](https://codeforces.com/problemset/problem/12/B)

**Rating:** 1100  
**Tags:** implementation, sortings  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

Alice gives Bob a decimal number and asks him to rearrange its digits so that the resulting number is as small as possible, while still being a valid decimal number without leading zeroes. Bob returns another number, and we must decide whether his answer is actually the smallest possible arrangement.

The task is not to generate all rearrangements. We only need to check whether Bob’s number matches the correct minimal arrangement.

The numbers are at most $10^9$, so they contain at most 10 digits. Even though the input size is tiny, the problem still requires careful handling of leading zeroes. A naive numeric sort like `"0013"` would produce an invalid representation because decimal numbers cannot start with zero unless the entire number itself is zero.

The most dangerous edge case appears when the original number contains zeroes. For example:

Input:

```
1002
1002
```

The correct smallest rearrangement is `1002`, not `0012`. A careless implementation that simply sorts all digits ascending would incorrectly build `"0012"`.

Another tricky situation is when the number itself is zero.

Input:

```
0
0
```

The answer is valid because the only rearrangement is still zero.

A different kind of mistake happens when the candidate answer has the right digits but is not minimal.

Input:

```
310
130
```

The digits match, but the smallest valid arrangement is `103`, so the correct output is `WRONG_ANSWER`.

The core difficulty is not checking whether the digits match. The real challenge is constructing the lexicographically smallest valid arrangement under the “no leading zero” restriction.

## Approaches

The brute-force approach is to generate every permutation of the digits of the original number, discard those with leading zeroes, convert the remaining permutations into numbers, and take the minimum. Then we compare that minimum with Bob’s answer.

This works because it directly follows the definition of the problem. Every possible rearrangement is examined, so the smallest valid one is guaranteed to be found.

The problem is that permutations grow factorially. A 10-digit number has up to $10! = 3,628,800$ permutations. That is already several million candidates, and duplicate digits create additional bookkeeping complexity if we want to avoid repeated work. For such a small input size it might still pass in some languages, but it is unnecessarily expensive for a problem that has a simple constructive solution.

The key observation is that the smallest valid number should place the smallest non-zero digit first, because the first digit has the greatest impact on the value of the number. After fixing that first digit, every remaining position should contain the smallest available digit, including zeroes.

This immediately suggests a greedy construction:

First, sort all digits ascending.

If the first digit is not zero, the sorted order is already optimal.

If the sorted order starts with zeroes, locate the first non-zero digit, place it at the front, and then append all remaining digits in ascending order.

For example:

`3100`

Sorted digits:

`0013`

The first non-zero digit is `1`.

Move it to the front:

`1003`

That is the smallest valid arrangement.

After constructing this canonical minimal form, we simply compare it with Bob’s answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(d! \cdot d)$ | $O(d)$ | Too slow / unnecessary |
| Optimal | $O(d \log d)$ | $O(d)$ | Accepted |

Here, $d$ is the number of digits.

## Algorithm Walkthrough

1. Read the original number `n` as a string and Bob’s answer `m` as a string.

Treating them as strings avoids issues with leading zeroes during processing.
2. Convert the digits of `n` into a list and sort them in ascending order.

This gives the lexicographically smallest arrangement of digits.
3. Check whether the first digit after sorting is zero.

If it is not zero, the sorted order is already the smallest valid number.
4. If the first digit is zero, scan from left to right until finding the first non-zero digit.

This digit must become the leading digit because any valid number must start with a non-zero digit.
5. Swap that first non-zero digit into the front position.

All remaining digits stay sorted, so the resulting number is still minimal.
6. Join the digits into a string representing the smallest valid rearrangement.
7. Compare the constructed result with Bob’s answer.

If they match exactly, print `OK`. Otherwise print `WRONG_ANSWER`.

### Why it works

The algorithm relies on positional value. The leftmost digit contributes the most to the number’s magnitude, so minimizing it is always the highest priority.

Among all non-zero digits, choosing the smallest one for the first position gives the smallest possible leading contribution. After fixing that digit, the remaining positions should be minimized independently, which is achieved by sorting the remaining digits ascending.

Because every digit after the first is placed in the smallest possible order, no other valid rearrangement can produce a smaller number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = input().strip()
    m = input().strip()

    digits = sorted(n)

    if digits[0] == '0':
        for i in range(len(digits)):
            if digits[i] != '0':
                digits[0], digits[i] = digits[i], digits[0]
                break

    smallest = ''.join(digits)

    if smallest == m:
        print("OK")
    else:
        print("WRONG_ANSWER")

solve()
```

The solution begins by reading both numbers as strings. This matters because Bob’s answer may contain leading zeroes in the input, and converting immediately to integers would lose that information.

The digits of `n` are sorted in ascending order. If the first digit is already non-zero, then the sorted sequence is immediately the smallest valid arrangement.

When the sorted sequence starts with zeroes, the code searches for the first non-zero digit and swaps it into the first position. This operation is enough because the remaining digits are already sorted ascending. No additional rearrangement is necessary.

The final comparison is performed as a string comparison. This is safer than numeric comparison because `"0012"` and `"12"` represent different answers in the context of this problem.

## Worked Examples

### Example 1

Input:

```
3310
1033
```

| Step | Digits State | Explanation |
| --- | --- | --- |
| Initial digits | `['3', '3', '1', '0']` | Original number |
| After sorting | `['0', '1', '3', '3']` | Smallest lexicographic order |
| First non-zero digit | `1` | Must become leading digit |
| After swap | `['1', '0', '3', '3']` | Smallest valid arrangement |
| Final string | `1033` | Compare with Bob’s answer |

The constructed answer matches Bob’s answer, so the output is:

```
OK
```

This trace demonstrates why leading zeroes cannot remain at the front even after sorting.

### Example 2

Input:

```
310
130
```

| Step | Digits State | Explanation |
| --- | --- | --- |
| Initial digits | `['3', '1', '0']` | Original number |
| After sorting | `['0', '1', '3']` | Lexicographically smallest |
| First non-zero digit | `1` | Smallest valid leading digit |
| After swap | `['1', '0', '3']` | Minimal valid arrangement |
| Final string | `103` | Compare with Bob’s answer |

Bob answered `130`, but the true minimal arrangement is `103`.

The correct output is:

```
WRONG_ANSWER
```

This example shows that matching digits alone is insufficient. The arrangement must also be minimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(d \log d)$ | Sorting the digits dominates |
| Space | $O(d)$ | Storage for the digit list |

The maximum number of digits is only 10, so the running time is effectively constant in practice. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = input().strip()
    m = input().strip()

    digits = sorted(n)

    if digits[0] == '0':
        for i in range(len(digits)):
            if digits[i] != '0':
                digits[0], digits[i] = digits[i], digits[0]
                break

    smallest = ''.join(digits)

    if smallest == m:
        print("OK")
    else:
        print("WRONG_ANSWER")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run("3310\n1033\n") == "OK", "sample 1"

# minimum value
assert run("0\n0\n") == "OK", "single zero"

# leading zero trap
assert run("1002\n1002\n") == "OK", "smallest valid arrangement keeps zeroes after first digit"

# wrong arrangement with same digits
assert run("310\n130\n") == "WRONG_ANSWER", "digits match but arrangement is not minimal"

# already sorted
assert run("1234\n1234\n") == "OK", "already minimal"

# maximum size boundary
assert run("1000000000\n1000000000\n") == "OK", "10 digits with many zeroes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 / 0` | `OK` | Handles the single-digit zero case |
| `1002 / 1002` | `OK` | Correct handling of leading zeroes |
| `310 / 130` | `WRONG_ANSWER` | Matching digits are not enough |
| `1234 / 1234` | `OK` | Already minimal ordering |
| `1000000000 / 1000000000` | `OK` | Boundary size with many zeroes |

## Edge Cases

Consider the input:

```
1002
1002
```

The sorted digits become:

```
0012
```

This arrangement is invalid because it starts with zero. The algorithm scans for the first non-zero digit, which is `1`, and swaps it into the front:

```
1002
```

The remaining digits stay sorted, so this is the smallest valid arrangement.

Now consider:

```
0
0
```

The digit list contains only one character:

```
['0']
```

No swap is needed because there is no non-zero digit. The constructed result remains `"0"`, which matches the correct answer.

Finally, consider:

```
909
990
```

Sorted digits:

```
099
```

After swapping the first non-zero digit to the front:

```
909
```

Bob answered `990`, which is larger. The algorithm correctly prints:

```
WRONG_ANSWER
```
