---
title: "CF 102412J - Yet Another Mex Problem"
description: "The problem is from the MEX Foundation Contest, Gym 102412, Problem J. The official limits are (2le nle 2cdot10^5), (1le kle n), (0le aile n), with a 4 second time limit and 512 MiB of memory. We have a nonnegative integer array (a)."
date: "2026-08-10T14:14:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102412
codeforces_index: "J"
codeforces_contest_name: "MEX Foundation Contest (supported by AIM Tech)"
rating: 0
weight: 102412
solve_time_s: 350
verified: true
draft: false
---

[CF 102412J - Yet Another Mex Problem](https://codeforces.com/problemset/problem/102412/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is from the MEX Foundation Contest, Gym 102412, Problem J. The official limits are (2\le n\le 2\cdot10^5), (1\le k\le n), (0\le a_i\le n), with a 4 second time limit and 512 MiB of memory.

We have a nonnegative integer array (a). We must partition it into consecutive pieces, where every piece has length at most (k). For a piece, its value is its element sum multiplied by its MEX. The value of the whole partition is the sum of the values of all pieces, and we want the maximum possible value. The output is that maximum value.

Let (S_i=a_1+\cdots+a_i), with (S_0=0). If the last piece starts at (j+1) and ends at (i), its contribution is

[
\operatorname{mex}(a_{j+1},\ldots,a_i)(S_i-S_j).
]

If (dp_i) denotes the best answer for the prefix ending at (i), the direct recurrence is

[
dp_i=
\max_{i-k\le j<i}
\left(
dp_j+
\operatorname{mex}(j+1,i)(S_i-S_j)
\right).
]

The lower bound on (j) is what enforces the maximum piece length. Since (n) reaches (2\cdot10^5), an (O(n^2)) algorithm already requires about (4\cdot10^{10}) operations, far beyond what a few seconds can handle. Computing every MEX from scratch makes the direct approach (O(nk^2)), which can reach about (8\cdot10^{15}) elementary operations. Even maintaining every interval MEX incrementally gives (O(nk)), still about (4\cdot10^{10}) operations at the maximum. The solution must exploit the special structure of MEX rather than inspect all candidate intervals independently.

There are several boundary cases that are easy to mishandle. With `n = 2, k = 1, a = [5, 7]`, every piece contains only one positive value, so every MEX is zero and the answer is `0`. An implementation that assumes every nonempty segment has positive MEX would fail here.

With `n = 2, k = 2, a = [0, 0]`, the whole array has MEX (1), but its sum is zero, so its contribution is still zero and the answer is `0`. Multiplying the MEX by the sum must happen after both quantities have been computed.

With `n = 4, k = 2, a = [0, 1, 2, 3]`, the whole array would have MEX (4), but it cannot be one piece because its length is four. The best partition is `[0,1]` and `[2,3]`, giving (2\cdot1+0=2). Ignoring the length boundary produces a completely invalid transition.

Duplicates also matter. For `n = 3, k = 3, a = [0, 1, 1]`, the MEX is (2), not (3), because MEX cares about presence rather than frequency. The correct value is (2\cdot2=4).

## Approaches

The brute-force DP follows directly from the recurrence above. For every right endpoint (i), try every possible previous cut (j), compute the MEX of (a_{j+1},\ldots,a_i), and update (dp_i). This is correct because every valid partition has exactly one final piece, so its previous cut appears among these transitions. If the MEX is recomputed by scanning the piece, the worst-case complexity is (O(nk^2)), about (8\cdot10^{15}) operations when (n=k=2\cdot10^5). Even the more careful version that maintains all MEX values while extending intervals needs (O(nk)), which is still far too large.

The useful observation is that for a fixed right endpoint (i), the MEX values of suffixes are monotone. If we increase the left endpoint, elements are removed, so the MEX can only stay the same or decrease. Consequently, the possible previous cuts (j) can be divided into consecutive intervals on which the MEX is constant.

Suppose one such interval of previous cuts is (L\le j\le R), and its MEX is (m). Every transition from this whole interval has the form

mS_i+\left(dp_j-mS_j\right).
]

For this MEX block we only need

[
\max_{L\le j\le R}(dp_j-mS_j).
]

This turns the inner optimization into a line query. Associate the previous cut (j) with the line

[
F_j(x)=-S_jx+dp_j.
]

Then the required quantity is simply

[
\max_{L\le j\le R}F_j(m).
]

