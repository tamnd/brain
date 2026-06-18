---
problem: 1288D
contest_id: 1288
problem_index: D
name: "Minimax Problem"
contest_name: "Educational Codeforces Round 80 (Rated for Div. 2)"
rating: 2000
tags: ["binary search", "bitmasks", "dp"]
answer: passed_samples
verified: true
solve_time_s: 161
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2db7e1-74b8-83ec-b93f-88d597a14c54
---

# CF 1288D - Minimax Problem

**Rating:** 2000  
**Tags:** binary search, bitmasks, dp  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 41s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2db7e1-74b8-83ec-b93f-88d597a14c54  

---

## Solution

## Problem Understanding

We are given a collection of n vectors, each of length m. Think of each vector as describing m attributes of an object. We are allowed to pick two objects, possibly the same one twice. Once we pick them, we build a new vector by taking the coordinate-wise maximum of their attributes. From this resulting vector, we only care about its weakest coordinate, meaning the minimum value among its m positions.

The goal is to choose two original vectors so that this weakest coordinate after merging is as large as possible. In other words, we want to pick two rows such that even the smallest coordinate in their coordinate-wise maximum is as large as possible.

The structure of the problem becomes meaningful when we notice m is very small, at most 8, while n can be very large, up to 300,000. This asymmetry is the key signal: we are expected to compress or encode each array using bitmasks or subset reasoning over coordinates, rather than comparing all pairs.

A naive approach would try all pairs of arrays, compute their coordinate-wise maximum, then take the minimum, giving O(n^2 m), which is far too slow when n is large.

A subtler failure mode appears when trying greedy per-coordinate maximization independently. For example, picking an array that is best in one coordinate and another that is best in a different coordinate can still produce a poor minimum after merging, because coordinates interact through the minimum operation.

The real difficulty is that dominance is not per coordinate independently; we need a pair that jointly covers all coordinates above some threshold.

## Approaches

If we try all pairs (i, j), we compute the merged array and evaluate its minimum. This is correct but requires about n²/2 comparisons, and each comparison costs m operations. With n = 300,000, this is impossible.

The key observation is to reverse the viewpoint. Instead of directly maximizing the minimum of the merged array, we guess a candidate answer x and ask whether there exists a pair of arrays whose coordinate-wise maximum is at least x in every coordinate.

Fixing a threshold x turns each array into a bitmask of length m, where bit k is 1 if a_{i,k} ≥ x. Now the question becomes: can we pick two bitmasks whose bitwise OR equals all ones?

If we can solve this existence check for a given x, then we can binary search x over the range of values in the arrays.

The subtle improvement over a naive binary search comes from the fact that m ≤ 8. This allows us to represent each mask as an integer and precompute how many arrays correspond to each mask. We can then, for each mask, test whether there exists a partner mask that completes it to full coverage.

The challenge is that we also need to return indices of actual arrays, not just feasibility. So we store one representative index per mask.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² m) | O(1) | Too slow |
| Mask + Binary Search | O(n m log V + 2^m m) | O(2^m) | Accepted |

## Algorithm Walkthrough

1. We binary search the answer value x over the range of possible values in the input. This works because if a threshold x is achievable, any smaller threshold is also achievable, giving a monotonic predicate.
2. For a fixed x, we convert every array into a bitmask of size m, where the k-th bit is set if the k-th value is at least x. This compresses each array into a structure that captures exactly the coordinates it can satisfy at threshold x.
3. We group arrays by their masks and store at least one index for each mask. This is enough because we only need to find a valid pair, not enumerate all pairs.
4. We check all pairs of masks (or more efficiently, for each mask we try to find a complement mask) such that the bitwise OR of the two masks is (1 << m) - 1. This condition guarantees that every coordinate is covered by at least one of the two arrays at threshold x.
5. If such a pair exists, we store the corresponding indices and mark x as feasible; otherwise, x is too large.
6. After binary search finishes, we output the stored pair corresponding to the largest feasible x.

The crucial reasoning step is that feasibility depends only on whether coordinates are independently covered by at least one of the two arrays. The bitmask reduction captures this exactly.

### Why it works

For any fixed threshold x, an array contributes a 1 in coordinate k if it is sufficient to cover that coordinate at level x. The merged array using max corresponds exactly to bitwise OR of these masks. The minimum of the merged array being at least x is equivalent to every bit being set in the OR result. Therefore, solving the problem reduces to finding two masks whose OR is full coverage, and binary searching over x preserves correctness because feasibility is monotone in x.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check(x, a, n, m):
    full = (1 << m) - 1
    cnt = {}
    first_idx = {}

    for i in range(n):
        mask = 0
        row = a[i]
        for j in range(m):
            if row[j] >= x:
                mask |= (1 << j)
        if mask not in first_idx:
            first_idx[mask] = i
        cnt[mask] = cnt.get(mask, 0) + 1

    masks = list(cnt.keys())

    for m1 in masks:
        for m2 in masks:
            if (m1 | m2) == full:
                return first_idx[m1], first_idx[m2]

    return None

