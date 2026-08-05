---
title: "CF 102483I - Inflation"
description: "There are balloons with capacities 1, 2, ..., n and gas canisters containing integer amounts of helium. Each canister must be assigned to exactly one balloon, and the amount of helium in a canister cannot be split. A balloon cannot receive more helium than its capacity."
date: "2026-08-05T18:49:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102483
codeforces_index: "I"
codeforces_contest_name: "2018-2019 ICPC Northwestern European Regional Programming Contest (NWERC 2018)"
rating: 0
weight: 102483
solve_time_s: 199
verified: true
draft: false
---

[CF 102483I - Inflation](https://codeforces.com/problemset/problem/102483/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

There are balloons with capacities `1, 2, ..., n` and gas canisters containing integer amounts of helium. Each canister must be assigned to exactly one balloon, and the amount of helium in a canister cannot be split. A balloon cannot receive more helium than its capacity.

The goal is not to maximize the total amount of helium. Instead, after choosing the assignment, we look at the balloon that is filled to the smallest fraction of its capacity. We want to make that worst filled balloon as full as possible.

The input gives the number of balloons and the helium amounts in all canisters. The output is the largest possible value `f` such that every balloon can end up with at least `f` of its capacity filled. If even one valid assignment avoiding explosions does not exist, the answer is `-1`.

The constraint `n <= 2 * 10^5` rules out anything that tries many assignments. There are `n!` possible pairings between balloons and canisters, so a direct search is impossible even for very small inputs. A valid solution needs to be around `O(n log n)` or similar, because sorting a few hundred thousand values is acceptable but quadratic work is not.

The first edge case is a canister that is too large for every possible matching. For example:

```
1
2
```

The only balloon has capacity `1`, but the canister contains `2` units. The correct output is:

```
-1
```

A careless solution that only optimizes the minimum fraction could output a positive value because the canister is "full", but it ignores the explosion constraint.

Another tricky case is empty canisters:

```
3
0 2 3
```

After sorting the canisters become `0, 2, 3`. The first balloon gets the empty canister, so the minimum fraction is `0`. The correct output is:

```
0.0
```

A solution that assumes every balloon can receive some positive amount would fail here.

A third case is when large canisters should be paired with large balloons:

```
3
1 1 3
```

The sorted assignment gives fractions `1/1`, `1/2`, and `3/3`, so the answer is `0.5`. A greedy approach that places the largest canister on the smallest balloon would immediately make an invalid assignment.

## Approaches

A brute-force solution would try every possible permutation of canisters. For each assignment, it would check whether any balloon explodes and calculate the minimum filled fraction. This approach is correct because it examines every possible arrangement, but the number of assignments is `n!`, which becomes unusable almost immediately.

A less extreme version would binary search the answer and run a matching algorithm for each possible fraction. For a fixed fraction `x`, each balloon of size `s` needs a canister containing between `x*s` and `s` helium. A general matching algorithm would work, but it is unnecessary because the balloons have a very special structure.

The key observation is that the balloon capacities are already sorted: `1, 2, ..., n`. If the canisters are sorted increasingly as `c1 <= c2 <= ... <= cn`, the best possible assignment is to pair the smallest canister with the smallest balloon, the second smallest with the second smallest balloon, and so on.

The reason is that assigning a larger canister to a smaller balloon can only make the capacity restriction harder, while moving smaller canisters toward smaller balloons improves the chance of satisfying all lower and upper bounds. After sorting, we only need to check each position independently.

For balloon `i`, the assigned canister must satisfy:

```
x * i <= ci <= i
```

The upper bound checks whether the balloon explodes. The lower bound determines the minimum possible fraction. The best answer is simply the smallest value of `ci / i` after sorting, provided all upper bounds are valid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all canister amounts in nondecreasing order. The sorted order represents the only assignment we need to consider, because the smallest canister should go to the smallest balloon.
2. Check the sorted canister at position `i` against balloon `i + 1`. If the canister contains more than `i + 1` helium, that balloon would explode and no valid assignment exists.
3. For every balloon that is valid, compute the fraction `canister / capacity`. The answer is the minimum of these fractions because the objective is to maximize the least filled balloon.
4. Print the minimum fraction with enough precision.

Why it works: after sorting, every prefix of the canisters contains the smallest available amounts. If the smallest `k` canisters can fill the smallest `k` balloons in sorted order, any other assignment cannot improve the weakest balloon because moving a larger canister to a smaller balloon only consumes a better resource where it is less useful. Thus the sorted pairing gives the maximum possible minimum fraction. The minimum ratio in this pairing is exactly the limiting balloon.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)
    c = list(map(int, input().split()))
    c.sort()

    ans = 1.0
    for i, x in enumerate(c, start=1):
        if x > i:
            print(-1)
            return
        ans = min(ans, x / i)

    print("{:.10f}".format(ans))

