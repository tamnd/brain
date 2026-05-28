---
title: "CF 146B - Lucky Mask"
description: "We are given two integers. The first number, a, is arbitrary. The second number, b, is guaranteed to be lucky, meaning every digit of b is either 4 or 7. For any positive integer, its \"mask\" is formed by taking only the digits 4 and 7 from left to right and concatenating them."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 146
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 104 (Div. 2)"
rating: 1300
weight: 146
solve_time_s: 90
verified: true
draft: false
---

[CF 146B - Lucky Mask](https://codeforces.com/problemset/problem/146/B)

**Rating:** 1300  
**Tags:** brute force, implementation  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers. The first number, `a`, is arbitrary. The second number, `b`, is guaranteed to be lucky, meaning every digit of `b` is either `4` or `7`.

For any positive integer, its "mask" is formed by taking only the digits `4` and `7` from left to right and concatenating them. For example, the mask of `72174994` is `7744` because those are the lucky digits that appear in order.

The task is to find the smallest integer `c` such that `c > a` and the mask of `c` equals `b`.

The constraints are small. Both numbers are at most `100000`, so even a direct simulation over many candidate numbers is completely realistic. A two-second limit with values around `10^5` usually allows several million simple operations comfortably. That means even checking numbers one by one is acceptable if each check is cheap.

The tricky part is not performance, it is correctly extracting the mask.

One easy mistake is forgetting that non-lucky digits are ignored instead of stopping the process.

For example:

Input:

```
1 47
```

The correct answer is:

```
47
```

A careless solution might reject `47` because it contains other digits before or after the lucky digits in some later candidates, but the mask only depends on the subsequence of lucky digits.

Another subtle case happens when the number itself is lucky.

Input:

```
1 7
```

The correct answer is:

```
7
```

The mask of `7` is still `7`. A buggy implementation that removes all digits first and accidentally treats the mask as empty would fail here.

There is also a boundary condition involving numbers with no lucky digits at all.

Input:

```
40 4
```

The correct answer is:

```
44
```

The number `41` has mask `4`, so actually the smallest valid answer is:

```
41
```

A careless implementation that only checks fully lucky numbers would incorrectly skip many valid answers.

## Approaches

The most direct approach is brute force. Start from `a + 1`, compute the mask of each number, and stop when the mask equals `b`.

To compute the mask, scan the digits from left to right and keep only `4` and `7`. If the resulting sequence matches `b`, we found the answer.

This works because the constraints are tiny. Even if we check tens or hundreds of thousands of numbers, each mask computation only touches a few digits. A number up to `10^5` has at most six digits, so the total work stays very small.

The brute-force method already passes comfortably.

The key observation is that the search space is naturally limited. Since `b` itself has at most six digits and only lucky digits matter, we do not need any advanced combinatorics or dynamic programming. The simplest simulation is already optimal enough.

Some people try to construct the answer digit by digit, but that creates unnecessary complexity. The mask condition is extremely cheap to test directly, so sequential search is the cleanest solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k · d) | O(d) | Accepted |
| Optimal | O(k · d) | O(d) | Accepted |

Here, `k` is the number of checked integers and `d` is the number of digits per integer. Since `d ≤ 6`, the runtime is effectively linear in the search range.

## Algorithm Walkthrough

1. Read integers `a` and `b`.
2. Convert `b` to a string because masks are easiest to compare as strings.
3. Start iterating from `a + 1` upward.
4. For each candidate number, convert it to a string and build its mask.

Scan every digit from left to right. Whenever the digit is `4` or `7`, append it to the mask.
5. Compare the constructed mask with `b`.

If they are equal, this candidate is the smallest valid answer because we are checking numbers in increasing order.
6. Print the candidate and terminate.

### Why it works

The algorithm checks every integer greater than `a` in strictly increasing order. For each integer, it computes exactly the definition of the mask by keeping only lucky digits in order.

The first number whose mask equals `b` must be the minimum valid answer because no smaller unchecked number exists. Since every candidate is tested correctly against the mask definition, the algorithm cannot miss the answer or return an invalid number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = input().split()
    a = int(a)

    x = a + 1

    while True:
        mask = []

        for ch in str(x):
            if ch == '4' or ch == '7':
                mask.append(ch)

        if ''.join(mask) == b:
            print(x)
            return

        x += 1

