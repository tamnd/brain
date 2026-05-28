---
title: "CF 4D - Mysterious Present"
description: "We are given a collection of envelopes, each with a width and height. A postcard already has fixed dimensions, and we want to build the longest possible nesting chain of envelopes such that:"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 4
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 4 (Div. 2 Only)"
rating: 1700
weight: 4
solve_time_s: 77
verified: true
draft: false
---
[CF 4D - Mysterious Present](https://codeforces.com/problemset/problem/4/D)

**Rating:** 1700  
**Tags:** dp, sortings  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of envelopes, each with a width and height. A postcard already has fixed dimensions, and we want to build the longest possible nesting chain of envelopes such that:

- the postcard fits into the first envelope,
- every next envelope is strictly larger in both width and height than the previous one.

Rotation is forbidden, so width must compare with width and height with height directly.

The output is not only the maximum chain length, but also one valid sequence of envelope indices in increasing nesting order.

The constraint that matters most is `n ≤ 5000`. A brute-force search over all subsets or all permutations is impossible because even `2^5000` or `5000!` is astronomically large. On the other hand, quadratic dynamic programming with about `5000^2 = 25,000,000` comparisons is completely realistic in C++ and still acceptable in Python with careful implementation.

The problem is essentially asking for the longest sequence where both dimensions increase strictly. That immediately suggests a longest increasing subsequence style dynamic programming solution after sorting.

Several edge cases can quietly break incorrect implementations.

Suppose multiple envelopes have the same dimensions.

Input:

```
3 1 1
2 2
2 2
3 3
```

Correct output:

```
2
1 3
```

The two `(2,2)` envelopes cannot both appear in the chain because the increase must be strict in both dimensions. A careless LIS implementation using `>=` instead of `>` would incorrectly allow them.

Another tricky case happens when an envelope fits only in one dimension.

Input:

```
3 2 2
3 2
2 3
4 4
```

Correct output:

```
1
3
```

Neither `(3,2)` nor `(2,3)` can hold the postcard because both dimensions must be strictly larger. Only `(4,4)` works. Filtering only by area or by one dimension would fail here.

A third edge case appears when no envelope can hold the postcard.

Input:

```
2 5 5
5 6
6 5
```

Correct output:

```
0
```

Strict inequality matters again. Equal width or equal height is not enough.

## Approaches

The brute-force idea is straightforward. We could try every subset of envelopes, then check whether the envelopes in that subset can be ordered into a valid chain. This works because the definition of a valid chain is easy to verify: every consecutive pair must strictly increase in both dimensions.

The problem is the number of subsets. With `n = 5000`, even iterating through all subsets is impossible. A recursive search that tries every possible continuation also explodes exponentially because each envelope can branch into many larger envelopes.

The structure of the problem gives a much cleaner path. If envelope `A` can go before envelope `B`, then `B` must be strictly larger in both dimensions. After sorting the envelopes, we can think of this as a directed acyclic graph where edges always move toward larger envelopes. Once the graph becomes acyclic, longest path dynamic programming becomes natural.

Sorting is the key observation. After sorting by width and height, any valid chain must move forward in the sorted order. Then we only need to compute:

`dp[i] = longest valid chain ending at envelope i`

For every earlier envelope `j`, if both dimensions of `j` are smaller than those of `i`, then `i` can extend the chain ending at `j`.

This turns the problem into a classic `O(n^2)` dynamic programming solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal DP with Sorting | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all envelopes and keep their original indices.

We must print indices from the original input order, so each envelope should store `(width, height, original_index)`.
2. Remove envelopes that cannot contain the postcard.

An envelope is usable only if:

```
width > postcard_width
height > postcard_height
```

Any envelope failing this condition can never appear in a valid chain.
3. Sort the remaining envelopes by width, then by height.

This guarantees that whenever we move from left to right, widths never decrease. It reduces the search space because valid transitions only need to consider earlier envelopes.
4. Initialize dynamic programming arrays.

Let:

```
dp[i] = length of longest chain ending at i
parent[i] = previous envelope index in that chain
```

Initially every envelope forms a chain of length `1`.
5. For every envelope `i`, check all earlier envelopes `j`.

If:

```
width[j] < width[i]
height[j] < height[i]
```

then envelope `i` can extend the chain ending at `j`.

Update:

```
dp[i] = dp[j] + 1
parent[i] = j
```

whenever this gives a longer chain.
6. Find the envelope with maximum `dp[i]`.

This is the end of the optimal chain.
7. Reconstruct the chain using the `parent` array.

Start from the best endpoint and repeatedly follow parents backward until `-1`.
8. Reverse the reconstructed sequence and print it.

Reconstruction happens backward, from largest envelope to smallest.

### Why it works

After sorting, every valid chain appears in increasing index order because widths and heights must both increase strictly. The DP transition considers every possible previous envelope that could legally precede the current one. Since `dp[j]` already stores the best chain ending at `j`, extending it with `i` gives the best chain ending at `i`.

The recurrence explores every valid predecessor exactly once, so no possible chain is missed. The maximum over all `dp[i]` values is the longest valid nesting chain.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, w, h = map(int, input().split())

    envelopes = []

    for i in range(1, n + 1):
        x, y = map(int, input().split())

        if x > w and y > h:
            envelopes.append((x, y, i))

    if not envelopes:
        print(0)
        return

    envelopes.sort()

    m = len(envelopes)

    dp = [1] * m
    parent = [-1] * m

    best_len = 1
    best_idx = 0

    for i in range(m):
        wi, hi, _ = envelopes[i]

        for j in range(i):
            wj, hj, _ = envelopes[j]

            if wj < wi and hj < hi:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j

        if dp[i] > best_len:
            best_len = dp[i]
            best_idx = i

    path = []

    cur = best_idx

    while cur != -1:
        path.append(envelopes[cur][2])
        cur = parent[cur]

    path.reverse()

    print(best_len)
    print(*path)

solve()
```

The first part filters unusable envelopes immediately. This simplifies the DP because every remaining envelope is guaranteed to fit the postcard.

Sorting uses Python's default tuple ordering, so envelopes are ordered by width first, then height. Since transitions still require strict comparison on both dimensions, equal widths or equal heights never create invalid chains.

The DP loop checks every earlier envelope as a possible predecessor. With `5000` envelopes, the worst-case number of comparisons is about twenty-five million, which is acceptable in Python when implemented iteratively.

The `parent` array is critical for reconstruction. Without it, we could compute the maximum chain length but would not know which envelopes formed that chain.

One subtle detail is using strict inequalities:

```
wj < wi and hj < hi
```

Replacing them with `<=` would incorrectly allow equal dimensions into the chain.

Another subtle point is filtering before sorting. If unusable envelopes remain, the DP might accidentally build chains starting from envelopes that cannot contain the postcard.

## Worked Examples

### Example 1

Input:

```
2 1 1
2 2
2 2
```

After filtering and sorting:

| i | Envelope | Original Index |
| --- | --- | --- |
| 0 | (2,2) | 1 |
| 1 | (2,2) | 2 |

DP progression:

| i | Envelope | Valid Previous | dp[i] | parent[i] |
| --- | --- | --- | --- | --- |
| 0 | (2,2) | none | 1 | -1 |
| 1 | (2,2) | none | 1 | -1 |

Best chain length is `1`.

One valid answer:

```
1
1
```

This example demonstrates why strict inequality matters. Even though the envelopes are identical, neither can contain the other.

### Example 2

Input:

```
5 1 1
2 3
3 4
4 5
3 3
5 6
```

Sorted envelopes:

| i | Envelope | Original Index |
| --- | --- | --- |
| 0 | (2,3) | 1 |
| 1 | (3,3) | 4 |
| 2 | (3,4) | 2 |
| 3 | (4,5) | 3 |
| 4 | (5,6) | 5 |

DP progression:

| i | Envelope | Best Previous | dp[i] | parent[i] |
| --- | --- | --- | --- | --- |
| 0 | (2,3) | none | 1 | -1 |
| 1 | (3,3) | none | 1 | -1 |
| 2 | (3,4) | (2,3) | 2 | 0 |
| 3 | (4,5) | (3,4) | 3 | 2 |
| 4 | (5,6) | (4,5) | 4 | 3 |

Reconstruction gives:

```
1 -> 2 -> 3 -> 5
```

This trace shows how equal widths prevent transitions. Envelope `(3,3)` cannot precede `(3,4)` because widths must increase strictly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Every envelope checks all earlier envelopes |
| Space | O(n) | DP and parent arrays store one value per envelope |

With `n ≤ 5000`, quadratic DP performs about twenty-five million comparisons in the worst case. That comfortably fits within the time limit in Python when implemented iteratively with fast input.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, w, h = map(int, input().split())

        envelopes = []

        for i in range(1, n + 1):
            x, y = map(int, input().split())

            if x > w and y > h:
                envelopes.append((x, y, i))

        if not envelopes:
            return "0"

        envelopes.sort()

        m = len(envelopes)

        dp = [1] * m
        parent = [-1] * m

        best_len = 1
        best_idx = 0

        for i in range(m):
            wi, hi, _ = envelopes[i]

            for j in range(i):
                wj, hj, _ = envelopes[j]

                if wj < wi and hj < hi:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        parent[i] = j

            if dp[i] > best_len:
                best_len = dp[i]
                best_idx = i

        path = []

        cur = best_idx

        while cur != -1:
            path.append(envelopes[cur][2])
            cur = parent[cur]

        path.reverse()

        return str(best_len) + "\n" + " ".join(map(str, path))

    return solve().strip()

# provided sample
assert run(
"""2 1 1
2 2
2 2
"""
) in ["1\n1", "1\n2"], "sample 1"

# no envelope fits
assert run(
"""2 5 5
5 6
6 5
"""
) == "0", "strict inequality"

# simple increasing chain
assert run(
"""3 1 1
2 2
3 3
4 4
"""
) == "3\n1 2 3", "basic chain"

# equal widths block transitions
assert run(
"""4 1 1
2 2
2 3
2 4
3 5
"""
) in ["2\n1 4", "2\n2 4", "2\n3 4"], "equal widths"

# single envelope
assert run(
"""1 1 1
2 2
"""
) == "1\n1", "minimum valid case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| No envelope fits | `0` | Strict inequality against postcard dimensions |
| Strictly increasing envelopes | Full chain length | Basic DP correctness |
| Equal widths | Chain cannot use equal widths | Correct transition condition |
| Single valid envelope | Length `1` | Minimum non-empty case |

## Edge Cases

Consider the case where envelopes share dimensions.

Input:

```
3 1 1
2 2
2 2
3 3
```

After sorting:

```
(2,2), (2,2), (3,3)
```

When processing the second `(2,2)`, the condition:

```
2 < 2
```

fails, so no transition occurs. Both copies remain chains of length `1`. Then `(3,3)` can extend either one, producing a final chain of length `2`.

Now consider envelopes that only partially exceed the postcard dimensions.

Input:

```
3 2 2
3 2
2 3
4 4
```

Filtering removes `(3,2)` because height is not strictly larger than `2`, and removes `(2,3)` because width is not strictly larger than `2`.

Only `(4,4)` remains, so the answer is:

```
1
3
```

Finally, consider the fully impossible case.

Input:

```
2 5 5
5 6
6 5
```

The first envelope fails because width is equal to the postcard width. The second fails because height is equal to the postcard height. The filtered list becomes empty immediately, and the algorithm prints:

```
0
```

This early filtering prevents invalid chains from ever entering the DP stage.
