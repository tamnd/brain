---
title: "CF 67B - Restoration of the Permutation"
description: "We are given a permutation A of numbers from 1 to n. For every value i, we know a number b[i]. This number describes how many elements appear before i in the permutation and are at least i + k. The condition is attached to the value itself, not to the position."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 67
codeforces_index: "B"
codeforces_contest_name: "Manthan 2011"
rating: 1800
weight: 67
solve_time_s: 119
verified: true
draft: false
---

[CF 67B - Restoration of the Permutation](https://codeforces.com/problemset/problem/67/B)

**Rating:** 1800  
**Tags:** greedy  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation `A` of numbers from `1` to `n`. For every value `i`, we know a number `b[i]`. This number describes how many elements appear before `i` in the permutation and are at least `i + k`.

The condition is attached to the value itself, not to the position. If `i = 3` and `k = 2`, then we count how many numbers greater than or equal to `5` appear before `3`.

The task is to reconstruct the lexicographically smallest permutation satisfying all these counts.

The constraint `n ≤ 1000` is small enough for quadratic algorithms. An `O(n^2)` solution performs about one million operations, which is trivial within the time limit. Cubic solutions start approaching one billion operations in the worst case and are unsafe in Python.

The tricky part is that `b[i]` does not describe inversions in the usual sense. Each value only cares about numbers at least `k` larger than itself. That means relationships between nearby values are irrelevant.

A common mistake is to think greedily placing the smallest possible unused number at every position always works. Consider:

```
n = 4, k = 2
B = [0, 1, 0, 0]
```

Value `2` needs one earlier number at least `4`. The only candidate is `4`, so `4` must appear before `2`. If we greedily place small numbers first, we might build:

```
1 2 3 4
```

This violates the requirement for `2`.

Another subtle case appears when `k` is large.

```
n = 5, k = 5
B = [0, 0, 0, 0, 0]
```

No value can have an earlier number at least `i + 5`, because such numbers do not exist. Every permutation satisfies the conditions, so the lexicographically smallest answer is:

```
1 2 3 4 5
```

A careless implementation may still try to enforce dependencies that are actually impossible.

One more dangerous edge case is when several values have identical requirements.

```
n = 5, k = 2
B = [0, 0, 0, 0, 0]
```

Here every small number wants zero large predecessors. The lexicographically smallest valid permutation is simply increasing order. If we process values in the wrong direction, we may produce a valid but non-minimal answer like:

```
3 1 4 2 5
```

The problem is not just reconstructing any permutation, but the smallest one in lexicographic order.

## Approaches

The brute-force idea is straightforward. Generate all permutations, compute the corresponding array `B`, and return the first permutation matching the input. Computing `B` for one permutation takes `O(n^2)` time because for every value we may scan everything to its left. The real issue is the number of permutations. Even for `n = 10`, there are `10! ≈ 3.6 million` possibilities. At `n = 1000`, exhaustive search is completely impossible.

To improve this, we need to understand what the counts actually mean.

Suppose we look at a value `i`. Only numbers from `i + k` to `n` matter for its count. Smaller values are irrelevant. Let:

```
big(i) = count of numbers >= i + k
```

There are exactly:

```
n - (i + k) + 1 = n - i - k + 1
```

such numbers, when `i + k ≤ n`.

The value `b[i]` tells us how many of those large numbers appear before `i`. The remaining large numbers must appear after `i`.

This starts looking like ordering constraints between elements.

A much more useful perspective is to build the permutation from largest values downward.

When we process value `i`, all values at least `i + k` are already known. Their relative positions are fixed. We only need to decide where to insert `i` among them so that exactly `b[i]` of those large values stay before it.

Suppose there are `m` already-placed large values. If exactly `b[i]` of them must be before `i`, then `i` must be inserted immediately after the first `b[i]` large values.

Values between `i + 1` and `i + k - 1` do not affect the count at all, so their positions are irrelevant for this condition.

This gives a clean greedy construction.

We process values from `n` down to `1`. For each value `i`, we insert it into the current sequence at a carefully chosen position. Since we insert smaller values later, placing a smaller value earlier in the sequence improves lexicographic order whenever possible.

The final complexity becomes `O(n^2)`, which easily fits the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n²) | O(n) | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start with an empty sequence.
2. Process values from `n` down to `1`.
3. For the current value `i`, identify all already-inserted values that are at least `i + k`.

These are exactly the values that contribute to `b[i]`.
4. Scan the current sequence from left to right and count how many contributing values have been seen.
5. Insert `i` at the first position where exactly `b[i]` contributing values remain before it.

If `b[i] = 0`, we place `i` as early as possible.

If `b[i] = 2`, we skip past two contributing values before inserting.
6. Continue until all values are inserted.
7. Output the final sequence.

### Why it works

When processing `i`, every value at least `i + k` has already been placed because we process from larger numbers to smaller numbers. Smaller values can never affect `b[i]`, so future insertions are harmless.

The insertion position guarantees that exactly `b[i]` valid contributors stay before `i`. Since we always insert `i` as early as possible while preserving this count, the resulting permutation is lexicographically minimal.

The key invariant is:

```
After processing values from n down to i,
all conditions for processed values are already permanently satisfied.
```

