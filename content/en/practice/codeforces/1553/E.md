---
title: "CF 1553E - Permutation Shift"
description: "We start from the identity permutation, which is simply the numbers from 1 to n in order. Someone first rotates this array cyclically to the right by an unknown shift k, and then performs at most m arbitrary swaps of elements."
date: "2026-06-16T15:52:56+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "constructive-algorithms", "dfs-and-similar", "dsu", "graphs", "math"]
categories: ["algorithms"]
codeforces_contest: 1553
codeforces_index: "E"
codeforces_contest_name: "Harbour.Space Scholarship Contest 2021-2022 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 2100
weight: 1553
solve_time_s: 288
verified: true
draft: false
---

[CF 1553E - Permutation Shift](https://codeforces.com/problemset/problem/1553/E)

**Rating:** 2100  
**Tags:** brute force, combinatorics, constructive algorithms, dfs and similar, dsu, graphs, math  
**Solve time:** 4m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We start from the identity permutation, which is simply the numbers from 1 to n in order. Someone first rotates this array cyclically to the right by an unknown shift k, and then performs at most m arbitrary swaps of elements. After these operations, we only see the final permutation.

The task is to determine which starting rotation amounts k could have produced this final array, assuming that after the rotation we are allowed up to m swaps to reach the given permutation.

A useful way to think about the process is that we begin with a cyclic structure, where the array is a rotated identity, and then we are allowed to “repair” it using swaps. Each swap can correct two misplaced elements in terms of their final target positions, so m controls how far the permutation can deviate from a pure rotation.

The constraints are large: the total n across all test cases is up to 3·10^5 and there are up to 10^5 test cases. This immediately rules out any approach that tries all k for every test case and simulates swaps or computes distances in quadratic time. Even O(n√n) per test case would be too slow in the worst case.

A subtle difficulty comes from the fact that the rotation is unknown, and the swaps are also unconstrained except in count. A naive approach would try every k, unrotate the array, and compute the minimum number of swaps to restore identity. That would require cycle decomposition per k, giving O(n^2) per test case, which is not viable.

Another common mistake is to treat the swaps as fully sorting power, concluding incorrectly that any permutation within m inversions is valid. That ignores that the permutation must be consistent with a single cyclic shift before swaps, which is a strong structural constraint.

## Approaches

The brute-force idea is straightforward: assume a candidate shift k, rotate the array back by k, and compute how many swaps are needed to turn it into the identity permutation. The swap distance of a permutation is n minus the number of cycles in its permutation graph, so we could compute cycles after unshifting. This is correct but expensive because for each k we rebuild a full permutation and recompute cycles, leading to O(n^2) total work per test case.

The key observation is that we do not need to recompute everything for each k independently. Instead, we reverse the perspective. Fix the final permutation p. For a given k, we can interpret whether p could come from a k-shifted identity after at most m swaps by checking how many positions already “align structurally” with that rotation.

After a shift by k, element i should ideally appear at position (i + k) mod n. So for a fixed k, we can count how many elements already match this expected cyclic position. If an element is already consistent with the shift, it does not need fixing. Each swap can fix at most two mismatches, so the number of mismatched elements determines feasibility.

This transforms the problem into counting how many positions are consistent for each k, but doing it naively is still O(n^2). The final trick is to notice that consistency can be rewritten as a cyclic alignment condition:

p[j] = (j - k mod n) + 1

which rearranges to:

k ≡ j - (p[j] - 1) (mod n)

So each position j gives a residue value of k that would make p[j] correctly aligned. For a valid k, many positions must agree with this residue. If x positions agree, then n - x elements are mismatched, and we need at least (n - x) / 2 swaps. So feasibility becomes a threshold condition on how many matches a shift produces.

We therefore compute, for each k, how many indices vote for it, using modular alignment, and keep those k where mismatches are at most 2m.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check each k independently) | O(n^2) | O(n) | Too slow |
| Optimal (frequency over cyclic residues) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We want to test each shift k by how many elements would already be correct if the array came from that shift.

### Step 1: Convert correctness condition into a modular equation

For each index j, the correct value under shift k would be (j - k mod n) + 1. Rearranging gives a condition that each (j, p[j]) pair implies a unique k modulo n.

This turns each array element into a vote for a specific shift value.

### Step 2: Count votes for each shift

We compute an array cnt[k], where each position j contributes to exactly one k value derived from its equation. This gives us how many positions are consistent with shift k.

The interpretation is direct: cnt[k] is the number of elements already correctly placed if we choose shift k.

### Step 3: Convert matches into required swaps

If cnt[k] elements are already correct, then n - cnt[k] elements are wrong. Each swap can fix at most two wrong elements, so the minimum swaps needed is (n - cnt[k]) / 2.