if __name__ == "__main__":
    solve()
```

The code first sorts the canisters so that the greedy pairing becomes possible. The loop uses `start=1` because balloon capacities are `1` through `n`, not `0` through `n-1`.

The condition `x > i` checks the explosion rule. This must happen before computing the answer because an overflowing balloon makes the whole assignment impossible.

The variable `ans` stores the weakest balloon fraction seen so far. Python floating point precision is enough here because the required error tolerance is `1e-6`.

There is no integer overflow concern in Python. In languages with fixed-width integers, the comparison should still be done carefully because the original values can be as large as `200000`.

## Worked Examples

For the first sample, the canisters are sorted and matched with balloons:

| Balloon capacity | Canister | Fraction | Current answer |
| --- | --- | --- | --- |
| 1 | 1 | 1.0 | 1.0 |
| 2 | 2 | 1.0 | 1.0 |
| 3 | 2 | 0.666... | 0.666... |
| 4 | 3 | 0.75 | 0.666... |
| 5 | 3 | 0.6 | 0.6 |

The smallest fraction is `0.6`, so no assignment can guarantee a better minimum fill rate.

For the second sample:

```
2
2 2
```

The sorted canisters are already `[2, 2]`.

| Balloon capacity | Canister | Valid? |
| --- | --- | --- |
| 1 | 2 | No |

The first balloon would receive twice its capacity. The algorithm immediately outputs `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the single linear scan |
| Space | O(n) | The array of canister amounts is stored |

The largest input has `200000` canisters, so sorting followed by one pass easily fits within the time limit and memory limit.

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
    return result.strip()

# minimum size
assert run("1\n0\n") == "0.0000000000"

# provided sample 1
assert run("5\n1 3 2 2 3\n") == "0.6000000000"

# impossible overflow
assert run("2\n2 2\n") == "-1"

# all equal values
assert run("4\n1 1 1 1\n") == "0.2500000000"

# catches ordering mistakes
assert run("3\n1 1 3\n") == "0.5000000000"

# maximum-size style input
assert run("5\n1 2 3 4 5\n") == "1.0000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0.0` | Single balloon and empty canister |
| `1 3 2 2 3` | `0.6` | Normal greedy pairing |
| `2 2` | `-1` | Explosion detection |
| `1 1 1 1` | `0.25` | Small ratios and repeated values |
| `1 1 3` | `0.5` | Correct sorted assignment |
| `1 2 3 4 5` | `1.0` | Perfect filling case |

## Edge Cases

For the overflowing canister case:

```
1
2
```

The sorted list contains one canister with value `2`. The algorithm compares it with balloon capacity `1` and detects `2 > 1`, so it returns `-1` before calculating any fraction.

For empty canisters:

```
3
0 2 3
```

The sorted order is unchanged. The fractions are `0/1`, `2/2`, and `3/3`. The minimum is `0`, which is the best possible answer because one balloon must remain empty.

For cases where the order matters:

```
3
1 1 3
```

The sorted assignment gives balloon capacities `1, 2, 3` with helium `1, 1, 3`. The fractions are `1`, `0.5`, and `1`. The algorithm returns `0.5`. Assigning the largest canister to the smallest balloon first would not improve the minimum fraction and could create invalid states in more complicated inputs.