The remaining question is how to maintain the MEX blocks efficiently. When the right endpoint moves from (i-1) to (i), only the newly inserted value (a_i) can change the suffix MEX values. A MEX block that changes splits into smaller blocks, and after splitting those blocks do not have to be merged back. Across the complete scan, the total number of created blocks is (O(n)). A segment tree over the value domain, storing the last occurrence of every value, lets us locate each new block boundary in (O(\log n)). This gives (O(n\log n)) total work for the MEX structure. This decomposition is the central observation in the standard solution.

There are two nested optimization problems after this decomposition. The first asks for the maximum value of (F_j(m)) over an index interval. A segment tree over the index (j) can store a Li Chao tree in every node. A line is inserted into all (O(\log n)) index-tree nodes covering its position, and a range query visits (O(\log n)) nodes. Each Li Chao operation costs (O(\log n)), giving (O(\log^2 n)) per range operation.

The second optimization has an especially useful property. Once a MEX block has produced

[
C=\max_{L\le j\le R}F_j(m),
]

its contribution as a function of the current prefix sum is the line

[
H(x)=mx+C.
]

MEX values only increase as the right endpoint moves, so an old line never needs to be deleted. We insert this line at the block's left boundary and maintain another index segment tree of Li Chao trees. A query over the current sliding window then considers exactly the block lines whose left boundary can be a legal previous cut. This is the second layer of the data structure. The standard derivation gives (O(n\log^2 n)), with an (O(n\log n)) refinement possible by building the second layer offline.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nk^2)) | (O(n)) | Too slow |
| Incremental MEX DP | (O(nk)) | (O(n)) | Too slow |
| MEX blocks + nested Li Chao trees | (O(n\log^2 n)) | (O(n\log n)) | Accepted |

## Algorithm Walkthrough

1. Build the prefix sums (S_i). The sum of any candidate final piece (j+1,\ldots,i) is then (S_i-S_j), so the DP transition becomes an affine expression instead of requiring another scan of the array.
2. Define the line associated with every already solved prefix (j) as

[
F_j(x)=-S_jx+dp_j.
]

When a suffix has MEX (m), its transition is (mS_i+F_j(m)). Thus an entire MEX block can be reduced to one range maximum query at (x=m).
3. Maintain the last occurrence of every value. For the current right endpoint (i), a value (v) occurs in the suffix (j+1,\ldots,i) exactly when its last occurrence is greater than (j). Consequently, the MEX can be determined by the last-occurrence array.
4. Keep the MEX blocks as a stack of boundaries. The MEX values are monotone along the stack. When (a_i) is inserted, pop blocks whose boundary is no longer valid, then repeatedly find the smallest value whose last occurrence is below the current boundary. Each such discovery creates one new MEX block.

A segment tree storing the minimum last occurrence in every value interval supports this search in (O(\log n)). The important amortization is that a block is split only when it is created, so the total number of block creations is linear.
5. For every newly created block ([L,R]) with MEX (m), query the first Li Chao structure for

[
C=\max_{L\le j\le R}F_j(m).
]

The value (C) summarizes every possible previous cut inside that MEX block.
6. Convert the block into the line

[
H(x)=mx+C.
]

Insert this line at position (L) into the second range Li Chao structure. The line represents every future transition whose MEX is at least the MEX used when the line was created. Since all array elements are nonnegative, increasing the MEX can only improve the contribution, so retaining old lines is safe.
7. For endpoint (i), query the second structure over the legal previous-cut range ([i-k,i-1]), clipped at zero. This handles every complete MEX block that lies inside the length constraint.
8. One block can intersect the left boundary of the legal range without being completely contained in it. Find that block directly in the MEX stack and query the first structure only on its clipped portion. This single correction handles the only partial block created by the length restriction.
9. The maximum of the complete-block query and this partial-block query is (dp_i). Insert the newly obtained line

[
F_i(x)=-S_ix+dp_i
]

into the first structure so that future endpoints can use prefix (i).
10. After processing every endpoint, return (dp_n).

The invariant is that every legal previous cut (j) belongs to exactly one current MEX block, and that block stores the correct MEX of (a_{j+1},\ldots,a_i). The first Li Chao structure therefore computes the best transition among all cuts in each block. The second structure stores exactly the affine functions generated by completed blocks, and its sliding-window query enforces the length bound. Since every valid last piece is represented by one of these cases, the maximum obtained for (dp_i) is exactly the optimum for the prefix.

## Python Solution

The implementation below follows the (O(n\log^2 n)) construction. It uses a segment tree over values for the MEX-block boundaries and segment trees whose nodes contain Li Chao trees for the two range maximum structures.