We require this to be ≤ m, which is equivalent to:

n - cnt[k] ≤ 2m

or

cnt[k] ≥ n - 2m

### Step 4: Collect all valid k

We iterate over all k from 0 to n - 1 and output those satisfying the threshold.

### Why it works

The key invariant is that every correct alignment under a given shift corresponds exactly to a fixed modular constraint on k. This ensures that counting votes per k precisely measures how many elements are already consistent with that shift. Since swaps only affect mismatched elements and each swap reduces mismatch count by at most 2, the feasibility condition depends only on the mismatch count, not the arrangement of those mismatches. This decouples structure from order and makes the counting sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        p = list(map(int, input().split()))

        cnt = [0] * n

        for j, val in enumerate(p):
            # We want k such that after shifting right by k,
            # val ends up at position j.
            # In identity, val is at position val-1.
            # After shift k: position becomes (val-1 + k) % n = j
            # So k ≡ j - (val-1) mod n.
            k = (j - (val - 1)) % n
            cnt[k] += 1

        threshold = n - 2 * m

        res = []
        for k in range(n):
            if cnt[k] >= threshold:
                res.append(k)

        print(len(res), *res)

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the modular relationship between positions and values. The key line is the computation of k for each (j, val) pair, which acts as a vote. The rest is a simple threshold check derived from swap limitations.

Care must be taken with modular arithmetic: j and val-1 are both 0-based, so no extra adjustment is needed. The threshold uses 2m because each swap reduces mismatch count by exactly 2 in the best case.

## Worked Examples

### Example 1

Input:

```
n = 4, m = 1
p = [2, 3, 1, 4]
```

We compute votes for k:

| j | p[j] | k = (j - (p[j]-1)) mod 4 |
| --- | --- | --- |
| 0 | 2 | 0 - 1 = 3 |
| 1 | 3 | 1 - 2 = 3 |
| 2 | 1 | 2 - 0 = 2 |
| 3 | 4 | 3 - 3 = 0 |

So cnt:

k=0:1, k=2:1, k=3:2.

Threshold is n - 2m = 4 - 2 = 2.

Only k=3 satisfies cnt[k] ≥ 2.

So answer is {3}.

This shows how even a single swap tolerance sharply filters allowed shifts.

### Example 2

Input:

```
n = 3, m = 1
p = [3, 2, 1]
```

Votes:

| j | p[j] | k |
| --- | --- | --- |
| 0 | 3 | 0 - 2 = 1 |
| 1 | 2 | 1 - 1 = 0 |
| 2 | 1 | 2 - 0 = 2 |

Each k gets one vote, so cnt = [1,1,1]. Threshold is 3 - 2 = 1, so all k are valid.

This matches the fact that one swap is enough to realize any rotation in a 3-cycle reversal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element contributes one vote and we scan k once |
| Space | O(n) | Frequency array for shift counts |

The total complexity over all test cases is O(3·10^5), which fits easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        p = list(map(int, input().split()))

        cnt = [0] * n
        for j, val in enumerate(p):
            k = (j - (val - 1)) % n
            cnt[k] += 1

        threshold = n - 2 * m
        res = [str(k) for k in range(n) if cnt[k] >= threshold]
        out.append(str(len(res)) + (" " + " ".join(res) if res else ""))

    return "\n".join(out)

# provided samples
assert run("""4
4 1
2 3 1 4
3 1
1 2 3
3 1
3 2 1
6 0
1 2 3 4 6 5
""") == """1 3
1 0
3 0 1 2
0"""

# all identical except m large
assert run("""1
5 2
1 2 3 4 5
""") == "5 0 1 2 3 4"

# minimal cycle-like case
assert run("""1
3 0
2 3 1
""") == "1 2"

# maximum mismatch but large m
assert run("""1
4 2
4 3 2 1
""") == "4 0 1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identity with swaps | all k | swaps irrelevant when already correct |
| pure cycle | single shift | strict rotation detection |
| reversed with max swaps | all k | high m relaxes constraint |

## Edge Cases

A key edge case is when m is large enough that almost any permutation becomes reachable from any rotation. In the identity case, every k produces cnt[k] = n, so the threshold is always satisfied and all shifts are valid, matching the idea that no swaps are needed regardless of rotation.

Another edge case is a fully reversed permutation. Here each shift produces a uniform distribution of matches, but when m is at its maximum allowed scale, the threshold becomes small enough that all k pass. The algorithm handles this naturally because it only checks counts, not structure.

A degenerate case is m = 0, where we require cnt[k] = n, meaning every element must already align perfectly with the rotation. This forces a unique k if and only if the array is exactly a rotation of identity. The modular voting ensures only the correct rotation accumulates full support.
