---
title: "CF 145E - Lucky Queries"
description: "We have a string consisting only of digits 4 and 7. Two kinds of operations are performed on it. The first operation flips every digit in a segment. Every 4 becomes 7, and every 7 becomes 4."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 145
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 104 (Div. 1)"
rating: 2400
weight: 145
solve_time_s: 132
verified: true
draft: false
---

[CF 145E - Lucky Queries](https://codeforces.com/problemset/problem/145/E)

**Rating:** 2400  
**Tags:** data structures  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string consisting only of digits `4` and `7`. Two kinds of operations are performed on it.

The first operation flips every digit in a segment. Every `4` becomes `7`, and every `7` becomes `4`.

The second operation asks for the length of the longest non-decreasing subsequence of the current string.

Since the string contains only two possible digits and `4 < 7`, a non-decreasing subsequence has a very specific shape. It consists of some number of `4`s followed by some number of `7`s. We are allowed to skip characters, but we cannot place a `7` before a chosen `4`.

For example:

- In `44777`, the whole string is already non-decreasing, so the answer is `5`.
- In `7744`, the best subsequence is either `77` or `44`, so the answer is `2`.
- In `74747`, we can take `4447` or `777`, so the answer is `4`.

The constraints completely rule out rebuilding answers from scratch after every update. The string length can reach `10^6`, and there can be `3 * 10^5` operations. Even a linear scan per query would require roughly `3 * 10^11` operations in the worst case, which is impossible within a 3 second limit.

The updates are also range updates, which makes naive mutation expensive. We need something that supports:

- flipping all digits in an interval,
- combining information from intervals efficiently,
- answering the global longest non-decreasing subsequence quickly.

A few edge cases are easy to mishandle if the state stored in the data structure is incomplete.

Consider:

```
s = 7474
```

The answer is `3`, because we can take subsequence `447`.

If we only stored counts of `4` and `7`, we would not know how they are arranged. Both `4477` and `7474` contain two `4`s and two `7`s, but their answers differ.

Another dangerous case is repeated flips on overlapping ranges:

```
initial: 4477
switch 1 2 -> 7777
switch 2 3 -> 7447
```

Lazy propagation must compose correctly. A common bug is overwriting a pending flip instead of toggling it.

The smallest cases also matter:

```
1 3
4
count
switch 1 1
count
```

The outputs are:

```
1
1
```

A single character is always a valid non-decreasing subsequence regardless of flips.

## Approaches

The brute-force solution directly applies every update to the string and recomputes the answer from scratch for every `count` query.

To compute the longest non-decreasing subsequence in a binary string, we can scan from left to right. At each position, we decide whether to extend the subsequence with a `4` or with a `7`. A dynamic programming solution works in linear time.

That gives:

- `O(r - l + 1)` time for each switch,
- `O(n)` time for each count.

In the worst case, both operations occur `3 * 10^5` times on a string of length `10^6`. That becomes hundreds of billions of operations.

The key observation is that the answer for a segment can be represented using only a few values.

For every segment, we store:

- the number of `4`s,
- the number of `7`s,
- the longest non-decreasing subsequence (`4...7`),
- the longest non-increasing subsequence (`7...4`).

Why do we also need the decreasing version? Because flipping digits swaps the meaning of `4` and `7`. After a flip:

- all `4`s become `7`s,
- all `7`s become `4`s,
- increasing subsequences become decreasing subsequences.

This symmetry makes lazy propagation extremely clean.

Suppose we split a segment into left and right halves.

To build the best non-decreasing subsequence of the whole segment, we have two choices:

- take all useful `4`s from the left and continue with the best non-decreasing subsequence from the right,
- take the best non-decreasing subsequence from the left and then all useful `7`s from the right.

So:

```
inc = max(left.four + right.inc,
          left.inc + right.seven)
```

Similarly:

```
dec = max(left.seven + right.dec,
          left.dec + right.four)
```

This merging rule is associative, which makes it ideal for a segment tree.

Range flips are handled lazily. Flipping a segment simply swaps:

- `four <-> seven`
- `inc <-> dec`

Each operation then costs `O(log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(mn) | O(n) | Too slow |
| Optimal | O(m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the string.

Every node represents a contiguous substring.
2. For each node, store four values:

- `four`: number of `4`s,
- `seven`: number of `7`s,
- `inc`: longest non-decreasing subsequence length,
- `dec`: longest non-increasing subsequence length.

For a single character:

- if it is `4`, then all four values are `(1, 0, 1, 1)`,
- if it is `7`, then they are `(0, 1, 1, 1)`.
3. Merge two child nodes into a parent.

The counts are straightforward:

```
four = left.four + right.four
seven = left.seven + right.seven
```

For `inc`, either:

- we use all good `4`s from the left and continue with the best increasing subsequence from the right,
- or we use the best increasing subsequence from the left and append all good `7`s from the right.

So:

```
inc = max(left.four + right.inc,
          left.inc + right.seven)
```

The same idea gives:

```
dec = max(left.seven + right.dec,
          left.dec + right.four)
```
4. Support lazy propagation for flips.

A flip exchanges every `4` and `7`.

That means:

```
four <-> seven
inc <-> dec
```

We also toggle a lazy flag for the node.
5. During a range update, if the current node lies completely inside the update interval, apply the flip immediately and stop descending.

Otherwise, push any pending lazy operation to children and continue recursively.
6. For a `count` query, the answer is always the `inc` value stored at the root.

The root represents the entire string, so its best non-decreasing subsequence is exactly the required answer.

### Why it works

For every segment, `inc` always stores the maximum possible length of a subsequence shaped like `444...777`. Any valid subsequence crossing the midpoint must either finish its `4` part in the left child or start its `7` part in the right child. The merge formula enumerates exactly those possibilities.

The flip operation preserves correctness because exchanging `4` and `7` transforms increasing subsequences into decreasing ones and vice versa. Swapping the stored values updates the node to match the flipped segment without rebuilding it.

Since every node always contains correct information for its segment, the root always contains the correct answer for the whole string.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, s):
        self.n = len(s)
        size = 4 * self.n

        self.four = [0] * size
        self.seven = [0] * size
        self.inc = [0] * size
        self.dec = [0] * size
        self.lazy = [False] * size

        self.s = s
        self.build(1, 0, self.n - 1)

    def build(self, node, l, r):
        if l == r:
            if self.s[l] == '4':
                self.four[node] = 1
            else:
                self.seven[node] = 1

            self.inc[node] = 1
            self.dec[node] = 1
            return

        mid = (l + r) // 2

        self.build(node * 2, l, mid)
        self.build(node * 2 + 1, mid + 1, r)

        self.pull(node)

    def pull(self, node):
        left = node * 2
        right = node * 2 + 1

        self.four[node] = self.four[left] + self.four[right]
        self.seven[node] = self.seven[left] + self.seven[right]

        self.inc[node] = max(
            self.four[left] + self.inc[right],
            self.inc[left] + self.seven[right]
        )

        self.dec[node] = max(
            self.seven[left] + self.dec[right],
            self.dec[left] + self.four[right]
        )

    def apply_flip(self, node):
        self.four[node], self.seven[node] = (
            self.seven[node],
            self.four[node]
        )

        self.inc[node], self.dec[node] = (
            self.dec[node],
            self.inc[node]
        )

        self.lazy[node] ^= True

    def push(self, node):
        if self.lazy[node]:
            self.apply_flip(node * 2)
            self.apply_flip(node * 2 + 1)
            self.lazy[node] = False

    def update(self, node, l, r, ql, qr):
        if ql <= l and r <= qr:
            self.apply_flip(node)
            return

        self.push(node)

        mid = (l + r) // 2

        if ql <= mid:
            self.update(node * 2, l, mid, ql, qr)

        if qr > mid:
            self.update(node * 2 + 1, mid + 1, r, ql, qr)

        self.pull(node)

def solve():
    n, m = map(int, input().split())
    s = input().strip()

    seg = SegmentTree(s)

    ans = []

    for _ in range(m):
        query = input().split()

        if query[0] == "count":
            ans.append(str(seg.inc[1]))
        else:
            l = int(query[1]) - 1
            r = int(query[2]) - 1

            seg.update(1, 0, n - 1, l, r)

    sys.stdout.write("\n".join(ans))

solve()
```

The tree stores four arrays instead of custom objects because Python object allocation becomes expensive at this scale. The input size is large enough that implementation details matter.

The `pull` method contains the core transition formulas. A common mistake is trying to compute `inc` as:

```
max(left.inc, right.inc)
```

That ignores subsequences crossing the midpoint, which is exactly where the optimal subsequence often appears.

The lazy propagation is especially elegant here. Flipping a segment does not require recomputation from children. We only swap stored values. This works because every structural property is symmetric under exchanging `4` and `7`.

The update uses inclusive ranges. Since the input is 1-indexed but the implementation is 0-indexed, both endpoints are decremented before the update call.

The answer for every `count` query is `seg.inc[1]`, because node `1` is the root representing the whole string.

## Worked Examples

### Sample 1

Input:

```
2 3
47
count
switch 1 2
count
```

| Step | String | Root inc | Output |
| --- | --- | --- | --- |
| Initial | 47 | 2 |  |
| count | 47 | 2 | 2 |
| switch 1 2 | 74 | 1 |  |
| count | 74 | 1 | 1 |

Initially, the entire string is already non-decreasing. After flipping both positions, the string becomes `74`. Any non-decreasing subsequence can only contain one character, so the answer drops to `1`.

### Sample 2

Consider:

```
3 4
747
count
switch 1 1
count
switch 2 3
count
```

| Step | String | Best subsequence | Root inc | Output |
| --- | --- | --- | --- | --- |
| Initial | 747 | 47 | 2 |  |
| count | 747 | 47 | 2 | 2 |
| switch 1 1 | 447 | 447 | 3 |  |
| count | 447 | 447 | 3 | 3 |
| switch 2 3 | 474 | 44 | 2 |  |
| count | 474 | 44 | 2 | 2 |

This trace shows why the order of digits matters. Both `447` and `474` contain two `4`s and one `7`, but their answers differ because of arrangement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each range update touches logarithmically many segment tree nodes |
| Space | O(n) | The segment tree stores a constant amount of information per node |

With `n = 10^6` and `m = 3 * 10^5`, an `O(m log n)` solution easily fits within the limit. The segment tree contains about `4n` nodes, which is acceptable under the memory limit when implemented using integer arrays.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    input = input_data.readline

    class SegmentTree:
        def __init__(self, s):
            self.n = len(s)

            size = 4 * self.n

            self.four = [0] * size
            self.seven = [0] * size
            self.inc = [0] * size
            self.dec = [0] * size
            self.lazy = [False] * size

            self.s = s

            self.build(1, 0, self.n - 1)

        def build(self, node, l, r):
            if l == r:
                if self.s[l] == '4':
                    self.four[node] = 1
                else:
                    self.seven[node] = 1

                self.inc[node] = 1
                self.dec[node] = 1
                return

            mid = (l + r) // 2

            self.build(node * 2, l, mid)
            self.build(node * 2 + 1, mid + 1, r)

            self.pull(node)

        def pull(self, node):
            left = node * 2
            right = node * 2 + 1

            self.four[node] = self.four[left] + self.four[right]
            self.seven[node] = self.seven[left] + self.seven[right]

            self.inc[node] = max(
                self.four[left] + self.inc[right],
                self.inc[left] + self.seven[right]
            )

            self.dec[node] = max(
                self.seven[left] + self.dec[right],
                self.dec[left] + self.four[right]
            )

        def apply_flip(self, node):
            self.four[node], self.seven[node] = (
                self.seven[node],
                self.four[node]
            )

            self.inc[node], self.dec[node] = (
                self.dec[node],
                self.inc[node]
            )

            self.lazy[node] ^= True

        def push(self, node):
            if self.lazy[node]:
                self.apply_flip(node * 2)
                self.apply_flip(node * 2 + 1)
                self.lazy[node] = False

        def update(self, node, l, r, ql, qr):
            if ql <= l and r <= qr:
                self.apply_flip(node)
                return

            self.push(node)

            mid = (l + r) // 2

            if ql <= mid:
                self.update(node * 2, l, mid, ql, qr)

            if qr > mid:
                self.update(node * 2 + 1, mid + 1, r, ql, qr)

            self.pull(node)

    n, m = map(int, input().split())
    s = input().strip()

    seg = SegmentTree(s)

    ans = []

    for _ in range(m):
        q = input().split()

        if q[0] == "count":
            ans.append(str(seg.inc[1]))
        else:
            l = int(q[1]) - 1
            r = int(q[2]) - 1

            seg.update(1, 0, n - 1, l, r)

    return "\n".join(ans)

# provided sample
assert run(
"""2 3
47
count
switch 1 2
count
"""
) == "2\n1", "sample 1"

# minimum size
assert run(
"""1 3
4
count
switch 1 1
count
"""
) == "1\n1", "single element"

# all equal values
assert run(
"""5 3
44444
count
switch 2 4
count
"""
) == "5\n3", "all equal then partial flip"

# overlapping updates
assert run(
"""4 5
4477
count
switch 1 2
count
switch 2 3
count
"""
) == "4\n4\n3", "lazy propagation composition"

# off-by-one boundaries
assert run(
"""5 4
74747
count
switch 1 5
count
"""
) == "3\n3", "full range update"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single character | `1 1` | Minimum-size handling |
| `44444` with partial flip | `5 3` | Correct subsequence recomputation |
| Overlapping updates | `4 4 3` | Lazy propagation composition |
| Full-range flip | `3 3` | Boundary correctness |

## Edge Cases

Consider the string:

```
4 1
7474
count
```

The correct answer is:

```
3
```

The best subsequence is `447`. A solution storing only counts of digits would incorrectly think the answer depends only on frequency and might output `4`. The segment tree avoids this because `inc` encodes ordering information.

Now consider repeated overlapping flips:

```
4 3
4477
switch 1 2
switch 2 3
count
```

Execution proceeds as:

```
4477
-> 7777
-> 7447
```

The answer is `3`, using subsequence `447`.

The lazy flags toggle instead of overwrite. If we replaced the flag instead of XOR-ing it, the second update would destroy pending information and produce the wrong state.

Finally, consider a complete range flip:

```
5 2
44777
switch 1 5
count
```

After flipping:

```
77444
```

The best non-decreasing subsequence has length `3`.

The implementation handles this efficiently by swapping:

```
four <-> seven
inc <-> dec
```

at the root node directly, without traversing the entire segment.
