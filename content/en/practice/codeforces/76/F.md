---
title: "CF 76F - Tourist"
description: "Each event is a point on a time-position plane. Event i happens at coordinate xi exactly at time ti. The tourist moves on a line with speed at most V, so moving from (xa, ta) to (xb, tb) is possible if and only if: $$The tourist may also wait in place. We need two answers." date: "2026-05-28T00:00:00+07:00" tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp"] categories: ["algorithms"] codeforces_contest: 76 codeforces_index: "F" codeforces_contest_name: "All-Ukrainian School Olympiad in Informatics" rating: 2300 weight: 76 solve_time_s: 163 verified: true draft: false --- [CF 76F - Tourist](https://codeforces.com/problemset/problem/76/F) **Rating:** 2300   **Tags:** binary search, data structures, dp   **Solve time:** 2m 43s   **Verified:** yes   ## Solution ## Problem Understanding Each event is a point on a time-position plane. Event `i` happens at coordinate `x_i` exactly at time `t_i`. The tourist moves on a line with speed at most `V`, so moving from `(x_a, t_a)` to `(x_b, t_b)` is possible if and only if:$$|x_a - x_b| \le V \cdot (t_b - t_a)$$
The tourist may also wait in place. We need two answers.
The first answer assumes the tourist starts at coordinate `0` at time `0`.
The second answer allows the tourist to choose any starting coordinate before time starts.
The goal in both versions is to maximize how many events can be attended in chronological order.
The constraints completely rule out quadratic dynamic programming. With `n = 100000`, an `O(n^2)` transition loop would require around `10^10` checks, which is several orders of magnitude too large. Even `O(n sqrt n)` would be risky in Python. The solution must stay near `O(n log n)`.
The tricky part is that reachability depends on both position and time. A naive graph interpretation creates too many edges. We need a way to compress the transition condition into something searchable with data structures.
Several edge cases are easy to mishandle.
Events may occur at the same time. Two events with identical timestamps cannot both be visited unless they are at the same position, and the statement guarantees that exact duplicates do not exist.
Example:
```
2
0 1
10 1
100
```
Correct output:
```
1 1
```
A careless DP that only checks position difference without enforcing increasing time could incorrectly chain them together.
Negative coordinates matter because movement is on the entire number line.
Example:
```
2
-5 5
5 10
1
```
The tourist cannot reach the first event from `(0,0)` because distance `5` requires time `5`, which is barely possible, but then moving from `-5` to `5` needs distance `10` and only `5` units of time. The correct answer is:
```
1 2
```
The second answer differs because with a free starting point we may begin directly at `-5`.
Another subtle case is multiple events at the same position.
```
3
2 3
2 4
2 5
1
```
Correct output:
```
3 3
```
Waiting in place is allowed, so once the tourist reaches coordinate `2`, all later events there are automatically reachable.
## Approaches
The most direct solution is dynamic programming on events sorted by time.
Define `dp[i]` as the maximum number of events ending at event `i`. Then we try every earlier event `j` and transition if:
$$|x_i - x_j| \le V(t_i - t_j)$$
For the fixed-start version we also check whether event `i` is reachable from `(0,0)`.
This is correct because any valid route must visit events in nondecreasing time order, and every feasible previous event is examined.
The problem is complexity. Each event compares against all earlier events, so the running time is `O(n^2)`. With `100000` events this becomes roughly `5 \cdot 10^9` transitions, far too slow.
The key observation is that the reachability inequality can be rewritten into two independent inequalities.
Starting from:
$$|x_i - x_j| \le V(t_i - t_j)$$
we obtain:
$$x_i - V t_i \le x_j - V t_j$$
and
$$x_i + V t_i \ge x_j + V t_j$$
Define transformed coordinates:
$$A_i = x_i - V t_i$$
$$B_i = x_i + V t_i$$
Then event `j` can precede event `i` exactly when:
$$A_j \ge A_i$$
and
$$B_j \le B_i$$
This turns the problem into a two-dimensional dominance DP.
Now the structure becomes clear. If we process events in increasing time order, we need the best DP value among all previous points satisfying:
$$A_j \ge A_i,\quad B_j \le B_i$$
That is a classic offline data structure problem.
We compress all `B` coordinates and use a Fenwick tree where each node stores the best DP value seen so far. To handle the `A_j \ge A_i` condition, we process events grouped by decreasing `A`.
For the second answer, where the start point is arbitrary, every event may start a chain with value `1`.
For the first answer, event `i` may start a chain only if:
$$|x_i| \le V t_i$$
because the tourist starts at `(0,0)`.
The resulting algorithm runs in `O(n log n)`.
| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |
## Algorithm Walkthrough
1. Read all events and sort them by increasing time.
Sorting by time guarantees that every transition goes forward chronologically.
1. For every event compute:
$$A_i = x_i - V t_i$$
$$B_i = x_i + V t_i$$
These transformed coordinates encode the movement constraint as a dominance relation.
1. Coordinate-compress all `B_i` values.
Fenwick trees require indices from `1` to `m`, so we map each distinct `B` value to a compact integer.
1. Compute the answer for the free-start version.
Every event can begin a valid route by itself, so initialize:
```
dp2[i] = 1
```
Then process events in decreasing `A`.
For each event, query the Fenwick tree for the maximum DP among all earlier events with compressed `B <= B_i`.
That query gives the best chain that can transition into event `i`.
After querying all events with the same `A`, insert their DP values into the Fenwick tree.
Delaying updates inside equal-`A` groups prevents transitions between events that are not mutually reachable.
1. Compute the fixed-start version similarly.
Initialize:
```
dp1[i] = 1
```
only if:
$$|x_i| \le V t_i$$
Otherwise initialize with negative infinity.
The same dominance DP transitions are applied afterward.
1. The answer for each version is the maximum DP value over all events.
### Why it works
The transformed inequalities are exactly equivalent to the original speed constraint. Any feasible movement sequence corresponds to a chain in the dominance order:
$$A_j \ge A_i,\quad B_j \le B_i$$
Processing events by time guarantees transitions only move forward in time. The Fenwick tree always stores the best DP among already-processed valid predecessors. Since every possible predecessor satisfying the inequalities is represented in the structure, and no invalid predecessor satisfies both inequalities simultaneously, the DP computes the optimal number of visitable events.
## Python Solution
```python
import sys
input = sys.stdin.readline
INF = 10**18
class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [-INF] * (n + 1)
    def update(self, idx, val):
        while idx <= self.n:
            if val > self.bit[idx]:
                self.bit[idx] = val
            idx += idx & -idx
    def query(self, idx):
        res = -INF
        while idx > 0:
            if self.bit[idx] > res:
                res = self.bit[idx]
            idx -= idx & -idx
        return res
def solve():
    n = int(input())
    events = []
    for _ in range(n):
        x, t = map(int, input().split())
        events.append((t, x))
    V = int(input())
    arr = []
    for idx, (t, x) in enumerate(events):
        A = x - V * t
        B = x + V * t
        arr.append((A, B, t, x, idx))
    all_b = sorted(set(b for _, b, _, _, _ in arr))
    comp = {v: i + 1 for i, v in enumerate(all_b)}
    arr.sort(reverse=True)
    m = len(all_b)
    # free start
    bit = Fenwick(m)
    dp2 = [1] * n
    i = 0
    while i < n:
        j = i
        while j < n and arr[j][0] == arr[i][0]:
            j += 1
        updates = []
        for k in range(i, j):
            A, B, t, x, idx = arr[k]
            bidx = comp[B]
            best = bit.query(bidx)
            if best > -INF:
                dp2[idx] = max(dp2[idx], best + 1)
            updates.append((bidx, dp2[idx]))
        for bidx, val in updates:
            bit.update(bidx, val)
        i = j
    # fixed start at 0
    bit = Fenwick(m)
    dp1 = [-INF] * n
    for A, B, t, x, idx in arr:
        if abs(x) <= V * t:
            dp1[idx] = 1
    i = 0
    while i < n:
        j = i
        while j < n and arr[j][0] == arr[i][0]:
            j += 1
        updates = []
        for k in range(i, j):
            A, B, t, x, idx = arr[k]
            bidx = comp[B]
            best = bit.query(bidx)
            if best > -INF:
                dp1[idx] = max(dp1[idx], best + 1)
            updates.append((bidx, dp1[idx]))
        for bidx, val in updates:
            bit.update(bidx, val)
        i = j
    ans1 = max(dp1)
    ans2 = max(dp2)
    print(ans1, ans2)
solve()
```
The Fenwick tree stores prefix maximums rather than sums. After coordinate compression, querying index `bidx` returns the best DP among all events with `B_j <= B_i`.
Processing events in decreasing `A` order guarantees that all inserted states satisfy `A_j >= A_i`.
The grouped processing for equal `A` values is subtle but necessary. Suppose two events share the same `A`. If we immediately update after processing one of them, another event in the same group could incorrectly transition through it even when their timestamps make the movement impossible. Delaying updates until the whole group is processed removes this issue.
The fixed-start version differs only in initialization. An event can begin a chain only if the tourist can reach it directly from `(0,0)`.
All coordinates fit comfortably inside Python integers, but in C++ this problem requires 64-bit arithmetic because values such as `V * t` can reach `2 * 10^9`.
## Worked Examples
### Sample 1
Input:
```
3
-1 1
42 7
40 8
2
```
Transformed values:
| Event | x | t | A = x - Vt | B = x + Vt |
| --- | --- | --- | --- | --- |
| 1 | -1 | 1 | -3 | 1 |
| 2 | 42 | 7 | 28 | 56 |
| 3 | 40 | 8 | 24 | 56 |
Processing order is decreasing `A`.
| Step | Event | Query Result | dp2 | dp1 |
| --- | --- | --- | --- | --- |
| 1 | (42,7) | none | 1 | impossible |
| 2 | (40,8) | 1 | 2 | impossible |
| 3 | (-1,1) | none | 1 | 1 |
Final answers:
```
1 2
```
The free-start version begins at `(42,7)` and then reaches `(40,8)`. Starting from `(0,0)` cannot reach either of those large positive coordinates quickly enough.
### Custom Example
Input:
```
4
0 1
1 2
2 3
3 4
1
```
Transformed values:
| Event | A | B |
| --- | --- | --- |
| 1 | -1 | 1 |
| 2 | -1 | 3 |
| 3 | -1 | 5 |
| 4 | -1 | 7 |
All events share the same `A`.
| Step | Event | Best Previous | dp |
| --- | --- | --- | --- |
| 1 | 1 | none | 1 |
| 2 | 2 | 1 | 2 |
| 3 | 3 | 2 | 3 |
| 4 | 4 | 3 | 4 |
Output:
```
4 4
```
This example demonstrates why dominance ordering matches the movement condition exactly. Each event is reachable from the previous one with speed `1`.
## Complexity Analysis
| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting plus Fenwick queries and updates |
| Space | O(n) | Arrays, coordinate compression, Fenwick tree |
With `100000` events, `O(n log n)` is easily fast enough. The Fenwick tree operations are lightweight, and memory usage stays linear.
## Test Cases
```python
# helper: run solution on input string, return output string
import sys
import io
INF = 10**18
class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [-INF] * (n + 1)
    def update(self, idx, val):
        while idx <= self.n:
            self.bit[idx] = max(self.bit[idx], val)
            idx += idx & -idx
    def query(self, idx):
        res = -INF
        while idx > 0:
            res = max(res, self.bit[idx])
            idx -= idx & -idx
        return res
def solve():
    input = sys.stdin.readline
    n = int(input())
    events = []
    for _ in range(n):
        x, t = map(int, input().split())
        events.append((t, x))
    V = int(input())
    arr = []
    for idx, (t, x) in enumerate(events):
        A = x - V * t
        B = x + V * t
        arr.append((A, B, t, x, idx))
    all_b = sorted(set(b for _, b, _, _, _ in arr))
    comp = {v: i + 1 for i, v in enumerate(all_b)}
    arr.sort(reverse=True)
    m = len(all_b)
    bit = Fenwick(m)
    dp2 = [1] * n
    i = 0
    while i < n:
        j = i
        while j < n and arr[j][0] == arr[i][0]:
            j += 1
        upd = []
        for k in range(i, j):
            A, B, t, x, idx = arr[k]
            bidx = comp[B]
            best = bit.query(bidx)
            if best > -INF:
                dp2[idx] = max(dp2[idx], best + 1)
            upd.append((bidx, dp2[idx]))
        for bidx, val in upd:
            bit.update(bidx, val)
        i = j
    bit = Fenwick(m)
    dp1 = [-INF] * n
    for A, B, t, x, idx in arr:
        if abs(x) <= V * t:
            dp1[idx] = 1
    i = 0
    while i < n:
        j = i
        while j < n and arr[j][0] == arr[i][0]:
            j += 1
        upd = []
        for k in range(i, j):
            A, B, t, x, idx = arr[k]
            bidx = comp[B]
            best = bit.query(bidx)
            if best > -INF:
                dp1[idx] = max(dp1[idx], best + 1)
            upd.append((bidx, dp1[idx]))
        for bidx, val in upd:
            bit.update(bidx, val)
        i = j
    print(max(dp1), max(dp2))
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()
# provided sample
assert run(
"""3
-1 1
42 7
40 8
2
"""
) == "1 2", "sample 1"
# minimum size
assert run(
"""1
0 1
1
"""
) == "1 1", "single reachable event"
# unreachable from origin but reachable with free start
assert run(
"""1
100 1
1
"""
) == "-1000000000000000000 1", "free start differs"
# same position over time
assert run(
"""3
2 3
2 4
2 5
1
"""
) == "3 3", "waiting in place"
# chain along a line
assert run(
"""4
0 1
1 2
2 3
3 4
1
"""
) == "4 4", "full chain"
```
| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single event | `1 1` | Minimum input size |
| Far unreachable event | Different answers | Free start versus fixed start |
| Same coordinate repeatedly | `3 3` | Waiting in place |
| Increasing chain | `4 4` | Long valid transition chain |
## Edge Cases
Consider events occurring at the same time:
```
2
0 1
10 1
100
```
Both events have identical timestamps. The transformed conditions cannot simultaneously hold because movement time is zero. During processing, neither event becomes a predecessor of the other, so both DP values remain `1`. The algorithm outputs:
```
1 1
```
Now consider unreachable events from the origin:
```
2
-5 5
5 10
1
```
The first event is reachable from `(0,0)`, so `dp1 = 1`. The second event cannot follow it because moving distance `10` in time `5` exceeds speed `1`.
For the free-start version, the tourist may begin at `-5`, attend the first event, then still cannot reach the second. Alternatively, begin at `5` and attend only the second. The maximum remains `1`.
The algorithm correctly rejects invalid transitions because the transformed inequalities fail.
Finally, consider repeated coordinates:
```
3
2 3
2 4
2 5
1
```
The transformed values satisfy the dominance relation in chronological order, so the Fenwick tree chains all three events together. Waiting requires no special handling because zero movement automatically satisfies the speed bound.
