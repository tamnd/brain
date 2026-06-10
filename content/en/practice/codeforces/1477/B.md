---
title: "CF 1477B - Nezzar and Binary String"
description: "We start with a binary string that must eventually become another binary string after a sequence of operations. Each day, a fixed segment is inspected. If that segment contains both 0 and 1, the process immediately fails."
date: "2026-06-10T23:53:23+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1477
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 698 (Div. 1)"
rating: 1900
weight: 1477
solve_time_s: 145
verified: true
draft: false
---

[CF 1477B - Nezzar and Binary String](https://codeforces.com/problemset/problem/1477/B)

**Rating:** 1900  
**Tags:** data structures, greedy  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a binary string that must eventually become another binary string after a sequence of operations.

Each day, a fixed segment is inspected. If that segment contains both `0` and `1`, the process immediately fails. That means that before every inspection, the inspected segment must be entirely `0`s or entirely `1`s.

After the inspection, during the night, we are allowed to modify fewer than half of the characters inside that same segment.

The input gives the original string `s`, the desired final string `f`, and the sequence of inspected segments. We must determine whether there exists some sequence of valid nightly modifications that transforms `s` into `f` while keeping every inspected segment uniform at the moment it is checked.

The constraints are the first thing that suggests the intended direction. Across all test cases, the total string length and total number of queries are both at most `2 · 10^5`. A solution that touches every position of a segment for every query would require roughly `O(nq)` operations, which can reach about `4 · 10^10` in the worst case. That is completely infeasible. We need something around `O((n+q) log n)`.

The most subtle aspect of the problem is that the operations are described forward in time, but the final string is already known. Forward simulation is difficult because at each night there may be many possible ways to modify the segment.

Several edge cases cause incorrect reasoning if we are not careful.

Consider a segment whose length is even and currently contains exactly half zeros and half ones.

```
length = 4
segment = 0011
```

To make the segment uniform, we would need to change exactly two characters. The rules only allow changing strictly less than half of the segment, so changing two characters is forbidden. Any solution that treats "at most half" as valid would incorrectly accept such cases.

Another dangerous case is a segment that already has a strict majority.

```
segment = 0001
```

Since fewer than half the positions may be changed, the only possible uniform state before the previous day is all zeros. Turning it into all ones would require changing three positions, which exceeds the limit. A careless implementation that allows either uniform value would be wrong.

Finally, when there are no queries at all, no transformations are possible.

```
n = 3, q = 0
s = 101
f = 111
```

The answer is `NO` because the string never changes. Any algorithm must explicitly verify that the reconstructed initial state equals `s`.

## Approaches

A brute force approach would try to simulate the process. Starting from `s`, for each query we would determine whether the inspected segment is uniform, then consider possible nightly modifications. The difficulty is that many different intermediate strings may be reachable. Exploring all possibilities quickly becomes exponential.

Even if we somehow avoided branching and only tracked one state, updating a whole segment for every query would cost `O(nq)` time. With both values reaching `2 · 10^5`, that is far beyond the limit.

The key observation is that the final string `f` is known. Instead of asking how we can reach `f`, we ask whether `f` could have arisen from a valid sequence of operations.

Suppose we are looking at a query segment `[l,r]` and we know the string immediately after that night's modification. What could the segment have looked like immediately before the modification?

Let the segment length be `len`, and let it currently contain `ones` ones.

Before the night operation, the segment must have been completely uniform, because it had just passed inspection.

If the uniform value was `0`, then the night operation changed exactly `ones` positions.

If the uniform value was `1`, then the night operation changed exactly `len - ones` positions.

Because fewer than half the positions may be changed, only one of these possibilities can be valid.

If `ones < len/2`, then the segment must previously have been all zeros.

If `ones > len/2`, then the segment must previously have been all ones.

If `ones = len/2`, neither possibility works, because both require changing exactly half the positions.

This completely removes the ambiguity.

Starting from `f`, we process the queries in reverse order. For each segment, we count how many ones it currently contains.

If the count is exactly half the segment length, reconstruction is impossible.

Otherwise, we overwrite the entire segment with the forced majority value and continue.

After reversing all queries, we obtain the only possible candidate for the original string. If it matches `s`, the answer is `YES`; otherwise `NO`.

The remaining challenge is supporting range count queries and range assignment updates efficiently. This is a classic lazy-propagation segment tree problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) or worse | O(n) | Too slow |
| Optimal | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree from the final string `f`.

Each node stores the number of ones in its interval.
2. Process the queries in reverse order.

Reversing transforms the problem from "many possible future states" into "at most one possible previous state".
3. For the current segment `[l,r]`, query the number of ones inside it.

Let `len = r - l + 1`.
4. If `2 * ones == len`, immediately return `NO`.