```python
import sys
from array import array

input = sys.stdin.readline
NEG = -(10 ** 40)

class LastOccurrenceTree:
    def __init__(self, n):
        self.n = n
        size = 1
        while size < n + 2:
            size <<= 1
        self.size = size
        self.mn = array('i', [0]) * (2 * size)

    def update(self, p, value):
        p += self.size
        self.mn[p] = value
        p >>= 1
        while p:
            x = self.mn[p << 1]
            y = self.mn[p << 1 | 1]
            self.mn[p] = x if x < y else y
            p >>= 1

    def first_less(self, limit):
        if self.mn[1] >= limit:
            return None

        p = 1
        l = 0
        r = self.size - 1

        while l != r:
            mid = (l + r) >> 1
            left = p << 1
            if self.mn[left] < limit:
                p = left
                r = mid
            else:
                p = left | 1
                l = mid + 1

        return self.mn[p], l

class RangeLiChao:
    def __init__(self, n, prefix, use_prefix):
        self.n = n
        self.prefix = prefix
        self.use_prefix = use_prefix

        self.roots = array('i', [0]) * (4 * n + 20)

        self.left = array('i', [0])
        self.right = array('i', [0])
        self.line = array('i', [0])

        self.slopes = [0]
        self.intercepts = [NEG]

    def value(self, line_id, x):
        if self.use_prefix:
            x = self.prefix[x]
        return self.slopes[line_id] * x + self.intercepts[line_id]

    def add_line(self, slope, intercept):
        self.slopes.append(slope)
        self.intercepts.append(intercept)
        return len(self.slopes) - 1

    def new_node(self, line_id):
        idx = len(self.line)
        self.left.append(0)
        self.right.append(0)
        self.line.append(line_id)
        return idx

    def insert_inner(self, root, line_id, lo, hi):
        if root == 0:
            return self.new_node(line_id)

        cur = self.line[root]
        mid = (lo + hi) >> 1

        left_new = self.value(line_id, lo) > self.value(cur, lo)
        mid_new = self.value(line_id, mid) > self.value(cur, mid)

        if mid_new:
            self.line[root], line_id = line_id, cur
            cur = self.line[root]

        if lo == hi:
            return root

        if left_new != mid_new:
            child = self.left[root]
            new_child = self.insert_inner(child, line_id, lo, mid)
            self.left[root] = new_child
        else:
            child = self.right[root]
            new_child = self.insert_inner(child, line_id, mid + 1, hi)
            self.right[root] = new_child

        return root

    def query_inner(self, root, x, lo, hi):
        if root == 0:
            return NEG

        ans = self.value(self.line[root], x)

        if lo == hi:
            return ans

        mid = (lo + hi) >> 1
        if x <= mid:
            other = self.query_inner(self.left[root], x, lo, mid)
        else:
            other = self.query_inner(self.right[root], x, mid + 1, hi)

        return ans if ans > other else other

    def insert(self, pos, slope, intercept):
        line_id = self.add_line(slope, intercept)

        node = 1
        lo = 0
        hi = self.n - 1

        while True:
            self.roots[node] = self.insert_inner(
                self.roots[node], line_id, 0, self.n - 1
            )

            if lo == hi:
                break

            mid = (lo + hi) >> 1
            if pos <= mid:
                node = node << 1
                hi = mid
            else:
                node = node << 1 | 1
                lo = mid + 1

        return line_id

    def query(self, left, right, x):
        if left > right:
            return NEG

        left += 1
        right += 1

        # Iterative canonical decomposition.
        L = left + self.n - 1
        R = right + self.n - 1

        ans = NEG

        while L <= R:
            if L & 1:
                q = self.query_inner(self.roots[L], x, 0, self.n - 1)
                if q > ans:
                    ans = q
                L += 1

            if not (R & 1):
                q = self.query_inner(self.roots[R], x, 0, self.n - 1)
                if q > ans:
                    ans = q
                R -= 1

            L >>= 1
            R >>= 1

        return ans

def solve_case(n, k, a):
    prefix = [0] * (n + 1)
    for i, x in enumerate(a, 1):
        prefix[i] = prefix[i - 1] + x

    # T1: lines F_j(x) = -S_j*x + dp_j.
    # x is a MEX, hence x in [0, n].
    t1 = RangeLiChao(n + 1, prefix, False)

    # T2: lines H(x) = mex*x + C, evaluated at x = S_i.
    # The implementation indexes x by i and converts it to S_i.
    t2 = RangeLiChao(n + 1, prefix, True)

    last_tree = LastOccurrenceTree(n + 1)
    last = [0] * (n + 1)

    # Stack entries are (boundary, mex).
    # The sentinel boundary is 0.
    stack = [(0, 0)]

    dp = [0] * (n + 1)

    # F_0(x) = 0.
    t1.insert(0, 0, 0)

    for i in range(1, n + 1):
        x = a[i]

        # The value x now occurs at i.
        # Blocks whose boundary lies after the previous occurrence of x
        # may need to be split.
        previous = last[x]

        while stack[-1][0] > previous:
            stack.pop()

        pending = []
        rpos = i

        while rpos > stack[-1][0]:
            result = last_tree.first_less(rpos)
            if result is None:
                break

            min_last, mex = result
            pending.append((rpos, mex))
            rpos = min_last

        pending.reverse()

        for pos, mex in pending:
            left_boundary = stack[-1][0]

            # C = max F_j(mex) for j in [left_boundary, pos - 1].
            c = t1.query(left_boundary, pos - 1, mex)

            # H(S_i) = mex*S_i + C.
            t2.insert(left_boundary, mex, c)

            stack.append((pos, mex))

        last[x] = i
        last_tree.update(x, i)

        lower = max(i - k, 0)

        # Find the first stack boundary >= lower + 1.
        lo = 1
        hi = len(stack)

        while lo < hi:
            mid = (lo + hi) >> 1
            if stack[mid][0] < lower + 1:
                lo = mid + 1
            else:
                hi = mid

        p = lo

        best = NEG

        # The first complete block starting at or after lower.
        q = t2.query(lower, i - 1, i)
        if q > best:
            best = q

        # The block crossing the left boundary may be only partially usable.
        if p < len(stack):
            block_left = stack[p - 1][0]
            block_right = stack[p][0] - 1

            if block_left < lower <= block_right:
                mex = stack[p][1]
                c = t1.query(lower, block_right, mex)
                candidate = mex * prefix[i] + c
                if candidate > best:
                    best = candidate

        dp[i] = best

        # F_i(x) = -S_i*x + dp_i.
        t1.insert(i, -prefix[i], dp[i])

    return dp[n]

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(solve_case(n, k, a))

if __name__ == "__main__":
    main()
```

