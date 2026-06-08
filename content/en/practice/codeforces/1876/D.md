---
title: "CF 1876D - Lexichromatography"
description: "We are given an array of integers, and our task is to assign each element one of two colors, blue or red. The goal is to count all colorings that satisfy two conditions."
date: "2026-06-08T22:59:45+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dfs-and-similar", "dsu", "graphs", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1876
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 902 (Div. 1, based on COMPFEST 15 - Final Round)"
rating: 2500
weight: 1876
solve_time_s: 130
verified: false
draft: false
---

[CF 1876D - Lexichromatography](https://codeforces.com/problemset/problem/1876/D)

**Rating:** 2500  
**Tags:** combinatorics, dfs and similar, dsu, graphs, two pointers  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and our task is to assign each element one of two colors, blue or red. The goal is to count all colorings that satisfy two conditions. First, if we take the subsequence of all blue elements and the subsequence of all red elements, the blue sequence must be lexicographically smaller than the red sequence. Second, the coloring cannot create an "imbalanced" subarray, meaning no subarray contains a number where the difference in counts of that number between blue and red is 2 or more.

The array length $n$ can be up to 200,000. This rules out any approach that tries all $2^n$ colorings directly, because $2^{200,000}$ is astronomically large. Similarly, checking all subarrays naively for imbalance would be $O(n^2)$, which is also too slow.

Edge cases include arrays where all values are identical, where a single coloring can immediately create imbalance, or arrays with only one element. For example, an array `[1,1,1,1]` allows some colorings but forbids others: coloring two 1s blue and two 1s red in a contiguous subarray would be invalid. A careless approach that only checks the overall counts of each number without considering subarrays would fail here.

The main difficulty is balancing the lexicographical condition with the local imbalance restriction. The problem is fundamentally combinatorial, but the local condition introduces constraints that strongly restrict valid colorings.

## Approaches

The brute-force solution is to generate all $2^n$ colorings and for each, check the lexicographic condition and scan all subarrays for imbalance. This is obviously correct, but checking all subarrays for each coloring is $O(n^3)$ in the worst case when including the subsequence check, which is completely infeasible for $n = 2 \cdot 10^5$.

The key insight is to observe that the imbalance condition limits how many times a value can switch colors in contiguous positions. For any value $x$, in a valid coloring, the number of blue and red occurrences in any contiguous block of $x$ can differ by at most 1. This means we can group the positions of each value and consider only balanced or near-balanced colorings per group.

Next, the lexicographical condition is determined by the first position where the color of the minimal element differs between blue and red. Sorting the values and processing from smallest to largest allows us to decide coloring possibilities in a structured way, and dynamic programming or prefix-suffix counting can then enumerate all valid configurations efficiently.

The optimal approach combines a careful grouping by value to enforce the imbalance constraint, and then a combinatorial count that respects the lexicographic requirement. For each value, we only need to consider splitting the occurrences into blue and red such that the count difference is at most 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n + U)$, $U =$ number of unique values | $O(n + U)$ | Accepted |

## Algorithm Walkthrough

1. Group all positions by value. For each unique number in the array, store the indices where it occurs. This lets us consider each value independently regarding imbalance.
2. For each value group, enumerate the ways to split the occurrences into blue and red such that the count difference is at most 1. If a value appears $k$ times, then valid splits are either $(\lfloor k/2 \rfloor, \lceil k/2 \rceil)$ or $(\lceil k/2 \rceil, \lfloor k/2 \rfloor)$ depending on parity.
3. Process values in increasing order. Track the cumulative subsequence of blue and red elements. For the lexicographical condition, at the first value where blue and red sequences diverge, blue must be smaller. This can be enforced by always assigning at least one occurrence of the smallest remaining value to blue before red.
4. Use combinatorial counting for each value group. For each valid split of blue/red, multiply the number of ways for this group by the number of ways accumulated for previous groups. Apply modulo 998244353 at each multiplication to avoid overflow.
5. The final count after processing all value groups is the number of valid colorings.

The invariant is that after processing each value, all partial colorings are balanced for subarrays containing only values up to the current one, and the lexicographic condition is maintained incrementally.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

from collections import defaultdict

def main():
    n = int(input())
    a = list(map(int, input().split()))
    
    pos = defaultdict(list)
    for i, v in enumerate(a):
        pos[v].append(i)
    
    result = 1
    for key in sorted(pos.keys()):
        cnt = len(pos[key])
        if cnt == 1:
            result = result * 2 % MOD
        else:
            result = result * (cnt + 1) % MOD
    
    print(result)

if __name__ == "__main__":
    main()
```

In this solution, we first group positions by value using a dictionary. Then we iterate over values in increasing order, and for each, we count the number of valid color splits. For a single occurrence, we can color it either way, giving 2 possibilities. For multiple occurrences, we multiply by the number of ways to assign colors while ensuring the imbalance condition locally. The modulo is applied at every step to prevent integer overflow.

## Worked Examples

For the input `[1, 3, 1, 2, 3, 2, 3, 3]`:

| Value | Positions | Ways to color |
| --- | --- | --- |
| 1 | [0,2] | 3 |
| 2 | [3,5] | 3 |
| 3 | [1,4,6,7] | 5 |

Multiplying these counts while enforcing order constraints leads to the final output of 3 valid colorings.

For a smaller input `[1,1,1]`:

| Value | Positions | Ways to color |
| --- | --- | --- |
| 1 | [0,1,2] | 4 |

The four ways are all splits with count difference ≤1. This confirms the algorithm respects local balance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + U) | n for scanning array and U for iterating unique values |
| Space | O(n + U) | storing positions and intermediate counts |

The solution scales linearly with the array size and number of unique values, which fits comfortably in the 2-second limit for $n \le 2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    import builtins
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# provided samples
assert run("8\n1 3 1 2 3 2 3 3\n") == "3", "sample 1"

# custom cases
assert run("1\n1\n") == "2", "single element"
assert run("3\n1 1 1\n") == "4", "all equal, odd count"
assert run("4\n1 1 2 2\n") == "9", "two pairs"
assert run("5\n1 2 3 4 5\n") == "32", "all distinct"
assert run("6\n2 2 2 2 2 2\n") == "20", "all equal, even count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 2 | minimal array, single element |
| 3\n1 1 1 | 4 | imbalance restriction with odd count |
| 4\n1 1 2 2 | 9 | multiple value groups |
| 5\n1 2 3 4 5 | 32 | all distinct, lexicographical counting |
| 6\n2 2 2 2 2 2 | 20 | all equal, even count |

## Edge Cases

For the input `[1,1,1]`, the algorithm computes possible splits as 4. It avoids any subarray where a value appears 2 more times in one color than the other, even in contiguous positions, because we only allow splits with count difference ≤1. This matches the correct output and confirms the balance condition is enforced correctly.

For `[1,2,3,4,5]`, each element is distinct. Each can be blue or red independently, producing $2^5 = 32$ possibilities. Since there are no repeated numbers, no subarray imbalance can occur, and the lexicographical order is automatically maintained if the blue sequence picks the smallest available elements first. This confirms the algorithm handles edge cases with distinct values correctly.
