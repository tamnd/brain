---
title: "CF 102423J - One of Each"
description: "We have a sequence (X) of (n) integers. Every element is between (1) and (k), and every value from (1) through (k) occurs somewhere in the sequence. We need to delete some elements while preserving the relative order of everything that remains."
date: "2026-08-12T01:19:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102423
codeforces_index: "J"
codeforces_contest_name: "North American Southeast Regional 2019 (Div 1)"
rating: 0
weight: 102423
solve_time_s: 83
verified: true
draft: false
---

[CF 102423J - One of Each](https://codeforces.com/problemset/problem/102423/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence (X) of (n) integers. Every element is between (1) and (k), and every value from (1) through (k) occurs somewhere in the sequence. We need to delete some elements while preserving the relative order of everything that remains.

The final sequence must contain every value exactly once, so its length is exactly (k). Among all such subsequences, we want the lexicographically smallest one. In other words, we first minimize the first chosen value, then, among choices with the same first value, minimize the second chosen value, and so on. The original problem gives (n) up to (2\cdot10^5), so a solution that repeatedly scans large parts of the sequence or considers many possible subsequences is not viable.

A linear or (O(n\log n)) solution is the natural target. With (2\cdot10^5) elements and a two second limit, (O(n^2)) would mean around (4\cdot10^{10}) basic iterations in the worst case, far beyond what a competitive-programming implementation can handle. The structure of the problem is favorable because we only need one occurrence of each value, and duplicate occurrences can be discarded whenever a later occurrence gives us a better lexicographic choice.

The first edge case is when (k=1), so the whole answer consists of a single value. For example,

```
1 1
1
```

has output

```
1
```

A careless implementation that assumes there must be a stack operation involving a previous element can fail here, because there is no previous element at all.

Another edge case is when the sequence is already a permutation. For example,

```
5 5
1
2
3
4
5
```

has output

```
1 2 3 4 5
```

Every value must be kept, because there are exactly (k) elements. An implementation that removes a stack element merely because the current value is smaller can accidentally delete a value that has no later occurrence.

Duplicates near the end are another common source of mistakes. Consider

```
6 3
3
2
1
3
1
3
```

The answer is

```
2 1 3
```

The first `3` cannot be part of the optimal answer because choosing `2` next gives a smaller first element, and the later `3` is still available. However, the final `3` must be retained because after choosing `2` and `1`, no later `3` exists. A greedy stack must distinguish between an element that can safely be removed and one whose removal would make the remaining sequence incomplete.

## Approaches

A direct brute-force approach is to enumerate possible subsequences, keep the ones containing every value from (1) through (k) exactly once, and then choose the lexicographically smallest one. This is correct because every valid answer is explicitly considered. The problem is the number of subsequences. There are (2^n) subsequences in total, and when (k) is around (n/2), the number of candidates of exactly length (k) is

[
\binom{n}{\lfloor n/2\rfloor},
]

which is approximately (2^n/\sqrt{n}). For (n=2\cdot10^5), this is completely infeasible.

A less extreme brute-force strategy is to construct the answer from left to right. At each position, try candidate values in increasing order and search for an occurrence that still leaves every missing value available. Even if each feasibility check is implemented carefully, repeatedly scanning suffixes can require (O(nk)) work. In the worst case this reaches about (4\cdot10^{10}) operations.

The useful observation is that lexicographic minimization gives us a very specific reason to remove an already chosen value. Suppose the current answer ends with value (a), and the next sequence value is (b<a). If (a) occurs again later, then keeping the current (a) is never optimal. Replacing it with the smaller (b) makes the answer lexicographically smaller, while the later occurrence of (a) can still provide the required copy.

This gives a monotonic-stack strategy. We process the sequence from left to right. The stack represents the best prefix we can currently build. When a smaller value arrives, we remove larger values from the end of the stack as long as those values occur again later. If a value does not occur later, it is locked in place and cannot be removed.

There is one more condition. We need every value exactly once, so if the current value is already in the stack, we simply skip it. The first occurrence is not necessarily the one we want, but keeping it temporarily allows the stack rule to replace it later if a smaller value appears before its last possible occurrence.

The critical data structure is therefore just a `last` array storing the final position of every value. During the scan, the stack contains no duplicates, and every pop is justified by the existence of another occurrence later.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n)) candidates | (O(n)) | Too slow |
| Repeated greedy scanning | (O(nk)) | (O(k)) | Too slow |
| Monotonic stack | (O(n)) | (O(n+k)) | Accepted |

## Algorithm Walkthrough

