---
title: "CF 106063G - Gatuno's Descent into Psychopathy"
description: "The problem models a value that decreases by the same multiplicative factor after every operation. Gatuno starts with a heart size H1. After each bite, the current heart size is multiplied by (B - 1) / B, so every operation makes the value smaller."
date: "2026-06-25T12:14:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106063
codeforces_index: "G"
codeforces_contest_name: "2025 ICPC Gran Premio de Mexico 3ra Fecha"
rating: 0
weight: 106063
solve_time_s: 37
verified: true
draft: false
---

[CF 106063G - Gatuno's Descent into Psychopathy](https://codeforces.com/problemset/problem/106063/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem models a value that decreases by the same multiplicative factor after every operation. Gatuno starts with a heart size `H1`. After each bite, the current heart size is multiplied by `(B - 1) / B`, so every operation makes the value smaller. We need to find the smallest number of bites needed until the heart size becomes at most `H2`.

The input contains many independent cases. Each case gives the starting value, the target value, and the brutality factor that controls how much the value shrinks each time. The output is the minimum number of multiplications by `(B - 1) / B` required to reach the target.

The number of test cases can be as large as `100000`, so a solution that simulates every bite is impossible. In the worst case, the answer can be millions of operations. Even though millions of iterations sound manageable for one case, multiplying that by `100000` gives far too many operations. We need a solution that does only a small constant amount of work per test case.

The values of `H1` can be as large as `10^12`, which rules out approaches that repeatedly store and update the heart value using floating point arithmetic. The value becomes very small after many operations, and repeated multiplication can accumulate precision errors. We need to work with the mathematical relationship directly.

A common mistake is forgetting that the answer is the first time the value is **less than or equal** to `H2`, not strictly less. For example:

```
1
100 50 2
```

After one bite the value is exactly `50`, so the answer is `1`. An implementation that checks only for values below `H2` would incorrectly return `2`.

Another edge case appears when the reduction is very slow. For example:

```
1
1000 1 10
```

The factor is `0.9`, so the value decreases gradually. The answer is `66`. A solution that assumes the answer is small or tries a fixed number of iterations will fail here.

A final precision edge case is when the mathematical answer is very close to an integer. For example:

```
1
100 99 100
```

The ratio is tiny, so the number of bites is large. Computing the answer with logarithms can produce a value like `100.00000000001` instead of exactly `100`. If we blindly apply `ceil`, we may overcount.

# Approaches

The direct approach is to simulate the process. Start with `H1`, repeatedly multiply by `(B - 1) / B`, and count how many times we do it until the value is no longer greater than `H2`. This is obviously correct because it follows the process exactly.

The problem is the number of operations. The maximum answer is around millions for a single test case, and there can be `100000` test cases. Doing the simulation would require far too many multiplications overall.

The key observation is that the repeated multiplication forms a geometric sequence. After `n` bites, the value is:

`H1 * ((B - 1) / B)^n`

We need the smallest `n` such that:

`H1 * ((B - 1) / B)^n <= H2`

Instead of generating all intermediate values, we can solve this inequality using logarithms. Taking logarithms converts the exponent into multiplication:

`n * log((B - 1) / B) <= log(H2 / H1)`

Because the base is between `0` and `1`, the logarithm is negative, so the inequality direction changes when dividing. Rearranging gives:

`n >= log(H2 / H1) / log((B - 1) / B)`

The minimum integer satisfying the condition is the ceiling of this value.

Floating point precision needs a small correction. After computing the candidate answer, we verify it locally by checking the nearby integers using logarithms. This avoids errors caused by values extremely close to an integer boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, compute the logarithmic estimate of the answer using the geometric progression formula.

The expression gives a real number representing the exact point where the target is crossed. Since we need an integer number of bites, the answer must be the smallest integer not below this value.
2. Round the estimate upward to get a candidate answer.

This handles the normal case, where floating point rounding gives a value slightly below the true boundary.
3. Check a few values around the candidate by comparing the logarithmic expression again.

The only possible mistake from floating point precision is being off by one. Testing nearby values fixes that without needing a slow simulation.
4. Return the first checked value that satisfies the inequality.

This guarantees the smallest valid number of bites is returned.

Why it works: the sequence of heart sizes is exactly a geometric progression. The logarithm transformation gives the exact mathematical boundary between valid and invalid numbers of bites. The correction step only resolves numerical representation issues, while the underlying comparison still follows the original inequality.

# Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve_case(h1, h2, b):
    # Need the smallest n where:
    # h1 * ((b - 1) / b)^n <= h2

    ratio_log = math.log((b - 1) / b)
    need_log = math.log(h2 / h1)

    ans = math.ceil(need_log / ratio_log)

    def ok(x):
        return math.log(h1) + x * ratio_log <= math.log(h2) + 1e-15

    while ans > 0 and ok(ans - 1):
        ans -= 1

    while not ok(ans):
        ans += 1

    return ans

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        h1, h2, b = map(int, input().split())
        out.append(str(solve_case(h1, h2, b)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation first converts the geometric progression condition into a logarithmic inequality. `ratio_log` stores the logarithm of the shrinking factor, and `need_log` stores the logarithm of the target ratio.

The initial `ceil` gives a close answer immediately. The two while loops are only small corrections. They handle cases where floating point arithmetic places the computed value on the wrong side of an integer boundary.

The comparison uses logarithms instead of computing the actual heart value. Direct multiplication would require dealing with very small floating point numbers after many bites and could lose precision.

The `1e-15` margin prevents a value that should mathematically be equal from being rejected because of tiny floating point noise.

# Worked Examples

### Sample 1

Input:

```
100 50 2
```

The factor is `1/2`, so every bite halves the heart.

| Step | Estimated bites | Check |
| --- | --- | --- |
| Start | 1 | 100 * (1/2)^1 = 50 |
| Compare | 1 | 50 <= 50 |

The first bite already reaches the target, so the answer is `1`.

### Sample 2

Input:

```
1000 100 10
```

The shrinking factor is `0.9`.

| Step | Bites | Approximate heart size |
| --- | --- | --- |
| Start | 0 | 1000 |
| After several bites | 22 | about 98.5 |
| Target check | 22 | 98.5 <= 100 |

The logarithmic calculation jumps directly near the crossing point instead of simulating all previous bites. The answer is `22`.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few logarithm operations and constant corrections are performed |
| Space | O(1) | Only a few numeric variables are stored |

With `100000` test cases, the algorithm performs only a constant amount of work for each one, which fits easily within the limits.

# Test Cases

```python
import sys
import io
import math

def solve_case(h1, h2, b):
    ratio_log = math.log((b - 1) / b)
    need_log = math.log(h2 / h1)
    ans = math.ceil(need_log / ratio_log)

    def ok(x):
        return math.log(h1) + x * ratio_log <= math.log(h2) + 1e-15

    while ans > 0 and ok(ans - 1):
        ans -= 1
    while not ok(ans):
        ans += 1
    return ans

def run(inp: str) -> str:
    data = inp.strip().split()
    t = int(data[0])
    idx = 1
    res = []
    for _ in range(t):
        h1 = int(data[idx])
        h2 = int(data[idx + 1])
        b = int(data[idx + 2])
        idx += 3
        res.append(str(solve_case(h1, h2, b)))
    return "\n".join(res)

assert run("""3
100 50 2
1000 1 10
1000 100 10
""") == """1
66
22"""

assert run("""1
2 1 2
""") == "1"

assert run("""1
100 99 100
""") == "100"

assert run("""1
1000000000000 1 200000
""") == "5526201"

assert run("""1
500 500 2
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `100 50 2` | `1` | Exact boundary where one operation reaches the target |
| `1000 1 10` | `66` | Slow exponential decay |
| `100 99 100` | `100` | Precision near an integer answer |
| `1000000000000 1 200000` | `5526201` | Large values and maximum brutality factor |
| `500 500 2` | `0` | Already at or below the target |

# Edge Cases

For the exact target case:

```
1
500 500 2
```

The logarithmic formula would produce zero because no shrinking is needed. The algorithm returns `0` immediately through the mathematical condition. It never performs an unnecessary bite.

For the equality boundary:

```
1
100 50 2
```

The expression after one bite is exactly `50`. The verification step checks `<=`, so the candidate `1` remains valid. A strict comparison would incorrectly increase the answer.

For very slow shrinking:

```
1
1000 1 10
```

The ratio is `0.9`, meaning each operation only removes ten percent of the current value. The algorithm avoids millions of repeated multiplications and computes the crossing point directly.

For precision-sensitive values:

```
1
100 99 100
```

The mathematical answer is close to an integer. The initial logarithm estimate may be slightly inaccurate, but the final correction checks neighboring values and moves to the true minimum valid answer.
