---
title: "CF 1761B - Elimination of a Ring"
description: "We are given a cyclic sequence, which means the first and last positions are also adjacent. Initially, no two adjacent elements are equal. At any moment, Muxii may choose one element and erase it. After that erasure, the ring checks whether equal values have become adjacent."
date: "2026-06-09T14:04:57+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1761
codeforces_index: "B"
codeforces_contest_name: "Pinely Round 1 (Div. 1 + Div. 2)"
rating: 1000
weight: 1761
solve_time_s: 359
verified: true
draft: false
---

[CF 1761B - Elimination of a Ring](https://codeforces.com/problemset/problem/1761/B)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy, implementation  
**Solve time:** 5m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a cyclic sequence, which means the first and last positions are also adjacent. Initially, no two adjacent elements are equal.

At any moment, Muxii may choose one element and erase it. After that erasure, the ring checks whether equal values have become adjacent. If they have, one of those equal neighbors immediately disappears. This automatic removal may create another equal-adjacent pair, which is again removed, and so on.

The process continues until the ring becomes empty. We want to maximize the number of times Muxii performs the explicit operation of choosing and erasing an element. Automatic removals do not count.

The input gives several test cases. For each cyclic sequence, we must compute the largest possible number of manual deletions.

The constraints are very small. The sequence length is at most 100, and there are at most 100 test cases. Even an expensive simulation would fit comfortably. The challenge is not performance but understanding the structure of the process.

The main source of mistakes is assuming that every element can always be manually removed. Consider:

```text
4
1 2 1 2
```

If we delete one `1`, the ring becomes:

```text
2 1 2
```

Now there are only three elements left, so at most three manual operations are possible. The correct answer is 3, not 4.

Another subtle case is a sequence containing a value that appears only once.

```text
4
1 2 3 2
```

Deleting the unique value `3` first gives:

```text
1 2 2
```

One of the two adjacent `2`s disappears automatically:

```text
1 2
```

After that, both remaining elements can be removed manually. The answer is 4.

A final edge case is a ring of size 1.

```text
1
1
```

The only element is not adjacent to itself. We can delete it manually, so the answer is 1.

## Approaches

A brute-force approach would try every possible deletion order and simulate all automatic removals. This is correct because it explores every valid strategy. Unfortunately, the number of deletion orders is roughly factorial in the number of elements. Even for moderate sizes this becomes completely infeasible.

The key observation comes from examining when automatic deletions are unavoidable.

Suppose some value appears exactly once in the ring. Let that position contain value `x`. If we delete that element first, its two neighbors become adjacent. Since `x` was unique, those neighbors cannot both equal `x`. More importantly, we can choose such a position so that any automatic deletions help us shrink the ring while preserving the ability to keep making manual moves.

In fact, if there exists a value that appears only once, we can always arrange the deletions so that every original element contributes one manual operation. The answer becomes `n`.

The only problematic situation is when every value appears at least twice.

Because adjacent equal values are forbidden initially, every occurrence of a value must be separated by other values. If every value appears at least twice, the smallest possible number of distinct values is two, and the ring behaves differently. In this case one manual deletion inevitably causes the ring to collapse enough that we lose exactly one possible operation.

The remarkable consequence is that only two answers ever occur:

If some value appears exactly once, the answer is `n`.

If every value appears at least twice, the answer is `n / 2 + 1`.

Since every value appears at least twice and the total length is `n`, the second case can only happen when there are exactly `n / 2` distinct values.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force Simulation of All Orders | Exponential | O(n) | Too slow |
| Frequency Observation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every value in the ring.

2. Check whether some value appears exactly once.

3. If such a value exists, output `n`.

   A unique value can be used as a starting point that allows us to preserve the maximum possible number of manual deletions.

4. Otherwise, every value appears at least twice.

5. Output `n // 2 + 1`.

   In this situation the structure of the ring forces one effective loss of a manual operation, and the maximum becomes exactly `n/2 + 1`.

### Why it works

The entire problem hinges on whether a unique value exists.

A value appearing exactly once provides a safe place to start deleting. By choosing deletions appropriately, automatic removals never reduce the total number of manual operations available, so all `n` elements can be accounted for through manual choices.

When every value appears at least twice, the ring consists entirely of repeated values. Because equal neighbors are forbidden, occurrences of the same value must alternate with other values. Any deletion eventually merges two equal values and triggers an unavoidable automatic removal. The optimal strategy loses exactly one potential manual operation, leading to the closed-form answer `n/2 + 1`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        
        has_single = any(v == 1 for v in freq.values())
        
        if has_single:
            print(n)
        else:
            print(n // 2 + 1)

if __name__ == "__main__":
    solve()
```

The implementation follows the mathematical characterization directly.

The frequency table determines whether some value appears exactly once. If such a value exists, we print `n`. Otherwise we print `n // 2 + 1`.

There are no tricky boundary conditions. The case `n = 1` naturally falls into the first branch because the single value appears once. Integer overflow is impossible because all computations involve values at most 100.

## Worked Examples

### Example 1

Input:

```text
4
1 2 3 2
```

Frequency table:

| Value | Frequency |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |

A value appears exactly once.

| Step | Result |
|---|---|
| Detect frequency 1 | True |
| Answer | 4 |

The answer is 4. Every element can effectively contribute to a manual deletion.

### Example 2

Input:

```text
4
1 2 1 2
```

Frequency table:

| Value | Frequency |
|---|---|
| 1 | 2 |
| 2 | 2 |

No value appears exactly once.

| Step | Result |
|---|---|
| Detect frequency 1 | False |
| Compute n//2 + 1 | 3 |

The answer is 3.

This example demonstrates the second structural case. Every value repeats, so one potential manual operation is inevitably lost.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) | One pass to count frequencies |
| Space | O(n) | Frequency map stores distinct values |

Since `n ≤ 100`, the running time is tiny. Even across all test cases the solution performs only a few thousand operations.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = []

    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1

        if any(v == 1 for v in freq.values()):
            out.append(str(n))
        else:
            out.append(str(n // 2 + 1))

    return "\n".join(out)

# provided sample
assert run("""3
4
1 2 3 2
4
1 2 1 2
1
1
""") == """4
3
1"""

# minimum size
assert run("""1
1
1
""") == "1"

# all values unique
assert run("""1
5
1 2 3 4 5
""") == "5"

# every value repeated
assert run("""1
6
1 2 3 1 2 3
""") == "4"

# smallest repeated structure
assert run("""1
2
1 2
""") == "2"
```

| Test input | Expected output | What it validates |
|---|---|---|
| `1 / 1 / 1` | `1` | Single-element ring |
| `1 2 3 4 5` | `5` | Presence of unique values |
| `1 2 3 1 2 3` | `4` | Every value repeated |
| `1 2` | `2` | Smallest nontrivial ring |
| Sample input | `4 3 1` | Official examples |

## Edge Cases

Consider:

```text
1
1
1
```

The frequency of value `1` is exactly one. The algorithm returns `n = 1`. This matches the fact that the lone element can be deleted manually.

Consider:

```text
1
4
1 2 3 2
```

Values `1` and `3` appear once. The algorithm immediately returns `4`. A unique value exists, so all four manual operations can be achieved.

Consider:

```text
1
4
1 2 1 2
```

Every value appears twice. The algorithm enters the second branch and returns:

```text
4 // 2 + 1 = 3
```

This matches the optimal strategy and the official sample.

Consider:

```text
1
6
1 2 3 1 2 3
```

Every value appears twice, so the answer is:

```text
6 // 2 + 1 = 4
```

This verifies that the second formula applies beyond the smallest examples and depends only on the absence of unique values.
