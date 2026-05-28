---
title: "CF 86A - Reflection"
description: "We are given two integers, l and r. For every number n inside this interval, we build another number called its reflection. The reflection is created digit by digit. Every decimal digit d becomes 9 - d."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 86
codeforces_index: "A"
codeforces_contest_name: "Yandex.Algorithm 2011: Round 2"
rating: 1600
weight: 86
solve_time_s: 129
verified: true
draft: false
---

[CF 86A - Reflection](https://codeforces.com/problemset/problem/86/A)

**Rating:** 1600  
**Tags:** math  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, `l` and `r`. For every number `n` inside this interval, we build another number called its reflection.

The reflection is created digit by digit. Every decimal digit `d` becomes `9 - d`. For example:

- `192 → 807`
- `10 → 89`
- `91 → 08 → 8`

The weight of a number is:

$$n \cdot \psi(n)$$

where $\psi(n)$ is the reflection of `n`.

The task is to find the maximum possible weight among all integers in the range `[l, r]`.

The range can go up to $10^9$. A brute-force scan over every number is immediately suspicious because the interval itself may contain almost one billion values. Even if computing the reflection took only a few operations, iterating through $10^9$ candidates would not fit into a 2-second limit.

The key difficulty is that the reflection depends on every digit independently, so the product is not monotonic. A larger number does not necessarily give a larger weight.

There are several easy-to-miss edge cases.

Consider the range:

```
8 10
```

The weights are:

- `8 * 1 = 8`
- `9 * 0 = 0`
- `10 * 89 = 890`

The maximum jumps dramatically at the transition from one digit length to another. A naive assumption such as “the answer is near r” fails here.

Another dangerous case is numbers ending in many `9`s:

```
99 → 0
999 → 0
```

Their reflection collapses to zero because all digits become `0`. A careless implementation that keeps leading zeros as decimal digits could incorrectly treat `"00"` as a meaningful two-digit number.

There is also a structural edge case around the middle of the valid range for a fixed digit count. For two-digit numbers:

| n | ψ(n) | Product |
| --- | --- | --- |
| 40 | 59 | 2360 |
| 44 | 55 | 2420 |
| 49 | 50 | 2450 |
| 50 | 49 | 2450 |
| 55 | 44 | 2420 |

The maximum appears around the center, not at either endpoint. Understanding this shape is the core of the solution.

## Approaches

The most direct solution is to iterate over every integer from `l` to `r`, compute its reflection, multiply the two values, and keep the maximum.

Computing the reflection is easy. If a digit is `d`, its reflected digit is `9 - d`. We can either process the number as a string or digit by digit mathematically.

This brute-force method is correct because it checks every candidate explicitly. The problem is the number of candidates. In the worst case, the interval length is close to $10^9$. Even with only a few arithmetic operations per number, this is far beyond feasible.

The turning point comes from rewriting the reflection algebraically.

Suppose `n` has exactly `k` digits. Let:

$$M = 10^k - 1$$

This is the number consisting entirely of `9`s with length `k`.

For example:

- `k = 2 → M = 99`
- `k = 3 → M = 999`

Reflecting every digit independently is exactly the same as:

$$\psi(n) = M - n$$

Example:

$$192 \rightarrow 999 - 192 = 807$$

So the weight becomes:

$$f(n)=n(M-n)$$

Expanding gives:

$$f(n) = -n^2 + Mn$$

This is a quadratic parabola opening downward. Its maximum occurs at:

$$n = \frac{M}{2}$$

That changes the whole problem. Instead of searching over billions of values, we only need to examine numbers near the parabola peak.

There is one complication. The formula only works for numbers with the same digit count. When the digit count changes, `M` changes too. Since `r ≤ 10^9`, there are at most 10 different digit lengths to consider.

For each digit length:

- determine the valid intersection with `[l, r]`
- compute the midpoint $M/2$
- check the closest integers around that midpoint inside the interval

Because a quadratic reaches its maximum at the center, only a constant number of candidates are needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(r - l + 1) | O(1) | Too slow |
| Optimal | O(number of digits) | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate over every possible digit length `k` from 1 to 10.

Since `r ≤ 10^9`, only a handful of digit lengths exist.
2. For the current digit length, compute:

$$M = 10^k - 1$$

This is the all-9 number for this length.

1. Compute the valid interval of `k`-digit numbers that also lie inside `[l, r]`.

The smallest `k`-digit number is:

$$10^{k-1}$$

except for `k = 1`, where the minimum is `1`.

The largest `k`-digit number is:

$$10^k - 1$$

1. Intersect this digit-length interval with `[l, r]`.

If the intersection is empty, skip this digit length.
2. The function for this digit length is:

$$f(n)=n(M-n)$$

Since this is a downward parabola, the maximum occurs near:

$$\frac{M}{2}$$

1. Let:

$$x = \left\lfloor \frac{M}{2} \right\rfloor$$

The optimal integer candidate must be either `x` or `x + 1`.

1. Clamp these candidates into the valid interval for this digit length.

Also check interval boundaries because the midpoint may lie outside the interval.
2. Evaluate the product for all collected candidates and keep the global maximum.

### Why it works

For a fixed digit length `k`, every number satisfies:

$$\psi(n)=M-n$$

where $M=10^k-1$. The weight function becomes:

$$f(n)=n(M-n)$$

which is a concave quadratic. A concave quadratic achieves its maximum at its vertex, located at $M/2$. Since we only care about integers inside a bounded interval, the optimal value must be one of the integers closest to the vertex or one of the interval boundaries if the vertex lies outside.

We independently maximize over each digit length, and every number in `[l, r]` belongs to exactly one digit-length group. Taking the best among all groups gives the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def reflection(x):
    s = str(x)
    t = ''.join(str(9 - int(c)) for c in s)
    return int(t)

def weight(x):
    return x * reflection(x)

l, r = map(int, input().split())

ans = 0

for k in range(1, 11):
    low = 1 if k == 1 else 10 ** (k - 1)
    high = 10 ** k - 1

    L = max(l, low)
    R = min(r, high)

    if L > R:
        continue

    M = high
    mid = M // 2

    candidates = {L, R}

    for x in [mid, mid + 1]:
        if L <= x <= R:
            candidates.add(x)

    for x in candidates:
        ans = max(ans, weight(x))

print(ans)
```

The solution groups numbers by digit length because the reflection formula depends on how many digits the number has.

For a fixed digit length, the reflection is equivalent to subtracting from the all-9 number of that length. The code still computes the reflection directly for clarity and safety. Since only a constant number of candidates are evaluated, efficiency is not affected.

The midpoint computation is subtle. The quadratic maximum occurs at `M / 2`, but `M` is odd for every all-9 number. That means the true maximum lies equally between two integers. We must check both `mid` and `mid + 1`.

The candidate set also includes interval boundaries. If the parabola peak lies outside the valid range for this digit length, the maximum over the interval occurs at the closest boundary.

Python integers automatically handle large products safely. In C++ this would require 64-bit integers because the answer can exceed `2^31`.

## Worked Examples

### Example 1

Input:

```
3 7
```

For one-digit numbers:

$$M = 9$$

The function is:

$$f(n)=n(9-n)$$

| k | Interval | M | mid | Candidates | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | [3, 7] | 9 | 4 | 3, 4, 5, 7 | 20 |

Checking:

- `3 * 6 = 18`
- `4 * 5 = 20`
- `5 * 4 = 20`
- `7 * 2 = 14`

Answer:

```
20
```

This example shows the symmetry of the quadratic around the midpoint.

### Example 2

Input:

```
8 10
```

| k | Interval | M | mid | Candidates | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | [8, 9] | 9 | 4 | 8, 9 | 8 |
| 2 | [10, 10] | 99 | 49 | 10 | 890 |

For `10`:

$$\psi(10)=89$$

$$10 \cdot 89 = 890$$

Answer:

```
890
```

This trace demonstrates why digit-length transitions are critical. Moving from `9` to `10` changes the reflection base from `9` to `99`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | At most 10 digit lengths and only constant candidate checks |
| Space | O(1) | Only a few integer variables are stored |

The runtime is effectively constant because the number of digit lengths never exceeds 10. This easily fits within the time limit even in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    def reflection(x):
        s = str(x)
        t = ''.join(str(9 - int(c)) for c in s)
        return int(t)

    def weight(x):
        return x * reflection(x)

    l, r = map(int, input().split())

    ans = 0

    for k in range(1, 11):
        low = 1 if k == 1 else 10 ** (k - 1)
        high = 10 ** k - 1

        L = max(l, low)
        R = min(r, high)

        if L > R:
            continue

        M = high
        mid = M // 2

        candidates = {L, R}

        for x in [mid, mid + 1]:
            if L <= x <= R:
                candidates.add(x)

        for x in candidates:
            ans = max(ans, weight(x))

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("3 7\n") == "20", "sample 1"

# minimum range
assert run("1 1\n") == "8", "single value"

# digit-length transition
assert run("8 10\n") == "890", "crossing 9 to 10"

# midpoint optimum
assert run("40 60\n") == "2450", "peak near center"

# all equal large value
assert run("999999999 999999999\n") == "0", "all nines reflect to zero"

# large boundary case
assert run("1000000000 1000000000\n") == "899999999000000000", "largest input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `8` | Minimum valid input |
| `8 10` | `890` | Digit-length transition |
| `40 60` | `2450` | Maximum near parabola center |
| `999999999 999999999` | `0` | Reflection of all 9s |
| `1000000000 1000000000` | `899999999000000000` | Largest boundary values |

## Edge Cases

Consider the input:

```
9 9
```

Reflection:

$$\psi(9)=0$$

Weight:

$$9 \cdot 0 = 0$$

The algorithm handles this naturally. For one-digit numbers:

$$M=9$$

and:

$$9(9-9)=0$$

No special handling is needed for leading zeros because integer conversion automatically removes them.

Now consider:

```
8 10
```

The midpoint for one-digit numbers is around `4`, which lies outside `[8,9]`. The algorithm correctly falls back to checking interval boundaries.

For two-digit numbers, the only valid candidate is `10`, whose reflection becomes `89`. The answer jumps from `8` to `890`.

Another important edge case is:

```
50 50
```

For two-digit numbers:

$$M=99$$

Reflection:

$$99-50=49$$

Weight:

$$50 \cdot 49=2450$$

The midpoint of the parabola lies between `49` and `50`, so both produce the same optimal value. Checking both `mid` and `mid+1` guarantees correctness for odd `M`.

Finally, consider:

```
999999999 1000000000
```

For `999999999`:

$$\psi=0$$

Weight is zero.

For `1000000000`:

$$\psi=8999999999$$

Weight becomes extremely large.

The algorithm processes the two digit lengths independently and correctly identifies the larger result from the 10-digit interval.
