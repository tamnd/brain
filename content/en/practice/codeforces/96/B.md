---
title: "CF 96B - Lucky Numbers (easy)"
description: "We need to find the smallest number greater than or equal to a given integer such that: 1. Every digit is either 4 or 7. 2. The count of 4s equals the count of 7s. These numbers are called super lucky numbers. For example, 47 is valid because it contains one 4 and one 7."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 96
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 77 (Div. 2 Only)"
rating: 1300
weight: 96
solve_time_s: 291
verified: true
draft: false
---

[CF 96B - Lucky Numbers (easy)](https://codeforces.com/problemset/problem/96/B)

**Rating:** 1300  
**Tags:** binary search, bitmasks, brute force  
**Solve time:** 4m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to find the smallest number greater than or equal to a given integer such that:

1. Every digit is either `4` or `7`.
2. The count of `4`s equals the count of `7`s.

These numbers are called super lucky numbers.

For example, `47` is valid because it contains one `4` and one `7`. The number `7744` is also valid because it has two of each digit. The number `4447` is not valid because the counts differ.

The input contains a single integer `n`, up to `10^9`. We must output the smallest super lucky number that is at least `n`.

The bound on `n` is the key observation. Since `10^9` has at most 10 digits, any answer also has only a small number of digits. A brute-force search over ordinary integers would still be terrible because lucky numbers are sparse. Checking every number from `n` upward could require millions or billions of iterations.

The structure of lucky numbers changes the problem completely. A valid number can only contain `4` and `7`, and the length must be even because the counts must match. With at most 10 digits, the total number of candidates is tiny.

For a length `2k`, we only need to choose which `k` positions contain `4`. The remaining positions become `7`. The number of such strings is:

$$\binom{2k}{k}$$

For lengths up to 10 digits:

$$\binom{2}{1} + \binom{4}{2} + \binom{6}{3} + \binom{8}{4} + \binom{10}{5} = 2 + 6 + 20 + 70 + 252 = 350$$

Only 350 candidates exist in total. That is small enough to generate all possibilities directly.

Several edge cases can silently break careless solutions.

If `n = 1`, the answer is `47`. A greedy approach that tries to keep the same number of digits could fail because no 1-digit super lucky number exists.

If `n = 999999999`, the answer becomes `4444477777`, which has more digits than `n`. Any solution restricted to the original digit count would miss this.

If `n` itself is already super lucky, such as `4477`, we must return it unchanged. Using a strict `>` comparison instead of `>=` would incorrectly skip it.

Another subtle case is lexicographic ordering. Suppose `n = 4500`. The valid 4-digit candidates are:

`4477, 4747, 4774, 7447, 7474, 7744`

The answer is `4747`. A naive greedy construction can get stuck after choosing an early digit incorrectly.

## Approaches

The most direct brute-force idea is to start from `n` and test each integer one by one.

For every number, we would examine its digits and check whether:

1. Every digit is `4` or `7`.
2. The counts of `4` and `7` match.

This works logically, but performance is disastrous. Lucky numbers are extremely sparse. Around `10^9`, we may need to scan millions of ordinary integers before finding the next valid one. With up to a billion possible values, this approach is not realistic.

The important observation is that the answer space itself is tiny.

A super lucky number:

1. Uses only digits `4` and `7`.
2. Has even length.
3. Contains exactly half `4`s and half `7`s.

Instead of searching through all integers, we can generate every valid candidate directly.

For each even length:

1. Choose positions for the `4`s.
2. Fill the remaining positions with `7`s.
3. Convert the resulting digit sequence into a number.

Because the maximum length we ever need is only 10 digits, the total number of valid candidates is just 350.

After generating them:

1. Sort the list.
2. Find the first value that is at least `n`.

This transforms the problem from searching a huge numeric range into searching a tiny precomputed set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer - n) | O(1) | Too slow |
| Optimal | O(350 log 350) | O(350) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Generate all super lucky numbers with lengths `2, 4, 6, 8, 10`.

We never need longer lengths because `n ≤ 10^9`, and the next possible answer fits within 10 digits.
3. For each even length `L`, generate all binary masks from `0` to `(1 << L) - 1`.

Each bit determines whether a position contains `4` or `7`.
4. Count how many bits are set in the mask.

A valid super lucky number must contain exactly `L / 2` digits equal to `4`.
5. Build the number digit by digit.

If a bit is set, place `4`. Otherwise place `7`.
6. Convert the constructed string into an integer and store it.
7. Sort all generated candidates.

Sorting guarantees increasing numeric order.
8. Scan the sorted list and output the first number `x` such that `x >= n`.

### Why it works

Every super lucky number has:

