---
title: "CF 283A - Cows and Sequence"
description: "We maintain a dynamic sequence of integers. Initially the sequence contains only one value, 0. Each operation changes the sequence in one of three ways. We may add some value x to the first a elements, append a new number to the end, or remove the last element."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 283
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 174 (Div. 1)"
rating: 1600
weight: 283
solve_time_s: 95
verified: true
draft: false
---

[CF 283A - Cows and Sequence](https://codeforces.com/problemset/problem/283/A)

**Rating:** 1600  
**Tags:** constructive algorithms, data structures, implementation  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a dynamic sequence of integers. Initially the sequence contains only one value, `0`.

Each operation changes the sequence in one of three ways. We may add some value `x` to the first `a` elements, append a new number to the end, or remove the last element. After every operation we must print the average of the current sequence.

The difficulty is not computing the average itself. The difficulty is supporting up to `2 * 10^5` operations while the sequence is constantly changing.

A direct simulation becomes dangerous because operation type 1 can affect many elements at once. If every operation updates a large prefix explicitly, the total work can reach roughly:

$$1 + 2 + 3 + \dots + 2 \cdot 10^5$$

which is about `2 * 10^10` updates. That is far beyond what fits in a 2 second time limit.

The memory limit is generous enough for linear-sized arrays, so storing information for each position is completely fine. The real requirement is reducing every operation to constant time.

There are a few edge cases that commonly break incorrect implementations.

Consider this input:

```
3
2 5
1 2 3
3
```

The sequence evolves like this:

```
[0, 5]
[3, 8]
[3]
```

The final average is `3.0`.

A buggy implementation may forget that the prefix increment applied to the removed element must disappear when that element is popped.

Another subtle case appears when the sequence size becomes `1` again:

```
2
1 1 7
3
```

The sequence becomes:

```
[7]
[7]
```

The second operation removes nothing except the appended structure from earlier operations. Some implementations accidentally erase accumulated increments on the remaining first element.

Negative values also matter:

```
3
2 -5
1 2 -3
3
```

The sequence becomes:

```
[0, -5]
[-3, -8]
[-3]
```

The average after the second operation is `-5.5`. Any solution relying on unsigned arithmetic or careless integer division fails here.

## Approaches

The brute-force approach stores the entire sequence explicitly.

For operation type 1, we iterate through the first `a` elements and add `x` to each one. For operation type 2, we append a value. For operation type 3, we pop the last value. We also maintain the total sum so the average can be printed in constant time.

This approach is correct because every operation directly matches the problem statement. The problem is the running time. A single prefix update may touch `O(n)` elements, and there can be `2 * 10^5` operations. In the worst case we perform about `2 * 10^10` element updates.

The key observation is that we never actually need the full sequence values individually. We only need the total sum and enough information to undo updates when elements are removed.

Suppose operation type 1 adds `x` to the first `a` elements. Instead of modifying every element, we can store that increment lazily. Let `add[i]` represent extra value that should affect position `i`.

When we add `x` to the first `a` elements, we simply do:

```
add[a - 1] += x
```

and increase the total sum by `a * x`.

Why does this work? Because position `a - 1` acts like a container for all increments affecting prefixes ending there. Later, when the last element is removed, any pending increment attached to that position should move one step left, since the shorter prefix still exists.

This transforms expensive range updates into constant-time bookkeeping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Maintain three pieces of information:

- `arr`, the base values of elements.
- `extra`, lazy increments associated with positions.
- `total`, the sum of the current sequence.
2. Initially:

- `arr = [0]`
- `extra = [0]`
- `total = 0`
3. For operation type `1 a x`:

- Add `x` to `extra[a - 1]`.
- Increase `total` by `a * x`.

We do not touch the actual first `a` elements individually. The total sum already reflects the update, and `extra[a - 1]` remembers that this increment belongs to a prefix ending there.
4. For operation type `2 k`:

- Append `k` to `arr`.
- Append `0` to `extra`.
- Increase `total` by `k`.

The new element starts with no pending prefix increment attached to it.
5. For operation type `3`:

- Let `idx` be the last position.
- Remove the contribution of the last element from `total`.
- The real value of the last element equals:

```
arr[idx] + extra[idx]
```
- Subtract this value from `total`.
- Before deleting the last position, move its pending increment to the previous position:

```
extra[idx - 1] += extra[idx]
```
- Pop the last elements from both arrays.

The transfer step is the core idea. Any prefix increment that affected the removed last element must continue affecting earlier elements.
6. After every operation:

- Print:

$$\frac{\text{total}}{\text{current size}}$$

### Why it works

The invariant is:

```
total = sum of all real sequence values
```

and

```
extra[i]
```

stores all pending prefix increments whose right boundary is exactly `i`.

When we add `x` to the first `a` elements, the total sum increases correctly by `a * x`. Instead of distributing that increment immediately, we attach it to position `a - 1`.

When the last element is removed, all increments associated with that position should continue affecting earlier elements. Moving `extra[last]` to `extra[last - 1]` preserves exactly that behavior.

Because every operation updates the invariant correctly, the printed average is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    arr = [0]
    extra = [0]
    total = 0

    out = []

    for _ in range(n):
        parts = list(map(int, input().split()))
        t = parts[0]

        if t == 1:
            a, x = parts[1], parts[2]

            extra[a - 1] += x
            total += a * x

        elif t == 2:
            k = parts[1]

            arr.append(k)
            extra.append(0)
            total += k

        else:
            idx = len(arr) - 1

            removed = arr[idx] + extra[idx]
            total -= removed

            if idx > 0:
                extra[idx - 1] += extra[idx]

            arr.pop()
            extra.pop()

        out.append(f"{total / len(arr):.10f}")

    sys.stdout.write("\n".join(out))

solve()
```

The solution keeps the actual appended values in `arr` and the deferred prefix increments in `extra`.

The variable `total` is always the true sum of the sequence after all operations. That allows each average to be computed immediately without rebuilding any values.

The most delicate part is operation type 3. The removed element is not just `arr[idx]`. It also includes all deferred increments stored in `extra[idx]`. Forgetting this produces wrong averages after several prefix additions.

Another easy mistake is deleting `extra[idx]` before transferring it to `extra[idx - 1]`. The transfer must happen first, otherwise increments affecting earlier elements disappear incorrectly.

The check `if idx > 0` avoids accessing an invalid position when only one element remains.

Using floating-point division is safe because the required precision is only `1e-6`.

## Worked Examples

### Example 1

Input:

```
5
2 1
3
2 3
2 1
3
```

| Step | Operation | arr | extra | total | Average |
| --- | --- | --- | --- | --- | --- |
| Initial | - | [0] | [0] | 0 | - |
| 1 | 2 1 | [0,1] | [0,0] | 1 | 0.5 |
| 2 | 3 | [0] | [0] | 0 | 0 |
| 3 | 2 3 | [0,3] | [0,0] | 3 | 1.5 |
| 4 | 2 1 | [0,3,1] | [0,0,0] | 4 | 1.333333 |
| 5 | 3 | [0,3] | [0,0] | 3 | 1.5 |

This example shows that append and pop operations behave normally even when no prefix increments exist. The total sum always matches the actual sequence.

### Example 2

Input:

```
5
2 5
1 2 3
2 4
1 3 2
3
```

| Step | Operation | arr | extra | total | Average |
| --- | --- | --- | --- | --- | --- |
| Initial | - | [0] | [0] | 0 | - |
| 1 | 2 5 | [0,5] | [0,0] | 5 | 2.5 |
| 2 | 1 2 3 | [0,5] | [0,3] | 11 | 5.5 |
| 3 | 2 4 | [0,5,4] | [0,3,0] | 15 | 5 |
| 4 | 1 3 2 | [0,5,4] | [0,3,2] | 21 | 7 |
| 5 | 3 | [0,5] | [0,5] | 15 | 7.5 |

After step 4, the real sequence is:

```
[5, 10, 6]
```

The final pop removes `6`, and the pending increment `2` moves left. That is why `extra` changes from `[0,3,2]` to `[0,5]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every operation performs only constant-time updates |
| Space | O(n) | Arrays store one entry per sequence element |

With at most `2 * 10^5` operations, linear time easily fits within the time limit. The memory usage is also small because only a few arrays of length at most `2 * 10^5` are stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    arr = [0]
    extra = [0]
    total = 0

    out = []

    for _ in range(n):
        parts = list(map(int, input().split()))
        t = parts[0]

        if t == 1:
            a, x = parts[1], parts[2]
            extra[a - 1] += x
            total += a * x

        elif t == 2:
            k = parts[1]
            arr.append(k)
            extra.append(0)
            total += k

        else:
            idx = len(arr) - 1

            removed = arr[idx] + extra[idx]
            total -= removed

            if idx > 0:
                extra[idx - 1] += extra[idx]

            arr.pop()
            extra.pop()

        out.append(f"{total / len(arr):.10f}")

    return "\n".join(out)

# provided sample
assert run(
"""5
2 1
3
2 3
2 1
3
"""
) == "\n".join([
    "0.5000000000",
    "0.0000000000",
    "1.5000000000",
    "1.3333333333",
    "1.5000000000"
]), "sample 1"

# minimum-size behavior
assert run(
"""1
1 1 5
"""
) == "5.0000000000", "single element increment"

# prefix increment then pop
assert run(
"""3
2 5
1 2 3
3
"""
) == "\n".join([
    "2.5000000000",
    "5.5000000000",
    "3.0000000000"
]), "lazy propagation after pop"

# negative values
assert run(
"""3
2 -5
1 2 -3
3
"""
) == "\n".join([
    "-2.5000000000",
    "-5.5000000000",
    "-3.0000000000"
]), "negative updates"

# repeated pops and pushes
assert run(
"""6
2 4
2 6
1 3 2
3
3
1 1 7
"""
) == "\n".join([
    "2.0000000000",
    "3.3333333333",
    "5.3333333333",
    "5.0000000000",
    "2.0000000000",
    "9.0000000000"
]), "state consistency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single increment on size 1 | 5.0 | Correct handling of smallest sequence |
| Prefix increment then pop | 3.0 final average | Proper transfer of lazy increments |
| Negative updates | Negative averages | Correct signed arithmetic |
| Repeated pops and pushes | Stable averages | State remains consistent across many mutations |

## Edge Cases

Consider the case where a removed element carries pending increments:

```
3
2 5
1 2 3
3
```

After the second operation:

```
arr = [0, 5]
extra = [0, 3]
```

The real sequence is `[3, 8]`.

When removing the last element, we subtract:

```
5 + 3 = 8
```

from the total. Then we transfer `extra[1]` into `extra[0]`. The remaining state becomes:

```
arr = [0]
extra = [3]
```

which correctly represents the sequence `[3]`.

Now consider shrinking back to a single element:

```
2
1 1 7
3
```

After the first operation:

```
arr = [0]
extra = [7]
```

The sequence is `[7]`.

Operation type 3 never appears here because the problem guarantees we never remove the final remaining element. The implementation safely avoids invalid indexing with:

```
if idx > 0:
```

Finally, consider negative updates:

```
3
2 -5
1 2 -3
3
```

The total evolves as:

```
-5
-11
-3
```

The averages become:

```
-2.5
-5.5
-3.0
```

Since the algorithm only performs integer additions and floating-point division at output time, negative values work naturally without any special handling.
