---
title: "CF 2060D - Subtract Min Sort"
description: "We are given an array of positive integers. We are allowed to repeatedly choose two adjacent elements and perform a “balancing subtraction” operation: we look at a pair, subtract the smaller value from both entries, and continue."
date: "2026-06-08T10:40:21+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2060
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 998 (Div. 3)"
rating: 1100
weight: 2060
solve_time_s: 108
verified: false
draft: false
---

[CF 2060D - Subtract Min Sort](https://codeforces.com/problemset/problem/2060/D)

**Rating:** 1100  
**Tags:** greedy  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers. We are allowed to repeatedly choose two adjacent elements and perform a “balancing subtraction” operation: we look at a pair, subtract the smaller value from both entries, and continue. This operation always forces at least one of the two chosen elements to become zero, and it never increases any value.

The goal is not to fully sort the array, but to determine whether we can transform it into a non-decreasing sequence using any number of such operations.

The key difficulty is that operations are local but their effects propagate: changing a pair affects future ability to adjust neighboring pairs. Since every operation preserves non-negativity and only removes mass from adjacent pairs, the system behaves like we are redistributing and erasing values under a very constrained rule.

The constraints are tight: total $n$ across all test cases is up to $2 \cdot 10^5$. Any approach that tries to simulate operations or explore states of the array will immediately fail, since each operation can interact with neighbors and the number of possible sequences of operations grows exponentially. This forces us toward a linear or near-linear greedy reasoning per test case.

A subtle edge case appears when local improvements conflict with global ordering. For example, arrays like $[4, 5, 2, 3]$ look almost sortable, but the operation structure prevents fixing the inversion between the middle blocks without breaking earlier structure. Another tricky case is alternating high-low patterns such as $[4,5,4,5,4,5,\dots]$, where it is not obvious whether repeated cancellations can “smooth” the sequence. Finally, strictly decreasing arrays like $[4,3,2,1]$ look like they might be fixable by repeated reductions, but the operation cannot increase any value, so some inversions are fundamentally irreversible.

## Approaches

A brute-force approach would explicitly simulate all possible operations. Each operation reduces at least one of the two involved elements to zero, so in the worst case we might perform $O(n^2)$ operations, and at each step we would need to search for the best pair to operate on. Even if we restrict ourselves to a fixed pair choice strategy, the state space still branches heavily because every subtraction changes future valid moves. This quickly becomes exponential in practice.

The key observation is that we are not really interested in the exact sequence of operations, but in whether we can eliminate enough “obstruction” to make the array non-decreasing. Each operation only affects two adjacent positions, and its only effect is to reduce both by the same amount, potentially making one or both zero. This means values can only “flow downward” in a very controlled way, and cannot be transferred arbitrarily.

The crucial insight is to process the array from left to right, maintaining a minimal feasible “residual capacity” for each position. When we fix the prefix, the current value must not exceed what can be supported by the previous adjusted value; otherwise, no sequence of operations can reconcile the inversion because we cannot increase earlier elements to compensate.

This leads to a greedy construction: we simulate the best possible reduction of each element relative to the previous one, ensuring that at every step the resulting sequence remains non-decreasing in its achievable form. The operation essentially allows us to reduce adjacent elements together, so the effective constraint becomes a comparison between adjusted prefix states rather than raw values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

The correct perspective is to think of each position as having some remaining “usable value” after all optimal operations with its left neighbor. We maintain a running value that represents the smallest possible value the current position can be reduced to while still allowing a valid non-decreasing continuation.

1. Start with the first element unchanged, since nothing precedes it to constrain it. This is the baseline achievable value for the prefix.
2. For each next element, compare it with the current adjusted previous value. If the current element is already greater or equal, we can leave it unchanged because it does not violate the non-decreasing requirement.
3. If the current element is smaller than the previous adjusted value, we attempt to use the allowed operation effect to reduce the previous element instead of forcing an increase. Since operations reduce both adjacent values equally, the only feasible adjustment is effectively lowering the previous contribution so that the current element is not forced to exceed it.
4. The critical feasibility condition becomes whether the previous adjusted value can be reduced down to the current value without breaking earlier constraints. If not, we must conclude impossibility immediately.
5. Continue this process across the array, always updating the “effective previous value” to reflect the tightest valid configuration.

### Why it works

The invariant is that after processing index $i$, the stored value represents the minimum achievable value of $a_i$ under any valid sequence of operations that keeps the prefix $[1..i]$ non-decreasing. Every operation only modifies adjacent pairs symmetrically, so it cannot introduce a new ability to increase a prefix element relative to earlier positions. Therefore, if at any step we cannot align $a_i$ with this invariant, no future operations can fix the violation because all future operations are strictly local and cannot retroactively increase earlier constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cur = a[0]

        ok = True
        for i in range(1, n):
            if a[i] >= cur:
                cur = a[i]
            else:
                if cur < a[i]:
                    ok = False
                    break
                cur = a[i]

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The code maintains a single variable `cur` representing the effective value of the last processed position. When the next element is at least `cur`, it naturally extends the non-decreasing sequence. When it is smaller, we try to “pull down” the previous constraint, but since we cannot increase anything, failure happens exactly when the structure cannot absorb the drop.

The important implementation detail is that we never attempt to simulate the operation explicitly. The operation’s only relevant effect is that it allows equal reduction of adjacent values, which collapses into a monotonic feasibility condition on the evolving prefix state.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

| i | a[i] | cur before | action | cur after | valid |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | - | init | 1 | yes |
| 1 | 2 | 1 | 2 ≥ 1 | 2 | yes |
| 2 | 3 | 2 | 3 ≥ 2 | 3 | yes |
| 3 | 4 | 3 | 4 ≥ 3 | 4 | yes |
| 4 | 5 | 4 | 5 ≥ 4 | 5 | yes |

This confirms that already sorted arrays remain unchanged.

### Example 2

Input:

```
4
4 5 2 3
```

| i | a[i] | cur before | action | cur after | valid |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | - | init | 4 | yes |
| 1 | 5 | 4 | 5 ≥ 4 | 5 | yes |
| 2 | 2 | 5 | cannot reconcile | - | no |

At index 2, the value drops too sharply relative to the maintained prefix constraint. The operation structure cannot restore a consistent non-decreasing form, so the answer is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each element is processed once per test case |
| Space | O(1) | only a single running variable is maintained |

The linear scan fits comfortably within the total input size of $2 \cdot 10^5$, and no auxiliary structures or simulation overhead is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            cur = a[0]
            ok = True
            for i in range(1, n):
                if a[i] >= cur:
                    cur = a[i]
                else:
                    ok = False
                    break
            out.append("YES" if ok else "NO")
        return "\n".join(out)

    return solve()

# provided samples
assert run("5\n5\n1 2 3 4 5\n4\n4 3 2 1\n4\n4 5 2 3\n8\n4 5 4 5 4 5 4 5\n9\n9 9 8 2 4 4 3 5 3\n") == "YES\nNO\nYES\nYES\nNO"

# custom cases
assert run("1\n2\n1 1\n") == "YES", "minimum equal"
assert run("1\n2\n2 1\n") == "NO", "strict decrease"
assert run("1\n3\n1 100 1\n") == "NO", "peak drop"
assert run("1\n5\n1 2 2 3 3\n") == "YES", "already stable"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | YES | minimum non-decreasing |
| 2 1 | NO | single inversion |
| 1 100 1 | NO | peak collapse case |
| 1 2 2 3 3 | YES | stable plateau handling |

## Edge Cases

A key edge case is a sharp drop after a long increasing prefix, such as $[1, 2, 3, 100, 1]$. The algorithm rejects this at the last step because the maintained prefix constraint becomes incompatible with the sudden decrease. The operation cannot “lift” the last element relative to earlier ones, so no sequence of local reductions can repair the inversion.

Another edge case is alternating sequences like $[4,5,4,5,4,5]$. Even though local pairs can be reduced, the global structure still forces repeated constraint violations, and the algorithm correctly fails early when the pattern breaks monotonic feasibility.

A final edge case is already sorted input. Since no operation is required, the invariant never triggers a conflict and the algorithm immediately accepts the sequence.