1. Even length.
2. Exactly half of its digits equal to `4`.
3. All remaining digits equal to `7`.

The algorithm generates every string satisfying these conditions for all relevant lengths. No valid candidate is skipped.

After sorting, the first value greater than or equal to `n` is exactly the smallest valid answer. Since the candidate list is complete and ordered, the algorithm cannot miss a smaller valid number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    lucky = []

    for length in range(2, 11, 2):
        half = length // 2

        for mask in range(1 << length):
            if bin(mask).count("1") != half:
                continue

            s = []

            for i in range(length):
                if (mask >> i) & 1:
                    s.append('4')
                else:
                    s.append('7')

            lucky.append(int("".join(s)))

    lucky.sort()

    for x in lucky:
        if x >= n:
            print(x)
            return

solve()
```

The solution directly implements the generation strategy.

The outer loop iterates over all even lengths from 2 through 10. Those are the only possible lengths for super lucky numbers in this problem.

Each bitmask represents one assignment of digits. A set bit means digit `4`, while an unset bit means digit `7`. The check:

```
bin(mask).count("1") != half
```

filters out masks that do not contain exactly half `4`s.

The number is built as a string first because digit concatenation is simpler and less error-prone that way.

Sorting is essential because masks do not naturally generate numbers in numeric order.

One subtle detail is the comparison:

```
if x >= n:
```

The equality matters. If `n` is already super lucky, we must return it immediately.

Another subtle point is that the answer may have more digits than `n`. For example:

```
999999999 -> 4444477777
```

Generating all lengths up to 10 guarantees this case is handled correctly.

## Worked Examples

### Example 1

Input:

```
4500
```

Generated 4-digit super lucky numbers:

| Candidate | >= 4500? |
| --- | --- |
| 4477 | No |
| 4747 | Yes |
| 4774 | Yes |
| 7447 | Yes |
| 7474 | Yes |
| 7744 | Yes |

The first valid candidate is `4747`.

Output:

```
4747
```

This trace shows why sorting matters. The first candidate satisfying the condition is automatically the minimum valid answer.

### Example 2

Input:

```
4477
```

Relevant candidates:

| Candidate | >= 4477? |
| --- | --- |
| 4477 | Yes |
| 4747 | Yes |
| 4774 | Yes |

The algorithm stops immediately at `4477`.

Output:

```
4477
```

This confirms the importance of using `>=` rather than `>`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(350 log 350) | At most 350 valid candidates are generated and sorted |
| Space | O(350) | The list of all super lucky numbers is stored |

The actual running time is tiny. Even generating every mask for lengths up to 10 only involves a few thousand iterations. This easily fits within the 2-second limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    lucky = []

    for length in range(2, 11, 2):
        half = length // 2

        for mask in range(1 << length):
            if bin(mask).count("1") != half:
                continue

            s = []

            for i in range(length):
                if (mask >> i) & 1:
                    s.append('4')
                else:
                    s.append('7')

            lucky.append(int("".join(s)))

    lucky.sort()

    for x in lucky:
        if x >= n:
            print(x)
            return

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("4500\n") == "4747\n", "sample 1"

# minimum input
assert run("1\n") == "47\n", "minimum case"

# already super lucky
assert run("4477\n") == "4477\n", "already valid"

# boundary before next candidate
assert run("4748\n") == "4774\n", "next larger candidate"

# maximum-style edge
assert run("999999999\n") == "4444477777\n", "needs longer length"

# exact smallest super lucky
assert run("47\n") == "47\n", "smallest valid number"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `47` | No 1-digit super lucky numbers exist |
| `4477` | `4477` | Equality case |
| `4748` | `4774` | Correct next candidate selection |
| `999999999` | `4444477777` | Answer may need more digits |
| `47` | `47` | Smallest valid super lucky number |

## Edge Cases

Consider the input:

```
1
```

The algorithm generates all 2-digit super lucky numbers first:

`47` and `74`.

After sorting, `47` is the first value satisfying `x >= 1`, so the answer is:

```
47
```

This case confirms that the algorithm correctly handles situations where the answer has more digits than the input.

Now consider:

```
999999999
```

No 8-digit or 9-digit super lucky number can satisfy the condition because:

1. Super lucky numbers require even length.
2. All 8-digit candidates are smaller than `999999999`.

The algorithm continues generating 10-digit candidates. The smallest one is:

```
4444477777
```

Since it is the first valid candidate greater than or equal to the input, it becomes the answer.

Finally, consider:

```
4477
```

The generated candidates include `4477` exactly. During the scan:

| Candidate | Condition |
| --- | --- |
| 4477 | `4477 >= 4477` is true |

The algorithm prints `4477` immediately. This confirms the comparison is inclusive, exactly matching the problem requirement.