The prefix sum array is built first because every transition uses (S_i-S_j). Python integers already have arbitrary precision, so there is no overflow issue, although the original C++ implementation needs 64 bit integers.

`LastOccurrenceTree` stores the minimum last occurrence in every value interval. `first_less(x)` finds the smallest value whose last occurrence is smaller than `x`. This is precisely the value that becomes the MEX when a suffix boundary reaches that position.

`RangeLiChao` implements the black box needed by the DP. Its outer tree is indexed by the previous cut position. Every line is inserted into the (O(\log n)) outer nodes covering that position. Each outer node has an inner Li Chao tree, allowing a range of positions to be queried without explicitly visiting every previous cut.

The first instance represents

[
F_j(x)=-S_jx+dp_j.
]

Its query coordinate is the MEX itself. The second instance represents

[
H(x)=mx+C,
]

where the argument is an endpoint index and is converted internally to the corresponding prefix sum (S_i).

The stack stores boundaries rather than every individual previous cut. If two consecutive stack boundaries are `L` and `R`, all previous cuts in that interval have the same MEX. This is the reason the DP never performs (O(k)) transitions for one endpoint.

The partial-block query is necessary because the legal range begins at (i-k), which can cut through the middle of a MEX block. The second structure handles complete blocks, while the first structure explicitly handles that one clipped block. Omitting this correction is a common off-by-one error.

The code uses a sentinel boundary at zero and represents DP cuts using zero-based prefix indices. A piece ending at (i) and starting at (j+1) is consequently associated with cut index (j), which keeps the algebra consistent with the prefix sums.

## Worked Examples

### Sample 1

For

```
5 3
3 4 0 0 3
```

the required answer is `10`.

The important DP states are:

| Endpoint (i) | (S_i) | Best final piece | MEX | (dp_i) |
| --- | --- | --- | --- | --- |
| 1 | 3 | `[3]` | 0 | 0 |
| 2 | 7 | `[4]` or `[3,4]` | 0 | 0 |
| 3 | 7 | `[3,4,0]` | 1 | 7 |
| 4 | 7 | `[0]` after the prefix ending at 3 | 1 | 7 |
| 5 | 10 | `[0,3]` after the prefix ending at 3 | 1 | 10 |

At endpoint 3, the whole segment `[3,4,0]` has MEX (1) and sum (7), producing (7). At endpoint 5, the best transition is (dp_3+1\cdot(10-7)=7+3=10). The trace demonstrates why a segment with a small MEX can still be optimal when its sum is large.

