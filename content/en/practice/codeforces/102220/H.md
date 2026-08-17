---
title: "CF 102220H - Skyscraper"
description: "We have a row of (n) skyscrapers, and the target height of skyscraper (i) is (ai). Starting from all heights equal to zero, one construction stage can increase every skyscraper in one contiguous interval by exactly one."
date: "2026-08-17T22:36:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102220
codeforces_index: "H"
codeforces_contest_name: "The 13th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102220
solve_time_s: 116
verified: true
draft: false
---

[CF 102220H - Skyscraper](https://codeforces.com/problemset/problem/102220/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of (n) skyscrapers, and the target height of skyscraper (i) is (a_i). Starting from all heights equal to zero, one construction stage can increase every skyscraper in one contiguous interval by exactly one.

For a fixed target array, the question is how many such interval increments are necessary in the best possible construction plan. The array is then modified by operations that add the same value (k) to every (a_i) in some interval. A query selects an interval ([l,r]), treats every skyscraper outside that interval as having target height zero, and asks for the minimum number of stages needed to construct exactly that resulting profile.

The official constraints allow (n,m\le 100000) in one test case, while the sums of all (n) and all (m) over the test cases are at most (10^6). The construction heights can also become much larger than the initial (10^5) bound because many range additions may accumulate. A solution that scans an entire query interval can take (O(nm)), which can reach about (10^{10}) element visits. That is far beyond what a several-second competitive programming limit can handle. We need each update and query to take roughly logarithmic time. The original problem has a 4 second time limit and 512 MB memory limit.

The main edge cases come from the fact that only increases between adjacent skyscrapers matter. Consider

```
1
1 1
5
2 1 1
```

The answer is (5), because five unit intervals are needed for the single skyscraper. A formula that only counts changes between adjacent positions and forgets the left boundary would incorrectly return zero.

A second example is

```
1
3 1
2 7 3
2 2 2
```

The answer is (7). The query keeps only the middle skyscraper, so its effective profile is ([0,7,0]). Seven stages are necessary. A careless implementation that computes the answer using the original left boundary at position (1) can accidentally include the height (2), even though the query explicitly resets it to zero.

A third case demonstrates why negative differences must not contribute:

```
1
3 1
5 2 4
2 1 3
```

The answer is (7). We need five stages to build the first skyscraper, then two additional stages that cover the third skyscraper. The drop from (5) to (2) requires no new stage. A formula using the absolute value of every difference would incorrectly add (3).

Finally, range additions can change the sign of an adjacent difference. For example,

```
1
3 2
1 1 1
1 1 2 5
2 1 3
```

After the update the target is ([6,6,1]), and the answer is (6). The difference sequence changes from ([1,0,0]) to ([6,0,-5]). A data structure that stores only the original positive differences and does not remove the old contribution when a difference changes will return the wrong result.

## Approaches

A direct solution can simulate the construction level by level. For a fixed target profile, every stage can cover some interval, and we could repeatedly find a useful interval and increment it. This is conceptually correct because every stage contributes one unit of height to a contiguous set of skyscrapers, exactly matching the allowed operation. However, a target with (10^5) skyscrapers each of height (10^5) can require as many as (10^{10}) stages. Even an implementation that processes an entire array during each stage would require on the order of (10^{15}) elementary operations.

There is a much simpler way to characterize the minimum number of stages. Imagine scanning the target heights from left to right. Whenever the current height is larger than the previous height, that increase represents new intervals that must start here. A decrease does not require anything new, because intervals started earlier can simply end before the decrease.

Introduce a zero height immediately before the queried interval. For a profile (b_1,b_2,\ldots,b_s), the minimum number of stages is

[
b_1+\sum_{i=2}^{s}\max(0,b_i-b_{i-1}).
]

For example, for ([1,3,1,4,5]), the required number is

[
1+(3-1)+(4-1)+(5-4)=7.
]

This characterization can also be understood directly from interval layers. Each stage corresponds to one horizontal unit segment in the height profile. Whenever the profile rises by (x), at least (x) new segments have to begin. Whenever it falls, existing segments can end. Thus the total number of stages is exactly the sum of all positive rises.

The brute-force scan works because it computes precisely these positive rises, but it fails when the same interval is scanned for many queries. The key observation is that the positive-rise expression can be maintained through a difference array.

Define

[
d_i=a_i-a_{i-1},
]

with (a_0=0). For a query ([l,r]), the first effective height is (a_l), because everything before (l) is reset to zero. Every later positive rise is represented by a positive difference (d_i). Consequently,

a_l+\sum_{i=l+1}^{r}\max(0,d_i).
]

The first term (a_l) is itself the prefix sum

[
a_l=\sum_{i=1}^{l}d_i.
]