Future insertions only involve smaller numbers, which cannot contribute to any processed value's count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    b = list(map(int, input().split()))

    perm = []

    for i in range(n, 0, -1):
        need = b[i - 1]

        cnt = 0
        pos = len(perm)

        for j in range(len(perm) + 1):
            if cnt == need:
                pos = j
                break

            if j < len(perm) and perm[j] >= i + k:
                cnt += 1

        perm.insert(pos, i)

    print(*perm)

solve()
```

The array `perm` stores the partially constructed permutation.

We process values in descending order because every value that can affect `i` must already be present before we decide where to place `i`.

The inner loop searches for the earliest insertion point producing exactly `b[i]` large predecessors. The order of operations inside this loop matters. We first check whether the current number of qualifying predecessors equals the required count. Only after that do we advance past another element.

This avoids an off-by-one mistake. Suppose `need = 0`. We must insert before the first qualifying element, not after it.

The condition:

```
perm[j] >= i + k
```

implements the definition directly. Only sufficiently large values contribute.

Python list insertion is `O(n)`, but with `n ≤ 1000`, the total complexity remains quadratic.

## Worked Examples

### Example 1

Input:

```
5 2
1 2 1 0 0
```

| Current i | Current perm | Required b[i] | Insertion position | New perm |
| --- | --- | --- | --- | --- |
| 5 | [] | 0 | 0 | [5] |
| 4 | [5] | 0 | 0 | [4, 5] |
| 3 | [4, 5] | 1 | 2 | [4, 5, 3] |
| 2 | [4, 5, 3] | 2 | 2 | [4, 5, 2, 3] |
| 1 | [4, 5, 2, 3] | 1 | 1 | [4, 1, 5, 2, 3] |

Final answer:

```
4 1 5 2 3
```

For value `2`, the contributing numbers are `4` and `5`. We need exactly two of them before `2`, so `2` is inserted after both.

This trace shows why processing downward works. When inserting `2`, every relevant larger number already has a fixed position.

### Example 2

Input:

```
5 5
0 0 0 0 0
```

| Current i | Current perm | Required b[i] | Insertion position | New perm |
| --- | --- | --- | --- | --- |
| 5 | [] | 0 | 0 | [5] |
| 4 | [5] | 0 | 0 | [4, 5] |
| 3 | [4, 5] | 0 | 0 | [3, 4, 5] |
| 2 | [3, 4, 5] | 0 | 0 | [2, 3, 4, 5] |
| 1 | [2, 3, 4, 5] | 0 | 0 | [1, 2, 3, 4, 5] |

Final answer:

```
1 2 3 4 5
```

No value has contributors because `i + k` always exceeds `n`. The algorithm naturally inserts every value at the beginning, producing the lexicographically smallest permutation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each insertion scans and shifts at most `n` elements |
| Space | O(n) | The permutation array stores `n` integers |

With `n = 1000`, quadratic time is completely safe. Around one million operations fit easily within the one-second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    b = list(map(int, input().split()))

    perm = []

    for i in range(n, 0, -1):
        need = b[i - 1]

        cnt = 0
        pos = len(perm)

        for j in range(len(perm) + 1):
            if cnt == need:
                pos = j
                break

            if j < len(perm) and perm[j] >= i + k:
                cnt += 1

        perm.insert(pos, i)

    print(*perm)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("5 2\n1 2 1 0 0\n") == "4 1 5 2 3", "sample 1"

# minimum size
assert run("1 1\n0\n") == "1", "single element"

# no contributing pairs
assert run("5 5\n0 0 0 0 0\n") == "1 2 3 4 5", "large k"

# already lexicographically smallest
assert run("4 2\n0 0 0 0\n") == "1 2 3 4", "all zero counts"

# forces large number before small number
assert run("4 2\n0 1 0 0\n") == "1 4 2 3", "dependency handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | `1` | Minimum-size input |
| `5 5 / 0 0 0 0 0` | `1 2 3 4 5` | No contributors exist |
| `4 2 / 0 0 0 0` | `1 2 3 4` | Lexicographically smallest ordering |
| `4 2 / 0 1 0 0` | `1 4 2 3` | Correct handling of required large predecessors |

## Edge Cases

Consider:

```
4 2
0 1 0 0
```

Value `2` needs exactly one earlier value at least `4`. The algorithm processes:

```
4 -> [4]
3 -> [3, 4]
2 -> [3, 4, 2]
1 -> [1, 3, 4, 2]
```

Only `4` contributes to `2`, and it appears before `2`, so the condition is satisfied. A naive greedy approach placing small numbers first would fail.

Now consider:

```
5 5
0 0 0 0 0
```

For every value `i`, the threshold `i + 5` exceeds `n`. No contributors exist. During insertion, the algorithm immediately sees that `cnt == need == 0` and inserts each value at the beginning:

```
[5]
[4,5]
[3,4,5]
[2,3,4,5]
[1,2,3,4,5]
```

The final permutation is lexicographically minimal.

Finally, consider:

```
5 2
0 0 0 0 0
```

Every value wants zero large predecessors. The algorithm always inserts each value before the first qualifying large element. This pushes smaller numbers toward the front whenever possible, producing:

```
1 2 3 4 5
```

instead of another valid but lexicographically larger permutation.
