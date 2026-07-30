---
title: "CF 102646B - Combining Arrays"
description: "The task is to merge two queues of numbers into one array. The only operation allowed is taking the current first element from either queue and appending it to the answer. The internal order of each original array cannot change."
date: "2026-07-30T23:11:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102646
codeforces_index: "B"
codeforces_contest_name: "Testing Round #XVII"
rating: 0
weight: 102646
solve_time_s: 114
verified: true
draft: false
---

[CF 102646B - Combining Arrays](https://codeforces.com/problemset/problem/102646/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to merge two queues of numbers into one array. The only operation allowed is taking the current first element from either queue and appending it to the answer. The internal order of each original array cannot change. Among all possible merged arrays, we need the one that is lexicographically smallest. The two input arrays together contain every number from `1` to `2n` exactly once, which means every value is unique.

The main difficulty is that a locally smaller first element is not always enough. If both arrays currently expose large values, the correct choice depends on comparing the remaining suffixes of both arrays. For example, choosing `5` over `6` is not necessarily optimal if the array starting with `6` continues with much smaller values.

The length of each array can reach `100000`, so the total number of elements is `200000`. An approach that tries all possible merges is impossible because the number of valid interleavings is exponential. Even comparing suffixes character by character every time can degrade to quadratic behavior, which is too slow for this input size.

The important edge cases come from suffix comparisons. If one array is exhausted, the remaining array must be copied because there is no longer a choice. For example:

```
1
A = [3]
B = [1]
```

The answer is:

```
1 3
```

A greedy solution that only checks the first elements works here, but it fails in more complex cases.

Another case is when the first elements are equal in ordinary string problems. Here the permutation property prevents equal values across the two arrays, but a solution that assumes it can always compare only one element would fail on:

```
n = 3
A = [6, 10, 4]
B = [9, 8, 11]
```

The correct answer begins with `6`, because the suffix `[6,10,4]` is smaller than `[9,8,11]`. The decision cannot be made by looking at later elements after choosing incorrectly.

## Approaches

The brute-force idea is to generate every possible sequence of choices. At every moment we can take from `A` or from `B`, so the number of possible merges is:

$$\binom{2n}{n}$$

For `n = 100000`, this is far beyond any practical limit. Even storing a small fraction of those possibilities is impossible.

A more reasonable greedy idea is to always choose the smaller current front element. This is not enough. Consider the decision point where the remaining arrays are:

```
A = [4, 100]
B = [5, 1]
```

Taking `4` first looks correct, but if we had:

```
A = [4, 100]
B = [4?]
```

we would need to compare longer parts. In this problem equal values cannot happen, but the same principle remains: the next choice depends on the entire remaining suffix.

The key observation is that at any point the optimal move is to take the lexicographically smaller remaining suffix. If `A[i:] < B[j:]`, taking from `A` is always safe because every future element of `A` stays in front of the remaining elements of `B` until we decide otherwise. If we take from the larger suffix first, the first position where the two suffixes differ gives a worse answer immediately.

The remaining challenge is comparing suffixes efficiently. We concatenate the two arrays with a separator value smaller than every element and build ranks for all suffixes. Prefix doubling gives these ranks in `O(n log n)` time. Then each suffix comparison becomes a constant-time rank comparison. Prefix doubling constructs lexicographic ranks of increasingly longer prefixes until every suffix has a unique rank.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(2n,n)) | O(2n) | Too slow |
| Compare suffixes directly | O(n²) | O(1) | Too slow |
| Suffix ranks + greedy merge | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build one combined array `S = A + [0] + B`. The value `0` acts as a separator because all real values are positive. We only use this array to compare suffixes, not to create the answer.
2. Compute the lexicographic rank of every suffix of `S` using prefix doubling. Each rank tells us which suffix is smaller.
3. Keep two pointers, `i` for the current position in `A` and `j` for the current position in `B`.
4. While both arrays still have elements, compare the ranks of suffixes starting at `i` in `A` and `j` in `B`. Append the first element of the smaller suffix and move its pointer forward.
5. When one array is empty, append the remaining elements of the other array directly. There are no more decisions to make.

The reason the greedy choice works is that the first differing position between two candidate suffixes determines the lexicographic order of every merge beginning with those suffixes. Choosing the smaller suffix preserves the best possible first undecided position, and repeating this argument after removing one element proves that every chosen element is part of the optimal merge.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_ranks(arr):
    n = len(arr)
    vals = {v: i for i, v in enumerate(sorted(set(arr)))}
    rank = [vals[x] for x in arr]
    k = 1

    while k < n:
        order = list(range(n))
        order.sort(key=lambda x: (rank[x], rank[x + k] if x + k < n else -1))

        new_rank = [0] * n
        for idx in range(1, n):
            a = order[idx - 1]
            b = order[idx]
            if (rank[a], rank[a + k] if a + k < n else -1) != (
                rank[b],
                rank[b + k] if b + k < n else -1,
            ):
                new_rank[b] = new_rank[a] + 1
            else:
                new_rank[b] = new_rank[a]

        rank = new_rank
        k <<= 1

    return rank

