---
title: "CF 222A - Shooshuns and Sequence "
description: "We have an array of integers and a strange operation that keeps the array length unchanged. In one operation, we look at the current k-th element, append a copy of it to the end, then remove the first element."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 222
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 137 (Div. 2)"
rating: 1200
weight: 222
solve_time_s: 85
verified: true
draft: false
---

[CF 222A - Shooshuns and Sequence ](https://codeforces.com/problemset/problem/222/A)

**Rating:** 1200  
**Tags:** brute force, implementation  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of integers and a strange operation that keeps the array length unchanged.

In one operation, we look at the current `k`-th element, append a copy of it to the end, then remove the first element. Effectively, the array shifts left by one position, and the old `k`-th value becomes the new last element.

The task is to determine the minimum number of operations needed to make every element equal. If this can never happen, we must print `-1`.

The constraints allow `n` up to `10^5`, which immediately rules out any simulation that repeatedly rebuilds arrays for many operations. A quadratic solution would already perform around `10^10` operations in the worst case, far beyond the time limit. Linear or near-linear complexity is the target.

The tricky part is understanding how values propagate through the sequence. The operation does not freely rearrange elements. Only one specific value, the current `k`-th element, survives and gets duplicated. Every other value slowly shifts toward the front and eventually disappears.

Several edge cases are easy to misunderstand.

Consider:

```
3 2
3 1 1
```

The answer is `1`. After one operation, the `2`-nd element is `1`, so we append `1` and remove `3`. The array becomes `[1,1,1]`.

Now consider:

```
3 2
1 3 1
```

The answer is `-1`. The suffix after position `k` is not uniform, and the value `3` can never disappear because it eventually becomes the duplicated value itself.

Another subtle case is when the array is already uniform:

```
5 3
7 7 7 7 7
```

The correct answer is `0`. A careless implementation might still count removals from the front and return a positive number.

The smallest input also matters:

```
1 1
42
```

The answer is `0`, since the sequence already consists of one repeated value.

## Approaches

A brute-force simulation is straightforward. At each step, we append the current `k`-th element and delete the first element. We continue until either all values become equal or we detect a cycle.

This works because the operation is deterministic. The problem is performance. Each operation may require checking whether all elements are equal, which costs `O(n)`, and shifting arrays also costs `O(n)` in a naive implementation. Since we may perform up to `n` operations before understanding the behavior, the total complexity can grow to `O(n^2)`.

The key observation is that only the suffix starting from position `k` really matters.

Suppose the final uniform value is `x`. Once an element reaches the `k`-th position, it starts getting copied forever. That means every element from index `k` onward must already equal `x`. Otherwise, a different value will eventually be duplicated, preventing the array from becoming uniform.

This completely changes the problem. Instead of simulating operations, we only need to check whether all elements from position `k` to the end are equal.

If they are not equal, the answer is immediately `-1`.

If they are equal to some value `x`, then every operation removes one element from the front. Eventually, all elements before position `k` that are not equal to `x` disappear. The minimum number of operations is exactly the count of prefix elements before `k` that differ from `x`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array and identify the target value as `a[k-1]`, using zero-based indexing.
2. Check every element from index `k-1` to `n-1`.
3. If any of these elements differs from the target value, print `-1` and stop.

This is correct because every one of these elements will eventually occupy the `k`-th position and become duplicated forever. If even one value differs, the sequence can never become uniform.
4. Otherwise, scan the prefix from index `0` to `k-2`.
5. Count how many elements in this prefix differ from the target value.
6. Print that count.

Each operation removes exactly one element from the front. We only need to remove the prefix elements that are not already equal to the final value.

### Why it works

The invariant is that the suffix starting at position `k` controls all future duplicated values.

After each operation, elements shift left. Eventually, every element originally at or after position `k` becomes the current `k`-th element and gets copied to the end. If those elements are not all identical, multiple values will keep reappearing forever.

If the suffix is uniform with value `x`, then `x` is the only value that ever gets duplicated. Every operation removes one front element, so the only remaining task is deleting prefix elements different from `x`. The number of such elements is exactly the minimum operations required.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    target = a[k - 1]

    for i in range(k - 1, n):
        if a[i] != target:
            print(-1)
            return

    ans = 0

    for i in range(k - 1):
        if a[i] != target:
            ans += 1

    print(ans)

solve()
```

The solution begins by selecting `a[k - 1]` as the only possible final value. Since every future duplicated element comes from positions that eventually pass through the `k`-th position, the suffix must already consist entirely of this value.

The first loop validates this condition. If any suffix element differs, we immediately terminate with `-1`.

The second loop counts how many prefix elements are different from the target. Those are exactly the elements that must be removed through operations.

The indexing is the most common source of mistakes here. The problem statement uses one-based indexing, but Python uses zero-based indexing. The `k`-th element corresponds to index `k - 1`.

Another subtle detail is that elements already equal to the target in the prefix do not require removal. They naturally remain correct once the differing values disappear.

## Worked Examples

### Example 1

Input:

```
3 2
3 1 1
```

Target value is `a[1] = 1`.

| Index | Value | In suffix check? | Matches target? |
| --- | --- | --- | --- |
| 1 | 1 | Yes | Yes |
| 2 | 1 | Yes | Yes |

The suffix is valid.

Now count differing prefix elements.

| Index | Value | Different from 1? | Count |
| --- | --- | --- | --- |
| 0 | 3 | Yes | 1 |

Answer: `1`

This demonstrates that once the suffix is uniform, we only need to remove incorrect prefix values.

### Example 2

Input:

```
3 2
1 3 1
```

Target value is `a[1] = 3`.

| Index | Value | In suffix check? | Matches target? |
| --- | --- | --- | --- |
| 1 | 3 | Yes | Yes |
| 2 | 1 | Yes | No |

A mismatch appears in the suffix, so the answer is `-1`.

This example shows why the suffix condition is necessary. The value `1` will eventually become the duplicated element, so the sequence can never stabilize to a single value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass for suffix validation and one pass for prefix counting |
| Space | O(1) | Only a few extra variables are used |

A linear scan over `10^5` elements easily fits within the time limit. Memory usage is constant apart from the input array itself.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    target = a[k - 1]

    for i in range(k - 1, n):
        if a[i] != target:
            print(-1)
            return

    ans = 0

    for i in range(k - 1):
        if a[i] != target:
            ans += 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue()

# provided sample
assert run("3 2\n3 1 1\n") == "1\n", "sample 1"

# impossible case
assert run("3 2\n1 3 1\n") == "-1\n", "sample 2"

# already equal
assert run("5 3\n7 7 7 7 7\n") == "0\n", "already equal"

# minimum size
assert run("1 1\n42\n") == "0\n", "single element"

# prefix removals needed
assert run("6 4\n1 2 3 5 5 5\n") == "3\n", "remove three bad prefix values"

# off-by-one around k
assert run("4 1\n2 2 2 3\n") == "-1\n", "entire array must match when k=1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 3 / 7 7 7 7 7` | `0` | Already uniform arrays |
| `1 1 / 42` | `0` | Minimum input size |
| `6 4 / 1 2 3 5 5 5` | `3` | Counting incorrect prefix values |
| `4 1 / 2 2 2 3` | `-1` | Boundary case where suffix is entire array |

## Edge Cases

Consider:

```
5 3
7 7 7 7 7
```

The target value is `7`. Every element from index `2` onward matches it, so the suffix check passes. The prefix also contains only `7`, so the count remains `0`. The algorithm correctly prints `0` because no operations are needed.

Now consider:

```
4 1
2 2 2 3
```

Since `k = 1`, the suffix begins at the first element, meaning the entire array must already be uniform. The target is `2`, but the last element is `3`, so the suffix check fails immediately and the algorithm prints `-1`.

Finally, consider:

```
6 4
1 2 3 5 5 5
```

The target value is `5`. Every element from index `3` onward equals `5`, so reaching a uniform array is possible. The prefix contains `1`, `2`, and `3`, all different from `5`, so the answer is `3`.

After three operations, those elements disappear from the front, leaving only `5`s in the sequence.