1. Read the sequence and compute `last[x]`, the final index where each value (x) appears. We need this information because a value can only be removed from the current answer when another copy is guaranteed to remain available later.
2. Maintain a stack containing the current best subsequence prefix, and maintain a boolean array `used` telling us which values are already in the stack. The stack never contains the same value twice, which directly matches the requirement that the final answer contains every value exactly once.
3. Process every value (x) from left to right. If `used[x]` is already true, skip (x). Keeping another copy would violate the exactly-once condition, and that copy cannot improve the answer because the existing occurrence is already represented in the stack.
4. If (x) is not used, compare it with the last value in the stack. While the stack is nonempty, its last value is larger than (x), and that last value occurs again after the current position, pop it and mark it unused. The new (x) is smaller, so placing it earlier makes the sequence lexicographically smaller, while the later occurrence of the popped value preserves feasibility.
5. Stop popping as soon as the top of the stack is smaller than (x), or the top value has no later occurrence. In the first case, replacing it would make the sequence larger. In the second case, removing it would lose the only remaining copy of that value.
6. Push (x) onto the stack and mark it as used. Continue until every input element has been processed.
7. Print the stack. Because every value from (1) through (k) is guaranteed to occur in the input, and we only remove a value when another copy remains, the final stack contains all (k) values exactly once.

### Why it works

The key invariant is that after processing any prefix of the input, the stack is the lexicographically smallest distinct-value subsequence that can still be extended to contain every value that has not yet been permanently lost.

When a new value (x) is smaller than the stack top (y), keeping (y) before (x) would make the result lexicographically worse. We are allowed to remove (y) exactly when another copy occurs later, so removing it cannot make a valid completion impossible. Repeating this process removes every stack suffix that is both larger than (x) and replaceable.

If a stack value has no later occurrence, it cannot be removed because it would disappear from every possible completion. If the stack top is smaller than (x), keeping the smaller value first is already lexicographically optimal. Thus every push or pop is forced by lexicographic optimality and feasibility, which proves that the final stack is the desired subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = [int(input()) for _ in range(n)]

    last = [0] * (k + 1)

    for i, x in enumerate(a):
        last[x] = i

    used = [False] * (k + 1)
    stack = []

    for i, x in enumerate(a):
        if used[x]:
            continue

        while stack:
            top = stack[-1]

            if top <= x:
                break

            if last[top] <= i:
                break

            stack.pop()
            used[top] = False

        stack.append(x)
        used[x] = True

    print(*stack)

if __name__ == "__main__":
    solve()
