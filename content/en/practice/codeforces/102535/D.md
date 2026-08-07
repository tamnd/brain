---
title: "CF 102535D - Clingy Mo"
description: "We have a line of explosives represented by an array E. An explosive at position i can activate only when there is at least one explosive somewhere before it and at least one explosive somewhere after it."
date: "2026-08-07T21:12:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "D"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 82
verified: true
draft: false
---

[CF 102535D - Clingy Mo](https://codeforces.com/problemset/problem/102535/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of explosives represented by an array `E`. An explosive at position `i` can activate only when there is at least one explosive somewhere before it and at least one explosive somewhere after it. The task is to add the ratings of exactly those explosives that satisfy this condition.

The input gives the number of explosives followed by their ratings from left to right. The output is the total rating contributed by all positions that are not at either end of the line and are surrounded by other explosives.

The constraint `n <= 100` is very small. A direct simulation or repeated checking is already fast enough because even an `O(n^2)` solution would perform only around ten thousand operations. However, the interesting part of the problem is recognizing the condition instead of overcomplicating it. The small bound also means we do not need advanced data structures or optimizations.

The ratings can be as large as 1000, so the final sum can reach about 100000. Python integers handle this easily, and there is no need for special overflow handling.

A common mistake is forgetting that the first and last explosives can never explode because one side is missing. For example:

```
Input:
3
5 8 2
```

The correct output is:

```
8
```

The middle explosive has neighbors on both sides, while the two ends do not. A careless implementation that only checks whether the array has multiple elements might incorrectly include the endpoints.

Another edge case is a line with fewer than three explosives:

```
Input:
2
5 10
```

The correct output is:

```
0
```

Neither explosive has both a left side and a right side. An implementation that loops incorrectly over the whole array and accesses nonexistent neighbors could fail or accidentally count an endpoint.

## Approaches

The straightforward approach is to inspect every explosive and ask whether there is something on both sides. For each position, we can scan the elements before it and after it. If both scans find at least one explosive, we add its rating to the answer. This is correct because the condition for an explosion is exactly the existence of a left and right neighbor somewhere in the array.

The problem with this method is that it repeats work. When checking many positions, the same information about the left and right sides is rediscovered again and again. In the worst case, every position performs a scan through almost the entire array, giving roughly `n * n` operations.

The key observation is that the condition does not depend on the values of the other explosives at all. It only depends on the position. Every position except the first and last one automatically has at least one element to its left and at least one element to its right. This turns the problem from repeatedly checking a condition into simply summing the middle section of the array.

The brute-force method works because it directly tests the rule for every explosive, but it fails by spending time rediscovering the same positional information. The observation that only the endpoints are invalid reduces the problem to a single pass through the valid range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted for these constraints, but unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of explosives and their ratings. The array order matters because the condition depends on an explosive's position.
2. Initialize the answer to zero. We only need a running sum because each explosive is considered independently.
3. Iterate through positions from index `1` to index `n - 2`. These are exactly the positions that have at least one element before them and at least one element after them.
4. Add the rating at each visited position to the answer. Every visited position satisfies the explosion condition by its location alone.
5. Print the accumulated sum.

Why it works:

The only positions that fail the requirement are the two ends of the array. The first position has no explosive on its left, and the last position has no explosive on its right. Every other position has at least one index smaller and at least one index larger, so every middle element must contribute its rating. The algorithm sums exactly these middle elements and excludes exactly the invalid endpoints, which proves the result is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    e = list(map(int, input().split()))

    ans = 0
    for i in range(1, n - 1):
        ans += e[i]

    print(ans)

if __name__ == "__main__":
    solve()
```

The input is stored in a list because we need direct access to positions. The loop starts at `1` instead of `0` because the first explosive cannot explode. It stops before `n - 1` because the last explosive also cannot explode.

When `n` is `1` or `2`, the range `range(1, n - 1)` is empty. This naturally gives an answer of zero without requiring a separate boundary condition.

The code only stores the input array and one integer accumulator. The sum operation order does not create any overflow issue in Python.

## Worked Examples

For the first sample:

```
6
1 3 5 2 3 10
```

The first and last values are excluded. The middle values are all valid.

| Index | Rating | Included? | Current sum |
| --- | --- | --- | --- |
| 1 | 3 | Yes | 3 |
| 2 | 5 | Yes | 8 |
| 3 | 2 | Yes | 10 |
| 4 | 3 | Yes | 13 |

The final answer is `13`. This trace shows that the algorithm includes every position with elements on both sides.

For the second sample:

```
2
5 10
```

There are no middle positions.

| Index | Rating | Included? | Current sum |
| --- | --- | --- | --- |
| None | None | No valid positions | 0 |

The final answer remains `0`. This demonstrates the boundary case where the entire array consists only of endpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each middle explosive is visited once |
| Space | O(1) excluding input storage | Only the answer variable is used during processing |

With `n <= 100`, the linear solution is easily within the time limit. Even the less efficient quadratic method would pass, but the linear approach directly reflects the structure of the condition and avoids unnecessary checks.

## Test Cases

```python
import sys
import io

def solve(data):
    lines = data.strip().split()
    if not lines:
        return ""
    n = int(lines[0])
    e = list(map(int, lines[1:]))

    ans = 0
    for i in range(1, n - 1):
        ans += e[i]
    return str(ans)

def run(inp: str) -> str:
    return solve(inp)

assert run("6\n1 3 5 2 3 10\n") == "13", "sample 1"
assert run("2\n5 10\n") == "0", "sample 2"

assert run("1\n7\n") == "0", "single explosive has no sides"
assert run("3\n4 9 6\n") == "9", "only middle explosive counts"
assert run("5\n1 1 1 1 1\n") == "3", "all equal values"
assert run("100\n" + " ".join(["1000"] * 100) + "\n") == "98000", "maximum size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` explosive | `0` | Minimum size and empty iteration range |
| `3` explosives | Middle value | Only one valid position exists |
| Five equal ratings | Sum of three middle values | Confirms endpoint exclusion |
| One hundred maximum ratings | `98000` | Maximum input size and large sums |

## Edge Cases

For the endpoint case:

```
Input:
3
5 8 2
```

The loop begins at index `1` and ends at index `1`, so only the value `8` is added. The algorithm never considers index `0` or index `2`, matching the rule that endpoints cannot explode. The output is `8`.

For the two-element case:

```
Input:
2
5 10
```

The loop becomes `range(1, 1)`, which contains no positions. The answer stays zero, correctly handling the situation where no explosive has both sides available.

For a single explosive:

```
Input:
1
100
```

There is no possible middle position. The loop does not execute, and the output is `0`. This prevents an off-by-one mistake where the only element might be counted despite having no neighbors.