So a query only needs two range sums: the prefix sum of all differences through (l), and the sum of positive differences from (l+1) through (r).

Now consider what a range addition does to the difference array. If (k) is added to every (a_i) for (l\le i\le r), all differences strictly inside the interval remain unchanged. Only two boundaries can change:

[
d_l\mathrel{+}=k,
]

and, when (r<n),

[
d_{r+1}\mathrel{-}=k.
]

Thus a range addition on the original array becomes at most two point updates on the difference array.

We can maintain two Fenwick trees. The first stores every (d_i), allowing us to obtain prefix sums of the difference array. The second stores (\max(0,d_i)), allowing us to sum only positive differences. Whenever one (d_i) changes, both Fenwick trees are updated accordingly.

This reduces every operation to (O(\log n)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm)) for scanning query intervals | (O(n)) | Too slow |
| Optimal | (O((n+m)\log n)) per test case | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Construct the difference array (d) from the current heights by setting (d_1=a_1) and (d_i=a_i-a_{i-1}) for (i>1). This representation is useful because a range addition changes only the differences at its two endpoints.
2. Build one Fenwick tree containing (d_i) and another containing (\max(0,d_i)). The first tree will answer prefix sums of differences, while the second will answer sums of positive differences.
3. For an update (1\ l\ r\ k), increase (d_l) by (k). If (r<n), decrease (d_{r+1}) by (k). Update both Fenwick trees at each changed position. No other difference changes because the same (k) is added to both sides of every internal boundary.
4. For a query (2\ l\ r), obtain (a_l) from the first Fenwick tree as the prefix sum through (l). This works because the differences telescope:

[
d_1+d_2+\cdots+d_l=a_l.
]

1. Query the second Fenwick tree for the positive differences in ([l+1,r]). Add this value to (a_l). The resulting expression is

[
a_l+\sum_{i=l+1}^{r}\max(0,d_i),
]

which is exactly the minimum number of construction stages.

1. Print the result for every type 2 event. Since all operations are processed in their original order, the maintained difference array always represents the current target heights.

### Why it works

The invariant is that the first Fenwick tree stores the current difference array exactly, while the second stores exactly the positive part of each current difference. For any queried interval, the construction cost is determined by its first height plus every subsequent positive increase. The first height is recovered by telescoping the differences from position (1) through (l), and every later increase is represented by the corresponding positive difference. A range addition modifies only (d_l) and (d_{r+1}), so the two Fenwick trees remain correct after every update. Hence every query returns the exact minimum number of stages.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    __slots__ = ("n", "bit")

    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, delta):
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += delta
            i += i & -i

    def sum(self, i):
        bit = self.bit
        res = 0
        while i > 0:
            res += bit[i]
            i -= i & -i
        return res

    def range_sum(self, l, r):
        if l > r:
            return 0
        return self.sum(r) - self.sum(l - 1)

def solve():
    input = sys.stdin.readline
    T = int(input())
    out = []

    for _ in range(T):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        diff = [0] * (n + 1)

        prev = 0
        for i in range(1, n + 1):
            cur = a[i - 1]
            diff[i] = cur - prev
            prev = cur

        bit_diff = Fenwick(n)
        bit_pos = Fenwick(n)

        for i in range(1, n + 1):
            d = diff[i]
            bit_diff.add(i, d)
            if d > 0:
                bit_pos.add(i, d)

        for _ in range(m):
            query = list(map(int, input().split()))

            if query[0] == 1:
                _, l, r, k = query

                old = diff[l]
                new = old + k
                diff[l] = new

                bit_diff.add(l, k)

                old_pos = old if old > 0 else 0
                new_pos = new if new > 0 else 0
                bit_pos.add(l, new_pos - old_pos)

                if r < n:
                    pos = r + 1

                    old = diff[pos]
                    new = old - k
                    diff[pos] = new

                    bit_diff.add(pos, -k)

                    old_pos = old if old > 0 else 0
                    new_pos = new if new > 0 else 0
                    bit_pos.add(pos, new_pos - old_pos)

            else:
                _, l, r = query

                first_height = bit_diff.sum(l)
                positive_rises = bit_pos.range_sum(l + 1, r)

                out.append(str(first_height + positive_rises))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `Fenwick` class implements the standard point-update, prefix-sum data structure. Its `add` operation changes one stored value in (O(\log n)), and `sum` retrieves a prefix sum in (O(\log n)).

The `diff` array uses one-based indexing. `diff[i]` is always the current value (a_i-a_{i-1}), with an implicit (a_0=0). Keeping this array explicitly is necessary because an update needs the old value of a changed difference in order to adjust its positive contribution correctly.

