---
title: "CF 2185D - OutOfMemoryError"
description: "We start with an array and a sequence of update operations. Each operation adds some value to one position. The unusual part is the crash rule. After every update, if any element of the current array becomes larger than h, the computer immediately crashes."
date: "2026-06-07T21:31:04+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2185
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1074 (Div. 4)"
rating: 1100
weight: 2185
solve_time_s: 154
verified: true
draft: false
---

[CF 2185D - OutOfMemoryError](https://codeforces.com/problemset/problem/2185/D)

**Rating:** 1100  
**Tags:** data structures, implementation, math, two pointers  
**Solve time:** 2m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array and a sequence of update operations. Each operation adds some value to one position.

The unusual part is the crash rule. After every update, if any element of the current array becomes larger than `h`, the computer immediately crashes. When that happens, the entire array is reset back to its original state, not to the state before the last operation.

We must process all operations in order and output the final array after every crash and reset has been applied.

The constraints are the first thing that shapes the solution. Across all test cases, the total number of array elements and operations is at most `2·10^5`. That means an `O(n + m)` or `O((n+m) log n)` solution is easily fast enough. On the other hand, any approach that scans the entire array after every operation would require up to `O(nm)` work, which becomes about `4·10^10` operations in the worst case and is completely infeasible.

The most dangerous part of the problem is the reset behavior. A crash does not undo only the last operation. It restores the original array from the beginning of the test case.

Consider:

```
n = 2, h = 5
a = [1, 1]

operations:
(1, 3)
(1, 3)
```

After the first update we get `[4,1]`.

After the second update we get `[7,1]`, which crashes.

The correct state becomes `[1,1]`, not `[4,1]`.

A solution that only reverts the last operation would produce the wrong answer.

Another subtle case is when several updates have accumulated since the most recent reset:

```
a = [0]
h = 5

operations:
+2
+2
+2
```

The states are:

```
[2]
[4]
[6] -> crash -> [0]
```

The final answer is `[0]`.

The overflow check must be performed against the accumulated value since the last reset, not against a single operation.

A third edge case is updates with `c = 0`.

```
a = [5]
h = 5

operation:
+0
```

The value remains exactly `5`, which is allowed because crashing happens only when a value becomes strictly greater than `h`.

The correct output remains `[5]`.

## Approaches

The most direct simulation keeps the current array explicitly. For every operation, we modify one position and then check whether any element exceeds `h`. If a crash occurs, we restore the original array.

This is correct because it follows the statement literally.

The problem is detecting crashes. After each operation we would need to scan all `n` elements to see whether some value exceeds `h`. With up to `2·10^5` operations and `2·10^5` elements, this becomes `O(nm)` in the worst case.

The key observation is that only one position changes during an operation.

Suppose we store, for each index, the total amount added since the most recent reset. Let

```
delta[i] = additions applied to position i since the last crash
```

The current value at position `i` is

```
a[i] + delta[i]
```

When an operation adds `c` to position `b`, only position `b` changes. Every other position keeps the same value as before.

That means a crash can only be triggered by the updated position. There is no need to inspect the whole array.

After updating `delta[b]`, we simply check whether

```
a[b] + delta[b] > h
```

If not, the operation succeeds.

If it is larger than `h`, a crash occurs and every accumulated modification since the previous reset disappears. Conceptually all `delta` values become zero.

Resetting an entire length-`n` array every time would again be expensive. We need a way to clear all accumulated updates in constant time.

The trick is to treat updates between crashes as belonging to a "generation". Each position remembers the generation in which its stored delta was last updated. When a crash occurs, we increment the generation counter. Any old delta automatically becomes irrelevant because its generation no longer matches the current one.

This is a standard lazy-reset technique.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store the original array `a`.
2. Create an array `delta` of length `n`, initially all zero.
3. Create an array `stamp` of length `n`, initially all zero.
4. Maintain a current generation number `cur`, initially `1`.
5. For an operation `(b, c)`, convert `b` to zero-based indexing.
6. If `stamp[b] != cur`, then the stored delta belongs to an old generation. Set `delta[b] = 0` and `stamp[b] = cur`.
7. Add `c` to `delta[b]`.
8. Check whether `a[b] + delta[b] > h`.
9. If the condition is false, continue to the next operation.
10. If the condition is true, a crash occurs. Increment `cur` by one. This logically clears all accumulated deltas because every existing stamp now belongs to an older generation.
11. After all operations, reconstruct the final array. For each position:

- If `stamp[i] == cur`, its value is `a[i] + delta[i]`.
- Otherwise, its value is simply `a[i]`.

### Why it works

At any moment, the current array differs from the original array only by updates performed since the most recent crash. For every index, `delta[i]` stores exactly the sum of those surviving updates.

The generation counter guarantees that all updates from earlier crashes are ignored. Incrementing the generation is equivalent to setting every delta to zero, but without touching the entire array.

Since an operation modifies only one position, only that position can newly exceed `h`. Checking `a[b] + delta[b]` is sufficient to determine whether a crash occurs. The algorithm always maintains the exact state described in the problem statement, so the final reconstructed array is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, m, h = map(int, input().split())
        a = list(map(int, input().split()))

        delta = [0] * n
        stamp = [0] * n
        cur = 1

        for _ in range(m):
            b, c = map(int, input().split())
            b -= 1

            if stamp[b] != cur:
                delta[b] = 0
                stamp[b] = cur

            delta[b] += c

            if a[b] + delta[b] > h:
                cur += 1

        ans = []
        for i in range(n):
            if stamp[i] == cur:
                ans.append(str(a[i] + delta[i]))
            else:
                ans.append(str(a[i]))

        out.append(" ".join(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The array `a` never changes because it represents the original state to which every crash resets.

The pair `(delta, stamp)` stores only updates from the current generation. Whenever an index is touched after a crash, its stale information is discarded lazily by checking the stamp.

The most delicate part is the crash handling. When a crash happens, we do not modify any element of `delta` or `stamp`. We only increment `cur`. This works because every stored update immediately becomes part of an old generation and is ignored from that point onward.

Another subtle point is the order of operations. We first apply the update, then test whether the value exceeds `h`. This matches the statement, where the crash occurs after the operation has been performed.

Python integers have arbitrary precision, so values up to roughly `2·10^14` cause no overflow issues.

## Worked Examples

### Example 1

Input:

```
n = 3, m = 4, h = 5
a = [1, 2, 1]

operations:
(1,4)
(2,4)
(3,3)
(2,0)
```

| Step | Operation | delta | Generation | Crash? |
| --- | --- | --- | --- | --- |
| Start | - | [0,0,0] | 1 | No |
| 1 | (1,4) | [4,0,0] | 1 | No |
| 2 | (2,4) | [4,4,0] | 1 | Yes, 2+4=6 |
| Reset | - | unchanged physically | 2 | - |
| 3 | (3,3) | [4,4,3] | 2 | No |
| 4 | (2,0) | [4,0,3] | 2 | No |

Final reconstruction uses only generation 2 updates:

```
[1, 2, 4]
```

This example shows why old updates must disappear completely after a crash. The additions stored before generation 2 are ignored.

### Example 2

Input:

```
n = 1, m = 3, h = 5
a = [0]

operations:
(1,2)
(1,2)
(1,2)
```

| Step | Current Value | Generation | Crash? |
| --- | --- | --- | --- |
| Start | 0 | 1 | No |
| +2 | 2 | 1 | No |
| +2 | 4 | 1 | No |
| +2 | 6 | 1 | Yes |

After the crash, generation becomes 2 and all accumulated updates vanish.

Final answer:

```
0
```

This trace demonstrates that a crash resets the entire history since the previous reset, not just the operation that caused the overflow.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each operation and each final reconstruction step is constant time |
| Space | O(n) | Arrays `delta` and `stamp` are stored per position |

The total `n + m` across all test cases is at most `2·10^5`, so the solution performs only linear work overall. This comfortably fits within the 2 second time limit and 256 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m, h = map(int, input().split())
        a = list(map(int, input().split()))

        delta = [0] * n
        stamp = [0] * n
        cur = 1

        for _ in range(m):
            b, c = map(int, input().split())
            b -= 1

            if stamp[b] != cur:
                delta[b] = 0
                stamp[b] = cur

            delta[b] += c

            if a[b] + delta[b] > h:
                cur += 1

        ans = []
        for i in range(n):
            if stamp[i] == cur:
                ans.append(str(a[i] + delta[i]))
            else:
                ans.append(str(a[i]))

        out.append(" ".join(ans))

    return "\n".join(out)

# provided sample
assert run(
"""3
3 4 5
1 2 1
1 4
2 4
3 3
2 0
5 3 1
1 1 1 1 1
1 1
1 1
2 1
4 4 1
1 0 0 0
1 1
4 4
3 3
4 4
"""
) == (
"""1 2 4
1 1 1 1 1
1 0 0 0"""
)

# minimum size
assert run(
"""1
1 1 5
0
1 3
"""
) == "3"

# exact boundary, no crash
assert run(
"""1
1 1 5
2
1 3
"""
) == "5"

# repeated crashes
assert run(
"""1
1 3 1
1
1 1
1 1
1 1
"""
) == "1"

# crash after accumulation
assert run(
"""1
1 3 5
0
1 2
1 2
1 2
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element, one update | `3` | Minimum-size instance |
| Value reaches exactly `h` | `5` | Overflow is strictly `>` |
| Repeated crashes | `1` | Multiple generation changes |
| Three accumulated updates | `0` | Crash depends on cumulative value |

## Edge Cases

### Crash must reset to the original array

Input:

```
1
2 2 5
1 1
1 3
1 3
```

After the first operation the array is `[4,1]`.

After the second operation it becomes `[7,1]`, which crashes.

The algorithm increments the generation counter. All stored updates become obsolete, so the final array is reconstructed as:

```
[1,1]
```

This matches the required reset-to-original behavior.

### Value equal to h is allowed

Input:

```
1
1 1 5
2
1 3
```

The updated value becomes exactly `5`.

The algorithm checks:

```
2 + 3 > 5
```

which is false.

No crash occurs, and the answer is:

```
5
```

Using `>= h` would incorrectly trigger a reset.

### Accumulated updates cause overflow

Input:

```
1
1 3 5
0
1 2
1 2
1 2
```

The sequence of values is:

```
2
4
6
```

The third operation exceeds `h`, so the generation counter advances and all accumulated updates disappear.

The reconstructed array is:

```
0
```

This confirms that the algorithm tracks the total contribution since the last reset, not just the most recent operation.
