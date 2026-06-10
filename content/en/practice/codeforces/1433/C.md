---
title: "CF 1433C - Dominant Piranha"
description: "We are asked to identify a dominant piranha in a linear aquarium. Each piranha has a size, and a piranha is dominant if it can eventually eat all other piranhas by repeatedly consuming an adjacent piranha smaller than itself. Every time it eats, its size increases by one."
date: "2026-06-11T05:03:44+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1433
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 677 (Div. 3)"
rating: 900
weight: 1433
solve_time_s: 505
verified: false
draft: false
---

[CF 1433C - Dominant Piranha](https://codeforces.com/problemset/problem/1433/C)

**Rating:** 900  
**Tags:** constructive algorithms, greedy  
**Solve time:** 8m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to identify a dominant piranha in a linear aquarium. Each piranha has a size, and a piranha is dominant if it can eventually eat all other piranhas by repeatedly consuming an adjacent piranha smaller than itself. Every time it eats, its size increases by one. The input provides multiple test cases, each specifying the number of piranhas and their sizes. The output must either be the 1-based index of any dominant piranha or -1 if none exists.

The constraints imply that a brute-force simulation of all possible moves is infeasible because the total number of piranhas across all test cases can reach 300,000. Simulating each possible eating sequence for every candidate piranha would produce a quadratic or worse complexity, which is unacceptable for a 2-second time limit.

Non-obvious edge cases arise when all piranhas have the same size. In such a scenario, no piranha can eat another, so the correct output is -1. Another subtle case is when the maximum size appears multiple times in the array; only the maximum with at least one neighbor smaller than itself can potentially be dominant. For example, in `[5, 5, 4, 3, 5]`, the first and last `5` cannot eat any adjacent piranha that is smaller, but the middle `5` can eat the `4` to its right, so it is a valid candidate.

## Approaches

The naive approach is to try each piranha as a candidate and simulate its moves until it either eats all other piranhas or gets stuck. This works because the rules are deterministic: a piranha can only eat a smaller adjacent one. However, for an array of size `n`, a single simulation could involve `O(n^2)` steps, and summing over all test cases would lead to operations exceeding `10^10`, which is too slow.

The key insight is that only piranhas with the **maximum size** can be dominant. A piranha smaller than the maximum can never consume a larger piranha, so it is immediately disqualified. Among the piranhas of maximum size, a piranha can be dominant only if it has **at least one neighbor smaller than itself**. This is because it needs a starting point to grow, and without a smaller neighbor, it cannot initiate the eating process. With this observation, we only need to scan the array once to find the maximum and then look at its neighbors. This reduces the complexity to linear in the array size for each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) per test case | O(n) | Too slow |
| Maximum + Neighbor Check | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of piranhas `n` and the array `a` of sizes.
2. Find the maximum size in the array.
3. Traverse the array to locate a piranha with this maximum size that has at least one neighbor smaller than itself.
4. If such a piranha exists, output its 1-based index and stop searching further.
5. If no such piranha is found after scanning the array, output -1.

Why it works: By definition, only piranhas of maximum size can eat all others. A maximum-size piranha with no smaller neighbors cannot start consuming, so it cannot dominate. Any maximum-size piranha with at least one smaller neighbor can greedily eat left or right, and after consuming the neighbor, it grows and can continue to eat until all other piranhas are gone. The invariant is that the candidate must always be able to initiate eating; the algorithm checks exactly that.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        max_size = max(a)
        
        dominant_index = -1
        for i in range(n):
            if a[i] == max_size:
                if (i > 0 and a[i-1] < max_size) or (i < n-1 and a[i+1] < max_size):
                    dominant_index = i + 1  # 1-based index
                    break
        print(dominant_index)

if __name__ == "__main__":
    solve()
```

The code begins by reading the number of test cases. For each test case, it computes the maximum size and then iterates through the array to find a maximum-size piranha that has at least one smaller neighbor. The `i + 1` adjustment converts from 0-based to 1-based indexing required by the problem. The break ensures we output the first valid candidate, although any valid candidate is acceptable.

## Worked Examples

**Example 1:** `[5, 3, 4, 4, 5]`

| i | a[i] | Neighbor check | Dominant? |
| --- | --- | --- | --- |
| 0 | 5 | right=3 < 5 | Yes |

The first piranha is maximum and has a smaller neighbor, so index `1` is valid. In the sample solution, the algorithm picks index `3` instead, which also works. Multiple answers are acceptable.

**Example 2:** `[1, 1, 1]`

| i | a[i] | Neighbor check | Dominant? |
| --- | --- | --- | --- |
| 0 | 1 | right=1 | No |
| 1 | 1 | left=1, right=1 | No |
| 2 | 1 | left=1 | No |

No maximum-size piranha has a smaller neighbor. Output `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single scan to find max and check neighbors |
| Space | O(1) extra | Only a few variables besides input array |

With the sum of `n` across all test cases ≤ 300,000, the algorithm comfortably runs in linear time within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio
    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("6\n5\n5 3 4 4 5\n3\n1 1 1\n5\n4 4 3 4 4\n5\n5 5 4 3 2\n3\n1 1 2\n5\n5 4 3 5 5\n") == "3\n-1\n4\n3\n3\n1", "sample 1"

# Custom cases
assert run("1\n2\n1 2\n") == "2", "two elements, dominant at end"
assert run("1\n3\n3 3 3\n") == "-1", "all equal sizes"
assert run("1\n4\n1 5 5 1\n") == "2", "middle max with left neighbor smaller"
assert run("1\n5\n5 1 5 1 5\n") == "1", "multiple maxima, first with smaller neighbor"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2\n1 2` | 2 | Correct identification when dominant is at the end |
| `3\n3 3 3` | -1 | No dominant piranha when all are equal |
| `4\n1 5 5 1` | 2 | Picks maximum with smaller neighbor correctly |
| `5\n5 1 5 1 5` | 1 | Chooses first maximum with valid neighbor |

## Edge Cases

For arrays where all piranhas have the same size, the algorithm correctly outputs -1 because no piranha has a smaller neighbor to initiate eating. In arrays with multiple maximums, the algorithm always finds the first maximum with a smaller neighbor. For minimal input size `n=2`, the check works correctly: if one piranha is strictly larger than the other, it will be chosen as dominant. For maximum input size, the linear scan ensures performance stays within constraints.
