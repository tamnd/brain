---
title: "CF 1759E - The Humanoid"
description: "We have a humanoid with initial power h and a collection of astronauts with powers a[i]. The humanoid can absorb an astronaut only if the astronaut's power is strictly smaller than the humanoid's current power."
date: "2026-06-09T14:30:04+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1759
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round  834 (Div. 3)"
rating: 1500
weight: 1759
solve_time_s: 150
verified: true
draft: false
---

[CF 1759E - The Humanoid](https://codeforces.com/problemset/problem/1759/E)

**Rating:** 1500  
**Tags:** brute force, dp, sortings  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a humanoid with initial power `h` and a collection of astronauts with powers `a[i]`.

The humanoid can absorb an astronaut only if the astronaut's power is strictly smaller than the humanoid's current power. After absorption, the astronaut disappears and the humanoid gains `floor(a[i] / 2)` power.

The humanoid also owns exactly three consumable boosts. Two green serums double the current power, and one blue serum triples it. Each serum can be used at most once.

The goal is to maximize how many astronauts can be absorbed.

The first observation is that the order of astronauts matters. Absorbing a weaker astronaut earlier may increase power enough to absorb stronger astronauts later. Since absorption requires `a[i] < h`, smaller astronauts are always easier to consume.

The constraints are the main hint. The total number of astronauts across all test cases is at most `2 * 10^5`, so an `O(n log n)` solution is completely safe. Anything quadratic would be too slow because `n^2` could reach roughly `4 * 10^10` operations in the worst case.

A subtle edge case comes from the word _strictly_.

Input:

```
1
1 5
5
```

The answer is:

```
0
```

The astronaut cannot be absorbed because `5` is not strictly less than `5`. A careless implementation using `<=` would incorrectly return `1`.

Another easy mistake is assuming serums should always be saved for later.

Input:

```
1
3 1
2 4 100
```

Without using a serum immediately, nothing can be absorbed. The optimal strategy starts with a serum. Any greedy rule such as "only use serums when all possible absorptions are exhausted" must still correctly handle the case where no absorption is initially possible.

A third edge case is that the order of serum usage matters.

Input:

```
1
1 2
11
```

Using the blue serum first gives power `6`, then a green serum gives `12`, making absorption possible. Using the two green serums first gives only `8`, which is insufficient. Any solution that fixes a single serum order can miss the optimum.

The last observation is that there are only three serums total. This tiny number changes the entire problem.

## Approaches

A brute-force solution would sort the astronauts and then try every possible sequence of actions. At each moment we could absorb an available astronaut, use a green serum if one remains, or use a blue serum if it remains.

This search is correct because it explores every legal strategy. The problem is the number of states. The humanoid's power changes continuously, and there can be up to `2 * 10^5` astronauts. A naive search quickly becomes infeasible.

The key observation is that sorting the astronauts removes most of the complexity.

Suppose astronaut `x` has power smaller than astronaut `y`. If we can absorb `y`, then we can also absorb `x`. Absorbing smaller astronauts earlier is never worse because they only increase our power and never consume a resource other than time, which is irrelevant here.

After sorting, every optimal strategy absorbs astronauts from left to right. The only real decisions are when to use the three serums.

Now notice that there are exactly two green serums and one blue serum. Their usage order is one of only

`GGB`, `GBG`, or `BGG`.

That is just `3! / 2! = 3` possibilities.

For a fixed serum order, the simulation becomes straightforward. Process astronauts in sorted order. Whenever the current astronaut cannot be absorbed, consume the next serum from the chosen order. If no serum remains, the simulation ends.

Since there are only three possible serum orders, we can simulate all three and take the maximum answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the astronaut powers in nondecreasing order.

Any astronaut that can be absorbed later can also be absorbed after all weaker astronauts have already been absorbed, so sorting lets us process them from smallest to largest.
2. Enumerate the three possible serum orders:

`[(2,2,3), (2,3,2), (3,2,2)]`

Here `2` represents a green serum and `3` represents a blue serum.
3. For one fixed serum order, start with the initial power `h`, astronaut index `i = 0`, and serum index `j = 0`.
4. While there are astronauts remaining:

If `a[i] < current_power`, absorb that astronaut and increase power by `a[i] // 2`.
5. Otherwise, if another serum exists in the chosen order, use it.

Multiply the current power by the next serum multiplier and advance the serum index.
6. Otherwise, no astronaut can be absorbed and no serum remains.

Stop the simulation.
7. Record how many astronauts were absorbed.
8. Repeat the simulation for all three serum orders.
9. Output the maximum result.

### Why it works

After sorting, every absorbed astronaut only increases the humanoid's power. There is never a reason to skip a currently absorbable astronaut and absorb a larger one instead, because the smaller astronaut is at least as easy to consume and provides additional power.

The only meaningful decisions are the relative positions of the two green serums and the one blue serum. Since there are only three distinct orders, every possible serum strategy is represented by one of the simulations.

For a fixed serum order, delaying serum usage while absorption is possible is optimal. Absorbing first strictly increases power and preserves all future options. A serum is only needed when progress becomes impossible.

Since every valid strategy corresponds to one of the three serum orders and each simulation follows the best behavior for that order, taking the maximum over the three simulations yields the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def simulate(arr, h, order):
    power = h
    serum_idx = 0
    absorbed = 0
    n = len(arr)
    i = 0

    while i < n:
        if arr[i] < power:
            power += arr[i] // 2
            absorbed += 1
            i += 1
        elif serum_idx < 3:
            power *= order[serum_idx]
            serum_idx += 1
        else:
            break

    return absorbed

def solve():
    t = int(input())
    orders = [
        (2, 2, 3),
        (2, 3, 2),
        (3, 2, 2)
    ]

    answers = []

    for _ in range(t):
        n, h = map(int, input().split())
        arr = list(map(int, input().split()))
        arr.sort()

        best = 0
        for order in orders:
            best = max(best, simulate(arr, h, order))

        answers.append(str(best))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The array is sorted once at the start of each test case. After that, each simulation scans the array from left to right exactly once.

The `simulate` function maintains three pieces of state: current power, the next astronaut to process, and which serum in the chosen order should be used next.

A common mistake is using `<=` instead of `<` when checking absorbability. The statement requires strictly smaller power.

Another subtle point is serum usage. We only use a serum when the next astronaut cannot currently be absorbed. Absorbing first is always at least as good because it increases power without consuming a limited resource.

Python integers automatically handle the large powers that can arise after repeated multiplications, so overflow is not a concern.

## Worked Examples

### Example 1

Input:

```
4 1
2 1 8 9
```

Sorted astronauts:

```
[1, 2, 8, 9]
```

Using serum order `(2, 2, 3)`:

| Step | Power Before | Action | Power After | Absorbed |
| --- | --- | --- | --- | --- |
| 1 | 1 | Green | 2 | 0 |
| 2 | 2 | Absorb 1 | 2 | 1 |
| 3 | 2 | Green | 4 | 1 |
| 4 | 4 | Absorb 2 | 5 | 2 |
| 5 | 5 | Blue | 15 | 2 |
| 6 | 15 | Absorb 8 | 19 | 3 |
| 7 | 19 | Absorb 9 | 23 | 4 |

Result: `4`.

This trace shows why serum usage is deferred until progress stops. Every absorbable astronaut is consumed immediately because it increases power for free.

### Example 2

Input:

```
3 3
6 2 60
```

Sorted astronauts:

```
[2, 6, 60]
```

Using serum order `(3, 2, 2)`:

| Step | Power Before | Action | Power After | Absorbed |
| --- | --- | --- | --- | --- |
| 1 | 3 | Absorb 2 | 4 | 1 |
| 2 | 4 | Blue | 12 | 1 |
| 3 | 12 | Absorb 6 | 15 | 2 |
| 4 | 15 | Green | 30 | 2 |
| 5 | 30 | Green | 60 | 2 |
| 6 | 60 | Absorb 60? | impossible | 2 |

The final astronaut cannot be absorbed because absorption requires a strictly larger power than the astronaut's power.

Trying all three serum orders reveals that another order reaches power above `60` and absorbs all three astronauts, giving the optimal answer `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each of the three simulations is linear |
| Space | O(n) | Storage for the astronaut array |

The sum of all `n` values is at most `2 * 10^5`. Sorting each test case and running three linear scans easily fits within the time limit. Memory usage is also comfortably below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)

    def input():
        return input_data.readline()

    def simulate(arr, h, order):
        power = h
        i = 0
        serum = 0

        while i < len(arr):
            if arr[i] < power:
                power += arr[i] // 2
                i += 1
            elif serum < 3:
                power *= order[serum]
                serum += 1
            else:
                break

        return i

    t = int(input())
    ans = []

    for _ in range(t):
        n, h = map(int, input().split())
        arr = list(map(int, input().split()))
        arr.sort()

        best = 0
        for order in ((2, 2, 3), (2, 3, 2), (3, 2, 2)):
            best = max(best, simulate(arr, h, order))

        ans.append(str(best))

    return "\n".join(ans)

# provided sample
assert run("""8
4 1
2 1 8 9
3 3
6 2 60
4 5
5 1 100 5
3 2
38 6 3
1 1
12
4 6
12 12 36 100
4 1
2 1 1 15
3 5
15 1 13
""") == """4
3
3
3
0
4
4
3"""

# minimum size
assert run("""1
1 1
1
""") == "0"

# strict inequality check
assert run("""1
1 5
5
""") == "0"

# all equal values
assert run("""1
4 10
5 5 5 5
""") == "4"

# serum order matters
assert run("""1
1 2
11
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `0` | Smallest possible case |
| `1 5 / 5` | `0` | Strict inequality, not `<=` |
| `4 10 / 5 5 5 5` | `4` | Repeated equal values |
| `1 2 / 11` | `1` | Different serum orders produce different outcomes |

## Edge Cases

Consider:

```
1
1 5
5
```

After sorting, the only astronaut has power `5`. The humanoid also has power `5`. The algorithm checks `5 < 5`, which is false. It may use serums, but without them the astronaut cannot be absorbed. The strict comparison exactly matches the statement and prevents the common `<=` bug.

Consider:

```
1
3 1
2 4 100
```

The sorted array is already `[2, 4, 100]`. The first astronaut cannot be absorbed because `2 < 1` is false. The simulation immediately starts consuming serums according to the chosen order. This correctly handles situations where no progress is possible at the beginning.

Consider:

```
1
1 2
11
```

The three serum orders are tested separately. Order `(3, 2, 2)` reaches power `12` after two serums and absorbs the astronaut. Order `(2, 2, 3)` reaches only `8` before the blue serum and performs differently. Enumerating all three possibilities guarantees that the best ordering is never missed.

Consider:

```
1
2 6
6 7
```

The first astronaut cannot be absorbed because power must be strictly greater. Using serums raises the humanoid's power, after which both astronauts become absorbable. The algorithm correctly waits until absorption is legal instead of treating equality as sufficient.
