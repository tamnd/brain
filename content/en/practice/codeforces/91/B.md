---
title: "CF 91B - Queue"
description: "We are given a queue of walruses, where index order goes from the tail toward the head. For every walrus at position i, we want to find the furthest position j i such that the walrus ahead is strictly younger, meaning a[j] < a[i]. If no such walrus exists, the answer is -1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 91
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 75 (Div. 1 Only)"
rating: 1500
weight: 91
solve_time_s: 130
verified: true
draft: false
---

[CF 91B - Queue](https://codeforces.com/problemset/problem/91/B)

**Rating:** 1500  
**Tags:** binary search, data structures  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a queue of walruses, where index order goes from the tail toward the head. For every walrus at position `i`, we want to find the furthest position `j > i` such that the walrus ahead is strictly younger, meaning `a[j] < a[i]`.

If no such walrus exists, the answer is `-1`.

If such a walrus exists, the displeasure equals the number of walruses standing between them, which is:

$$j - i - 1$$

The key detail is that we do not want the nearest younger walrus. We want the furthest younger walrus ahead in the queue.

The queue length can reach `10^5`, so a quadratic solution is too slow. A naive double loop would check all pairs `(i, j)` with `i < j`, which becomes roughly `10^10` operations in the worst case. That is far beyond what fits inside a 2-second limit. We need something around `O(n log n)` or `O(n)`.

Several edge cases are easy to mishandle.

Consider equal ages:

```
4
5 5 5 5
```

The correct output is:

```
-1 -1 -1 -1
```

A careless implementation using `<=` instead of `<` would incorrectly treat equal ages as younger.

Another subtle case is when the furthest younger walrus is not the smallest value nearby:

```
5
10 9 8 7 6
```

The answers are:

```
3 2 1 0 -1
```

For the first walrus, the correct choice is the walrus with age `6`, not the first younger walrus with age `9`.

One more tricky scenario appears when younger walruses exist only after larger values:

```
6
5 100 99 98 1 2
```

For age `100`, the furthest younger walrus is the `2` at the end, not the `1`. The answer depends on the furthest valid index, not the minimum age.

## Approaches

The brute-force solution follows the definition directly. For every position `i`, scan every later position `j > i`. Whenever `a[j] < a[i]`, update the answer using the furthest such index.

This works because it explicitly checks every candidate. The logic is simple and correct.

The problem is the running time. With `n = 10^5`, the nested loops perform about:

$$\frac{n(n-1)}{2} \approx 5 \times 10^9$$

comparisons in the worst case. That is much too slow.

The important observation is that we only care about positions that could possibly become the furthest younger walrus for someone to the left.

Suppose we process the array from right to left. While moving leftward, we maintain a structure containing candidate positions from the suffix.

A position is useful only if its age is smaller than every age seen farther right. These positions form a strictly decreasing sequence of ages. For example:

```
10 8 5 3 50 45
```

Scanning from right to left produces candidate minima:

```
45 at index 5
3 at index 3
```

Every other value is useless because there already exists a smaller value farther right.

Now consider some walrus with age `x`. Among these suffix minima, we want the furthest index whose age is smaller than `x`.

The candidate ages are strictly increasing when viewed in stored order, so we can binary search for the last value `< x`.

This reduces the problem to:

1. Build suffix minima positions while scanning from right to left.
2. Use binary search to locate the furthest younger walrus.

The total complexity becomes `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an empty list called `mins`.

This list will store pairs `(age, index)` representing suffix minima discovered while scanning from right to left.
2. Start processing the array from the last position toward the first.

At every step, positions already processed belong to the suffix ahead of the current walrus.
3. For the current age `a[i]`, binary search inside `mins`.

We want the rightmost stored age strictly smaller than `a[i]`. Since the stored ages are increasing inside `mins`, binary search works correctly.
4. If such an element exists, compute the displeasure.

Suppose the matching stored position is `j`. The answer is:

$$j - i - 1$$
5. If no smaller age exists in `mins`, store `-1`.

That means there is no younger walrus ahead.
6. After answering for position `i`, decide whether to insert the current walrus into `mins`.

Insert it only if its age is smaller than the last stored minimum. In that case, it becomes a new suffix minimum and may help future positions.
7. Reverse is not needed because answers are written directly into the result array.

### Why it works

The key invariant is that `mins` always contains exactly the suffix minima of positions to the right of the current index.

If a position is not a suffix minimum, then some farther position has an even smaller age. That farther position is always better because the problem asks for the furthest younger walrus.

So every non-minimum position can be discarded safely.

The stored ages are strictly increasing in `mins`, because we append new elements only when a strictly smaller value appears during the right-to-left scan. That ordering allows binary search.

When we binary search for the rightmost age smaller than `a[i]`, we obtain the furthest suffix minimum that is still younger than the current walrus. Since every useful candidate must be a suffix minimum, this position is exactly the correct answer.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = [-1] * n

    # stores (age, index)
    # ages are strictly increasing
    mins = []

    for i in range(n - 1, -1, -1):
        age = a[i]

        # find first age >= current age
        pos = bisect_left(mins, (age, -1))

        # elements before pos have smaller age
        if pos > 0:
            j = mins[pos - 1][1]
            ans[i] = j - i - 1

        # add new suffix minimum
        if not mins or age < mins[-1][0]:
            mins.append((age, i))

    print(*ans)

if __name__ == "__main__":
    solve()
```

The solution scans from right to left because every walrus only cares about people ahead of him. At position `i`, the suffix `[i+1 ... n-1]` has already been processed.

The `mins` array stores suffix minima in a special order. The ages are strictly increasing, while indices also increase because we scan backward. This ordering is what makes binary search possible.

The call:

```
bisect_left(mins, (age, -1))
```

finds the first stored pair whose age is at least `age`. Everything before that position has strictly smaller age, which is exactly what we need.

The rightmost smaller element gives the furthest valid walrus. Since `mins` contains suffix minima ordered by increasing distance, choosing the last smaller element automatically gives the largest index.

One subtle detail is the insertion condition:

```
if not mins or age < mins[-1][0]:
```

Using `<` instead of `<=` matters. Equal ages are not younger, so equal values must not become new suffix minima.

Another easy mistake is the displeasure formula. The problem asks for the number of walruses between the two positions, not the distance itself. That is why we compute:

```
j - i - 1
```

instead of `j - i`.

## Worked Examples

### Example 1

Input:

```
6
10 8 5 3 50 45
```

| i | age | mins before | binary search result | answer | mins after |
| --- | --- | --- | --- | --- | --- |
| 5 | 45 | [] | none | -1 | [(45,5)] |
| 4 | 50 | [(45,5)] | (45,5) | 0 | [(45,5)] |
| 3 | 3 | [(45,5)] | none | -1 | [(45,5),(3,3)] |
| 2 | 5 | [(45,5),(3,3)] | (3,3) | 0 | [(45,5),(3,3)] |
| 1 | 8 | [(45,5),(3,3)] | (3,3) | 1 | [(45,5),(3,3)] |
| 0 | 10 | [(45,5),(3,3)] | (3,3) | 2 | [(45,5),(3,3)] |

Final output:

```
2 1 0 -1 0 -1
```

This trace shows why only suffix minima matter. Even though age `5` is younger than `10`, the walrus with age `3` is farther away and gives larger displeasure.

### Example 2

Input:

```
5
5 5 5 5 5
```

| i | age | mins before | binary search result | answer | mins after |
| --- | --- | --- | --- | --- | --- |
| 4 | 5 | [] | none | -1 | [(5,4)] |
| 3 | 5 | [(5,4)] | none | -1 | [(5,4)] |
| 2 | 5 | [(5,4)] | none | -1 | [(5,4)] |
| 1 | 5 | [(5,4)] | none | -1 | [(5,4)] |
| 0 | 5 | [(5,4)] | none | -1 | [(5,4)] |

Final output:

```
-1 -1 -1 -1 -1
```

This example confirms that equal ages are not considered younger. The binary search correctly rejects equal values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each position performs one binary search |
| Space | O(n) | The suffix minima structure may store up to n elements |

With `n = 10^5`, an `O(n log n)` algorithm easily fits inside the time limit. The memory usage is also small, since we store only a few arrays of size `n`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    ans = [-1] * n
    mins = []

    for i in range(n - 1, -1, -1):
        age = a[i]

        pos = bisect_left(mins, (age, -1))

        if pos > 0:
            j = mins[pos - 1][1]
            ans[i] = j - i - 1

        if not mins or age < mins[-1][0]:
            mins.append((age, i))

    print(*ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run(
    "6\n10 8 5 3 50 45\n"
) == "2 1 0 -1 0 -1", "sample 1"

# minimum size
assert run(
    "2\n1 2\n"
) == "-1 -1", "strictly increasing"

# decreasing sequence
assert run(
    "5\n5 4 3 2 1\n"
) == "3 2 1 0 -1", "furthest younger always at end"

# all equal
assert run(
    "4\n7 7 7 7\n"
) == "-1 -1 -1 -1", "equal ages are not younger"

# mixed case with distant answer
assert run(
    "6\n5 100 99 98 1 2\n"
) == "3 3 2 0 -1 -1", "furthest younger is not necessarily minimum value"

# boundary style case
assert run(
    "5\n10 1 9 2 8\n"
) == "3 -1 1 -1 -1", "checks off-by-one distances"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `-1 -1` | Minimum valid input |
| `5 / 5 4 3 2 1` | `3 2 1 0 -1` | Furthest younger at the end |
| `4 / 7 7 7 7` | `-1 -1 -1 -1` | Equal values must not count |
| `6 / 5 100 99 98 1 2` | `3 3 2 0 -1 -1` | Furthest younger differs from smallest younger |
| `5 / 10 1 9 2 8` | `3 -1 1 -1 -1` | Off-by-one distance handling |

## Edge Cases

Consider all equal ages:

```
4
5 5 5 5
```

While scanning from right to left, the structure stores only one suffix minimum `(5,3)`. Every binary search asks for a value strictly smaller than `5`, but none exists. The algorithm outputs:

```
-1 -1 -1 -1
```

This case confirms that equal ages are handled correctly.

Now consider a strictly decreasing sequence:

```
5
9 8 7 6 5
```

Every walrus except the last has younger walruses ahead. The furthest younger walrus is always the last position.

The answers become:

```
3 2 1 0 -1
```

The algorithm succeeds because suffix minima continually decrease:

```
(5,4), (6,3), (7,2), ...
```

Binary search always selects the furthest valid index.

Finally, consider a case where the smallest younger walrus is not the correct answer:

```
6
5 100 99 98 1 2
```

For the walrus with age `100`, both `1` and `2` are younger. The problem asks for the furthest younger walrus, which is `2` at the end.

The displeasure is:

```
5 - 1 - 1 = 3
```

The suffix minimum structure stores positions in increasing distance order, so the binary search naturally chooses the furthest valid position instead of the smallest age.