def solve():
    n = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    combined = A + [0] + B
    rank = build_ranks(combined)

    ans = []
    i = 0
    j = n + 1

    while i < n and j < 2 * n + 1:
        if rank[i] < rank[j]:
            ans.append(A[i])
            i += 1
        else:
            ans.append(B[j - n - 1])
            j += 1

    while i < n:
        ans.append(A[i])
        i += 1

    while j < 2 * n + 1:
        ans.append(B[j - n - 1])
        j += 1

    print(*ans)

if __name__ == "__main__":
    solve()
```

The `build_ranks` function is the suffix comparison engine. Initially, every suffix is ranked only by its first value. Each doubling step sorts suffixes using the rank of the current block and the rank of the next block. After enough iterations, the rank array completely represents suffix order.

The separator value `0` is smaller than every real number, so it safely separates the two arrays. Because all numbers in the original arrays are distinct, a suffix from `A` cannot be a prefix of a suffix from `B`, so the separator does not create incorrect comparisons.

The merge loop maintains two pointers. The pointer for `B` starts at `n + 1` because the second array begins after the separator in the combined array. The comparison uses the precomputed ranks instead of scanning values, avoiding repeated work.

Python integers do not overflow, and the code never creates the exponential number of possible merges. The only delicate part is keeping the separator index and the conversion between combined-array indices and `B` indices correct.

## Worked Examples

For:

```
n = 3
A = [1,2,3]
B = [4,5,6]
```

| i | j | Compare | Action | Answer |
| --- | --- | --- | --- | --- |
| 0 | 4 | [1,2,3] < [4,5,6] | Take A | 1 |
| 1 | 4 | [2,3] < [4,5,6] | Take A | 1 2 |
| 2 | 4 | [3] < [4,5,6] | Take A | 1 2 3 |
| 3 | 4 | A empty | Take B | 1 2 3 4 5 6 |

This shows the case where one array is entirely smaller and the algorithm consumes it first.

For:

```
n = 7
A = [6,10,4,2,13,12,7]
B = [9,8,11,3,5,1,14]
```

| i | j | Comparison | Choice |
| --- | --- | --- | --- |
| 0 | 8 | [6,10,4,...] < [9,8,11,...] | A |
| 1 | 8 | [10,4,2,...] > [9,8,11,...] | B |
| 1 | 9 | [10,4,2,...] > [8,11,...] | B |
| 1 | 10 | [10,4,2,...] < [11,3,...] | A |
| 2 | 10 | [4,2,...] < [11,3,...] | A |
| 3 | 10 | [2,...] < [11,3,...] | A |

The trace demonstrates why comparing only the first element is insufficient. After taking `6`, the algorithm correctly switches to `B` because its remaining suffix is smaller.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Prefix doubling performs logarithmically many sorting rounds, followed by a linear merge. |
| Space | O(n) | The combined array and rank arrays store a constant number of values per element. |

The input size allows roughly linear or near-linear solutions. The logarithmic factor from suffix ranking is acceptable for `n = 100000`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    n = int(sys.stdin.readline())
    A = list(map(int, sys.stdin.readline().split()))
    B = list(map(int, sys.stdin.readline().split()))

    combined = A + [0] + B

    def build_ranks(arr):
        n = len(arr)
        rank = [x for x in arr]
        k = 1
        while k < n:
            order = sorted(range(n), key=lambda x: (rank[x], rank[x+k] if x+k < n else -1))
            nr = [0] * n
            for a, b in zip(order, order[1:]):
                nr[b] = nr[a] + ((rank[a], rank[a+k] if a+k < n else -1) != (rank[b], rank[b+k] if b+k < n else -1))
            rank = nr
            k *= 2
        return rank

    r = build_ranks(combined)
    ans = []
    i, j = 0, n + 1

    while i < n and j < 2*n + 1:
        if r[i] < r[j]:
            ans.append(A[i])
            i += 1
        else:
            ans.append(B[j-n-1])
            j += 1

    ans += A[i:]
    ans += B[j-n-1:]

    sys.stdin = old
    return " ".join(map(str, ans)) + "\n"

assert run("3\n1 2 3\n4 5 6\n") == "1 2 3 4 5 6\n"
assert run("5\n1 3 5 7 9\n2 4 6 8 10\n") == "1 2 3 4 5 6 7 8 9 10\n"
assert run("1\n2\n1\n") == "1 2\n"
assert run("3\n6 10 4\n9 8 11\n") == "6 9 8 10 4 11\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / [2] / [1]` | `1 2` | Minimum size and choosing the smaller suffix |
| Sorted arrays | Fully sorted merge | Simple greedy behavior |
| Mixed suffix ordering | Non-trivial switching | Full suffix comparison |
| Small arrays | Correct indexing | Separator and pointer boundaries |

## Edge Cases

When one array becomes empty, the algorithm does not attempt another comparison. For:

```
n = 1
A = [3]
B = [1]
```

The suffix rank comparison chooses `B`, producing `1 3`. After that, `B` is empty and the remaining `3` is appended.

A common mistake is comparing only current elements. The case:

```
A = [6,10,4]
B = [9,8,11]
```

starts with `6 < 9`, so `A` is chosen. Later the comparison changes because the remaining suffixes have changed. The algorithm handles this by recomputing the choice after every removal using the stored suffix ranks.

The separator position is another place where errors occur. The combined array is indexed as:

```
A + [0] + B
```

so the first element of `B` is at index `n + 1`. The implementation keeps the combined index for comparisons and converts back to a `B` index only when adding an answer element.
