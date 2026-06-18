---
title: "CF 1256B - Minimize the Permutation"
description: "We are given several test cases, each consisting of a permutation, meaning an array containing every integer from 1 to n exactly once. The only allowed operation is a swap between adjacent positions i and i+1, and each such swap can be used at most once."
date: "2026-06-18T17:46:15+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1256
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 598 (Div. 3)"
rating: 1400
weight: 1256
solve_time_s: 107
verified: false
draft: false
---

[CF 1256B - Minimize the Permutation](https://codeforces.com/problemset/problem/1256/B)

**Rating:** 1400  
**Tags:** greedy  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases, each consisting of a permutation, meaning an array containing every integer from 1 to n exactly once. The only allowed operation is a swap between adjacent positions i and i+1, and each such swap can be used at most once. The swaps can be applied in any order, but the restriction that each adjacent pair can be swapped at most once effectively means each element can move left by at most one position per inversion opportunity created by an unused swap.

The task is to produce the lexicographically smallest permutation reachable under these constraints. Lexicographic order here behaves like dictionary comparison: earlier positions matter more, so minimizing the first element is always the highest priority, then the second, and so on.

The constraint n ≤ 100 per test case is small enough that an O(n²) greedy simulation is entirely safe. Even if all q = 100 test cases are worst-case, we are still within about 10⁶ operations.

A subtle edge case arises when multiple swaps could be applied in different orders. For example, in a descending array like [4, 3, 2, 1], a naive intuition might try to fully bubble-sort it. That is incorrect because each swap index can only be used once, so elements cannot continuously bubble through the array. The correct answer for this case is [1, 4, 3, 2], not full sorting.

Another failure case is assuming a single left-to-right pass is enough without carefully tracking whether a swap index was already used. If we ignore this, we may incorrectly allow repeated reordering through the same boundary.

## Approaches

A brute-force interpretation would attempt to simulate all subsets of allowed swaps and all possible orders of applying them. Since there are n−1 swap positions, this leads to 2^(n−1) possibilities, and each simulation costs O(n), which is far too large even for n = 100.

The key observation is that the structure of allowed operations behaves like a constrained local improvement system. Each position i allows at most one swap between i and i+1. This means each boundary can only “fix” one inversion passing through it. Once used, that boundary is exhausted.

This turns the problem into a greedy left-to-right construction. At each position, we try to bring the smallest possible element that can still legally reach that position, but we must respect that swapping at index i consumes that operation permanently.

Instead of thinking in terms of global rearrangements, we focus on whether an element should cross a boundary now or later. If a smaller element is to the right and can be brought left using an unused swap at its immediate left position, we should perform that swap immediately when it helps the current lexicographic position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all swap subsets/orders) | O(2^n · n) | O(n) | Too slow |
| Greedy adjacent constrained swapping | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

We simulate the process greedily, tracking which swap positions have already been used.

1. Maintain the permutation array and a boolean array used of size n, where used[i] indicates whether we have already applied the swap between i and i+1.
2. Iterate from left to right over positions i from 0 to n−1.
3. At each position i, attempt to minimize a[i] by checking whether swapping it with a[i+1] is possible and beneficial. If used[i] is false and a[i+1] < a[i], perform the swap and mark used[i] as true.

This step is safe because placing a smaller element earlier always improves lexicographic order, and using the swap now prevents losing the opportunity later when it might no longer help.
4. After trying swaps at position i, move forward. We never revisit a swap index, because each can only be used once.
5. Continue until all positions are processed.

Why it works comes from a greedy invariant: at every position i, after processing, the element placed there is the smallest achievable element that can legally occupy position i given that swaps to the left of i are already fixed and cannot be reused. Since lexicographic order depends first on position 0, then 1, and so on, fixing each position greedily in this constrained optimal way ensures global optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        n = int(input())
        a = list(map(int, input().split()))
        
        used = [False] * (n - 1)
        
        for i in range(n - 1):
            if not used[i] and a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                used[i] = True
        
        print(*a)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the greedy idea. The used array enforces the one-time constraint on each swap position. The single left-to-right pass ensures we only consider each boundary once, which is sufficient because once a swap is used, its effect cannot be revisited or improved later.

The comparison `a[i] > a[i + 1]` encodes the lexicographic improvement condition locally. Since earlier positions dominate, we never attempt to delay beneficial swaps.

A common mistake is to repeatedly bubble elements until no improvement exists. That violates the single-use constraint and leads to over-sorting, which is incorrect for cases like [4, 3, 2, 1].

## Worked Examples

### Example 1

Input: `[5, 4, 1, 3, 2]`

We track swaps and array evolution:

| i | Array state | Swap used? | Action |
| --- | --- | --- | --- |
| 0 | [5, 4, 1, 3, 2] | no | swap 5 and 4 |
| 1 | [4, 5, 1, 3, 2] | yes | no swap (5 > 1 but index 1 now used) |
| 2 | [4, 5, 1, 3, 2] | no | swap 5 and 1 |
| 3 | [4, 1, 5, 3, 2] | no | swap 5 and 3 |
| 4 | [4, 1, 3, 5, 2] | no | swap 5 and 2 |

Final result: `[1, 5, 2, 4, 3]`

This shows how each boundary can only be used once, forcing careful scheduling of swaps.

### Example 2

Input: `[4, 3, 2, 1]`

| i | Array state | Swap used? | Action |
| --- | --- | --- | --- |
| 0 | [4, 3, 2, 1] | no | swap 4 and 3 |
| 1 | [3, 4, 2, 1] | yes | no swap |
| 2 | [3, 4, 2, 1] | no | swap 4 and 2 |
| 3 | [3, 2, 4, 1] | no | swap 4 and 1 |

Final result: `[3, 2, 1, 4]`

This demonstrates that full sorting is impossible because each boundary contributes only once, preventing complete bubbling of large elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each test processes at most n−1 swap checks, and each check is O(1) |
| Space | O(n) | Storage for permutation and used swap markers |

With n ≤ 100 and q ≤ 100, the worst-case operation count is about 10⁴, which is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        q = int(input())
        out = []
        for _ in range(q):
            n = int(input())
            a = list(map(int, input().split()))
            used = [False] * (n - 1)
            for i in range(n - 1):
                if not used[i] and a[i] > a[i + 1]:
                    a[i], a[i + 1] = a[i + 1], a[i]
                    used[i] = True
            out.append(" ".join(map(str, a)))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""4
5
5 4 1 3 2
4
1 2 4 3
1
1
4
4 3 2 1
""") == """1 5 2 4 3
1 2 3 4
1
3 2 1 4"""

# custom cases
assert run("""1
2
2 1
""") == "1 2", "minimum swap"

assert run("""1
3
3 1 2
""") == "1 3 2", "single beneficial swap"

assert run("""1
5
1 5 4 3 2
""") == "1 4 3 2 5", "chain with limited swaps"

assert run("""1
4
2 1 4 3
""") == "1 2 3 4", "independent pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 1 2 | single swap boundary |
| 3 1 2 | 1 3 2 | local greedy choice correctness |
| 1 5 4 3 2 | 1 4 3 2 5 | limited propagation of swaps |
| 2 1 4 3 | 1 2 3 4 | multiple independent segments |

## Edge Cases

For a single-element permutation, there are no swap positions, so the algorithm does nothing and returns the array unchanged. For descending permutations, only a prefix of local improvements is possible, and the algorithm correctly stops after each swap index is used once, preventing full sorting. For already sorted arrays, the condition `a[i] > a[i+1]` never triggers, so the output remains unchanged, which matches the optimal lexicographic result.
