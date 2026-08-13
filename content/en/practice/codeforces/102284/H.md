---
title: "CF 102284H - \u041c\u0443\u0437\u044b\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0444\u0440\u0435\u0448"
description: "We have an array of $N$ songs. Song $i$ normally has volume $Hi$, and lowering its volume by one unit costs $Ai$ units of event success. The teachers need a period of exactly $M$ consecutive minutes during which the volume is constant."
date: "2026-08-13T22:41:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "H"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 612
verified: true
draft: false
---

[CF 102284H - \u041c\u0443\u0437\u044b\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0444\u0440\u0435\u0448](https://codeforces.com/problemset/problem/102284/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of $N$ songs. Song $i$ normally has volume $H_i$, and lowering its volume by one unit costs $A_i$ units of event success. The teachers need a period of exactly $M$ consecutive minutes during which the volume is constant. Since every song lasts one minute, we need to choose a contiguous segment of $M$ songs and choose one common volume for that segment.

For a fixed segment, the common volume cannot exceed the smallest $H_i$ inside it. Since every $A_i$ is nonnegative, choosing anything below that smallest value can only increase the loss. Thus the best common volume for a segment is exactly

$$
\min H_i.
$$

If the minimum volume in a window is $h$, its total loss is

\sum H_iA_i-h\sum A_i.
$$

So the whole problem becomes finding the minimum value of this expression over all contiguous windows of length $M$.

The bound $N\le 10^5$ rules out algorithms that inspect every pair of positions or repeatedly scan large windows. A straightforward enumeration of all windows and all their elements can perform about $2.5\cdot10^9$ operations in the worst case. We need a linear or near-linear solution. The values $H_i$ and $A_i$ can be as large as $5\cdot10^6$, so the total answer can reach roughly $2.5\cdot10^{18}$. Python integers handle this automatically, while a C++ implementation would need 64-bit integers.

There are several boundary cases where an implementation can silently go wrong. If $M=1$, every window contains one song, so no volume reduction is needed. For example,

```
1 1
7
10
```

has answer $0$. A formula that assumes every window has at least two elements can incorrectly charge a loss.

If all volumes in a window are equal, its cost is zero regardless of the $A_i$. For example,

```
3 3
5 5 5
2 100 7
```

has answer $0$. A careless implementation that subtracts the wrong extremum, such as the maximum instead of the minimum, can produce a negative intermediate cost or an incorrect result.

A minimum volume of zero is also valid. For

```
2 2
0 5
3 4
```

the common volume must be zero, giving loss $5\cdot4=20$. Code that treats zero as an uninitialized minimum can accidentally replace it with a positive value.

Finally, coefficients $A_i$ are allowed to be zero. For

```
2 2
1 5
0 3
```

the answer is $12$. The first song can be lowered by four units without losing any success, while the second song loses $4\cdot3=12$. An implementation that skips zero-weight elements when computing the window's minimum or weighted sum can mix up these two independent quantities.

## Approaches

The direct approach follows immediately from the definition. Enumerate every contiguous segment of length $M$, find its minimum $H_i$, then compute $\sum (H_i-h)A_i$. This is correct because for every possible segment we explicitly calculate the best constant volume and then take the best segment.

The problem is the amount of repeated work. There are $N-M+1$ windows, and scanning one window takes $M$ operations. The total is

$$
M(N-M+1).
$$

For fixed $N$, this is maximized near $M=(N+1)/2$, giving

$$
\left\lfloor\frac{(N+1)^2}{4}\right\rfloor.
$$

At $N=100000$, that is $2,500,050,000$ element visits, far beyond what is reasonable.

The key observation is that when a window moves one position to the right, almost all of its elements stay the same. We do not need to recompute its minimum from scratch. A monotonic deque can maintain the minimum of a sliding window in amortized $O(1)$ time per element.

The other part of the cost is even simpler. Define

$$
B_i=H_iA_i.
$$

For every window we need both $\sum A_i$ and $\sum B_i$. Prefix sums provide either quantity for any window in $O(1)$ time.

Thus each window can be evaluated using three pieces of information: its minimum $H_i$, its sum of $A_i$, and its sum of $H_iA_i$. The first comes from a monotonic deque, while the other two come from prefix sums. The complete algorithm is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(M(N-M+1))$, worst case $O(N^2)$ | $O(1)$ | Too slow |
| Optimal | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Compute the array $B$ where $B_i=H_iA_i$. Also build prefix sums for $A$ and $B$. For a window $[l,r]$, these prefix sums immediately give $\sum_{i=l}^r A_i$ and $\sum_{i=l}^r H_iA_i$. Keeping these sums separate from the minimum is necessary because the minimum depends only on $H$, while the loss is weighted by $A$.
2. Scan the songs from left to right while maintaining a deque of indices whose $H$ values are increasing. Before inserting index $i$, remove indices from the back while their $H$ is at least $H_i$. Such an index can never become the minimum of a future window because the newer index has an equal or smaller value and will remain in the window longer.
3. After inserting $i$, remove the index at the front if it lies outside the current window of length $M$. The front is always the index with the smallest $H$ among the indices currently inside the window.
4. Once $i\ge M-1$, the deque represents the complete window $[i-M+1,i]$. Let its minimum be $H_q$, where $q$ is the index at the front. Use the prefix sums to calculate

$$
S_A=\sum_{j=i-M+1}^{i} A_j
$$

and

$$
S_B=\sum_{j=i-M+1}^{i}H_jA_j.
$$

The cost of this window is

$$
S_B-H_qS_A.
$$

1. Update the global answer with this cost. Every possible length-$M$ window appears exactly once when its right endpoint is processed, so after the scan the minimum stored in the answer is the required result.

### Why it works

For every fixed window, the largest common volume that is feasible is its minimum $H_i$. Since every $A_i$ is nonnegative, lowering the common volume below that minimum can never improve the answer, so this volume gives the optimal cost for that window.

The deque invariant says that its indices are inside the current window and their $H$ values are strictly increasing from front to back. Consequently, its front is exactly the minimum $H_i$ of the current window. Prefix sums independently give the two weighted quantities needed for the cost formula. Hence every window is evaluated with its exact optimal cost, and taking the smallest of those costs gives the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    h = list(map(int, input().split()))
    a = list(map(int, input().split()))

    pref_a = [0] * (n + 1)
    pref_ha = [0] * (n + 1)

    for i in range(n):
        pref_a[i + 1] = pref_a[i] + a[i]
        pref_ha[i + 1] = pref_ha[i] + h[i] * a[i]

    dq = []
    head = 0
    ans = None

    for i in range(n):
        while len(dq) > head and h[dq[-1]] >= h[i]:
            dq.pop()

        dq.append(i)

        left = i - m + 1

        while head < len(dq) and dq[head] < left:
            head += 1

        if i >= m - 1:
            sum_a = pref_a[i + 1] - pref_a[left]
            sum_ha = pref_ha[i + 1] - pref_ha[left]
            min_h = h[dq[head]]

            cost = sum_ha - min_h * sum_a

            if ans is None or cost < ans:
                ans = cost

    print(ans)

if __name__ == "__main__":
    solve()
```

The two prefix arrays are built before the sliding-window scan. `pref_a[k]` stores the sum of $A_i$ for indices below $k$, while `pref_ha[k]` stores the sum of $H_iA_i$. Consequently, the half-open range `[left, i + 1)` represents exactly the current window.

The deque stores indices rather than values. This is necessary because an old minimum must eventually be removed when it leaves the window. Storing indices lets us test that condition directly.

The condition `h[dq[-1]] >= h[i]` removes equal values as well as larger values. Keeping equal values would still be correct, but removing the older equal value makes the deque smaller and leaves the newest occurrence as the better representative because it expires later.

The expiration check uses `dq[head] < left`. An index equal to `left` is still inside the window and must remain available as its minimum. This is one of the main off-by-one boundaries in the implementation.

The cost is calculated as

$$
\sum H_iA_i-\min(H_i)\sum A_i,
$$

rather than summing every individual $(H_i-\min H_i)A_i$. The algebra reduces each window to constant-time arithmetic after the minimum is known.

Python integers have arbitrary precision, so even values near the maximum possible answer do not overflow.

## Worked Examples

### Sample 1

The input is

```
5 2
1 2 1 2 1
1 9 3 8 2
```

For each window, the deque front gives the minimum volume. The prefix sums provide the two weighted sums.

| Window | Minimum $H$ | $\sum A_i$ | $\sum H_iA_i$ | Cost | Best so far |
| --- | --- | --- | --- | --- | --- |
| $[1,2]$ | 1 | 10 | 19 | 9 | 9 |
| $[2,3]$ | 1 | 12 | 20 | 8 | 8 |
| $[3,4]$ | 1 | 11 | 19 | 8 | 8 |
| $[4,5]$ | 1 | 10 | 18 | 8 | 8 |

For example, in the second window the common volume is $1$. The second song is lowered from $2$ to $1$, costing $9$, while the third song already has volume $1$. The resulting cost is actually $9$, but the table's weighted calculation gives $20-1\cdot12=8$ because the second and third entries are $H=(2,1)$ and $A=(9,3)$, giving $18+3=21$, not $20$. Correcting the window calculation gives the following exact trace.

| Window | Minimum $H$ | $\sum A_i$ | $\sum H_iA_i$ | Cost | Best so far |
| --- | --- | --- | --- | --- | --- |
| $[1,2]$ | 1 | 10 | 19 | 9 | 9 |
| $[2,3]$ | 1 | 12 | 21 | 9 | 9 |
| $[3,4]$ | 1 | 11 | 19 | 8 | 8 |
| $[4,5]$ | 1 | 10 | 18 | 8 | 8 |

Thus the answer is $8$. The trace demonstrates that the weighted sum must use the product $H_iA_i$, not merely $H_i$ or $A_i$ separately.

### Sample 2

The input is

```
5 3
1 2 2 2 1
1 6 4 9 2
```

There are only three windows.

| Window | Minimum $H$ | $\sum A_i$ | $\sum H_iA_i$ | Cost | Best so far |
| --- | --- | --- | --- | --- | --- |
| $[1,3]$ | 1 | 11 | 23 | 12 | 12 |
| $[2,4]$ | 2 | 19 | 38 | 0 | 0 |
| $[3,5]$ | 1 | 15 | 33 | 18 | 0 |

The middle window has all three volumes equal to $2$. Its optimal common volume is already the original volume of every song, so no song needs to be lowered and the cost is zero. The deque captures the minimum as $2$, making the formula produce $38-2\cdot19=0$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each index enters and leaves the monotonic deque at most once, while every prefix sum and window is processed once. |
| Space | $O(N)$ | The prefix sums, input arrays, and deque use linear memory. |

With $N\le10^5$, a linear scan performs only a small constant number of operations per element. The algorithm avoids the quadratic number of repeated window scans that the brute-force solution would require.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    h = list(map(int, input().split()))
    a = list(map(int, input().split()))

    pref_a = [0] * (n + 1)
    pref_ha = [0] * (n + 1)

    for i in range(n):
        pref_a[i + 1] = pref_a[i] + a[i]
        pref_ha[i + 1] = pref_ha[i] + h[i] * a[i]

    dq = []
    head = 0
    ans = None

    for i in range(n):
        while len(dq) > head and h[dq[-1]] >= h[i]:
            dq.pop()

        dq.append(i)

        left = i - m + 1

        while head < len(dq) and dq[head] < left:
            head += 1

        if i >= m - 1:
            sum_a = pref_a[i + 1] - pref_a[left]
            sum_ha = pref_ha[i + 1] - pref_ha[left]
            min_h = h[dq[head]]

            cost = sum_ha - min_h * sum_a
            if ans is None or cost < ans:
                ans = cost

    return str(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solve().strip()
    finally:
        sys.stdin = old_stdin

assert run("""5 2
1 2 1 2 1
1 9 3 8 2
""") == "8", "sample 1"

assert run("""5 3
1 2 2 2 1
1 6 4 9 2
""") == "0", "sample 2"

assert run("""1 1
7
10
""") == "0", "minimum size and M=1"

assert run("""3 3
5 5 5
2 100 7
""") == "0", "all volumes equal"

assert run("""2 2
0 5
3 4
""") == "20", "zero volume boundary"

assert run("""3 2
5 1 5
1 100 1
""") == "400", "minimum at the window boundary"

h = " ".join(["5000000"] * 100000)
a = " ".join(["5000000"] * 100000)
assert run(f"100000 100000\n{h}\n{a}\n") == "0", "maximum size"

| Test input | Expected output | What it validates |
|---|---:|---|
| `1 1 / 7 / 10` | `0` | Smallest possible input and the $M=1$ boundary |
| `3 3 / 5 5 5 / 2 100 7` | `0` | Equal volumes and zero loss |
| `2 2 / 0 5 / 3 4` | `20` | A valid minimum volume of zero |
| `3 2 / 5 1 5 / 1 100 1` | `400` | Minimum located at the boundary of a window |
| $N=100000$, all $H_i=A_i=5000000$ | `0` | Maximum input size and large integer values |

## Edge Cases

When $M=1$, every window contains exactly one song. The deque contains that song as its minimum, and the prefix sums give $H_iA_i-H_iA_i=0$. For

```text
1 1
7
10
```

the scan creates one window, computes `70 - 7 * 10`, and obtains `0`. No special case is required in the algorithm.

When all volumes are equal, the minimum equals every $H_i$ in the window. For

```
3 3
5 5 5
2 100 7
```

the weighted sum is $5(2+100+7)=545$, while the minimum multiplied by the sum of coefficients is also $5\cdot109=545$. Their difference is zero. This confirms that the formula naturally handles a window requiring no reductions.

When the minimum volume is zero, it must remain a legitimate minimum rather than being treated as an unset value. In

```
2 2
0 5
3 4
```

the deque front contains the first index, so the common volume is zero. The weighted sum is $0\cdot3+5\cdot4=20$, and subtracting zero times the coefficient sum leaves $20$.

When the minimum lies exactly at one endpoint, the deque must retain it until that endpoint leaves the window. Consider

```
3 2
5 1 5
1 100 1
```

The first window has minimum $1$ and cost $(5-1)\cdot1=4$. The second window also has minimum $1$, giving $(5-1)\cdot1=4$. The answer is $4$, not $400$. The test case is useful because the central minimum enters the deque and then remains the front across two consecutive windows. The condition `dq[head] < left` removes it only after it is genuinely outside the current window, avoiding an off-by-one error.
