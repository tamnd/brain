---
title: "CF 1806B - Mex Master"
description: "We are given an array and may permute its elements however we like. After choosing an ordering, we build a new array consisting of sums of neighboring elements: $$b=[a1+a2, a2+a3, ldots, a{n-1}+an]." date: "2026-06-09T09:11:13+07:00" tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"] categories: ["algorithms"] codeforces_contest: 1806 codeforces_index: "B" codeforces_contest_name: "Codeforces Round 858 (Div. 2)" rating: 900 weight: 1806 solve_time_s: 290 verified: false draft: false --- [CF 1806B - Mex Master](https://codeforces.com/problemset/problem/1806/B) **Rating:** 900   **Tags:** constructive algorithms, greedy   **Solve time:** 4m 50s   **Verified:** no   ## Solution ## Problem Understanding We are given an array and may permute its elements however we like. After choosing an ordering, we build a new array consisting of sums of neighboring elements:$$b=[a_1+a_2,\ a_2+a_3,\ \ldots,\ a_{n-1}+a_n].$$
The score of the arrangement is the MEX of $b$, where MEX is the smallest non-negative integer that does not appear.
Our task is not to construct the optimal ordering. We only need the minimum possible score obtainable after rearranging the original numbers.
The constraints immediately suggest that the answer must come from a simple structural observation. The total length over all test cases is only $2\cdot 10^5$, so an $O(n)$ or $O(n \log n)$ solution per test case is easily fast enough. Any approach that tries many permutations is hopeless because even $n=20$ already makes enumeration impossible.
The interesting part is that only the values $0$, $1$, and "greater than $1$" matter.
Consider a few edge cases.
If there is a positive number between every pair of zeros, then no adjacent pair sums to $0$. For example:
```
0 1 0
```
The adjacent sums are:
```
1 1
```
MEX is $0$.
A careless solution that only checks whether zeros exist would incorrectly return $1$.
Now consider:
```
0 0
```
The only adjacent sum is:
```
0
```
MEX is $1$.
Finally:
```
0 0 0 2
```
No matter how we arrange the numbers, at least one adjacent pair of zeros exists. That creates a sum $0$. At the same time, every positive number is at least $2$, so sum $1$ can never appear. The resulting minimum MEX is $1$.
These examples already hint that only the counts of zeros and ones control the answer.
## Approaches
A brute-force solution would try every permutation of the array. For each permutation it would build the adjacent-sum array, compute its MEX, and keep the minimum.
This is correct because it directly checks every possible arrangement. Unfortunately, it requires $n!$ permutations. Even $n=12$ would already be completely infeasible.
The key observation is that the minimum possible MEX can only be $0$, $1$, or $2$.
To obtain MEX $0$, we need to avoid creating a sum equal to $0$. Since all values are non-negative, the only way to get a sum $0$ is with two adjacent zeros.
Thus MEX $0$ is possible exactly when we can arrange the array so that no two zeros are adjacent.
Suppose there are $z$ zeros and $p=n-z$ positive numbers.
Each positive number can separate at most one gap between consecutive zeros. To place all zeros without adjacency we need
$$z \le p+1.$$
Equivalently,
$$z \le n-z+1.$$
If this holds, we can eliminate all occurrences of $0$ from the adjacent-sum array, so MEX becomes $0$.
Now assume $z>p+1$. Then some pair of adjacent zeros is unavoidable, so $0$ must appear.
Can we make MEX equal to $1$? We need $0$ to appear but $1$ not to appear.
A sum $1$ can only be produced by $0+1$, because all numbers are non-negative integers.
If the array contains no ones, then sum $1$ is impossible, hence the answer is immediately $1$.
The only remaining situation is:
$$z>p+1$$
and there is at least one value equal to $1$.
Then $0$ is unavoidable, and some $0+1$ adjacency is also unavoidable. In that case both $0$ and $1$ appear, so the minimum MEX is $2$.
This completely determines the answer.
| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!\cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |
## Algorithm Walkthrough
1. Count the number of zeros, call it $z$.
2. Count the number of ones, call it $o$.
3. Let $p=n-z$, the number of positive elements.
4. If $z \le p+1$, output $0$.
In this case the zeros can be separated by positive elements, so no adjacent pair sums to $0$. Since $0$ is absent from the adjacent-sum array, its MEX is $0$.
5. Otherwise, some adjacent pair of zeros is unavoidable, so $0$ appears.
6. If $o=0$, output $1$.
A sum $1$ requires a $0$ and a $1$. Without any ones, sum $1$ cannot occur.
7. Otherwise output $2$.
Here $0$ appears because adjacent zeros are unavoidable, and $1$ can also be forced to appear because a $1$ exists. The smallest missing value becomes $2$.
### Why it works
The only way to create sum $0$ is with adjacent zeros. Therefore the possibility of achieving MEX $0$ depends entirely on whether all zeros can be separated.
If zeros cannot all be separated, then $0$ necessarily belongs to the adjacent-sum array. The next question becomes whether $1$ can be avoided.
Because all values are non-negative, the only representation of $1$ as a sum of two array elements is $0+1$. If no element equal to $1$ exists, then sum $1$ is impossible and the MEX is $1$. Otherwise both $0$ and $1$ occur, forcing the MEX to be $2$.
No other answer is possible.
## Python Solution
```python
import sys
input = sys.stdin.readline
def solve():
    t = int(input())
    ans = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        zeros = a.count(0)
        ones = a.count(1)
        positive = n - zeros
        if zeros <= positive + 1:
            ans.append("0")
        elif ones == 0:
            ans.append("1")
        else:
            ans.append("2")
    sys.stdout.write("\n".join(ans))
if __name__ == "__main__":
    solve()
```
The implementation follows the proof directly.
The variable `zeros` determines whether adjacent zeros can be avoided. The condition `zeros <= positive + 1` is exactly the separator condition derived above.
If adjacent zeros are unavoidable, we only need to know whether any element equals `1`. No other value matters because only `0+1` can produce a sum equal to `1`.
All arithmetic easily fits in standard Python integers.
## Worked Examples
### Example 1
Input:
```
3
0 0 1
```
| Quantity | Value |
| --- | --- |
| zeros | 2 |
| ones | 1 |
| positive | 1 |
| check | $2 \le 1+1$ |
Since the condition holds, zeros can be separated:
```
0 1 0
```
Adjacent sums:
```
1 1
```
MEX is $0$.
Answer:
```
0
```
This demonstrates that merely having zeros does not force sum $0$ to appear.
### Example 2
Input:
```
8
1 0 0 0 2 0 3 0
```
| Quantity | Value |
| --- | --- |
| zeros | 5 |
| ones | 1 |
| positive | 3 |
| check | $5 \le 3+1$ is false |
Adjacent zeros are unavoidable, so $0$ appears.
A value $1$ exists, hence sum $1$ can also occur.
Therefore both $0$ and $1$ belong to the adjacent-sum array, making the minimum MEX equal to $2$.
Answer:
```
2
```
This is exactly the third sample.
## Complexity Analysis
| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass to count zeros and ones |
| Space | $O(1)$ | Only a few counters are stored |
The total input size over all test cases is at most $2\cdot10^5$, so a linear scan of every array easily fits within the limits.
## Test Cases
```python
import sys
import io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        zeros = a.count(0)
        ones = a.count(1)
        positive = n - zeros
        if zeros <= positive + 1:
            out.append("0")
        elif ones == 0:
            out.append("1")
        else:
            out.append("2")
    return "\n".join(out)
# provided samples
assert run(
"""3
2
0 0
3
0 0 1
8
1 0 0 0 2 0 3 0
"""
) == "1\n0\n2"
# minimum size
assert run(
"""1
2
5 7
"""
) == "0"
# all zeros
assert run(
"""1
5
0 0 0 0 0
"""
) == "1"
# many zeros and a one
assert run(
"""1
5
0 0 0 0 1
"""
) == "2"
# enough positive separators
assert run(
"""1
6
0 0 1 2 3 4
"""
) == "0"
```
| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 7` | `0` | No zero sum can exist |
| `0 0 0 0 0` | `1` | Adjacent zeros unavoidable, no ones |
| `0 0 0 0 1` | `2` | Adjacent zeros unavoidable, one exists |
| `0 0 1 2 3 4` | `0` | Positive numbers can separate all zeros |
## Edge Cases
Consider:
```
2
0 0
```
Here `zeros = 2`, `positive = 0`. The condition `2 <= 1` is false. There are no ones, so the answer is `1`. The only adjacent sum is `0`, whose MEX is indeed `1`.
Consider:
```
3
0 0 1
```
Here `zeros = 2`, `positive = 1`. The condition `2 <= 2` is true. We can arrange the numbers as `0 1 0`, producing adjacent sums `1, 1`. Since `0` is absent, the answer is `0`.
Consider:
```
5
0 0 0 0 1
```
Here `zeros = 4`, `positive = 1`. The condition `4 <= 2` is false, so some adjacent zeros must exist. Since a `1` is present, both sums `0` and `1` can occur. The answer is `2`.
These cases cover every possible branch of the solution.
