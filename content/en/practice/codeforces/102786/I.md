---
title: "CF 102786I - \u041f\u0440\u043e\u0431\u043b\u0435\u043c\u0430 \u0441\u0432\u043e\u0431\u043e\u0434\u043d\u043e\u0433\u043e \u043c\u0435\u0441\u0442\u0430"
description: "Edit We have a row of n goods, represented by an array of weights. The row changes over time: each query swaps the elements at two positions. After every swap, we must determine whether the whole array is sorted in nondecreasing order."
date: "2026-07-27T19:30:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102786
codeforces_index: "I"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u042f\u0440\u0413\u0423 \u0438\u043c. \u041f.\u0413. \u0414\u0435\u043c\u0438\u0434\u043e\u0432\u0430 Demidov Open IT Cup 2019"
rating: 0
weight: 102786
solve_time_s: 61
verified: true
draft: false
---

[CF 102786I - \u041f\u0440\u043e\u0431\u043b\u0435\u043c\u0430 \u0441\u0432\u043e\u0431\u043e\u0434\u043d\u043e\u0433\u043e \u043c\u0435\u0441\u0442\u0430](https://codeforces.com/problemset/problem/102786/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
Edit

# Problem Understanding

We have a row of `n` goods, represented by an array of weights. The row changes over time: each query swaps the elements at two positions. After every swap, we must determine whether the whole array is sorted in nondecreasing order.

The answer does not depend on how the array became its current state. For each moment after a swap, we only need to know whether every element is no larger than the element immediately after it.

The limits force us to avoid checking the entire array after every query. With `n` and `q` both reaching `100000`, a solution that scans all `n` positions for each swap performs up to `10^10` comparisons, which is far beyond what a 2 second limit allows. We need a solution where each query changes only a small amount of maintained information.

The main edge cases come from the fact that a swap does not always affect only the two swapped positions. It can also change the relationships with neighboring elements. For example:

```
Input
3 1
1 3 2
2 3
```

After the swap, the array becomes `[1, 2, 3]`, so the output is:

```
Sorted!
```

A solution that only checks whether the swapped values themselves are in the correct order would miss the fact that the neighbor relationship at position `1` also changed.

Another important case is equal values:

```
Input
3 1
5 5 5
1 3
```

The output is:

```
Sorted!
```

A strict comparison such as `a[i] < a[i+1]` would incorrectly mark this array as unsorted because equal adjacent values are allowed.

A final tricky situation is when the array becomes sorted before later queries:

```
Input
4 2
1 3 2 4
2 3
1 4
```

After the first swap the array is sorted, but the second swap breaks it again. We must answer every query independently from the current state, not stop after the first successful moment.

# Approaches

A straightforward approach is to simulate every swap and then scan the entire array to check whether every adjacent pair is ordered. This is correct because a nondecreasing array is exactly an array where all adjacent comparisons satisfy `a[i] <= a[i+1]`.

The problem is the cost. Each of the `q` queries requires up to `n-1` comparisons, resulting in `O(nq)` work. In the worst case this is about `10^10` operations, which is too slow.

The structure of the problem gives us a smaller target. A swap only changes the values at two positions, so most adjacent pairs keep exactly the same order. If we maintain the number of adjacent pairs that are currently wrong, then a single swap only requires updating the pairs touching the swapped positions.

The array is sorted precisely when this count is zero. Before a swap, we remove the contribution of the affected neighboring pairs, perform the swap, then add their new contribution. Since each position has only two neighbors, every query changes a constant number of pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O(n+q) | O(n) | Accepted |

# Algorithm Walkthrough

1. Build a counter of bad adjacent pairs. For every index `i`, check whether `a[i] > a[i+1]`. If this is true, the pair is a violation of sorted order and increases the counter.
2. For each swap query, identify the two positions being exchanged. The only adjacent pairs that can change are the pairs involving either swapped position, so collect those indices before making any modification.
3. Remove the old contribution of every affected adjacent pair from the counter. This step is needed because the current values are about to disappear from those positions.
4. Swap the two array values.
5. Add the new contribution of every affected adjacent pair after the swap. The counter now describes the current array again.
6. If the counter is zero, print `Sorted!`. Otherwise, print `Unsorted!`.

The reason this works is that every possible disorder in a nondecreasing array appears as a bad adjacent pair. If no adjacent pair is decreasing, then every element is at most the next one, which means the whole array is sorted. The swap operation cannot change any pair that is not adjacent to one of the swapped positions, so updating only those pairs preserves the exact count of violations.

# Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    bad = 0
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            bad += 1

    ans = []

    def value_bad(i):
        return i >= 0 and i + 1 < n and a[i] > a[i + 1]

    for _ in range(q):
        x, y = map(int, input().split())
        x -= 1
        y -= 1

        affected = set()

        for pos in (x, y):
            affected.add(pos - 1)
            affected.add(pos)

        for pos in affected:
            if value_bad(pos):
                bad -= 1

        a[x], a[y] = a[y], a[x]

        for pos in affected:
            if value_bad(pos):
                bad += 1

        if bad == 0:
            ans.append("Sorted!")
        else:
            ans.append("Unsorted!")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The variable `bad` stores the number of adjacent inversions. The helper function checks whether a particular adjacent pair is invalid while also handling boundaries, because positions outside the array should never be counted.

The affected set may contain duplicates when the swapped positions are next to each other. Using a set avoids removing or adding the same adjacent pair twice. This matters for swaps like positions `2` and `3`, where both positions share a neighboring pair.

The code converts positions from the input format, which starts at `1`, into Python indices starting at `0`. The swap happens only after the old contribution is removed, because counting the modified array without removing the previous state would mix two different versions of the array.

# Worked Examples

For the first sample:

| Query | Array after swap | Bad adjacent pairs | Answer |
| --- | --- | --- | --- |
| Start | 1 2 5 3 4 | (5,3) |  |
| 3 4 | 1 2 3 5 4 | (5,4) | Unsorted! |
| 4 5 | 1 2 3 4 5 | none | Sorted! |
| 1 5 | 5 2 3 4 1 | (5,2), (4,1) | Unsorted! |
| 5 1 | 1 2 3 4 5 | none | Sorted! |

This example shows that the counter can move from nonzero to zero and back again. The algorithm does not store whether the array was sorted before, it recomputes the affected information after every modification.

For the second sample:

| Query | Array after swap | Bad adjacent pairs | Answer |
| --- | --- | --- | --- |
| Start | 1 2 | none |  |
| 1 2 | 2 1 | (2,1) | Unsorted! |
| 1 2 | 1 2 | none | Sorted! |
| 1 2 | 2 1 | (2,1) | Unsorted! |

This case demonstrates repeated swaps of the same positions. The maintained counter follows the current array state and does not depend on previous answers.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n+q) | The initial scan checks every adjacent pair once, and each query updates only a constant number of pairs. |
| Space | O(n) | The array and a constant amount of additional information are stored. |