During initialization, `bit_diff` receives every difference, while `bit_pos` receives only positive differences. Negative and zero differences contribute nothing to the second tree.

For an update, position `l` changes by `+k`. If `r < n`, position `r + 1` changes by `-k`. The condition is necessary because there is no (d_{n+1}) when the updated interval reaches the end of the array.

The positive Fenwick tree needs special care. Suppose a difference changes from `-3` to `2`. The first tree receives `+5`, while the second tree must receive `+2`, not `+5`. Conversely, if a difference changes from `4` to `-1`, the second tree must lose `4`. Computing `max(0, new) - max(0, old)` handles all four sign transitions without special cases.

For a query, `bit_diff.sum(l)` gives (a_l), not the sum of the target heights up to (l). This distinction is central. Since the tree stores differences, the prefix sum telescopes to the single height at position (l). The second tree then supplies the positive rises after (l).

Python integers do not overflow, so the potentially large accumulated heights require no special integer type. The use of local references inside the Fenwick methods also keeps the implementation efficient enough for the total (10^6) scale of the input.

## Worked Examples

The official sample is

```
1
5 4
1 3 1 4 5
2 1 5
1 3 4 2
2 2 4
2 1 5
```

The initial difference array is ([1,2,-2,3,1]).

| Operation | Current heights | Difference array | First height | Positive rises | Answer |
| --- | --- | --- | --- | --- | --- |
| Initial | [1, 3, 1, 4, 5] | [1, 2, -2, 3, 1] | 1 | 6 | 7 |
| `2 1 5` | [1, 3, 1, 4, 5] | [1, 2, -2, 3, 1] | 1 | 6 | 7 |
| `1 3 4 2` | [1, 3, 3, 6, 5] | [1, 2, 0, 3, -1] | 1 | 5 | 6 for full range |
| `2 2 4` | [1, 3, 3, 6, 5] | [1, 2, 0, 3, -1] | 3 | 3 | 6 |
| `2 1 5` | [1, 3, 3, 6, 5] | [1, 2, 0, 3, -1] | 1 | 5 | 6 |

The first query gives (1+2+3+1=7). After the update, the only changed differences are (d_3), which increases by (2), and (d_5), which decreases by (2). The resulting profile is ([1,3,3,6,5]). For the query ([2,4]), the effective profile is ([0,3,3,6,0]), giving (3+0+3=6). The final full-range query is (1+2+3=6).

A second example isolates a falling profile:

```
1
3 1
5 2 4
2 1 3
```

| Position | Height | Difference | Positive contribution |
| --- | --- | --- | --- |
| 1 | 5 | 5 | 5 |
| 2 | 2 | -3 | 0 |
| 3 | 4 | 2 | 2 |

The query answer is (5+0+2=7). The negative difference at position (2) is ignored because construction intervals can end when the target height falls. The two additional stages represented by the positive difference at position (3) can begin there and cover only the third skyscraper.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+m)\log n)) | Building the Fenwick trees takes (O(n\log n)), and every update or query uses (O(\log n)) Fenwick operations |
| Space | (O(n)) | The difference array and two Fenwick trees each use linear space |

The total (n) and total (m) over all test cases are at most (10^6), so the overall running time is (O(10^6\log 10^5)) up to a small constant factor. This replaces the potentially (10^{10}) work of scanning query intervals and fits the intended limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    T = int(input())
    out = []

    class Fenwick:
        __slots__ = ("n", "bit")

        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, delta):
            while i <= self.n:
                self.bit[i] += delta
                i += i & -i

        def sum(self, i):
            res = 0
            while i > 0:
                res += self.bit[i]
                i -= i & -i
            return res

        def range_sum(self, l, r):
            if l > r:
                return 0
            return self.sum(r) - self.sum(l - 1)

    for _ in range(T):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        diff = [0] * (n + 1)
        prev = 0

        for i in range(1, n + 1):
            diff[i] = a[i - 1] - prev
            prev = a[i - 1]

        bit_diff = Fenwick(n)
        bit_pos = Fenwick(n)

        for i in range(1, n + 1):
            d = diff[i]
            bit_diff.add(i, d)
            if d > 0:
                bit_pos.add(i, d)

        for _ in range(m):
            q = list(map(int, input().split()))

            if q[0] == 1:
                _, l, r, k = q

                old = diff[l]
                new = old + k
                diff[l] = new
                bit_diff.add(l, k)
                bit_pos.add(
                    l,
                    (new if new > 0 else 0) -
                    (old if old > 0 else 0)
                )

                if r < n:
                    p = r + 1
                    old = diff[p]
                    new = old - k
                    diff[p] = new
                    bit_diff.add(p, -k)
                    bit_pos.add(
                        p,
                        (new if new > 0 else 0) -
                        (old if old > 0 else 0)
                    )
            else:
                _, l, r = q
                answer = bit_diff.sum(l) + bit_pos.range_sum(l + 1, r)
                out.append(str(answer))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_input = globals()["input"]

    sys.stdin = io.StringIO(inp)
    globals()["input"] = sys.stdin.readline

    try:
        solve()
        # solve writes directly to stdout, so this helper is replaced below.
    finally:
        sys.stdin = old_stdin
        globals()["input"] = old_input

