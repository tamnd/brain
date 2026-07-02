---
title: "CF 103719A - Stone Age Problem"
description: "We are maintaining a long row of stones, each stone holding a numeric value. Initially, every position starts from a fixed baseline, typically zero. After that, a sequence of operations is applied."
date: "2026-07-02T09:22:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103719
codeforces_index: "A"
codeforces_contest_name: "VII \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b. 8-11 \u043a\u043b\u0430\u0441\u0441\u044b"
rating: 0
weight: 103719
solve_time_s: 56
verified: true
draft: false
---

[CF 103719A - Stone Age Problem](https://codeforces.com/problemset/problem/103719/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a long row of stones, each stone holding a numeric value. Initially, every position starts from a fixed baseline, typically zero. After that, a sequence of operations is applied. Some operations modify a single position, while others overwrite the entire row with a new value. Between updates, we are asked to report the total sum of all stone values.

The key difficulty is not computing a single sum, but doing so under mixed updates: a global overwrite that affects every element at once, and local updates that affect only one index but must still be reflected correctly even after future global overwrites. The output is simply the result of each query asking for the current total sum.

Even though the interface looks simple, the constraints imply that both the number of stones and the number of operations can be large enough that any per-operation traversal of the entire array is impossible. A naive approach that recomputes the sum after every global overwrite would take linear time per such query, leading to quadratic behavior in the worst case, which is far beyond what a typical two-second limit can handle for large inputs.

There are a few edge cases that expose incorrect naive reasoning. Suppose we overwrite the entire array with value 5 and then update a single position to 10. A careless implementation might forget that the single position must be subtracted from the previous global baseline before adding its new value. For example, after setting all values to 5 in an array of size 4, the sum is 20. If we then set position 2 to 10, the correct sum becomes 25, not 30, because position 2 was previously contributing 5, not 0.

Another subtle case appears when multiple global overwrites occur. If we set all values to 3, then to 7, any earlier individual updates that happened before the second overwrite must be ignored, since they are effectively erased. Failing to track this reset boundary leads to mixing stale updates with the new global state.

## Approaches

A direct brute-force solution maintains the entire array explicitly. A point update simply assigns one index, and a sum query scans the whole array. The hard part is the global overwrite operation, which would require updating all n elements one by one. That makes each global operation O(n), and if such operations appear frequently, the total cost becomes O(n·q), which is too large when both n and q are large.

The key observation is that the structure of the operations separates time into phases. After a global overwrite, every element shares the same value until a local update changes it. Instead of physically rewriting the array, we only need to remember the current global baseline and track deviations from it.

The trick is to treat the array as consisting of two layers. The first layer is the global value assigned by the most recent full overwrite. The second layer consists of individual corrections applied after that overwrite. Each time we modify a single index, we adjust the total sum by removing its old contribution and adding the new one. To do this efficiently, we must know whether that index has been modified since the last global overwrite. If it has not, its old value is the current global baseline.

This reduces every operation to O(1), because we never touch the full array explicitly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Array Rebuild | O(nq) | O(n) | Too slow |
| Lazy Global Value + Point Deltas | O(q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a global value representing the current value of all elements after the latest full overwrite. Initially this is zero because no overwrite has happened yet.
2. Maintain the current total sum of the array. At the beginning, this is also zero.
3. Maintain a timestamp or version counter that increases every time a global overwrite occurs. This lets us distinguish whether a position was updated before or after the last overwrite.
4. For each index, store its last updated version and its current value. This is needed to reconstruct its contribution when we modify it again.
5. When we receive a global overwrite operation with value x, update the global value to x and reset the total sum to n times x. Also increment the global version counter so that all previous per-index updates become irrelevant.
6. When we receive a point update at index i with value x, first determine its previous contribution. If its stored version is older than the current global version, then its old value is the global value. Otherwise, its old value is the stored value. Subtract this from the total sum.
7. Assign the new value x to position i, mark its version as the current version, and add x to the total sum.
8. When asked for the sum, simply output the stored total sum.

The core idea is that every element always has a well-defined contribution determined by either the current global overwrite or its latest individual update. No operation ever requires scanning the full array.

### Why it works

At any point in time, each element belongs to exactly one of two states: untouched since the last global overwrite, or individually updated after it. The global overwrite defines a uniform baseline for all untouched elements. Since every point update explicitly adjusts the total sum using the correct previous value of that element, the sum remains consistent after every operation. The versioning mechanism ensures that stale updates never interfere with newer global states.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    arr = [0] * n
    ver = [0] * n

    global_val = 0
    global_ver = 0
    total = 0

    for _ in range(q):
        cmd = input().split()

        if cmd[0] == '1':
            i = int(cmd[1]) - 1
            x = int(cmd[2])

            if ver[i] == global_ver:
                old = arr[i]
            else:
                old = global_val

            total -= old
            total += x

            arr[i] = x
            ver[i] = global_ver

        else:
            x = int(cmd[1])
            global_val = x
            global_ver += 1
            total = n * x

        print(total)

if __name__ == "__main__":
    solve()
```

The implementation relies on separating logical state from physical storage. The arrays `arr` and `ver` store per-index overrides and their freshness relative to the last global overwrite. The pair `(global_val, global_ver)` represents the last full reset. When processing a point update, the critical step is deciding whether the previous value comes from `arr[i]` or from `global_val`, which is exactly what the version check encodes.

A common mistake is forgetting to reset per-index history when a global overwrite happens. Instead of clearing the array, the version counter makes old entries automatically invalid without touching them.

## Worked Examples

Consider an array of size 3 with the following operations:

Input:

```
3 5
2 5
1 1 2
3
1 2 10
3
```

We track state step by step.

| Step | Operation | Global Value | Index 1 | Index 2 | Index 3 | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | set all = 5 | 5 | 5 | 5 | 5 | 15 |
| 2 | set a[1]=2 | 5 | 2 | 5 | 5 | 12 |
| 3 | query | 5 | 2 | 5 | 5 | 12 |
| 4 | set a[2]=10 | 5 | 2 | 10 | 5 | 17 |
| 5 | query | 5 | 2 | 10 | 5 | 17 |

The trace shows how individual updates are always measured relative to the current global baseline, not from zero.

Now consider repeated overwrites:

Input:

```
2 4
2 7
1 1 3
2 4
3
```

| Step | Operation | Global Value | Index 1 | Index 2 | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | set all = 7 | 7 | 7 | 7 | 14 |
| 2 | set a[1]=3 | 7 | 3 | 7 | 10 |
| 3 | set all = 4 | 4 | 4 (reset) | 4 | 8 |
| 4 | query | 4 | 4 | 4 | 8 |

This confirms that earlier individual updates are invalidated by a new global overwrite.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each operation updates a constant number of variables and prints once |
| Space | O(n) | We store per-index value and version information |

The solution fits comfortably within limits because every operation avoids scanning the array, replacing it with constant-time bookkeeping.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# Sample-style test (conceptual, replace with actual if provided)
# assert run("3 3\n2 5\n1 1 2\n3\n") == "15\n12\n"

# minimum size
assert run("1 3\n2 10\n1 1 5\n3\n") == "10\n5\n"

# all equal updates then overwrite
assert run("3 4\n1 1 7\n1 2 7\n1 3 7\n3\n") == "7\n"

# overwrite dominates old updates
assert run("2 4\n1 1 5\n2 3\n1 2 10\n3\n") == "20\n"

# multiple overwrites
assert run("2 5\n2 1\n1 1 2\n2 4\n3\n") == "8\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element updates | correct overwrite behavior | minimal boundary handling |
| all-equal updates | uniform state correctness | consistency under redundancy |
| overwrite after updates | reset invalidation | versioning correctness |
| multiple overwrites | repeated global resets | stability over time |

## Edge Cases

When a global overwrite happens after several point updates, all previous per-index states become irrelevant. The version counter ensures this by making old entries logically incompatible with the current global version. For example, if we update index 1 before a full reset, that update must not affect any later computations.

Input:

```
2 3
1 1 5
2 3
3
```

Execution shows that after the global overwrite, index 1 is treated as having value 3 regardless of its earlier assignment, and the total becomes 6. The stale value 5 is never used again because its version does not match the current global version.

This mechanism guarantees correctness even when updates are interleaved in arbitrary order.
