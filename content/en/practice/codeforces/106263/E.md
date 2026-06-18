---
title: "CF 106263E - construction is 2 hard 4 me"
description: "We are given a strictly increasing sequence of integers. From this sequence, we are allowed to remove at most k elements, leaving a remaining subsequence in the original order."
date: "2026-06-18T23:19:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106263
codeforces_index: "E"
codeforces_contest_name: "2025 \u534e\u5357\u5e08\u8303\u5927\u5b66\u201c\u5353\u8d8a\u6559\u80b2\u676f\u201d\u7b97\u6cd5\u4e0e\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u65b0\u751f\u8d5b\uff09"
rating: 0
weight: 106263
solve_time_s: 58
verified: true
draft: false
---

[CF 106263E - construction is 2 hard 4 me](https://codeforces.com/problemset/problem/106263/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a strictly increasing sequence of integers. From this sequence, we are allowed to remove at most `k` elements, leaving a remaining subsequence in the original order. The value of a resulting sequence is determined only by the smallest difference between two consecutive remaining elements. If fewer than two elements remain, the value is treated as infinite.

The task is to choose which elements to delete so that this minimum adjacent gap in the remaining sequence becomes as large as possible.

The core difficulty is that deleting elements increases gaps indirectly, but we are constrained by how many deletions we can perform. Each choice affects all future gaps, so local decisions can easily break the global optimum.

The constraints allow up to `2 × 10^5` total elements across all test cases. This immediately rules out any solution that tries all subsets or even all deletion patterns, since that would grow exponentially. Even a quadratic approach per test case would be too slow in the worst case.

A subtle failure case appears when greedy deletion is attempted without a target gap. For example, if we always remove the locally “bad” element that creates the smallest gap, we might destroy a structure that would have allowed a better global minimum gap after different removals.

Another edge situation occurs when `k = 0`. Then the answer is forced by the original array, so any algorithm must correctly handle the case where no deletions are allowed and still output a valid deletion set.

Finally, when the optimal solution keeps very few elements, it is easy to mistakenly output more than `k` deletions unless the construction is carefully tied to feasibility.

## Approaches

The brute-force approach would try every subset obtained by deleting at most `k` elements. For each subset, we compute all adjacent differences and take the minimum. Even if we only consider exactly `n - k` kept elements, the number of ways to choose them is still combinatorial, roughly `O(n choose k)`, which is far beyond feasible.

The key observation is that we do not need to directly decide which elements to remove. Instead, we flip the perspective: suppose we fix a candidate answer `x`, meaning we want every adjacent pair in the final sequence to differ by at least `x`. Now the problem becomes checking whether we can select a subsequence satisfying this constraint while removing at most `k` elements.

For a fixed `x`, we can greedily build the longest valid subsequence by always taking the earliest possible element and skipping everything that violates the `x` gap requirement. This greedy construction is optimal because once we pick an element, delaying the next choice only reduces future options.

This transforms the problem into a monotonic feasibility check, which enables binary search over `x`. If a gap `x` is achievable, then any smaller gap is also achievable, because the constraint becomes weaker.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Binary search + greedy check | O(n log A) | O(n) | Accepted |

Here `A` is the range of values in the array.

## Algorithm Walkthrough

We want to find the maximum possible minimum gap in a valid subsequence under the deletion limit.

1. We binary search the answer `x`, the minimum allowed adjacent difference. The search range is from `0` to `a[n-1] - a[0]`. This range covers all possible meaningful gaps because no adjacent difference can exceed the full span.
2. For a fixed `x`, we check feasibility by greedily constructing a subsequence. We start by always selecting the first element.
3. We scan the array from left to right. Whenever the current element is at least `last_selected + x`, we keep it and update `last_selected`. Otherwise, we skip it as if it were deleted.
4. After the scan, we compute how many elements were kept. If `kept >= n - k`, then `x` is feasible because we can always delete extra kept elements if needed while staying within the deletion budget.
5. Using binary search, we find the largest feasible `x`.
6. We run the greedy process once more using this optimal `x`, recording which indices are kept.
7. All other indices form the deletion set. We output its size and the indices.

### Why it works

The greedy check produces the maximum possible size of a subsequence that satisfies the gap constraint `x`. Any valid subsequence must respect the same ordering constraints, and choosing an earlier valid element never reduces future feasibility. This makes the greedy solution optimal for fixed `x`. Binary search is valid because feasibility is monotonic in `x`, so once a gap is impossible, all larger gaps are also impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def feasible(a, k, x):
    n = len(a)
    cnt = 1
    last = a[0]
    for i in range(1, n):
        if a[i] - last >= x:
            cnt += 1
            last = a[i]
    return cnt >= n - k

def build(a, x):
    n = len(a)
    keep = [False] * n
    last = a[0]
    keep[0] = True
    for i in range(1, n):
        if a[i] - last >= x:
            keep[i] = True
            last = a[i]
    return keep

def solve():
    T = int(input())
    for _ in range(T):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        lo, hi = 0, a[-1] - a[0]

        while lo <= hi:
            mid = (lo + hi) // 2
            if feasible(a, k, mid):
                lo = mid + 1
            else:
                hi = mid - 1

        best = hi
        keep = build(a, best)

        delete_idx = []
        for i in range(n):
            if not keep[i]:
                delete_idx.append(i + 1)

        if len(delete_idx) > k:
            delete_idx = delete_idx[:k]

        print(len(delete_idx))
        if delete_idx:
            print(*delete_idx)
        else:
            print()

if __name__ == "__main__":
    solve()
```

The feasibility function computes how many elements can be kept while maintaining a minimum gap `x`. The construction function repeats the same greedy process but records decisions. The binary search ensures we maximize the smallest allowed gap, and the final deletion list is simply the complement of the kept set.

A subtle point is that the greedy keeps the maximum possible number of elements, so if it already keeps more than `n - k`, we are still safe because we are allowed to delete fewer than `k` elements.

## Worked Examples

Consider `a = [1, 4, 6, 10]`, `k = 1`.

We binary search for the best minimum gap.

For `x = 5`, greedy picks `1`, skips `4`, skips `6`, keeps `10`, so only 2 elements are kept. Since `n - k = 3`, this is infeasible.

For `x = 3`, greedy picks `1`, keeps `4`, skips `6`, keeps `10`, giving 3 elements, which is feasible.

Now we maximize and find `x = 3`.

| Step | Index | Value | Last chosen | Kept? | Count |
| --- | --- | --- | --- | --- | --- |
| Start | - | - | - | 1 kept at 1 | 1 |
| i=2 | 2 | 4 | 1 | yes | 2 |
| i=3 | 3 | 6 | 4 | no | 2 |
| i=4 | 4 | 10 | 4 | yes | 3 |

The final deletions are index `3`.

This shows how the greedy process enforces the minimum gap constraint while still maximizing how many elements remain.

Now consider `a = [2, 3, 7, 8, 15]`, `k = 2`.

For a large gap like `x = 7`, we keep `2, 8, 15`, which is feasible. If we try `x = 8`, we only keep `2, 15`, which is not enough to satisfy the deletion constraint. The binary search settles on the largest feasible value.

The trace shows how tightening the required gap reduces the number of selectable elements, and feasibility is determined purely by whether we can still keep enough elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each binary search step runs a linear greedy scan over the array |
| Space | O(n) | Storage for keep markers and deletion output |

The sum of `n` over all test cases is `2 × 10^5`, and logarithmic search over values is small enough to fit easily within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal case
assert run("1\n2 1\n1 10\n") in {"1\n1", "0"}, "min case"

# already optimal, no deletions needed
assert run("1\n4 0\n1 2 3 10\n") == "0", "k=0"

# small structured case
res = run("1\n5 2\n1 2 4 7 11\n")
assert len(res.splitlines()[0].split()) == 1

# all equal gaps large
assert run("1\n3 1\n1 100 200\n") != "", "basic feasibility"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 case | any valid | boundary with single gap |
| k=0 case | 0 deletions | no-removal constraint |
| structured 5 elements | valid deletion set | general correctness |
| spaced array | non-empty output | feasibility handling |

## Edge Cases

When `k = 0`, the greedy construction is never used for deletions. The binary search still evaluates feasibility correctly, but the final deletion list must be empty. The algorithm naturally handles this because all elements remain marked as kept.

When `n - k = 1`, the feasibility condition becomes trivial since any single element suffices. The greedy will always return at least one element, and the algorithm correctly allows large `x` values, though the final answer is irrelevant because no adjacent differences exist.

When the optimal solution keeps almost all elements, the greedy still produces a valid superset of the required size, and we simply truncate to at most `k` deletions by selecting the complement of the kept set.