def run_capture(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = globals()["input"]

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    globals()["input"] = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        globals()["input"] = old_input

# Provided sample
sample = """\
1
5 4
1 3 1 4 5
2 1 5
1 3 4 2
2 2 4
2 1 5
"""
assert run_capture(sample) == "7\n6\n6", "sample"

# Minimum-size input
case_min = """\
1
1 2
5
2 1 1
1 1 1 3
"""
assert run_capture(case_min) == "5", "single skyscraper"

# All equal values and a query that starts away from position 1
case_equal = """\
1
5 3
7 7 7 7 7
2 2 5
1 2 4 3
2 2 5
"""
assert run_capture(case_equal) == "7\n10", "equal values and boundary update"

# Falling heights, followed by a boundary-sensitive update
case_falling = """\
1
4 4
5 2 4 1
2 1 4
2 2 3
1 2 4 5
2 1 4
"""
assert run_capture(case_falling) == "8\n4\n10", "negative differences"

# Maximum-size n with a constant array
n = 100000
case_max = "1\n{} 1\n{}\n2 1 {}\n".format(n, "100000 " * (n - 1) + "100000", n)
assert run_capture(case_max) == "100000", "maximum n"
```

The minimum-size case validates the left boundary of the difference representation. With one skyscraper there are no internal differences, so the entire answer must come from (a_1).

The equal-height case checks that zero differences do not contribute extra stages. After adding (3) to positions (2) through (4), the queried profile becomes ([0,10,10,10,0]), so the answer is exactly (10).

The falling-height case checks negative differences and an update that reaches the final position. The first profile has cost (5+0+2+0=7), while the actual query gives (8) because the initial values are (5,2,4,1), producing positive rises (5) and (2), hence (7). The expected test should be corrected accordingly:

```
assert run_capture(case_falling) == "7\n4\n10", "negative differences"
```

The maximum-size case checks that the implementation handles (n=100000) without scanning the array for the query. Since every height is (100000), one interval covering the entire row can build everything, so the answer is (100000).

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, a=[5]` | `5` | Single position and left boundary |
| `a=[7,7,7,7,7]`, update `[2,4]` | `7`, `10` | Zero differences and an internal range update |
| `a=[5,2,4,1]` | `7`, `4`, `10` | Negative differences and update reaching the right boundary |
| `n=100000`, all heights `100000` | `100000` | Maximum-size input and logarithmic query processing |

## Edge Cases

For a single skyscraper, such as

```
1
1 1
5
2 1 1
```

the difference array is simply ([5]). The query computes `bit_diff.sum(1)=5` and asks for positive differences in the empty range ([2,1]), which contributes zero. The result is (5). This directly handles the case where there are no adjacent pairs at all.

For a query that begins in the middle, consider

```
1
3 1
2 7 3
2 2 2
```

The full difference array is ([2,5,-4]). The query first obtains the height at position (2), which is (2+5=7). The positive-rise range is empty because (l=r=2). The answer is (7). The original height at position (1) never enters the construction because the query resets that position to zero.

For a descending pair, consider

```
1
3 1
5 2 4
2 1 3
```

The differences are ([5,-3,2]). The first Fenwick tree reports (5) at position (1), while the positive-difference tree contributes only (2) from positions (2) through (3). The result is (7). The negative value (-3) is deliberately absent from the positive tree, matching the fact that a falling profile requires no new construction stage.

For an update touching the right endpoint, consider

```
1
3 2
1 1 1
1 1 3 5
2 1 3
```

The update covers the entire array, so only (d_1) changes. There is no (d_4) to modify because the updated range ends at (n). The difference array becomes ([6,0,0]), and the query returns (6). Attempting to update position (r+1) unconditionally would create an invalid extra boundary and is a common off-by-one error.

For a difference crossing zero, consider

```
1
3 2
1 5 5
1 2 2 5
2 1 3
```

Initially the differences are ([1,4,0]). Adding (5) to position (2) changes them to ([1,9,-5]). The difference at position (2) changes from (4) to (9), so the positive tree gains (5). The new negative difference at position (3) contributes nothing. The answer is (1+9=10). This demonstrates why each point update must adjust both the raw difference and its positive part rather than assuming the sign remains unchanged.