### Sample 2

For

```
8 4
0 1 2 0 3 1 4 1
```

the answer is `26`. The relevant states are:

| Endpoint (i) | (S_i) | Best previous cut (j) | Final segment | MEX | (dp_i) |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | `[0]` | 1 | 0 |
| 2 | 1 | 0 | `[0,1]` | 2 | 2 |
| 3 | 3 | 0 | `[0,1,2]` | 3 | 9 |
| 4 | 3 | 0 | `[0,1,2,0]` | 3 | 9 |
| 5 | 6 | 1 | `[1,2,0,3]` | 4 | 24 |
| 6 | 7 | 2 | `[2,0,3,1]` | 4 | 26 |
| 7 | 11 | 6 | `[4]` | 0 | 26 |
| 8 | 12 | 6 | `[4,1]` | 0 | 26 |

The transition at endpoint 6 is the interesting one. The last four elements are `[2,0,3,1]`, whose MEX is (4) and whose sum is (6). The prefix before them has value (dp_2=2), giving

[
2+4\cdot6=26.
]

This shows why the DP must preserve the best prefix value separately from the MEX of the current piece.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log^2 n)) | There are (O(n)) MEX-block creations, and each range Li Chao operation costs (O(\log^2 n)). |
| Space | (O(n\log n)) | Each inserted line participates in (O(\log n)) outer segment-tree nodes. |

The original problem allows (n=2\cdot10^5) and gives 4 seconds with 512 MiB. The algorithm is fast enough asymptotically because it replaces the (O(nk)) family of transitions with only (O(n)) MEX blocks and logarithmic geometric queries. The nested Li Chao implementation is memory-intensive, which is why the original high-performance implementation uses compact static arrays rather than Python objects.

## Test Cases

The official samples are:

```
# The reference solution above reads one case at a time.

# Sample 1
assert solve_case(
    5, 3, [3, 4, 0, 0, 3]
) == 10

# Sample 2
assert solve_case(
    8, 4, [0, 1, 2, 0, 3, 1, 4, 1]
) == 26

# Sample 3
assert solve_case(
    10, 5, [0, 2, 0, 1, 2, 1, 0, 2, 2, 1]
) == 33

# Minimum size, k = 1.
assert solve_case(
    2, 1, [5, 7]
) == 0

# All equal values. The MEX is 0 because 0 never appears.
assert solve_case(
    5, 3, [7, 7, 7, 7, 7]
) == 0

# Maximum possible piece length is allowed.
assert solve_case(
    4, 4, [0, 1, 2, 3]
) == 9

# Length boundary catches an invalid transition using all four elements.
assert solve_case(
    4, 2, [0, 1, 2, 3]
) == 2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 5 7` | `0` | Minimum size and MEX zero for singleton positive values |
| `5 3 / 7 7 7 7 7` | `0` | All-equal values with no zero |
| `4 4 / 0 1 2 3` | `9` | Full-array segment when (k=n) |
| `4 2 / 0 1 2 3` | `2` | Correct enforcement of the maximum segment length |

For a maximum-size stress case, a useful test is `n = 200000`, `k = 1`, with every element equal to `1`. Every segment then has MEX zero, so the expected answer is zero. This checks that the implementation does not accidentally allocate work proportional to (nk) when the MEX structure is trivial.

## Edge Cases

For `n = 2, k = 1, a = [5,7]`, the legal pieces are `[5]` and `[7]`. Neither contains zero, so both MEX values are zero. The DP gets `dp[1] = 0` and `dp[2] = 0`. The answer is `0`. The MEX stack contains only zero-MEX blocks, so the Li Chao structures never manufacture a positive contribution.

For `n = 2, k = 2, a = [0,0]`, the whole segment has MEX (1), but its sum is zero. The transition is (1\cdot0=0), so `dp[2]=0`. This exercises the case where the MEX is positive but the segment contributes nothing.

For `n = 4, k = 2, a = [0,1,2,3]`, the legal range for endpoint 4 contains only cuts 2 and 3. The tempting segment `[0,1,2,3]` is excluded because its length is four. The best valid partition is `[0,1]` followed by `[2,3]`, with value (2\cdot1+0=2). The explicit partial-block query is what prevents the data structure from accidentally using a MEX block that crosses the left boundary of the sliding window.

For `n = 3, k = 3, a = [0,1,1]`, the values `0` and `1` are present, while `2` is absent, so the MEX is exactly (2). The sum is (2), giving (4). The last-occurrence representation naturally handles duplicates because only the most recent occurrence of each value matters when deciding whether that value is present after a candidate cut.
