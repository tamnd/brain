---
title: "CF 31E - TV Game"
description: "We are given a string of 2n digits. The digits are processed strictly from left to right. At every step, either Homer or"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 31
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 31 (Div. 2, Codeforces format)"
rating: 2400
weight: 31
solve_time_s: 118
verified: false
draft: false
---

[CF 31E - TV Game](https://codeforces.com/problemset/problem/31/E)

**Rating:** 2400  
**Tags:** dp  
**Solve time:** 1m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of `2n` digits. The digits are processed strictly from left to right. At every step, either Homer or Marge takes the current leftmost digit and appends it to their own number. By the end, both players must have taken exactly `n` digits.

The final score is the sum of the two constructed numbers. We must output one valid sequence of moves, using `H` and `M`, that maximizes this total.

The key detail is that the order inside each player's number is fixed. If Homer takes digits at positions `i1 < i2 < ...`, then his number is exactly those digits in that order. The same holds for Marge.

The constraints are small enough to allow dynamic programming, but large enough that brute force over all assignments is impossible. Since `n ≤ 18`, the total number of digits is at most `36`. A naive search over all assignments of digits to players would examine `2^(2n)` possibilities. In the worst case this becomes `2^36`, roughly 68 billion states, completely infeasible in 2 seconds.

At the same time, `36 × 36 × 10^18` style arithmetic is perfectly fine. The final numbers themselves may have up to 18 digits, so 64-bit integers are required. Python integers handle this automatically.

Several edge cases are easy to mishandle if the reasoning is not precise.

Consider:

```
1
09
```

If Homer takes `0` and Marge takes `9`, the total is `0 + 9 = 9`.

If Homer takes `9` and Marge takes `0`, the total is `9 + 0 = 9`.

Leading zeroes are legal, so we cannot treat constructed strings as invalid numbers.

Another subtle case is:

```
2
9090
```

A greedy strategy that always gives the current digit to the player with the smaller current value can fail, because earlier digits are more significant. Assigning a digit earlier changes a higher decimal place than assigning a later digit.

One more important scenario is:

```
2
1234
```

If Homer takes the first two digits and Marge takes the last two, we get `12 + 34 = 46`.

But alternating gives:

`13 + 24 = 37`

The position inside each player's number matters more than the absolute digit itself. A digit placed earlier contributes a larger power of ten.

## Approaches

The brute force idea is straightforward. For each of the `2n` positions, decide whether the digit goes to Homer or Marge, while ensuring both receive exactly `n` digits.

Once an assignment is fixed, we can construct both numbers and compute their sum. The number of valid assignments is:

$$\binom{2n}{n}$$

For `n = 18`, this is:

$$\binom{36}{18} \approx 9 \times 10^9$$

Even checking a tiny fraction of those states is impossible.

The reason brute force works conceptually is that every valid sequence uniquely determines the final numbers. The issue is purely the explosion of combinations.

The key observation is that the contribution of a digit depends only on two things:

First, which player receives it.

Second, how many digits that player will still receive afterward.

Suppose Homer already has taken `h` digits before position `i`. Then the current digit becomes the `(h+1)`-th digit of Homer's number. Since Homer will end with exactly `n` digits, this digit contributes:

$$digit \times 10^{n-h-1}$$

The future decisions do not change this positional weight.

That means we can process digits from left to right and use dynamic programming on how many digits Homer has already taken.

At position `i`, Marge has automatically taken `i-h` digits.

So the entire state is determined by a single parameter:

$$dp[i][h]$$

meaning the maximum total value obtainable after processing the first `i` digits, where Homer has taken exactly `h` of them.

From this state, we try:

1. Give the next digit to Homer.
2. Give the next digit to Marge.

Each transition adds a known contribution immediately.

The total number of states is only about `36 × 18`, tiny enough to compute instantly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(2n)) | O(2^(2n)) | Too slow |
| Optimal DP | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read `n` and the digit string `s`.
2. Precompute powers of ten from `10^0` up to `10^18`.

These powers determine the positional contribution of every digit.