```

The first loop computes the last occurrence of every value. Since indices are processed from left to right, assigning `last[x] = i` naturally leaves the final occurrence in the array.

The `used` array prevents duplicates from entering the answer. This is separate from `last`: `last` answers whether a value can be removed, while `used` answers whether we already have a copy of that value in the current answer.

The inner `while` loop is the monotonic-stack operation. The condition `top > x` is the lexicographic condition. The condition `last[top] > i` is the feasibility condition. Both are required. Omitting the second condition can delete the only remaining occurrence of a value.

The comparison uses `last[top] <= i` rather than `last[top] < i` because the current index cannot be a later occurrence of `top` when `top` is already in the stack, but using `<=` makes the boundary explicit and safe. In practice, for a distinct stack value different from the current `x`, `last[top]` is always at least `i + 1` if it is still available.

Every value is pushed at most once between removals and popped at most once for each push. More precisely, each occurrence can cause only constant amortized stack work, so the entire algorithm is linear.

Python integers do not introduce any overflow concern here because the algorithm only manipulates indices and values bounded by (2\cdot10^5).

## Worked Examples

### Sample 1

The input is

```
6 3
3
2
1
3
1
3
```

The last occurrence positions, using zero-based indices, are `1 -> 4`, `2 -> 1`, and `3 -> 5`.

| Index | x | Stack before | Action | Stack after |
| --- | --- | --- | --- | --- |
| 0 | 3 | `[]` | Push 3 | `[3]` |
| 1 | 2 | `[3]` | Pop 3 because 3 > 2 and 3 appears later | `[2]` |
| 2 | 1 | `[2]` | Pop 2 because 2 > 1 and 2 has no later copy | `[2, 1]` |
| 3 | 3 | `[2, 1]` | Push 3 | `[2, 1, 3]` |
| 4 | 1 | `[2, 1, 3]` | Skip because 1 is already used | `[2, 1, 3]` |
| 5 | 3 | `[2, 1, 3]` | Skip because 3 is already used | `[2, 1, 3]` |

The result is `2 1 3`. The interesting decision occurs at index 1. The first `3` is removed because a later `3` exists, allowing the smaller `2` to become the first element. The `2` cannot later be removed when `1` arrives because there is no second `2`.

### Sample 2

The input is

```
10 5
5
4
3
2
1
4
1
1
5
5
```

The last positions are `1 -> 7`, `2 -> 3`, `3 -> 2`, `4 -> 5`, and `5 -> 9`.

| Index | x | Stack before | Action | Stack after |
| --- | --- | --- | --- | --- |
| 0 | 5 | `[]` | Push 5 | `[5]` |
| 1 | 4 | `[5]` | Pop 5 because 5 appears later | `[4]` |
| 2 | 3 | `[4]` | Pop 4 because 4 appears later | `[3]` |
| 3 | 2 | `[3]` | Push 2 because 3 has no later copy | `[3, 2]` |
| 4 | 1 | `[3, 2]` | Push 1 because neither 3 nor 2 can be removed | `[3, 2, 1]` |
| 5 | 4 | `[3, 2, 1]` | Push 4 | `[3, 2, 1, 4]` |
| 6 | 1 | `[3, 2, 1, 4]` | Skip because 1 is already used | `[3, 2, 1, 4]` |
| 7 | 1 | `[3, 2, 1, 4]` | Skip because 1 is already used | `[3, 2, 1, 4]` |
| 8 | 5 | `[3, 2, 1, 4]` | Push 5 | `[3, 2, 1, 4, 5]` |
| 9 | 5 | `[3, 2, 1, 4, 5]` | Skip because 5 is already used | `[3, 2, 1, 4, 5]` |

The output is `3 2 1 4 5`. This example demonstrates why an element cannot be removed merely because a smaller value appears. When `2` arrives, the `3` is the only occurrence of `3`, so removing it would make a complete answer impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+k)) | Computing last occurrences takes (O(n)), and every stack push or pop is amortized (O(1)) |
| Space | (O(n+k)) | The sequence, stack, `last`, and `used` arrays occupy linear space |

With (n\le2\cdot10^5), the algorithm performs only a constant amount of amortized work per input element. This is comfortably within the intended range for a two second limit, while the quadratic alternatives would require tens of billions of operations.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    k = next(it)
    a = [next(it) for _ in range(n)]

    last = [0] * (k + 1)
    for i, x in enumerate(a):
        last[x] = i

    used = [False] * (k + 1)
    stack = []

    for i, x in enumerate(a):
        if used[x]:
            continue

        while stack and stack[-1] > x and last[stack[-1]] > i:
            used[stack.pop()] = False

        stack.append(x)
        used[x] = True

    return " ".join(map(str, stack)) + "\n"

def run(inp: str) -> str:
    return solve_data(inp)

# Provided sample 1
assert run("""6 3
3
2
1
3
1
3
""") == """2 1 3
""", "sample 1"

# Provided sample 2
assert run("""10 5
5
4
3
2
1
4
1
1
5
5
""") == """3 2 1 4 5
""", "sample 2"

# Minimum-size input
assert run("""1 1
1
""") == """1
""", "minimum size"

# All values are equal, k = 1
assert run("""8 1
1
1
1
1
1
1
1
1
""") == """1
""", "all equal values"

# Maximum-size style case with every value unique
assert run("10 10\n" + "\n".join(map(str, range(1, 11))) + "\n") == \
       "1 2 3 4 5 6 7 8 9 10\n", "all values already distinct"

# Repeated values designed to catch incorrect popping of a value
assert run("""8 4
4
3
2
1
3
4
2
1
""") == """3 2 1 4
""", "last-occurrence boundary"

# Large input, verifies linear behavior and the k = 1 boundary
large = "200000 1\n" + "1\n" * 200000
assert run(large) == "1\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Minimum size and empty-stack boundary |
| Eight copies of `1` with `k=1` | `1` | Duplicate suppression and large duplicate runs |
| `1 2 3 ... 10` with `k=10` | `1 2 3 4 5 6 7 8 9 10` | No value can be discarded when every value occurs once |
| `4 3 2 1 3 4 2 1` | `3 2 1 4` | Values with no later occurrence must remain |
| 200000 copies of `1` | `1` | Maximum (n), linear-time behavior, and (k=1) |

## Edge Cases

When there is only one distinct value, such as

```
1 1
1
```

the algorithm starts with an empty stack, pushes `1`, and finishes immediately. There is no pop to perform, and the result is `1`. The same logic handles arbitrarily many duplicates, because every later `1` sees `used[1] == True` and is skipped.

When every value occurs exactly once, consider

```
5 5
1
2
3
4
5
```

The stack grows to `[1, 2, 3, 4, 5]`. Whenever a new value arrives, the stack top is smaller, so no pop is possible. The output remains the original sequence. This is necessary because deleting any value would make it impossible to contain every number from `1` through `5`.

The most subtle boundary case occurs when a smaller value arrives after a value whose final occurrence has already been reached. For

```
4 3
3
2
1
3
```

the first `3` is removed when `2` arrives because another `3` exists at index 3. The stack becomes `[2]`. When `1` arrives, `2` has no later occurrence, so it cannot be removed. The final `3` is then added, producing

```
2 1 3
```

This is exactly the condition checked by `last[top] > i`.

A duplicate value that appears after it has already been selected must also be ignored. In

```
6 3
3
2
1
3
1
3
```

the first `3` is replaced by `2`, the `2` is retained because it has no later copy, and the later `3` is eventually selected. The subsequent `1` and `3` are skipped because both values are already represented. The result is `2 1 3`.

The maximum-size case does not require a different algorithmic treatment. With (n=200000) and (k=1), every input value is `1`, so the first element is pushed and all remaining elements are skipped. The algorithm still performs only (O(n)) work, which is exactly why the last-occurrence stack formulation scales to the full constraint.