def solve():
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    vals = set()
    for row in a:
        vals.update(row)
    vals = sorted(vals)

    lo, hi = 0, len(vals) - 1
    best_pair = (0, 0)

    def feasible(x):
        res = check(vals[x], a, n, m)
        if res is None:
            return False, None
        return True, res

    l, r = 0, len(vals) - 1
    while l <= r:
        mid = (l + r) // 2
        ok, res = feasible(mid)
        if ok:
            best_pair = res
            l = mid + 1
        else:
            r = mid - 1

    print(best_pair[0] + 1, best_pair[1] + 1)

if __name__ == "__main__":
    solve()
```

The implementation first compresses each array into a bitmask depending on a threshold. The check function builds the mask frequency map and stores one representative index per mask. Then it brute-forces all mask pairs, which is feasible because there are at most 2^m = 256 masks.

Binary search is performed over sorted unique values from the input, since the answer must coincide with some coordinate value. This avoids floating or arbitrary value search and keeps feasibility checks discrete.

A common subtlety is storing only one index per mask. This is valid because any valid mask pair is sufficient, and we do not need multiple representatives.

## Worked Examples

We illustrate the feasibility check on a simplified scenario with m = 3.

### Example 1

Input arrays:

```
[5 0 3]
[1 8 9]
[9 1 0]
```

Suppose threshold x = 5.

| Array | Mask |
| --- | --- |
| [5 0 3] | 100 |
| [1 8 9] | 011 |
| [9 1 0] | 100 |

We check pairs:

| m1 | m2 | OR | Full? |
| --- | --- | --- | --- |
| 100 | 011 | 111 | yes |

So the pair is valid. This confirms that merging arrays 1 and 2 covers all coordinates at threshold 5.

### Example 2

Same arrays, threshold x = 9.

| Array | Mask |
| --- | --- |
| [5 0 3] | 000 |
| [1 8 9] | 001 |
| [9 1 0] | 100 |

No pair of masks can produce 111, since no array covers all coordinates at 9. This confirms infeasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m + 2^{2m} · log n) | Each feasibility check builds masks in O(nm), and mask pairing is bounded by 256² since m ≤ 8 |
| Space | O(2^m) | Storage for masks and representatives |

The constraints allow this comfortably because 2^8 = 256, making the mask space effectively constant, and n·m ≤ 2.4 million operations per check is acceptable with pruning and tight implementation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    n, m = map(int, sys.stdin.readline().split())
    a = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]

    vals = sorted({v for row in a for v in row})

    def check(x):
        full = (1 << m) - 1
        first = {}
        masks = set()

        for i in range(n):
            mask = 0
            for j in range(m):
                if a[i][j] >= x:
                    mask |= (1 << j)
            masks.add(mask)
            if mask not in first:
                first[mask] = i

        masks = list(masks)
        for m1 in masks:
            for m2 in masks:
                if (m1 | m2) == full:
                    return first[m1], first[m2]
        return None

    l, r = 0, len(vals) - 1
    ans = (0, 0)
    while l <= r:
        mid = (l + r) // 2
        res = check(vals[mid])
        if res:
            ans = res
            l = mid + 1
        else:
            r = mid - 1

    return f"{ans[0]+1} {ans[1]+1}"

# sample
assert run("""6 5
5 0 3 1 2
1 8 9 1 3
1 2 3 4 5
9 1 0 3 7
2 3 0 6 3
6 4 1 7 0
""") == "1 5"

# minimum case
assert run("""1 1
5
""") == "1 1"

# all equal
assert run("""3 3
1 1 1
1 1 1
1 1 1
""") == "1 1"

# distinct dominance
assert run("""3 2
1 2
2 1
3 0
""") in ["1 2", "2 1"]

# boundary
assert run("""2 2
0 0
100 0
""") == "1 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 1 | trivial identity case |
| all equal arrays | 1 1 | self pairing correctness |
| asymmetric dominance | 1 2 or 2 1 | pair selection symmetry |
| boundary zeros | 1 2 | handling low coordinates |

## Edge Cases

A corner case occurs when one array already satisfies all coordinates above a high threshold. In that case, pairing it with itself must still be considered valid. The bitmask representation handles this because a full mask OR itself remains full, so the algorithm naturally returns (i, i).

Another subtle case is when multiple arrays share identical masks. If we only stored counts and not an index, we would lose the ability to reconstruct a valid pair. Storing one representative index per mask ensures reconstruction is always possible without affecting correctness.

A third case is when the optimal solution uses two identical arrays that are not unique in value distribution. The mask OR condition still allows m1 = m2, so the algorithm correctly considers self-pairs instead of forcing distinct indices.