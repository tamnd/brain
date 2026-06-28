---
title: "CF 104872A - Three Suitcases"
description: "We are given three separate suitcases, each contributing a fixed weight to a single combined baggage check-in. The airline does not charge per suitcase, but instead looks at the total weight after everything is combined."
date: "2026-06-28T10:35:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104872
codeforces_index: "A"
codeforces_contest_name: "2023-2024 Russia Team Open, High School Programming Contest (VKOSHP XXIV)"
rating: 0
weight: 104872
solve_time_s: 67
verified: false
draft: false
---

[CF 104872A - Three Suitcases](https://codeforces.com/problemset/problem/104872/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three separate suitcases, each contributing a fixed weight to a single combined baggage check-in. The airline does not charge per suitcase, but instead looks at the total weight after everything is combined. Depending on this total weight, the cost falls into one of three fixed price brackets: a cheaper fee for very light total luggage, a medium fee for moderate weight, and a higher fee once the total crosses a heavier threshold.

The task is to compute the sum of the three weights and then select the correct pricing tier based on where this sum falls. The output is simply the minimum cost Katya will pay, which in this problem is equivalent to the only valid cost determined by the total weight.

The constraints are extremely small: each suitcase weight is between 1 and 10. This means the total weight ranges from 3 to 30. Since there are no multiple test cases and no combinatorial choices, any solution runs in constant time. Even a direct conditional check is sufficient, and there is no need for optimization techniques or precomputation.

There are no subtle hidden edge cases beyond correctly handling the boundary conditions between pricing tiers. The only real source of mistakes is misinterpreting whether the interval endpoints are inclusive or exclusive. For example, a total weight of exactly 5 belongs to the middle bracket, while exactly 10 belongs to the highest bracket.

A naive incorrect approach would be to use strict inequalities everywhere, such as treating “less than 5” and “less than 10” without carefully separating the inclusive boundaries. For instance, if a programmer writes `if total < 5`, `elif total < 10`, `else`, this is correct, but switching to `<= 5` or `<= 10` without adjusting the rest can silently shift boundary assignments and produce wrong outputs.

## Approaches

A brute-force interpretation would treat the problem as enumerating all possible weight combinations of the three suitcases and evaluating the cost for each. Since each weight is fixed in the input, this degenerates into a single evaluation anyway. If we generalize the thinking, brute force would check all possible triples of weights in the allowed range, compute their sums, and map each sum to a cost. With a maximum of 10 values per suitcase, that would be at most 10³ = 1000 combinations, which is still trivial, but unnecessary.

The key simplification is recognizing that the suitcases are independent and only their total sum matters. Once we collapse the three inputs into a single integer, the entire problem reduces to a one-dimensional range classification. Instead of reasoning about combinations, we are just placing a number into one of three intervals.

This reduction eliminates any need for iteration over combinations. The structure of the problem guarantees that all information about ordering or distribution is irrelevant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(1000) | O(1) | Accepted but unnecessary |
| Optimal Sum + Classification | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three suitcase weights and compute their sum. This step compresses all relevant information into a single value because the airline pricing depends only on total weight, not distribution.
2. Read the three cost values corresponding to the weight ranges. These represent fixed outputs tied to intervals of the total sum.
3. Compare the total weight against the first threshold of 5. If the sum is strictly less than 5, select the first cost. This matches the definition of the cheapest tier.
4. If the sum is not less than 5, compare it against 10. If it is strictly less than 10, select the second cost. This ensures that all values from 5 up to 9 inclusive fall into the middle bracket.
5. If neither of the above conditions hold, the sum must be at least 10, so select the third cost.

The reasoning behind the structure is that the intervals partition the entire number line from 3 to 30 into disjoint regions, and every possible sum falls into exactly one region.

### Why it works

The algorithm relies on the fact that the pricing function is a piecewise constant function over the total weight. Each possible total weight maps deterministically to exactly one interval. Because the conditions are evaluated in increasing order of thresholds, every input is classified exactly once, and no overlap or gap exists between ranges. This guarantees correctness without needing any additional checks or backtracking.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x = int(input())
    y = int(input())
    z = int(input())
    a = int(input())
    b = int(input())
    c = int(input())

    total = x + y + z

    if total < 5:
        print(a)
    elif total < 10:
        print(b)
    else:
        print(c)

if __name__ == "__main__":
    solve()
```

The solution begins by reading all six integers in order. The first three are aggregated immediately into `total`, since individual suitcase structure does not influence the decision anymore.

The conditional chain is carefully ordered from smallest threshold to largest. This ordering is important because it allows each condition to be expressed as a simple upper bound check without needing to encode both lower and upper bounds explicitly. A common mistake is to write overlapping conditions such as `5 <= total < 10` incorrectly, but here the sequential structure avoids that entirely.

## Worked Examples

We construct two representative traces: one below the first threshold and one inside the middle range.

### Example 1

Input:

```
2
3
1
10
20
30
```

| Step | x | y | z | total | Decision |
| --- | --- | --- | --- | --- | --- |
| Start | 2 | 3 | 1 | - | - |
| After sum | 2 | 3 | 1 | 6 | - |
| Check `< 5` | - | - | - | 6 | false |
| Check `< 10` | - | - | - | 6 | true → b |

Output:

```
20
```

This case confirms that values in the middle interval correctly map to the second cost.

### Example 2

Input:

```
4
4
4
5
6
7
```

| Step | x | y | z | total | Decision |
| --- | --- | --- | --- | --- | --- |
| Start | 4 | 4 | 4 | - | - |
| After sum | 4 | 4 | 4 | 12 | - |
| Check `< 5` | - | - | - | 12 | false |
| Check `< 10` | - | - | - | 12 | false → c |

Output:

```
7
```

This trace shows that once the sum crosses the highest threshold, the algorithm correctly falls back to the final pricing tier.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations and comparisons are performed |
| Space | O(1) | No additional data structures are used |

The constraints ensure that constant time behavior is sufficient. Even under extreme repetition of this problem, the per-test cost remains constant, so the solution trivially satisfies all limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample (as interpreted)
assert run("2\n3\n5\n10\n20\n30\n") == "20"

# minimum values
assert run("1\n1\n1\n5\n6\n7\n") == "5"

# boundary at 4
assert run("2\n1\n1\n100\n200\n300\n") == "100"

# boundary at 5
assert run("2\n2\n1\n100\n200\n300\n") == "200"

# boundary at 10
assert run("4\n4\n2\n100\n200\n300\n") == "300"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1,1,1 | 5 | minimum sum case |
| 2,1,1 | 100 | just below 5 threshold |
| 2,2,1 | 200 | exactly 5 threshold |
| 4,4,2 | 300 | exactly 10 threshold |

## Edge Cases

The only meaningful edge cases come from boundary values at 5 and 10.

For a total weight of exactly 5, say inputs `2 2 1`, the sum is 5. The algorithm evaluates `total < 5` as false, then `total < 10` as true, correctly selecting the second cost. This confirms that the lower bound of the second interval is inclusive.

For a total weight of exactly 10, say inputs `4 4 2`, the sum is 10. Both `total < 5` and `total < 10` are false, so the algorithm falls through to the final branch and selects the third cost. This confirms that the third interval correctly starts at 10 and includes it without needing an explicit condition.

No other corner cases exist because the input range is too small to introduce overflow, and there are no structural dependencies between inputs.