solve()
```

The solution directly follows the algorithm.

The input is split into two strings because `b` is most naturally compared as text. We only convert `a` to an integer since we need arithmetic on it.

The loop starts from `a + 1` because the answer must be strictly greater than `a`.

For every candidate number `x`, we scan its decimal representation character by character. Whenever we encounter `4` or `7`, we append it to the mask list. Joining the list produces the exact mask string.

Using strings avoids mistakes with leading concatenation logic or integer arithmetic. Since numbers are tiny, this approach is both simpler and fully efficient.

The order of checking matters. We test candidates sequentially, so the first successful one is automatically minimal.

## Worked Examples

### Example 1

Input:

```
1 7
```

| Candidate `x` | Digits Scanned | Mask Built | Matches `7` |
| --- | --- | --- | --- |
| 2 | 2 | "" | No |
| 3 | 3 | "" | No |
| 4 | 4 | "4" | No |
| 5 | 5 | "" | No |
| 6 | 6 | "" | No |
| 7 | 7 | "7" | Yes |

Output:

```
7
```

This trace shows that numbers without lucky digits simply produce an empty mask. The algorithm keeps scanning until the mask exactly matches the target.

### Example 2

Input:

```
40 4
```

| Candidate `x` | Digits Scanned | Mask Built | Matches `4` |
| --- | --- | --- | --- |
| 41 | 4, 1 | "4" | Yes |

Output:

```
41
```

This example demonstrates why we cannot restrict ourselves to fully lucky numbers. The answer may contain arbitrary non-lucky digits as long as the extracted lucky digits form the required mask.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · d) | We check `k` candidate numbers, each with at most `d` digits |
| Space | O(d) | The mask stores at most all digits of one number |

Here, `d` is at most 6 because all numbers are small. Even if we scan many candidates, the total number of digit operations stays tiny compared to the time limit. Memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a, b = input().split()
    a = int(a)

    x = a + 1

    while True:
        mask = []

        for ch in str(x):
            if ch == '4' or ch == '7':
                mask.append(ch)

        if ''.join(mask) == b:
            print(x)
            return

        x += 1

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue()

# provided sample
assert run("1 7\n") == "7\n", "sample 1"

# minimum-style case
assert run("1 4\n") == "4\n", "smallest lucky target"

# mask appears inside non-lucky number
assert run("40 4\n") == "41\n", "non-lucky digits ignored"

# multiple lucky digits
assert run("100 47\n") == "147\n", "mixed digits produce target mask"

# answer is fully lucky
assert run("46 47\n") == "47\n", "direct lucky number"

# larger boundary-style case
assert run("99999 4\n") == "100004\n", "crossing digit length boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 4` | `4` | Smallest simple valid answer |
| `40 4` | `41` | Non-lucky digits must be ignored |
| `100 47` | `147` | Mask can appear inside a larger number |
| `46 47` | `47` | Fully lucky numbers are valid |
| `99999 4` | `100004` | Correct handling after increasing digit count |

## Edge Cases

Consider the input:

```
40 4
```

The algorithm starts at `41`.

For `41`, the digits are scanned left to right:

- `4` is lucky, so it is added to the mask.
- `1` is ignored.

The constructed mask becomes `"4"`, which matches the target immediately. The algorithm prints `41`.

This case confirms that arbitrary digits between lucky digits do not matter.

Now consider:

```
1 7
```

The algorithm checks numbers sequentially:

- `2`, `3`, `5`, and `6` produce empty masks.
- `4` produces mask `"4"`.
- `7` produces mask `"7"`.

The first match is `7`, so the output is correct.

This verifies that a single lucky digit works correctly and that empty masks are handled safely.

Finally, consider:

```
99999 4
```

The algorithm continues past five-digit numbers into six-digit numbers.

The first candidate with mask `"4"` is:

```
100004
```

Its digits contain exactly one lucky digit, `4`, so the mask is `"4"`.

This confirms that the implementation handles digit-length expansion correctly and does not rely on fixed-width assumptions.
