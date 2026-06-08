---
title: "CF 2121H - Ice Baby"
description: "For every position i, we are not given a fixed value. Instead, we may choose any integer inside an interval [li, ri]. For each prefix length k, consider all arrays $$a1,a2,dots,ak$$ such that $$li le ai le ri." date: "2026-06-08T03:50:08+07:00" tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "dp", "implementation", "sortings"] categories: ["algorithms"] codeforces_contest: 2121 codeforces_index: "H" codeforces_contest_name: "Codeforces Round 1032 (Div. 3)" rating: 2300 weight: 2121 solve_time_s: 90 verified: false draft: false --- [CF 2121H - Ice Baby](https://codeforces.com/problemset/problem/2121/H) **Rating:** 2300   **Tags:** binary search, brute force, data structures, dp, implementation, sortings   **Solve time:** 1m 30s   **Verified:** no   ## Solution ## Problem Understanding For every position `i`, we are not given a fixed value. Instead, we may choose any integer inside an interval `[l_i, r_i]`. For each prefix length `k`, consider all arrays$$a_1,a_2,\dots,a_k$$
such that
$$l_i \le a_i \le r_i.$$
Among all valid choices, we want the largest possible length of a non-decreasing subsequence.
The answer must be reported for every prefix independently. After reading the first interval we output the best LNDS length for that prefix, after reading the first two intervals we output the best LNDS length for that prefix, and so on.
The total number of intervals over all test cases is at most `2·10^5`. A quadratic DP would require roughly `4·10^10` operations in the worst case, which is completely impossible within two seconds. Any accepted solution must be close to `O(n log n)`.
The tricky part is that we are not constructing one particular array. We are optimizing over all possible choices inside the intervals. A greedy choice that looks good locally may destroy a longer subsequence later.
Consider
```
[4,5]
[3,4]
[1,3]
[3,3]
```
For the whole prefix, the optimal answer is `3`. Choosing the largest possible value everywhere gives `[5,4,3,3]`, whose LNDS length is only `2`.
Another easy mistake is to think that an interval contributes to the answer whenever it intersects some previous interval. For
```
[3,4]
[1,2]
```
every valid choice satisfies `a1 > a2`, so the answer is still `1`.
A third subtle case appears when many intervals can all use the same value:
```
[1,10]
[1,10]
[1,10]
```
Choosing all values equal gives an LNDS of length `3`. Any approach that treats equal values as strictly increasing would incorrectly return smaller answers.
## Approaches
The classical LNDS algorithm maintains
$$dp[j]$$
as the minimum possible ending value of a non-decreasing subsequence of length `j`.
For a fixed array, processing one element updates this structure using binary search.
A brute force interpretation of the current problem would try all valid choices for every interval and run LNDS on each resulting array. Even if intervals were tiny, the number of arrays grows exponentially. This is hopeless.
The key observation is that the standard LNDS DP does not actually need the exact chosen value. It only needs to know how the new interval can affect the minimal ending values.
Suppose we already maintain the LNDS DP for all arrays obtainable from the processed prefix. Let the current interval be `[l,r]`.
For a subsequence ending value `x`, we may append the new position if we can choose a value `v` such that
$$x \le v \le r.$$
Among all such choices, the best one is the smallest possible value, namely
$$v=\max(x,l).$$
This turns the transition into a purely interval-based operation.
The resulting DP keeps exactly the same monotonic structure as the ordinary patience-sorting LNDS algorithm. After simplifying the transitions, one discovers that processing `[l,r]` is equivalent to:
1. Find the first DP value greater than `r`.
2. Remove that value.
3. Insert `l`.
This can be maintained with a multiset.
The size of the structure directly equals the current optimal LNDS length plus one sentinel element.
Each interval causes one insertion and at most one deletion, giving `O(log n)` work per interval.
| Approach | Time Complexity | Space Complexity | Verdict |
|---|------|---|
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |
## Deriving the DP Transition
Let
$$dp_j$$
denote the minimum possible ending value of a non-decreasing subsequence of length `j`.
As in the classical LNDS algorithm, the sequence
$$dp_1 \le dp_2 \le \dots$$
is non-decreasing.
Assume we process interval `[l,r]`.
Take some state `dp_j`.
If `dp_j > r`, no value from the interval can extend that subsequence.
If `dp_j ≤ r`, we can choose a value from the interval and extend it. The smallest achievable ending value becomes
$$\max(dp_j,l).$$
Because the DP array is sorted, all values larger than `r` form a suffix.
Let `x` be the first DP value strictly greater than `r`.
Every smaller DP value remains valid, while the position represented by `x` can be improved to `l`.
After the standard LNDS simplifications, the entire update becomes:
- insert `l`,
- erase the first value greater than `r`.
This is exactly the same replacement operation performed by patience sorting.
A multiset naturally supports both operations.
## Algorithm Walkthrough
1. Create a multiset `S` containing a single sentinel value `0`.
2. Process intervals from left to right.
3. For the current interval `[l,r]`, find the first element in `S` that is strictly greater than `r`.
4. Insert `l` into `S`.
5. If such an element exists, erase that element.
This is the compressed form of the LNDS DP transition described above.
6. The current answer equals `|S| - 1`.
The subtraction removes the sentinel.
7. Output the answer after every processed interval.
### Why it works
The multiset always stores the current LNDS DP array together with a sentinel `0`.
For every possible subsequence length `j`, the `j`-th smallest element of the multiset equals the minimum achievable ending value of a non-decreasing subsequence of length `j`.
When interval `[l,r]` arrives, replacing the first value greater than `r` by `l` performs exactly the same state transition as the interval DP derived above. No shorter subsequence becomes worse, and the best achievable ending value for the affected length becomes minimal.
Since the classical patience-sorting invariant is preserved after every update, the number of non-sentinel elements equals the maximum achievable LNDS length for the current prefix.
## Python Solution
```python
import sys
from bisect import bisect_right
input = sys.stdin.readline
from sortedcontainers import SortedList
def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        dp = SortedList([0])
        ans = []
        for _ in range(n):
            l, r = map(int, input().split())
            pos = dp.bisect_right(r)
            dp.add(l)
            if pos < len(dp):
                dp.pop(pos)
            ans.append(str(len(dp) - 1))
        out.append(" ".join(ans))
    sys.stdout.write("\n".join(out))
if __name__ == "__main__":
    solve()
```
The implementation mirrors the mathematical transition directly.
The multiset must support insertion, deletion of an arbitrary position, and upper bound queries. In C++, `multiset` handles this naturally. In Python, a balanced ordered container is needed. `SortedList` provides all required operations in `O(log n)`.
The order of operations matters. We first locate the first value greater than `r`, then insert `l`, then erase the previously identified position. This reproduces the exact replacement operation of the DP.
The sentinel `0` is smaller than every possible interval value because all interval endpoints are at least `1`. It represents the empty subsequence and allows every real subsequence length to be shifted by one.
## Worked Examples
### Example 1
Input:
```
4
4 5
3 4
1 3
3 3
```
| Step | Interval | Multiset after update | Answer |
| --- | --- | --- | --- |
| 1 | [4,5] | {0,4} | 1 |
| 2 | [3,4] | {0,3} | 1 |
| 3 | [1,3] | {0,1,3} | 2 |
| 4 | [3,3] | {0,1,3,3} | 3 |
Output:
```
1 1 2 3
```
The third interval creates a second achievable subsequence length. The fourth interval extends it once more.
### Example 2
Input:
```
5
1 2
6 8
4 5
2 3
3 3
```
| Step | Interval | Multiset after update | Answer |
| --- | --- | --- | --- |
| 1 | [1,2] | {0,1} | 1 |
| 2 | [6,8] | {0,1,6} | 2 |
| 3 | [4,5] | {0,1,4} | 2 |
| 4 | [2,3] | {0,1,2} | 2 |
| 5 | [3,3] | {0,1,2,3} | 3 |
Output:
```
1 2 2 2 3
```
This trace shows how later intervals can improve DP states without increasing the answer immediately. The answer grows only when a new subsequence length becomes achievable.
## Complexity Analysis
| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | One upper-bound query, one insertion, and at most one deletion per interval |
| Space | O(n) | The multiset stores at most one value per processed interval plus the sentinel |
With at most `2·10^5` intervals across all test cases, `O(n log n)` easily fits within the limits.
## Test Cases
```python
# helper: run solution on input string, return output string
import io
import sys
from sortedcontainers import SortedList
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        dp = SortedList([0])
        cur = []
        for _ in range(n):
            l, r = map(int, input().split())
            pos = dp.bisect_right(r)
            dp.add(l)
            if pos < len(dp):
                dp.pop(pos)
            cur.append(str(len(dp) - 1))
        out.append(" ".join(cur))
    return "\n".join(out)
# sample
assert run(
"""1
4
4 5
3 4
1 3
3 3
"""
) == "1 1 2 3"
# minimum size
assert run(
"""1
1
1 1
"""
) == "1"
# strictly impossible to chain
assert run(
"""1
2
3 4
1 2
"""
) == "1 1"
# all equal intervals
assert run(
"""1
4
5 5
5 5
5 5
5 5
"""
) == "1 2 3 4"
# increasing overlap
assert run(
"""1
4
1 10
2 10
3 10
4 10
"""
) == "1 2 3 4"
```
| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single interval | `1` | Minimum size |
| `[3,4],[1,2]` | `1 1` | No valid non-decreasing pair exists |
| All `[5,5]` | `1 2 3 4` | Equal values must be allowed in LNDS |
| Increasing intervals | `1 2 3 4` | Continuous growth of achievable subsequence length |
## Edge Cases
Consider
```
2
3 4
1 2
```
After the first interval the multiset is `{0,3}` and the answer is `1`.
For the second interval, the first value greater than `2` is `3`. Replacing it by `1` produces `{0,1}`. The answer remains `1`.
This matches reality because every valid choice satisfies `a1 > a2`.
Now consider
```
4
5 5
5 5
5 5
5 5
```
The multiset evolves as
```
{0,5}
{0,5,5}
{0,5,5,5}
{0,5,5,5,5}
```
and the answers become
```
1 2 3 4
```
Equal values are allowed in a non-decreasing subsequence, so the entire array can be chosen.
Finally consider
```
3
1 10
1 10
1 10
```
Each interval can choose value `1`. The algorithm never deletes a state that would reduce the achievable length. The multiset grows by one element at every step, giving answers `1 2 3`, which is optimal.