A previous uniform segment cannot produce a state with exactly half ones and half zeros while changing strictly less than half of the positions.
5. If `2 * ones < len`, assign the entire segment to zero.

The segment must have been all zeros before this operation.
6. Otherwise assign the entire segment to one.

The segment must have been all ones before this operation.
7. Continue until all reversed queries have been processed.
8. After reconstruction finishes, compare every position with the original string `s`.

If any position differs, return `NO`.
9. If the reconstructed string matches `s`, return `YES`.

### Why it works

The crucial invariant is that while processing queries in reverse, the segment tree always represents the unique state of the string immediately after the corresponding forward-time operation.

Consider a reversed query segment. Let its current number of ones be `ones`.

If `ones < len/2`, obtaining this state from an all-one segment would require changing more than half the positions. The only valid predecessor is an all-zero segment.

If `ones > len/2`, the symmetric argument shows that the only valid predecessor is an all-one segment.

If `ones = len/2`, both candidate predecessors require changing exactly half the positions, which is forbidden.

Thus every reverse step is either uniquely determined or impossible. The algorithm reconstructs exactly the set of states that could exist in a valid forward process. If reconstruction reaches a string different from `s`, then no valid sequence starts from `s`. If reconstruction reaches `s`, replaying the reverse reasoning forward yields a valid sequence of operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [-1] * (4 * self.n)
        self._build(1, 0, self.n - 1, arr)

    def _build(self, node, l, r, arr):
        if l == r:
            self.tree[node] = arr[l]
            return

        mid = (l + r) // 2
        self._build(node * 2, l, mid, arr)
        self._build(node * 2 + 1, mid + 1, r, arr)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def _apply(self, node, l, r, val):
        self.tree[node] = (r - l + 1) * val
        self.lazy[node] = val

    def _push(self, node, l, r):
        if self.lazy[node] == -1 or l == r:
            return

        mid = (l + r) // 2
        val = self.lazy[node]

        self._apply(node * 2, l, mid, val)
        self._apply(node * 2 + 1, mid + 1, r, val)

        self.lazy[node] = -1

    def update(self, ql, qr, val):
        self._update(1, 0, self.n - 1, ql, qr, val)

    def _update(self, node, l, r, ql, qr, val):
        if qr < l or r < ql:
            return

        if ql <= l and r <= qr:
            self._apply(node, l, r, val)
            return

        self._push(node, l, r)

        mid = (l + r) // 2
        self._update(node * 2, l, mid, ql, qr, val)
        self._update(node * 2 + 1, mid + 1, r, ql, qr, val)

        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def query(self, ql, qr):
        return self._query(1, 0, self.n - 1, ql, qr)

    def _query(self, node, l, r, ql, qr):
        if qr < l or r < ql:
            return 0

        if ql <= l and r <= qr:
            return self.tree[node]

        self._push(node, l, r)

        mid = (l + r) // 2
        return (
            self._query(node * 2, l, mid, ql, qr) +
            self._query(node * 2 + 1, mid + 1, r, ql, qr)
        )

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, q = map(int, input().split())
        s = input().strip()
        f = input().strip()

        queries = []
        for _ in range(q):
            l, r = map(int, input().split())
            queries.append((l - 1, r - 1))

        st = SegmentTree([int(c) for c in f])

        ok = True

        for l, r in reversed(queries):
            ones = st.query(l, r)
            length = r - l + 1

            if ones * 2 == length:
                ok = False
                break

            if ones * 2 < length:
                st.update(l, r, 0)
            else:
                st.update(l, r, 1)

        if not ok:
            ans.append("NO")
            continue

        for i in range(n):
            if st.query(i, i) != int(s[i]):
                ok = False
                break

        ans.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The segment tree stores only one piece of information, the number of ones in each interval. That is exactly what the reverse process needs to decide the predecessor state.

Lazy propagation is essential because each reverse step overwrites an entire segment with all zeros or all ones. Without lazy propagation, a single update could cost linear time.

The comparison against `s` is performed only after all reverse operations have been applied. At that point the segment tree represents the reconstructed initial string.

The equality test uses `ones * 2 == length` instead of floating-point division. This avoids precision issues and directly expresses the strict-half condition from the statement.

## Worked Examples

### Example 1

```
n = 5
s = 00000
f = 00111

queries:
[1,5]
[1,3]
```

Reverse order is `[1,3]`, then `[1,5]`.

| Step | Segment | Ones | Length | Action | State |
| --- | --- | --- | --- | --- | --- |
| Start | - | - | - | Initial `f` | 00111 |
| 1 | [1,3] | 1 | 3 | Majority 0, fill 0 | 00011 |
| 2 | [1,5] | 2 | 5 | Majority 0, fill 0 | 00000 |

Final reconstructed string is `00000`, which equals `s`.

Answer: `YES`.

This trace shows the central idea of reverse reconstruction. Each segment has a strict majority, so the predecessor is uniquely determined.

