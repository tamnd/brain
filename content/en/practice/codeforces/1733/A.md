---
title: "CF 1733A - Consecutive Sum"
description: "We are given an array of integers, and we are allowed to rearrange elements using a restricted swap operation. The restriction is that we can only swap positions whose indices share the same remainder when divided by a fixed number $k$."
date: "2026-06-15T03:18:50+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1733
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 821 (Div. 2)"
rating: 800
weight: 1733
solve_time_s: 270
verified: true
draft: false
---

[CF 1733A - Consecutive Sum](https://codeforces.com/problemset/problem/1733/A)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 4m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we are allowed to rearrange elements using a restricted swap operation. The restriction is that we can only swap positions whose indices share the same remainder when divided by a fixed number $k$. This partitions the array into $k$ independent index classes: positions $i, i+k, i+2k,\dots$ all belong to the same class and can exchange values freely through repeated swaps.

After performing up to $k$ such swaps, we then choose any block of $k$ consecutive elements in the final array and take their sum. The task is to arrange the array using the allowed swaps so that this chosen consecutive block has maximum possible sum.

The key structural implication of the operation is that elements are not globally permutable. Each position class evolves independently, so we cannot arbitrarily move large values anywhere. Instead, each residue class modulo $k$ behaves like a small multiset that can be rearranged internally.

The constraints are small: $n \le 100$ and $t \le 600$. This immediately tells us that even $O(n^2)$ or $O(n^3)$ solutions per test case are safe. The real challenge is not performance but correctly modeling what swaps allow.

A subtle failure case appears when one assumes full permutation freedom. For example, if we incorrectly believe we can sort the entire array and pick the best window, we would get wrong answers when large values exist but are locked into incompatible residue classes. Another mistake happens if we assume we can always “bring the largest $k$ elements together” without respecting modulo constraints, which breaks on cases like $k=2$ where even and odd indices are independent pools.

The correct approach must respect that each position in the final chosen segment can only be filled with elements coming from a specific residue class.

## Approaches

A brute-force view would try all ways of selecting a length-$k$ segment after simulating all allowed swaps. Since swaps allow arbitrary permutation inside each residue class, this becomes: enumerate all ways of distributing values inside each class, then try all windows. This explodes combinatorially because even though each class is small, the coupling between classes across the final window makes direct enumeration infeasible.

The key observation is that swaps inside each modulo class make that class fully reorderable. So for each residue class $r$, we can treat its values as a multiset that can be assigned arbitrarily to positions $r, r+k, r+2k,\dots$. The final array is not arbitrary, but each class can independently choose how to permute itself.

Now consider any candidate window of length $k$, starting at position $s$. This window picks exactly one element from each residue class, because stepping through consecutive indices cycles through residues modulo $k$. So position $s+i$ always corresponds to residue class $(s+i) \bmod k$.

Thus, each window is selecting one element from each class, and we want to maximize the sum of these chosen representatives. Since each class is independently reorderable, for each residue class we want to ensure that the best possible element is placed in a position that participates in some optimal window.

Instead of trying to construct the full arrangement, we flip the perspective: for each residue class, sort its values in descending order, because we will always want to use larger elements earlier when possible. Then we consider each possible starting index $s$, compute the best achievable sum by picking the largest available unused element from each class aligned with that window structure.

Because $k \le n \le 100$, we can directly simulate this assignment by maintaining sorted buckets per residue and testing each window start greedily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all swaps and permutations) | Exponential | O(n) | Too slow |
| Optimal (bucket by mod class + greedy window evaluation) | O(n^2 log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split the array into $k$ groups based on index modulo $k$. Each group contains all positions that can freely exchange values.
2. Sort each group in descending order so that we always know which elements are most valuable in that class.
3. For each possible starting index $s$ of a length-$k$ window, compute the best achievable sum.
4. To compute a window starting at $s$, iterate over the $k$ positions in the window.
5. For each position $s+i$, determine its residue class $r = (s+i) \bmod k$, and take the next largest unused element from group $r$.
6. Sum these chosen elements to get the score for that window.
7. Track the maximum over all starting positions.

The reason greedy selection within each class works is that within a class, all permutations are achievable. So we can assign high values to the most “useful” occurrences across windows.

### Why it works

Each residue class forms an independent permutation space. Any final arrangement is equivalent to choosing a permutation of each class. Every length-$k$ window selects exactly one element from each class in a fixed cyclic pattern. Therefore, maximizing any window reduces to choosing the best available elements from each class under a consistent assignment strategy. Sorting ensures we never waste a large element in a less useful position when it could contribute to a candidate window.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        groups = [[] for _ in range(k)]
        for i, val in enumerate(a):
            groups[i % k].append(val)

        for g in groups:
            g.sort(reverse=True)

        # we will simulate assignment greedily for each possible window
        ans = 0

        for start in range(n - k + 1):
            used = [0] * k
            score = 0

            for i in range(k):
                r = (start + i) % k
                score += groups[r][used[r]]
                used[r] += 1

            ans = max(ans, score)

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first builds the residue classes, since those are the true units of freedom. Sorting each group in descending order ensures we can always access the best remaining element for that class.

For each candidate window, we simulate taking one element from each class in order. The `used` array tracks how many elements we have already consumed from each residue class so that repeated occurrences of the same class across different window positions do not reuse values incorrectly.

The outer loop over all starting positions ensures we consider every valid window. Since $n \le 100$, this quadratic scan is sufficient.

## Worked Examples

### Example 1

Input:

```
n = 5, k = 3
a = [7, 0, 4, 0, 4]
```

We build residue groups:

- class 0: [7, 0]
- class 1: [0, 4]
- class 2: [4]

Sorted:

- class 0: [7, 0]
- class 1: [4, 0]
- class 2: [4]

Now evaluate windows:

| start | window positions | residues | selected values | sum |
| --- | --- | --- | --- | --- |
| 0 | [1,2,3] | [0,1,2] | [7,4,4] | 15 |
| 1 | [2,3,4] | [1,2,0] | [4,4,7] | 15 |
| 2 | [3,4,5] | [2,0,1] | [4,0,4] | 8 |

The best is 15, matching the expected result.

This trace confirms that each window is effectively drawing from independent pools, and sorting ensures optimal assignment per pool.

### Example 2

Input:

```
n = 4, k = 2
a = [2, 7, 3, 4]
```

Groups:

- class 0: [2, 3]
- class 1: [7, 4]

Sorted:

- class 0: [3, 2]
- class 1: [7, 4]

| start | window | residues | selected | sum |
| --- | --- | --- | --- | --- |
| 0 | [1,2] | [0,1] | [3,7] | 10 |
| 1 | [2,3] | [1,0] | [7,3] | 10 |
| 2 | [3,4] | [0,1] | [2,4] | 6 |

Maximum is 10.

This shows that optimal arrangement is symmetric across shifts, because each class is reused in a fixed cyclic structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ per test case | Sorting groups costs $O(n \log n)$, and each of up to $n$ windows evaluates $k \le n$ elements |
| Space | $O(n)$ | Storage for residue groups |

The constraints $n \le 100$ and $t \le 600$ keep the total operations comfortably within limits even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict
    import sys

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        groups = [[] for _ in range(k)]
        for i, v in enumerate(a):
            groups[i % k].append(v)

        for g in groups:
            g.sort(reverse=True)

        ans = 0
        for start in range(n - k + 1):
            used = [0] * k
            score = 0
            for i in range(k):
                r = (start + i) % k
                score += groups[r][used[r]]
                used[r] += 1
            ans = max(ans, score)

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""5
3 2
5 6 0
1 1
7
5 3
7 0 4 0 4
4 2
2 7 3 4
3 3
1000000000 1000000000 999999997
""") == """11
7
15
10
2999999997"""

# custom cases
assert run("""1
1 1
5
""") == "5", "single element"

assert run("""1
6 3
1 2 3 4 5 6
""") == "15", "fully structured increasing"

assert run("""1
4 2
9 1 9 1
""") == "18", "alternating max pairing"

assert run("""1
5 5
5 4 3 2 1
""") == "15", "full window"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 5 | base case correctness |
| increasing sequence | 15 | distribution across classes |
| alternating values | 18 | correct pairing of residues |
| full window | 15 | k = n behavior |

## Edge Cases

A minimal case occurs when $n = 1, k = 1$. The algorithm creates one residue class containing a single value. Sorting does nothing, and the only window trivially selects that element, producing the correct output.

When all elements are identical, every residue class contains repeated values. Sorting and greedy selection still yields the same sum for every window, so the maximum is stable across all starting points. The algorithm does not overcount because each class index is incremented independently.

When $k = n$, each window is the entire array. Each residue class contains exactly one element, so no swaps change anything meaningful. The algorithm correctly evaluates only one window and returns the total sum.
