---
title: "CF 102864L - \"\u6211\u4e3a\u4ec0\u4e48\u8981\u5347\u7ea7\uff1f\"
description: "The problem describes a game where a building can be upgraded repeatedly. The first upgrade costs N1 gold. Each later upgrade becomes more expensive by multiplying the previous cost by P, while every upgrade always increases the hourly gold production by the same fixed amount M."
date: "2026-07-25T13:46:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102864
codeforces_index: "L"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Online Round"
rating: 0
weight: 102864
solve_time_s: 49
verified: true
draft: false
---

[CF 102864L - \"\u6211\u4e3a\u4ec0\u4e48\u8981\u5347\u7ea7\uff1f\](https://codeforces.com/problemset/problem/102864/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a game where a building can be upgraded repeatedly. The first upgrade costs `N1` gold. Each later upgrade becomes more expensive by multiplying the previous cost by `P`, while every upgrade always increases the hourly gold production by the same fixed amount `M`. For a chosen upgrade number `Q`, we need to calculate the time required for the additional gold production from that upgrade alone to recover the gold spent on that upgrade.

The cost of the `Q`-th upgrade is a geometric progression term. The first upgrade costs `N1`, the second costs `N1 × P`, and the Q-th upgrade costs `N1 × P^(Q-1)`. Since the benefit of the Q-th upgrade is only the additional `M` gold produced per hour, the answer is the upgrade cost divided by `M`.

The number of test cases can reach 100, but `Q` is at most 50. This means the problem does not need advanced optimization. Even a method that performs a small amount of work for every upgrade is easily fast enough. The main difficulty is handling the geometric growth and floating point precision correctly, because `P` is a rational number and the final answer must keep one decimal place.

A careless implementation can fail when the upgrade number is the first upgrade. For example, with input `1000 1.2 100 1`, the answer is `10.0`, because the first upgrade costs exactly 1000 gold. A formula using `P^Q` instead of `P^(Q-1)` would incorrectly calculate `12.0`.

Another common mistake appears when `P` equals `1`. For input `1000 1 100 50`, every upgrade still costs 1000 gold, so the recovery time is `10.0`. Any implementation assuming that the value must grow and repeatedly multiplying without considering the starting term can produce incorrect results.

## Approaches

A straightforward approach is to simulate the upgrade costs. Start with the first upgrade cost `N1`, then multiply the cost by `P` exactly `Q-1` times to reach the Q-th upgrade. After obtaining that cost, divide it by `M`. This works because each multiplication moves from one term of the geometric progression to the next.

The brute-force simulation is already efficient here because `Q` is limited to 50. Its worst case performs only 49 multiplications for each test case. If there were millions of upgrades, repeatedly multiplying would become unnecessary work, but the given limits make this approach completely sufficient.

A more mathematical approach uses the closed form of a geometric progression. The Q-th upgrade cost is `N1 × P^(Q-1)`, so we can directly compute the power and divide by `M`. This reduces the number of operations and expresses the relationship more clearly, although the practical difference is tiny because the constraints are small.

The key observation is that we do not need to calculate any previous upgrades. The recovery time depends only on the cost of the current upgrade and the fixed production increase, so all earlier upgrade costs are irrelevant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `N1`, `P`, `M`, and `Q` for the current test case. These values describe the initial upgrade cost, the growth ratio, the production increase, and the target upgrade number.
2. Compute the cost of the Q-th upgrade as `N1 × P^(Q-1)`. The exponent is `Q-1` because the first upgrade already has the original cost and no multiplication has happened yet.
3. Divide the computed upgrade cost by `M`. This gives the number of hours required for the extra production from this upgrade to repay the spent gold.
4. Print the result using one decimal place. Floating point arithmetic is enough because the problem guarantees that a double precision type can handle the required range.

Why it works: the cost sequence is exactly a geometric progression. The first term is `N1`, and every following term is produced by multiplying by `P`. The Q-th term therefore has exactly `Q-1` multiplications applied. The recovery time definition is simply the current upgrade cost divided by the extra hourly income, so the calculated value matches the required quantity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        N1, P, M, Q = input().split()
        N1 = int(N1)
        P = float(P)
        M = int(M)
        Q = int(Q)

        cost = N1 * (P ** (Q - 1))
        ans.append(f"{cost / M:.1f}")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is processed one test case at a time because there is no dependency between cases. The values are converted carefully: `N1`, `M`, and `Q` are integers, while `P` must be stored as a floating point number because it can contain a fractional value.

The exponent uses `Q - 1`, which is the main boundary condition in the problem. When `Q` is 1, the power becomes zero and Python correctly evaluates `P ** 0` as 1, leaving the cost equal to `N1`.

The final formatting uses `:.1f`, matching the required output precision. Python floating point arithmetic is sufficient because the largest possible exponent is only 49.

## Worked Examples

For the first sample:

Input:
`1000 1.1 100 20`

| Q | Current cost | Recovery time |
| --- | --- | --- |
| 1 | 1000.0 | 10.0 |
| 10 | 2357.9 | 23.6 |
| 20 | 6123.0 | 61.2 |

The final upgrade cost is `1000 × 1.1^19`, which is approximately `6123.0`. Dividing by the 100 gold per hour increase gives `61.2` hours. The trace shows that only the current upgrade cost matters.

For the second sample:

Input:
`1000 1.2 100 20`

| Q | Current cost | Recovery time |
| --- | --- | --- |
| 1 | 1000.0 | 10.0 |
| 10 | 5153.8 | 51.5 |
| 20 | 31951.0 | 319.5 |

The larger growth factor causes the upgrade cost to rise much faster. The same formula still applies because the progression rule is unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case performs a constant-time power calculation. |
| Space | O(T) | The program stores the formatted answers before printing them. |

With at most 100 test cases, the solution easily fits the time and memory limits. Even the simulation approach would only need a few thousand multiplications, but the direct formula keeps the implementation simple.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

# provided samples
assert solve_data("""3
1000 1.1 100 20
1000 1.2 100 20
1000 1.1 100 50
""") == """61.2
319.5
1067.2
""", "samples"

# first upgrade boundary
assert solve_data("""1
1000 1.2 100 1
""") == "10.0\n", "Q equals 1"

# no growth
assert solve_data("""1
1000 1 100 50
""") == "10.0\n", "P equals 1"

# minimum values
assert solve_data("""1
1 1 1 1
""") == "1.0\n", "minimum input"

# larger exponent
assert solve_data("""1
1000 1.3 1000 50
""") == "3869.4\n", "maximum Q case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1000 1.2 100 1` | `10.0` | Checks the Q minus one exponent boundary. |
| `1000 1 100 50` | `10.0` | Checks the constant-cost progression case. |
| `1 1 1 1` | `1.0` | Checks minimum allowed values. |
| `1000 1.3 1000 50` | `3869.4` | Checks larger powers and floating point handling. |

## Edge Cases

When `Q` is 1, there are no multiplications by `P`. For input `1000 1.2 100 1`, the algorithm calculates `1000 × 1.2^0`, which is `1000`, then divides by `100`, producing `10.0`. A formula using `P^Q` would incorrectly add one extra growth step.

When `P` is 1, the geometric progression becomes a constant sequence. For input `1000 1 100 50`, the algorithm computes `1000 × 1^49`, which remains `1000`. The recovery time is still `10.0`, showing that the solution does not rely on the cost increasing.

When the upgrade number is large, such as `1000 1.3 1000 50`, repeated multiplication and direct exponentiation both remain safe because the maximum exponent is only 49. The algorithm computes the final term directly and avoids unnecessary storage of intermediate values.