The solution easily fits the constraints because the total number of operations grows linearly with the input size. Even at `100000` swaps, each query performs only a few set insertions, comparisons, and array accesses.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""5 4
1 2 5 3 4
3 4
4 5
1 5
5 1
""") == """Unsorted!
Sorted!
Unsorted!
Sorted!
""", "sample 1"

assert run("""2 3
1 2
1 2
1 2
1 2
""") == """Unsorted!
Sorted!
Unsorted!
""", "sample 2"

assert run("""2 1
7 7
1 2
""") == """Sorted!
""", "equal values"

assert run("""5 1
1 2 3 5 4
4 5
""") == """Sorted!
""", "boundary adjacent swap"

assert run("""5 1
5 4 3 2 1
1 5
""") == """Unsorted!
""", "large disorder after distant swap"

assert run("""100000 1
""" + " ".join(["1"] * 100000) + """
1 100000
""") == """Sorted!
""", "maximum size all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Mixed answers | General swap handling and recovery to sorted order |
| Sample 2 | Alternating answers | Repeated swaps of the same positions |
| Equal values | Sorted! | Nondecreasing comparison must allow equality |
| Adjacent boundary swap | Sorted! | Correct updates near neighboring positions |
| Reverse order swap | Unsorted! | Multiple existing violations |
| Maximum size all equal | Sorted! | Linear preprocessing and memory usage |

# Edge Cases

For equal values, the algorithm uses `>` rather than `>=` when counting bad pairs. With input:

```
3 1
5 5 5
1 3
```

the affected adjacent pairs are checked after the swap, but both comparisons remain valid because `5 <= 5`. The counter stays zero and the answer is `Sorted!`.

For a swap that fixes the entire array, the algorithm removes the old bad pairs before the exchange and then adds the new ones. With:

```
3 1
1 3 2
2 3
```

the initial bad pair is `(3,2)`. It is removed, the swap creates `[1,2,3]`, and no bad pair is added. The counter becomes zero, so the output is `Sorted!`.

For a swap that changes two neighboring positions, duplicate affected indices must not be processed twice. In:

```
4 1
1 4 2 3
2 3
```

the positions share the adjacent pair around them. The set of affected edges keeps this pair only once, preventing an incorrect change in the counter.

For repeated queries that undo each other, the algorithm always works with the current array. In:

```
2 2
1 2
1 2
1 2
```

the first query creates one bad pair and the second query removes it. The outputs are:

```
Unsorted!
Sorted!
```

The maintained counter describes the present state after every operation, which is exactly the information needed for each answer.

```

```

I can also adapt this editorial into a shorter Codeforces-style version if you need one that fits a contest blog format.