### Example 2

```
n = 2
s = 00
f = 01

query:
[1,2]
```

Reverse processing:

| Step | Segment | Ones | Length | Action |
| --- | --- | --- | --- | --- |
| Start | - | - | - | State = 01 |
| 1 | [1,2] | 1 | 2 | Impossible |

The segment contains exactly one zero and one one. Reaching such a state from a uniform segment would require changing exactly half of the positions.

Answer: `NO`.

This example demonstrates the most important rejection condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each query performs one range query and one range assignment |
| Space | O(n) | Segment tree and lazy arrays |

The total values of `n` and `q` across all test cases are at most `2 · 10^5`. With logarithmic operations on the segment tree, the total work is comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    from io import StringIO
    sys.stdin = StringIO(inp)
    out = StringIO()

    input = sys.stdin.readline

    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [0] * (4 * self.n)
            self.lazy = [-1] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr)

        def build(self, node, l, r, arr):
            if l == r:
                self.tree[node] = arr[l]
                return
            m = (l + r) // 2
            self.build(node * 2, l, m, arr)
            self.build(node * 2 + 1, m + 1, r, arr)
            self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

        def apply(self, node, l, r, v):
            self.tree[node] = (r - l + 1) * v
            self.lazy[node] = v

        def push(self, node, l, r):
            if self.lazy[node] == -1 or l == r:
                return
            m = (l + r) // 2
            v = self.lazy[node]
            self.apply(node * 2, l, m, v)
            self.apply(node * 2 + 1, m + 1, r, v)
            self.lazy[node] = -1

        def update(self, node, l, r, ql, qr, v):
            if qr < l or r < ql:
                return
            if ql <= l and r <= qr:
                self.apply(node, l, r, v)
                return
            self.push(node, l, r)
            m = (l + r) // 2
            self.update(node * 2, l, m, ql, qr, v)
            self.update(node * 2 + 1, m + 1, r, ql, qr, v)
            self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

        def query(self, node, l, r, ql, qr):
            if qr < l or r < ql:
                return 0
            if ql <= l and r <= qr:
                return self.tree[node]
            self.push(node, l, r)
            m = (l + r) // 2
            return (
                self.query(node * 2, l, m, ql, qr)
                + self.query(node * 2 + 1, m + 1, r, ql, qr)
            )

    t = int(input())
    ans = []

    for _ in range(t):
        n, q = map(int, input().split())
        s = input().strip()
        f = input().strip()

        qs = []
        for _ in range(q):
            l, r = map(int, input().split())
            qs.append((l - 1, r - 1))

        st = SegmentTree([int(c) for c in f])

        ok = True

        for l, r in reversed(qs):
            ones = st.query(1, 0, n - 1, l, r)
            ln = r - l + 1

            if ones * 2 == ln:
                ok = False
                break

            st.update(1, 0, n - 1, l, r, 1 if ones * 2 > ln else 0)

        if ok:
            for i in range(n):
                if st.query(1, 0, n - 1, i, i) != int(s[i]):
                    ok = False
                    break

        ans.append("YES" if ok else "NO")

    return "\n".join(ans)

assert run("""1
1 0
0
0
""") == "YES"

assert run("""1
1 0
0
1
""") == "NO"

assert run("""1
2 1
00
01
1 2
""") == "NO"

assert run("""1
5 2
00000
00111
1 5
1 3
""") == "YES"

assert run("""1
5 1
11111
11111
1 5
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, q=0, s=f` | YES | Minimum instance |
| `n=1, q=0, s≠f` | NO | No operations available |
| `00 → 01` with segment length 2 | NO | Exact-half impossibility |
| First sample case | YES | Successful reverse reconstruction |
| All ones with redundant query | YES | Uniform segments remain valid |

## Edge Cases

Consider:

```
1
2 1
00
01
1 2
```

The segment length is `2` and contains exactly one `1`. During reverse processing we obtain `ones = 1`, `length = 2`, so `2 * ones = length`. The algorithm immediately rejects. This matches the rules because changing exactly one position out of two is not strictly less than half.

Consider:

```
1
4 1
0000
0001
1 4
```

The segment contains one `1` and three `0`s. Reverse processing sees a strict zero majority and reconstructs the predecessor as `0000`. The final reconstructed string equals `s`, so the answer is `YES`. The algorithm correctly identifies the only possible predecessor.

Consider:

```
1
3 0
101
111
```

There are no queries. The reverse phase performs no work. The reconstructed string remains `111`, which does not equal the original string `101`. The algorithm returns `NO`, correctly recognizing that no modifications can occur.

Consider:

```
1
3 0
101
101
```

Again there are no queries, but now the reconstructed string already matches `s`. The algorithm returns `YES`, which is exactly the intended behavior when no changes are needed.
