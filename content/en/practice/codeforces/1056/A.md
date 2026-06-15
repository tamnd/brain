---
title: "CF 1056A - Determine Line"
description: "We are given a sequence of moments during a tram ride, where each moment corresponds to a stop where Arkady briefly observed which tram lines serve that stop. Each stop lists a set of line identifiers, and Arkady remembers the full set at every observed stop."
date: "2026-06-15T09:54:52+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1056
codeforces_index: "A"
codeforces_contest_name: "Mail.Ru Cup 2018 Round 3"
rating: 800
weight: 1056
solve_time_s: 205
verified: true
draft: false
---

[CF 1056A - Determine Line](https://codeforces.com/problemset/problem/1056/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 3m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of moments during a tram ride, where each moment corresponds to a stop where Arkady briefly observed which tram lines serve that stop. Each stop lists a set of line identifiers, and Arkady remembers the full set at every observed stop.

The task is to determine which tram line Arkady could have been riding. A line is valid if it appears in every observed stop, because the tram must pass through every stop Arkady saw, and therefore its line must be present in the intersection of all observed sets.

The input provides multiple sets of integers, each representing the lines available at a particular stop. The output is any ordering of all integers that are common to every set.

The constraints are small: at most 100 stops, each with at most 100 line identifiers ranging from 1 to 100. This immediately rules out any need for advanced data structures or optimizations beyond simple set intersection. Even an O(n * r) or O(100 * 100) solution is trivial under a 1-second limit.

A subtle issue that can trip implementations is assuming union instead of intersection. For example, if one incorrectly collects all seen lines across stops, they might output lines that appear only once. Another pitfall is failing to initialize the intersection properly. Starting from an empty set and intersecting will always yield an empty result, while starting from the first stop is correct.

A concrete failure case for a naive union-based idea:

Input:

```
2
2 1 2
2 2 3
```

Union approach would produce `{1,2,3}`, but the correct answer is `{2}` because only line 2 appears at both stops.

## Approaches

The brute-force idea is to consider every possible tram line from 1 to 100 and check whether it appears in every stop’s list. For each candidate line, we scan all stops and verify membership. If there are n stops and each check scans up to 100 values, the complexity becomes O(100 * n * 100), which is still small here but conceptually redundant.

The structure of the problem suggests a simpler approach: instead of testing each candidate line, we directly compute the intersection of all sets. The first stop gives a baseline set of possible lines. Every subsequent stop filters this set by removing any line not present in that stop. After processing all stops, the remaining set is exactly the set of valid tram lines.

This works because a valid line must survive every filtering step. Each stop acts as a constraint, and intersection naturally encodes “must satisfy all constraints simultaneously”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check all lines) | O(100 * n * 100) | O(1) extra | Accepted |
| Optimal (set intersection) | O(n * 100) | O(100) | Accepted |

## Algorithm Walkthrough

1. Read all stops, each as a set of integers representing tram lines.
2. Initialize the candidate set using the first stop. This is the only correct starting point because it already satisfies the first observed constraint.
3. For each subsequent stop, replace the candidate set with its intersection with the current stop’s set. This step removes any line that is not present at that stop.
4. After processing all stops, output the remaining elements of the candidate set in any order.

### Why it works

At every step, the candidate set represents exactly the lines that appear in all stops processed so far. This invariant holds because intersection preserves membership only for elements present in both sets. Since we start with the first stop, the invariant is true initially. Each new stop preserves correctness by filtering out invalid lines without introducing new ones. After processing all stops, the invariant extends to the entire input, meaning the final set is exactly the set of lines common to every stop.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

first = set(map(int, input().split()[1:]))

for _ in range(n - 1):
    parts = list(map(int, input().split()))
    s = set(parts[1:])
    first &= s

print(*first)
```

The solution begins by reading the number of stops. The first stop initializes the working set, since it defines the initial valid candidates. Each subsequent line is parsed by skipping the first number (which is just the count of elements in that stop), and converting the remaining values into a set.

The key operation is `first &= s`, which performs in-place intersection. This ensures that only lines present in both sets survive. Using in-place intersection avoids unnecessary memory allocation and keeps the implementation compact.

A common mistake is forgetting to skip the first integer in each line, which represents the size of the set rather than a line identifier. Another mistake is reinitializing the candidate set inside the loop, which would discard previous constraints.

## Worked Examples

### Example 1

Input:

```
3
3 1 4 6
2 1 4
5 10 5 6 4 1
```

We track the candidate set step by step.

| Step | Stop lines | Candidate set |
| --- | --- | --- |
| 1 | {1, 4, 6} | {1, 4, 6} |
| 2 | {1, 4} | {1, 4} |
| 3 | {10, 5, 6, 4, 1} | {1, 4} |

After processing all stops, the remaining candidates are `{1, 4}`.

This confirms that only lines consistently present across all observations survive repeated filtering.

### Example 2

Input:

```
2
2 7 8
3 5 7 9
```

| Step | Stop lines | Candidate set |
| --- | --- | --- |
| 1 | {7, 8} | {7, 8} |
| 2 | {5, 7, 9} | {7} |

The final answer is `{7}` because it is the only line common to both stops.

This shows how a line that appears in most but not all stops is eliminated correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 100) | Each intersection involves at most 100 elements and is repeated for up to 100 stops |
| Space | O(100) | We store only the current candidate set of possible tram lines |

The constraints are tight but small enough that even repeated set operations are trivial. The solution runs comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys as _sys

    input = _sys.stdin.readline

    n = int(input().strip())
    first = set(map(int, input().split()[1:]))

    for _ in range(n - 1):
        parts = list(map(int, input().split()))
        s = set(parts[1:])
        first &= s

    return " ".join(map(str, first)).strip()

# provided sample
assert run("""3
3 1 4 6
2 1 4
5 10 5 6 4 1
""") == "1 4", "sample 1"

# all identical
assert run("""2
3 1 2 3
3 1 2 3
""") in ["1 2 3", "3 2 1"], "all equal"

# disjoint except one
assert run("""3
2 1 2
2 2 3
2 2 4
""") == "2", "single common element"

# single possible line repeated
assert run("""2
1 42
3 42 1 2
""") == "42", "forced line"

# minimal overlap
assert run("""2
2 1 100
2 50 1
""") == "1", "boundary overlap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical sets | all elements | stability when intersection does nothing |
| disjoint except one | single value | correct elimination |
| forced line | 42 | handling singleton intersections |
| boundary overlap | 1 | correctness under sparse overlap |

## Edge Cases

One edge case is when the first stop contains many lines but later stops progressively reduce the set to a single element. The algorithm handles this naturally because intersection is monotonically non-increasing.

For example:

```
3
5 1 2 3 4 5
3 2 4 6
2 2 7
```

Step-by-step:

First set is `{1,2,3,4,5}`.

After second stop `{2,4}` remains.

After third stop `{2}` remains.

The invariant is that the candidate set always contains exactly those lines valid for all processed stops, so shrinking is safe and irreversible.

Another edge case is when all stops share multiple lines. The intersection will preserve all of them without needing any special handling, since no step ever removes a valid common element.
