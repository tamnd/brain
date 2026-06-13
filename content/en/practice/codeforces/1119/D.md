---
title: "CF 1119D - Frets On Fire"
description: "Each string of the ukulele is described by a starting pitch si. Moving to a higher fret increases the pitch by exactly one. If we only look at frets from l to r, then string i contributes every integer in the interval $$[si+l,; si+r]." date: "2026-06-12T04:29:33+07:00" tags: ["codeforces", "competitive-programming", "binary-search", "sortings"] categories: ["algorithms"] codeforces_contest: 1119 codeforces_index: "D" codeforces_contest_name: "Codeforces Global Round 2" rating: 1800 weight: 1119 solve_time_s: 97 verified: true draft: false --- [CF 1119D - Frets On Fire](https://codeforces.com/problemset/problem/1119/D) **Rating:** 1800   **Tags:** binary search, sortings   **Solve time:** 1m 37s   **Verified:** yes   ## Solution ## Problem Understanding Each string of the ukulele is described by a starting pitch `s_i`. Moving to a higher fret increases the pitch by exactly one. If we only look at frets from `l` to `r`, then string `i` contributes every integer in the interval$$[s_i+l,\; s_i+r].$$
For a query, we take the union of these intervals over all strings and must count how many distinct integers appear.
The huge number of frets is actually a distraction. A query never asks us to enumerate pitches. It only specifies a fret range length
$$L = r-l+1.$$
Every string contributes an interval of length `L`:
$$[s_i+l,\; s_i+l+L-1].$$
Adding the same value `l` to every interval shifts all intervals equally and does not change how they overlap. The answer depends only on `L`, not on `l` itself.
The input size immediately rules out anything quadratic. We may have `n = 100000` strings and `q = 100000` queries. Even an `O(n)` computation per query would require about `10^{10}` operations in the worst case. We need preprocessing close to `O(n log n)` and then logarithmic query handling.
A subtle point is that duplicate tuning values must be handled correctly. Suppose:
```
n = 3
s = [5, 5, 5]
```
For a query with `L = 1`, all strings contribute the same pitch. The answer is `1`, not `3`.
Another easy mistake is assuming only adjacent strings matter before sorting. Consider:
```
s = [100, 0, 50]
```
The natural structure only appears after sorting. Without sorting, interval gaps are meaningless.
A third source of bugs is handling intervals that just touch. For example:
```
s = [0, 3]
L = 3
```
The intervals are `[0,2]` and `[3,5]`. They do not overlap, so the union size is `6`.
But for:
```
s = [0,2]
L = 3
```
the intervals are `[0,2]` and `[2,4]`. They share the value `2`, so the union size is `5`, not `6`.
The distinction between a gap of `L` and a gap of `L-1` is crucial.
## Approaches
A brute-force interpretation would construct all intervals for a query and compute the size of their union. After sorting the intervals by starting point, we could merge them and count covered integers.
This is correct because the answer is exactly the size of the union of all pitch intervals. Unfortunately, even after sorting the strings once, each query still requires scanning all `n` intervals. With `100000` queries and `100000` strings, that becomes roughly `10^{10}` operations.
The key observation is that every query only changes the common interval length `L`.
Let the sorted tuning values be
$$a_1 \le a_2 \le \dots \le a_n.$$
For a query length `L`, string `i` contributes
$$[a_i,\; a_i+L-1]$$
after removing the irrelevant shift by `l`.
Consider two neighboring starting positions. Let
$$d_i=a_{i+1}-a_i.$$
If `d_i < L`, the two intervals overlap or touch, so they merge into a single component.
If `d_i \ge L`, there is a gap between them. The uncovered part has size
$$d_i-L.$$
Imagine starting with one giant interval spanning from `a_1` to `a_n+L-1`.
Its length is
$$(a_n-a_1)+L.$$
Every gap where `d_i \ge L` removes exactly `d_i-L` integers from that span.
Thus
$$\text{answer}(L)
=
(a_n-a_1)+L
-
\sum_{d_i\ge L}(d_i-L).$$
Rearranging gives
$$\text{answer}(L)
=
L
+
\sum_{i=1}^{n-1}\min(d_i,L).$$
This formula is the entire problem.
Now the query becomes:
$$L + \sum \min(d_i,L).$$
The gaps `d_i` are fixed. Sort them once. For a given `L`, all gaps smaller than `L` contribute their actual value, and all larger gaps contribute `L`.
A prefix-sum array over sorted gaps lets us evaluate the expression in `O(log n)` using binary search.
| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(qn) | O(n) | Too slow |
| Optimal | O(n log n + q log n) | O(n) | Accepted |
## Algorithm Walkthrough
1. Read all tuning values and sort them.
2. Compute the adjacent differences
$$d_i=a_{i+1}-a_i.$$
These differences completely describe where interval unions may split.
3. Sort all differences.
4. Build a prefix-sum array over the sorted differences.
5. For each query, compute
$$L=r-l+1.$$
Only this length matters.
6. Binary search for the first difference that is at least `L`.
Let that position be `pos`.
7. All differences before `pos` contribute their actual values. Their total is obtained from the prefix sums.
8. All remaining differences contribute exactly `L` each because
$$\min(d_i,L)=L.$$
9. Compute
$$\sum \min(d_i,L)
=
\text{prefix}[pos]
+
(m-pos)\cdot L,$$
where `m=n-1`.
10. Output
$$L+\sum \min(d_i,L).$$
### Why it works
For a fixed query length `L`, each string contributes an interval of length `L`. After sorting starting positions, adjacent intervals are separated by a distance `d_i`.
Whenever `d_i < L`, the intervals connect and no uncovered region appears. Whenever `d_i \ge L`, exactly `d_i-L` integers are missing between consecutive merged components.
Starting from the total span `(a_n-a_1)+L` and subtracting all missing regions yields
$$L+\sum \min(d_i,L).$$
The algorithm evaluates exactly this formula. Every difference contributes either itself or `L`, which is precisely the definition of `min(d_i,L)`. Since all contributions are accounted for once, the computed value equals the size of the union of all pitch intervals.
## Python Solution
```python
import sys
from bisect import bisect_left
input = sys.stdin.readline
n = int(input())
s = list(map(int, input().split()))
s.sort()
gaps = [s[i + 1] - s[i] for i in range(n - 1)]
gaps.sort()
pref = [0]
for x in gaps:
    pref.append(pref[-1] + x)
q = int(input())
ans = []
m = n - 1
for _ in range(q):
    l, r = map(int, input().split())
    L = r - l + 1
    pos = bisect_left(gaps, L)
    total = pref[pos] + (m - pos) * L
    ans.append(str(L + total))
print(" ".join(ans))
```
The first step is sorting the tuning values. Once sorted, only adjacent differences matter because every larger difference is composed of adjacent ones.
The array `gaps` stores these adjacent differences. Sorting `gaps` allows binary searching the point where values become at least `L`.
The prefix-sum array lets us obtain the sum of all gaps smaller than `L` in constant time after binary search.
`bisect_left` is the correct choice. Gaps equal to `L` must contribute `L`, not their original value. Since both values are equal, either interpretation gives the same contribution, but `bisect_left` cleanly splits the array into `< L` and `>= L`.
All arithmetic uses Python integers, which safely handle values up to roughly `10^18`. The answer itself may also exceed `10^18`, so fixed-width 64-bit arithmetic must be considered carefully in other languages.
## Worked Examples
### Sample 1
Input:
```
6
3 1 4 1 5 9
3
7 7
0 2
8 17
```
Sorted tuning values:
```
[1, 1, 3, 4, 5, 9]
```
Sorted gaps:
```
[0, 1, 1, 2, 4]
```
Prefix sums:
```
[0, 0, 1, 2, 4, 8]
```
#### Query 1: L = 1
| L | pos | gaps < L sum | remaining count | total min sum | answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 4 | 4 | 5 |
Answer = `5`.
#### Query 2: L = 3
| L | pos | gaps < L sum | remaining count | total min sum | answer |
| --- | --- | --- | --- | --- | --- |
| 3 | 4 | 4 | 1 | 7 | 10 |
Answer = `10`.
#### Query 3: L = 10
| L | pos | gaps < L sum | remaining count | total min sum | answer |
| --- | --- | --- | --- | --- | --- |
| 10 | 5 | 8 | 0 | 8 | 18 |
Answer = `18`.
This example shows that once `L` becomes larger than every gap, all intervals merge into one component and the answer grows linearly with `L`.
### Custom Example
Input:
```
3
0 10 20
1
0 4
```
Here:
```
L = 5
gaps = [10, 10]
```
| L | pos | gaps < L sum | remaining count | total min sum | answer |
| --- | --- | --- | --- | --- | --- |
| 5 | 0 | 0 | 2 | 10 | 15 |
The intervals are:
```
[0,4]
[10,14]
[20,24]
```
Their union size is `5 + 5 + 5 = 15`, matching the formula.
This trace demonstrates the case where every gap exceeds `L`, so no intervals merge.
## Complexity Analysis
| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log n) | Sorting plus one binary search per query |
| Space | O(n) | Gaps and prefix sums |
With `n,q ≤ 100000`, sorting costs about `O(100000 log 100000)` and each query requires only a logarithmic search. This comfortably fits the limits.
## Test Cases
```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    s = list(map(int, sys.stdin.readline().split()))
    s.sort()
    gaps = [s[i + 1] - s[i] for i in range(n - 1)]
    gaps.sort()
    pref = [0]
    for x in gaps:
        pref.append(pref[-1] + x)
    q = int(sys.stdin.readline())
    ans = []
    m = n - 1
    for _ in range(q):
        l, r = map(int, sys.stdin.readline().split())
        L = r - l + 1
        pos = bisect_left(gaps, L)
        total = pref[pos] + (m - pos) * L
        ans.append(str(L + total))
    return " ".join(ans)
# provided sample
assert run(
"""6
3 1 4 1 5 9
3
7 7
0 2
8 17
"""
) == "5 10 18"
# minimum size
assert run(
"""1
42
1
0 0
"""
) == "1"
# all equal values
assert run(
"""4
5 5 5 5
2
0 0
0 4
"""
) == "1 5"
# intervals never merge
assert run(
"""3
0 10 20
1
0 4
"""
) == "15"
# touching intervals
assert run(
"""2
0 2
1
0 2
"""
) == "5"
# huge coordinates
assert run(
"""2
0 1000000000000000000
1
0 999999999999999999
"""
) == "2000000000000000000"
```
| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single string | 1 | Minimum size case |
| All tuning values equal | 1 5 | Duplicate starting positions |
| `0 10 20`, `L=5` | 15 | No interval merging |
| `0 2`, `L=3` | 5 | Intervals touching at one point |
| Huge coordinates | 2000000000000000000 | 64-bit boundary behavior |
## Edge Cases
Consider:
```
3
5 5 5
1
0 0
```
All gaps are zero. After sorting, `gaps = [0,0]`. For `L=1`, every gap contributes `0`, so the answer is
$$1+0+0=1.$$
All strings generate the same pitch, which is correct.
Now consider:
```
2
0 3
1
0 2
```
Here `L=3` and the gap equals `3`. Binary search places this gap among values `>= L`. Its contribution becomes `L=3`. The answer is
$$3+3=6.$$
The intervals `[0,2]` and `[3,5]` are disjoint, covering six integers.
Finally:
```
2
0 2
1
0 2
```
Again `L=3`, but now the gap is `2`. The contribution is `2`, giving
$$3+2=5.$$
The intervals `[0,2]` and `[2,4]` overlap at one point, producing exactly five distinct pitches. This is the boundary where many off-by-one implementations fail, but the `min(gap, L)` formula handles it naturally.
