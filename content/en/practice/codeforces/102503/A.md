---
title: "CF 102503A - Vincent Adultman"
description: "We have four people with heights v, a, r, and p. We must choose exactly three of them and stack those three people together. The resulting height is the sum of their three individual heights. The rollercoaster accepts the resulting person if that sum is at least h."
date: "2026-08-09T19:06:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "A"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 520
verified: true
draft: false
---

[CF 102503A - Vincent Adultman](https://codeforces.com/problemset/problem/102503/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We have four people with heights `v`, `a`, `r`, and `p`. We must choose exactly three of them and stack those three people together. The resulting height is the sum of their three individual heights. The rollercoaster accepts the resulting person if that sum is at least `h`.

The task is to determine whether at least one of the four possible groups of three reaches the required height. If such a group exists, we print `WAW`; otherwise, we print `AWW`.

The input contains the four heights on the first four lines, followed by the required minimum height `h`. Every value is between 12 and 150, so the values are tiny and integer arithmetic is more than sufficient. More importantly, there are exactly four people, which means there are only `C(4,3) = 4` possible groups to check. Even a direct exhaustive search performs a constant number of additions and comparisons, so the 1 second time limit is nowhere near restrictive.

There are a few boundary cases that can cause an incorrect implementation if the condition is written carelessly. First, reaching exactly the required height is enough. For example, with heights `12, 12, 12, 20` and `h = 36`, choosing the three people of heights `12, 12, 12` gives exactly `36`, so the correct output is `WAW`. Using `>` instead of `>=` would incorrectly print `AWW`.

A second case occurs when the only successful group contains the tallest person. For example, with heights `12, 12, 12, 20` and `h = 44`, the three largest heights sum to `44`, so the answer is `WAW`. An implementation that checks only the first three input values would miss the valid group.

A third case is when even the three tallest people are too short. With heights `20, 20, 20, 20` and `h = 61`, every possible group has height `60`, so the answer is `AWW`. The fact that four people together would reach `80` does not help, because the formed person must contain exactly three people.

## Approaches

A brute-force solution can simply enumerate every group of three people, add their heights, and check whether the sum is at least `h`. This is completely correct because every legal choice is examined. With four people, there are exactly `C(4,3) = 4` such groups, so the worst case requires four additions and four comparisons, up to constant overhead for enumeration.

There is actually no point where this brute-force method becomes too slow for the given problem. The input size is fixed at four people, so its running time is `O(1)`. In a generalized version with `n` people, checking every triple would take `O(n^3)`, which could become expensive. For this particular Codeforces problem, however, `n = 4`, making the exhaustive method both simple and fully accepted.

We can make the same observation even more compactly. Among all groups of three people, the group with the largest possible sum consists of the three tallest people. If those three cannot reach `h`, no other group can. If they can, that group itself is a valid choice. Thus, sorting the four heights and checking the three largest values also solves the problem in constant time, although sorting is unnecessary.

The direct enumeration is preferable because it mirrors the definition of the task exactly and avoids introducing an operation that the problem does not need. The crucial insight is that the search space contains only four choices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(1)` for four people | `O(1)` | Accepted |
| Check three tallest | `O(1)` for four people | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read the four heights into an array and read the required height `h`. Keeping the heights together makes it easy to reason about every possible group of three.
2. Enumerate every combination of three distinct positions among the four heights. There are only four combinations, so every legal group can be checked directly.
3. For each combination, calculate the sum of its three heights and compare it with `h`. Use `>=` because a person whose height is exactly the minimum allowed height can ride.
4. If any sum is at least `h`, immediately print `WAW`. Finding one successful group is enough because the question asks whether at least one valid group exists.
5. If all four combinations fail the comparison, print `AWW`. At that point every possible group of three has been checked, so no valid arrangement exists.

### Why it works

The invariant is that after checking any number of combinations, every checked combination has been correctly classified as either tall enough or too short. The algorithm examines all four possible groups of three. If it prints `WAW`, it has found a group whose sum is at least `h`, so the answer is valid. If it prints `AWW`, every possible group has sum below `h`, so no valid group exists. Since the algorithm considers every legal choice, it cannot miss a solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

v = int(input())
a = int(input())
r = int(input())
p = int(input())
h = int(input())

heights = [v, a, r, p]

for i in range(4):
    for j in range(i + 1, 4):
        for k in range(j + 1, 4):
            if heights[i] + heights[j] + heights[k] >= h:
                print("WAW")
                sys.exit()

print("AWW")
```

The four heights are stored in a list so the combination loops can work uniformly. The three nested loops use `i < j < k`, which guarantees that every set of three people is considered exactly once and that no person is selected twice.

The comparison uses `>= h`, matching the requirement that the formed person's height may be exactly the threshold. As soon as a valid triple is found, `sys.exit()` terminates the program because examining any remaining triples cannot change the answer.

There is no integer overflow concern in Python, and even in languages with fixed-width integer types the largest possible sum here is only `150 + 150 + 150 = 450`.

The input contains only one test case, so there is no outer test-case loop. The requested `input = sys.stdin.readline` form is still used for efficient and standard competitive-programming input handling.

## Worked Examples

### Sample 1

The four heights are all `20`, and the required height is `61`. Every group of three has the same sum.

| `i` | `j` | `k` | Selected heights | Sum | `sum >= h` |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 20, 20, 20 | 60 | No |
| 0 | 1 | 3 | 20, 20, 20 | 60 | No |
| 0 | 2 | 3 | 20, 20, 20 | 60 | No |
| 1 | 2 | 3 | 20, 20, 20 | 60 | No |

All four legal groups fail because `60 < 61`. The algorithm reaches the final `print("AWW")`, producing the correct output.

### Sample 2

The heights are `24, 55, 42, 69`, with `h = 143`.

| `i` | `j` | `k` | Selected heights | Sum | `sum >= h` |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 24, 55, 42 | 121 | No |
| 0 | 1 | 3 | 24, 55, 69 | 148 | Yes |

The second group already reaches `143`, so the algorithm prints `WAW` and exits without needing to examine the remaining two combinations. This demonstrates why the algorithm can stop as soon as one valid group is found.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(1)` | There are exactly four triples to examine. |
| Space | `O(1)` | The algorithm stores only four heights and a constant number of loop variables. |

The constraints are extremely small, and the algorithm performs only a handful of integer additions and comparisons. It is comfortably within both the 1 second time limit and the 512 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    heights = [int(input()), int(input()), int(input()), int(input())]
    h = int(input())

    for i in range(4):
        for j in range(i + 1, 4):
            for k in range(j + 1, 4):
                if heights[i] + heights[j] + heights[k] >= h:
                    return "WAW"

    return "AWW"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("20\n20\n20\n20\n61\n") == "AWW", "sample 1"
assert run("24\n55\n42\n69\n143\n") == "WAW", "sample 2"

# Minimum-size values, and exactly reaching the threshold.
assert run("12\n12\n12\n12\n36\n") == "WAW", "minimum values at boundary"

# Maximum-size values, with a threshold that is exactly reachable.
assert run("150\n150\n150\n12\n450\n") == "WAW", "maximum values at boundary"

# All groups are one unit short of the threshold.
assert run("20\n20\n20\n20\n61\n") == "AWW", "just below threshold"

# The only successful group contains the fourth input value.
assert run("12\n12\n12\n20\n44\n") == "WAW", "valid group uses fourth person"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `12 12 12 12, h = 36` | `WAW` | Minimum values and exact threshold |
| `150 150 150 12, h = 450` | `WAW` | Maximum values and exact threshold |
| `20 20 20 20, h = 61` | `AWW` | Three people are just below the requirement |
| `12 12 12 20, h = 44` | `WAW` | A successful group must include the fourth person |

## Edge Cases

The equality boundary is handled by the `>=` comparison. For input

```
12
12
12
12
36
```

the first triple has sum `12 + 12 + 12 = 36`. Since `36 >= 36`, the algorithm immediately returns `WAW`. An implementation using `>` would incorrectly reject this case.

The case where the fourth person is essential is handled because the nested loops do not privilege any input position. For

```
12
12
12
20
44
```

the first three triples have sums below `44`, but the combination containing heights `12, 12, 20` reaches `44`. When the loops reach indices `1, 2, 3`, the condition succeeds and the output is `WAW`.

The case where four people would be enough but three are not is also handled correctly. With

```
20
20
20
20
61
```

each legal triple has height `60`. The algorithm never considers all four people together, because the task allows only three people in the formed person. Every triple fails, so the output is `AWW`.

Finally, the maximum values do not require any special handling. With

```
150
150
150
12
450
```

the first three people already reach `450`, exactly the required height. The algorithm prints `WAW`, and Python's integer arithmetic handles the sum directly without any overflow concerns.

A shorter editorial could also use the even simpler observation that only the three tallest people matter, but the exhaustive version is arguably clearer for this problem because there are only four possible triples.