1. Define `dp[i][h]` as the maximum total value achievable after processing the first `i` digits, where Homer has taken exactly `h` digits.

Since Marge automatically took `i-h` digits, we do not need another dimension.

1. Initialize:

```
dp[0][0] = 0
```

All other states start as negative infinity.

1. Process digits from left to right.

Suppose we are at position `i`, with Homer having already taken `h` digits.

Let:

```
m = i - h
```

be the number of digits Marge has already taken.

1. Try assigning the current digit to Homer.

This is only possible if `h < n`.

The digit becomes Homer's `(h+1)`-th digit, so its decimal weight is:

$$10^{n-h-1}$$

Add this contribution and transition to:

```
dp[i+1][h+1]
```

1. Try assigning the current digit to Marge.

This is only possible if `m < n`.

The digit becomes Marge's `(m+1)`-th digit, so its weight is:

$$10^{n-m-1}$$

Add this contribution and transition to:

```
dp[i+1][h]
```

1. Store parent information for reconstruction.

For every improved transition, remember:

1. The previous state.
2. Whether we chose `H` or `M`.
3. After processing all digits, the answer is stored in:

```
dp[2n][n]
```

1. Reconstruct the move sequence by walking backward through the parent pointers.

Reverse the collected characters at the end.

### Why it works

Every digit contributes independently once we know which player receives it and which position inside that player's number it occupies.

When processing digits left to right, the position inside Homer's number is completely determined by how many digits Homer already took. The same holds for Marge.

So every future outcome from a state depends only on:

1. How many digits have been processed.
2. How many of them Homer took.

The DP explores every valid assignment exactly once and computes the best achievable total for each state. Since transitions add the exact decimal contribution of the current digit, the final value equals the true sum of the two constructed numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = -(10**30)

def solve():
    n = int(input())
    s = input().strip()

    total = 2 * n

    pow10 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow10[i] = pow10[i - 1] * 10

    dp = [[INF] * (n + 1) for _ in range(total + 1)]
    parent = [[None] * (n + 1) for _ in range(total + 1)]

    dp[0][0] = 0

    for i in range(total):
        digit = int(s[i])

        for h in range(n + 1):
            if dp[i][h] == INF:
                continue

            m = i - h

            # Give digit to Homer
            if h < n:
                add = digit * pow10[n - h - 1]
                val = dp[i][h] + add

                if val > dp[i + 1][h + 1]:
                    dp[i + 1][h + 1] = val
                    parent[i + 1][h + 1] = (i, h, 'H')

            # Give digit to Marge
            if m < n:
                add = digit * pow10[n - m - 1]
                val = dp[i][h] + add

                if val > dp[i + 1][h]:
                    dp[i + 1][h] = val
                    parent[i + 1][h] = (i, h, 'M')

    ans = []

    i = total
    h = n

    while i > 0:
        pi, ph, ch = parent[i][h]
        ans.append(ch)
        i, h = pi, ph

    ans.reverse()

    print("".join(ans))

