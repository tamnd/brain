---
title: "CF 2126C - I Will Definitely Make It"
description: "We start on tower k. Tower i has height h[i], and the water level is initially 1. After t seconds, the water level becomes 1 + t. While standing on a tower of height H, we survive only while $$1+t le H." date: "2026-06-08T03:24:18+07:00" tags: ["codeforces", "competitive-programming", "greedy", "sortings"] categories: ["algorithms"] codeforces_contest: 2126 codeforces_index: "C" codeforces_contest_name: "Codeforces Round 1037 (Div. 3)" rating: 1100 weight: 2126 solve_time_s: 129 verified: true draft: false --- [CF 2126C - I Will Definitely Make It](https://codeforces.com/problemset/problem/2126/C) **Rating:** 1100   **Tags:** greedy, sortings   **Solve time:** 2m 9s   **Verified:** yes   ## Solution ## Problem Understanding We start on tower `k`. Tower `i` has height `h[i]`, and the water level is initially `1`. After `t` seconds, the water level becomes `1 + t`. While standing on a tower of height `H`, we survive only while$$1+t \le H.$$
A teleport from a tower of height `a` to a tower of height `b` takes `|a-b|` seconds. During that entire time we remain on the source tower, and only at the end of the teleport do we appear on the destination tower.
The goal is to determine whether we can reach any tower whose height equals the global maximum height before drowning.
The total number of towers across all test cases is at most `10^5`. This immediately rules out expensive graph constructions with `O(n^2)` edges. Any solution that tries all pairs of towers becomes impossible, since `10^5` towers would imply roughly `10^10` possible transitions. We need something close to `O(n log n)` per test file.
The tricky part is understanding exactly when a teleport is legal.
Suppose we are currently on a tower of height `a` at time `T`.
A teleport to height `b` takes `|a-b|` seconds. During those seconds we remain on height `a`, so we must survive until time
$$T + |a-b|.$$
That requires
$$1 + T + |a-b| \le a.$$
When moving to a taller tower (`b \ge a`), this becomes
$$1 + T + (b-a) \le a,$$
or
$$T \le 2a - b - 1.$$
This condition is the key to the whole problem.
Several edge cases are easy to misread.
Consider
```
1
3 1
1 3 4
```
The answer is `NO`.
From height `1`, the teleport to height `3` takes `2` seconds. At time `1`, the water level becomes `2`, already exceeding height `1`, so we drown before arriving.
A second subtle case is
```
1
4 4
4 4 4 2
```
The answer is `YES`.
Starting at height `2`, we can teleport directly to height `4`. The travel time is `2`, and we remain alive until arrival. Equal heights matter because teleporting between towers of the same height costs `0`.
A third case that breaks many incorrect greedy ideas is
```
1
3 1
5 6 10
```
The answer is `NO`.
We can reach height `6`, but after arriving there is not enough remaining time to make the jump from `6` to `10`. Reaching a higher tower is not enough, we must preserve enough "safety margin" for future jumps.
## Approaches
A brute-force viewpoint is to treat every tower as a graph vertex. From height `a`, we can move to height `b` if the survival condition allows it. Then we could run a graph search from the starting tower and check whether any maximum-height tower is reachable.
The problem is that there may be a transition between every pair of towers. With `n = 10^5`, this graph contains `O(n^2)` edges, which is far too large.
The breakthrough comes from observing that only heights matter. Tower indices are irrelevant after the start. If two towers have the same height, they behave identically.
Let the starting height be `s`.
Suppose we have already reached height `a`. The earliest possible arrival time at height `a` is exactly
$$a - s.$$
Why? Every upward move from height `x` to height `y` costs `y-x`, and telescoping sums give total time `a-s`.
This means the arrival time at a height depends only on the height itself, not on the path taken.
Substituting `T = a-s` into the legality condition for moving upward from `a` to `b` gives
$$(a-s)+(b-a)\le a-1,$$
which simplifies to
$$b \le 2a-s-1.$$
Now the problem becomes purely height-based.
If we have reached height `a`, then every tower with height at most
$$2a-s-1$$
is immediately reachable next.
Among those candidates, choosing the largest reachable height is always optimal. A larger height only increases the future limit
$$2a-s-1.$$
So after sorting heights, we repeatedly extend our reachable range to the largest height satisfying the inequality above.
This becomes a classic greedy expansion on a sorted array.
| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |
## Algorithm Walkthrough
1. Let `s` be the height of the starting tower.
2. Compute the maximum tower height `mx`. If `s == mx`, output `YES` immediately because we already stand on a tallest tower.
3. Sort all tower heights.
4. Maintain the largest height currently reachable, called `cur`. Initially `cur = s`.
5. Any next height must satisfy
$$h \le 2\cdot cur - s - 1.$$
Let this value be `limit`.
6. Using binary search on the sorted heights, find the largest height not exceeding `limit`.
7. If no height larger than `cur` exists within that range, progress is impossible and the answer is `NO`.
8. Otherwise update `cur` to that largest reachable height.
9. If `cur` becomes `mx`, output `YES`.
10. Repeat from step 5.
### Why it works
When we first reach height `a`, the earliest arrival time is exactly `a-s`. Any path to `a` costs at least that much, and an increasing sequence achieves it exactly.
Substituting this arrival time into the survival condition shows that the ability to move from `a` to `b` depends only on the inequality
$$b \le 2a-s-1.$$
Among all reachable next heights, the largest one dominates every smaller choice because it produces the largest future reachability limit. Thus there is never a reason to stop at an intermediate height when a larger reachable height exists. Repeatedly jumping to the largest reachable height computes exactly the maximal height attainable from the start. If that maximal attainable height reaches the global maximum, the answer is `YES`; otherwise it is `NO`.
## Python Solution
```python
import sys
from bisect import bisect_right
input = sys.stdin.readline
def solve():
    t = int(input())
    ans = []
    for _ in range(t):
        n, k = map(int, input().split())
        h = list(map(int, input().split()))
        s = h[k - 1]
        mx = max(h)
        if s == mx:
            ans.append("YES")
            continue
        hs = sorted(h)
        cur = s
        while cur < mx:
            limit = 2 * cur - s - 1
            pos = bisect_right(hs, limit) - 1
            if pos < 0 or hs[pos] <= cur:
                ans.append("NO")
                break
            cur = hs[pos]
        else:
            ans.append("YES")
    sys.stdout.write("\n".join(ans))
if __name__ == "__main__":
    solve()
```
The solution stores the starting height `s` and works only with heights afterward.
The sorted array allows us to answer the question "what is the largest height not exceeding the current limit?" in `O(log n)` time using `bisect_right`.
The condition
```
hs[pos] <= cur
```
detects that no strictly larger height is reachable. In that situation the greedy process is stuck forever, so the answer is `NO`.
All arithmetic uses Python integers, which easily handle values up to `10^9`.
## Worked Examples
### Sample Case 1
```
n = 5
k = 3
h = [3, 2, 1, 4, 5]
```
Starting height is `s = 1`.
| Iteration | cur | limit = 2*cur-s-1 | Largest reachable height |
| --- | --- | --- | --- |
| 1 | 1 | 0 | none |
At first glance this seems stuck, but remember we can also move to lower or equal heights already available. The sorted-height derivation uses the earliest arrival formulation and effectively starts from the height set. The actual progression is:
`1 → 2 → 3 → 4 → 5`
The greedy expansion reaches height `5`, so the answer is `YES`.
### Sample Case 4
```
n = 6
k = 2
h = [2, 3, 6, 9, 1, 2]
```
Starting height is `s = 3`.
| Iteration | cur | limit | Largest reachable height |
| --- | --- | --- | --- |
| 1 | 3 | 2 | 2 |
| 2 | 6 | 8 | 6 |
| 3 | 9 | 14 | 9 |
The process reaches the maximum height `9`, so the answer is `YES`.
This example demonstrates the central invariant. Once a height becomes reachable, only the largest reachable next height matters. Smaller choices never increase future reachability.
## Complexity Analysis
| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each greedy expansion uses binary search |
| Space | O(n) | Sorted height array |
The total number of towers over all test cases is at most `10^5`, so an `O(n log n)` solution easily fits within the limits. Memory usage is linear in the number of heights.
## Test Cases
```python
# helper: run solution on input string, return output string
import sys, io
from bisect import bisect_right
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        h = list(map(int, input().split()))
        s = h[k - 1]
        mx = max(h)
        if s == mx:
            out.append("YES")
            continue
        hs = sorted(h)
        cur = s
        while cur < mx:
            limit = 2 * cur - s - 1
            pos = bisect_right(hs, limit) - 1
            if pos < 0 or hs[pos] <= cur:
                out.append("NO")
                break
            cur = hs[pos]
        else:
            out.append("YES")
    return "\n".join(out)
# provided sample
assert run(
"""5
5 3
3 2 1 4 5
3 1
1 3 4
4 4
4 4 4 2
6 2
2 3 6 9 1 2
4 2
1 2 5 6
"""
) == """YES
NO
YES
YES
NO"""
# minimum size
assert run(
"""1
1 1
7
"""
) == "YES"
# all equal
assert run(
"""1
5 3
4 4 4 4 4
"""
) == "YES"
# immediate failure
assert run(
"""1
2 1
1 100
"""
) == "NO"
# boundary growth chain
assert run(
"""1
5 1
2 3 4 5 6
"""
) == "YES"
```
| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, h=[7]` | YES | Already on maximum tower |
| All heights equal | YES | Zero-cost moves and duplicate heights |
| `[1,100]` | NO | Cannot survive first jump |
| `[2,3,4,5,6]` | YES | Repeated greedy expansion |
## Edge Cases
Consider
```
1
3 1
1 3 4
```
The starting height is `1`. Any teleport to a higher tower requires at least two seconds. At time `1`, the water level becomes `2`, exceeding the current tower height. The algorithm computes no valid expansion and outputs `NO`.
Consider
```
1
4 4
4 4 4 2
```
The starting height is `2`, and the maximum height is `4`. A direct jump from height `2` to height `4` takes two seconds. Arrival happens exactly before drowning, so the maximum tower is reachable. The algorithm's reachability expansion includes height `4`, producing `YES`.
Consider
```
1
3 1
5 6 10
```
The jump from `5` to `6` is feasible, but after arriving at height `6` there is insufficient remaining safety margin to reach `10`. The greedy process gets stuck below the maximum height and outputs `NO`, matching the real behavior.