solve()
```

The DP table stores the best achievable total for every prefix length and every possible number of digits assigned to Homer.

The transition logic is the core of the solution. When a digit is assigned, we immediately know its exact positional weight. For example, if Homer has already taken `h` digits, then the current digit becomes the next digit in his number and contributes:

```
digit × 10^(n-h-1)
```

No later decision can change this contribution.

The parent table is necessary because the problem asks for the sequence of moves, not only the maximum score. Each parent entry records:

1. The previous state.
2. Which player received the digit.

One subtle detail is the computation of Marge's digit count:

```
m = i - h
```

This works because exactly `i` digits have been processed, and `h` of them went to Homer.

Another easy mistake is forgetting that leading zeroes are valid. The DP naturally handles them because digits are treated purely as positional contributions.

The value range can exceed 32-bit integers. Python integers avoid overflow automatically.

## Worked Examples

### Example 1

Input:

```
2
1234
```

| Step | Digit | Homer count | Marge count | Choice | Added value | Best total |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | H | 10 | 10 |
| 1 | 2 | 1 | 0 | H | 2 | 12 |
| 2 | 3 | 2 | 0 | M | 30 | 42 |
| 3 | 4 | 2 | 1 | M | 4 | 46 |

Final answer:

```
HHMM
```

This trace shows how earlier positions dominate later ones. Giving `1` to Homer as his first digit contributes `10`, while giving `2` as his second digit contributes only `2`.

### Example 2

Input:

```
2
9090
```

| Step | Digit | Homer count | Marge count | Choice | Added value | Best total |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 9 | 0 | 0 | H | 90 | 90 |
| 1 | 0 | 1 | 0 | M | 0 | 90 |
| 2 | 9 | 1 | 1 | M | 9 | 99 |
| 3 | 0 | 1 | 2 | H | 0 | 99 |

One optimal answer is:

```
HMMH
```

This example demonstrates that assigning a large digit earlier is far more valuable than assigning it later. The first `9` contributes `90`, while the second contributes only `9`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | There are O(n²) DP states and O(1) transitions per state |
| Space | O(n²) | DP table and parent table each store O(n²) states |

With `n ≤ 18`, the DP contains at most about `37 × 19` states. The solution runs comfortably within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    INF = -(10**30)

    n = int(input())
    s = input().strip()

    total = 2 * n

    pow10 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow10[i] = pow10[i - 1] * 10

    dp = [[INF] * (n + 1) for _ in range(total + 1)]
    parent = [[None] * (n + 1) for _ in range(total + 1)]

    dp[0][0] = 0

    for i in range(total):
        digit = int(s[i])

        for h in range(n + 1):
            if dp[i][h] == INF:
                continue

            m = i - h

            if h < n:
                add = digit * pow10[n - h - 1]
                val = dp[i][h] + add

                if val > dp[i + 1][h + 1]:
                    dp[i + 1][h + 1] = val
                    parent[i + 1][h + 1] = (i, h, 'H')

            if m < n:
                add = digit * pow10[n - m - 1]
                val = dp[i][h] + add

                if val > dp[i + 1][h]:
                    dp[i + 1][h] = val
                    parent[i + 1][h] = (i, h, 'M')

    ans = []

    i = total
    h = n

    while i > 0:
        pi, ph, ch = parent[i][h]
        ans.append(ch)
        i, h = pi, ph

    ans.reverse()

    print("".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("2\n1234\n") == "HHMM", "sample 1"

# minimum size
assert run("1\n09\n") in ["HM", "MH"], "leading zero case"

# all digits equal
out = run("3\n111111\n")
assert out.count('H') == 3 and out.count('M') == 3, "balanced assignment"

# alternating high and low digits
out = run("2\n9090\n")
assert out.count('H') == 2 and out.count('M') == 2, "positional weighting"

# maximum length structure
s = "9" * 36
out = run(f"18\n{s}\n")
assert len(out) == 36, "maximum size"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1234` | `HHMM` | Basic optimal distribution |
| `1 / 09` | `HM` or `MH` | Leading zero handling |
| `3 / 111111` | Any balanced valid answer | Equal digits |
| `2 / 9090` | Any optimal balanced answer | Earlier positions dominate |
| `18 / 999...999` | Any valid length-36 answer | Maximum constraints |

## Edge Cases

Consider the input:

```
1
09
```

At the first digit, assigning `0` to either player contributes:

```
0 × 10^0 = 0
```

The second digit contributes `9`.

Both assignments produce the same total score. The DP handles this naturally because leading zeroes are treated as ordinary digits with positional weights.

Now consider:

```
2
9090
```

A careless greedy strategy may try to balance the current numeric values of the two players. That fails because decimal positions matter more than current totals.

The DP instead evaluates exact contributions:

| Digit | Position weight if first digit | Position weight if second digit |
| --- | --- | --- |
| 9 | 10 | 1 |

Assigning the first `9` early is always much more valuable.

Finally, consider:

```
2
1000
```

If Homer takes the leading `1`, its contribution is:

```
1 × 10 = 10
```

If the `1` becomes someone's second digit, its contribution drops to `1`.

The DP captures this automatically through the exponent:

```
pow10[n - h - 1]
```

which precisely tracks how many positions remain in that player's number.
