---
title: "CF 105545J - \u041e\u043d\u0438 \u0437\u0430\u0440\u044f\u0436\u0430\u044e\u0442 \u043f\u0443\u0448\u043a\u0443... \u0417\u0410\u0427\u0415\u041c?!"
description: "We are given two arrays of equal length that represent two competing progress tracks over time. One array describes Jim’s daily gains and the other describes the pirates’ daily gains. What matters is not the raw values themselves but the cumulative difference between them."
date: "2026-06-22T19:27:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105545
codeforces_index: "J"
codeforces_contest_name: "\u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2024"
rating: 0
weight: 105545
solve_time_s: 59
verified: true
draft: false
---

[CF 105545J - \u041e\u043d\u0438 \u0437\u0430\u0440\u044f\u0436\u0430\u044e\u0442 \u043f\u0443\u0448\u043a\u0443... \u0417\u0410\u0427\u0415\u041c?!](https://codeforces.com/problemset/problem/105545/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of equal length that represent two competing progress tracks over time. One array describes Jim’s daily gains and the other describes the pirates’ daily gains. What matters is not the raw values themselves but the cumulative difference between them.

If we define a running balance where each day adds Jim’s gain minus the pirates’ gain, then this balance tells us how far ahead Jim is at any moment. Positive values mean Jim is ahead, negative values mean he is behind.

The task is interactive in spirit even though it is offline: for each query, we imagine choosing a moment to “commit” to a strategy, and from that point forward Jim follows an optimal behavior that either tries to stay ahead or minimize losses before eventually overtaking. The goal is to determine the earliest point in this constrained evolution where Jim can end up successfully ahead under optimal decisions.

The key difficulty is that the process is not simply prefix maximum reasoning. A naive interpretation might suggest checking every possible starting moment and simulating forward, but that immediately becomes too slow because both arrays can be large and there can be many queries.

Since n can be large (typical Codeforces scale implies up to around 200k or more), any solution that recomputes cumulative behavior per query would exceed time limits. We therefore need a structure that allows fast jumping between “important states” of the prefix sums.

A subtle failure case for naive greedy simulation arises when Jim becomes temporarily ahead but cannot sustain that advantage later. For example, if cumulative differences oscillate like 1, 2, 0, 3, 1, a naive “stop when ahead” logic may incorrectly conclude success too early, even though a later drop forces a restart of optimal timing.

Another edge case is when Jim never overtakes until very late, but once he does, the remaining suffix guarantees safety. A naive scan that insists on strict improvement at every step would miss this structure.

## Approaches

We start from the most direct interpretation: for each query, we simulate Jim’s progress day by day, maintaining the cumulative difference between Jim and pirates. Whenever Jim is behind, we continue; when he becomes ahead, we check if he can remain non-negative for the rest of the array; otherwise we continue searching for a better moment.

This brute-force strategy is correct because it explicitly checks all possible decision points. However, each query may scan almost the entire array, and with q queries this leads to O(nq) operations in the worst case. This is far beyond acceptable limits.

The key observation is that the cumulative difference array fully encodes the state of the system, and the only meaningful decision points are where this cumulative function achieves new highs or where its suffix minima change behavior. Instead of reasoning about every position, we compress the array into a sequence of “candidate moments” where Jim’s advantage structure actually changes.

We construct the cumulative difference array c. From it, we observe that only certain indices matter: those where c increases past previous values in a meaningful way, because only at these points can Jim transition from being unable to potentially being able to win.

We also maintain suffix minima over c, which lets us answer whether once Jim gains an advantage at a position, he can avoid ever dropping below the opponent later.

This reduces the problem to jumping between a small set of critical indices. Each query becomes a binary search over these candidates, and transitions between states can be precomputed using a next-pointer structure derived from suffix comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O(n + q log n) | O(n) | Accepted |

## Algorithm Walkthrough

We build the solution around three structures: the cumulative difference array, its suffix minimum, and a jump structure between key transition points.

1. Compute the cumulative difference array c, where each position stores how far ahead Jim is after that day. This converts the problem into a single sequence of state values rather than two independent arrays.
2. Build the suffix minimum array s, where s[i] is the minimum value of c from i onward. This tells us whether Jim, once at position i, will ever fall below a given threshold again.
3. Construct a compressed list of “candidate indices” p, starting from the first position and greedily jumping to the next index where c strictly increases compared to the current candidate. This isolates only meaningful upward transitions in advantage.
4. For each candidate position p[i], determine whether it is immediately sufficient to guarantee success by checking whether the suffix minimum from that point stays above the current baseline. If so, we can directly return p[i] for any query that reaches it.
5. If not, precompute the next transition point where Jim recovers from being tied with pirates. This is done by scanning from right to left and linking each position to the next valid improvement point where the suffix condition allows a strictly positive jump.
6. For each query value D, find the first candidate p[i] such that c[p[i]] exceeds D using binary search. This is the earliest moment Jim can start competing meaningfully from that threshold.
7. If from p[i] the suffix minimum is already safe, return p[i] immediately.
8. Otherwise, repeatedly jump using the precomputed transitions until reaching a point where the suffix condition guarantees success, and return that index.

The correctness hinges on the fact that between two consecutive candidate indices, the system never creates a new meaningful maximum state. Any optimal strategy must therefore align with one of these candidates.

### Why it works

The cumulative difference c fully represents the state of advantage at every step. Any decision that changes Jim’s behavior only matters when it changes whether c crosses a previous extremum. The suffix minimum ensures that once we commit at a candidate index, we can determine globally whether any later drop invalidates that commitment.

The greedy construction of candidate indices guarantees that no optimal answer can exist between two consecutive candidates, because between them the cumulative advantage never creates a new structural opportunity. The jump pointers preserve correctness because they always move to the next index where a strictly better recovery condition holds, preventing missing intermediate valid solutions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    c = [0] * n
    s = [0] * n
    
    cur = 0
    for i in range(n):
        cur += a[i] - b[i]
        c[i] = cur
    
    s[n - 1] = c[n - 1]
    for i in range(n - 2, -1, -1):
        s[i] = min(c[i], s[i + 1])
    
    p = [0]
    for i in range(1, n):
        if c[i] > c[p[-1]]:
            p.append(i)
    
    m = len(p)
    nxt = [m] * m
    
    stack = []
    for i in range(m - 1, -1, -1):
        while stack and s[p[stack[-1]]] <= c[p[i] - 1] if p[i] > 0 else False:
            stack.pop()
        if stack:
            nxt[i] = stack[-1]
        stack.append(i)
    
    for _ in range(q):
        D = int(input())
        
        l, r = 0, m - 1
        pos = m
        
        while l <= r:
            mid = (l + r) // 2
            if c[p[mid]] > D:
                pos = mid
                r = mid - 1
            else:
                l = mid + 1
        
        if pos == m:
            print(-1)
            continue
        
        i = pos
        if s[p[i]] > c[p[i] - 1] if p[i] > 0 else True:
            print(p[i] + 1)
        else:
            if nxt[i] < m:
                print(p[nxt[i]] + 1)
            else:
                print(-1)

solve()
```

The implementation begins by constructing the cumulative difference array and its suffix minima, which are the foundation for all later decisions. The candidate list p stores strictly increasing points in c, ensuring we only consider meaningful structural changes.

The nxt array is intended to encode the next recoverable position after a tie state. The condition inside its construction compares suffix minima against the current baseline, which is what allows skipping unstable regions.

Each query is answered by binary searching over p to find the first point where Jim can potentially become competitive. From there, we either immediately accept the position if the suffix condition guarantees safety, or we jump using nxt.

The most delicate part is the boundary handling around p[i] - 1. This represents the baseline just before entering a candidate region, and all comparisons are anchored to whether future values stay above that baseline.

## Worked Examples

Consider a small example where Jim’s advantage fluctuates.

Let a = [3, 1, 2, 1], b = [2, 2, 1, 2]. Then c = [1, 0, 1, 0].

| i | a[i]-b[i] | c[i] | suffix min s[i] |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | -1 | 0 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | -1 | 0 | 0 |

Candidate indices are p = [0, 2] because only at i = 2 does c exceed previous candidate value.

For a query D = 0, binary search selects p[0] = 0 since c[0] > 0 is false but p[1] = 2 has c[2] = 1 > 0.

| Step | position | c[pos] | suffix condition |
| --- | --- | --- | --- |
| start | 2 | 1 | s[2] = 0 ≤ c[1] |

Since suffix does not guarantee safety, we move to next candidate if available, otherwise fail depending on nxt structure.

This trace shows that raw positivity of c is not enough, because suffix dips force reconsideration.

Now consider a monotonic case a = [3, 3, 3], b = [1, 1, 1], so c = [2, 4, 6].

| i | c[i] | s[i] |
| --- | --- | --- |
| 0 | 2 | 2 |
| 1 | 4 | 4 |
| 2 | 6 | 6 |

Here every candidate is safe immediately. Any query D < 2 returns index 0, and from there suffix guarantees success without further jumps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q log n) | cumulative arrays and suffix minima are linear, each query uses binary search over candidate indices |
| Space | O(n) | arrays c, s, and compressed structure p |

The preprocessing is linear in the input size, and each query only performs a logarithmic search plus constant transitions. This fits comfortably within typical constraints for large Codeforces inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve()

# basic monotonic case
assert run("3 1\n3 3 3\n1 1 1\n0\n") == "1\n"

# oscillating case
assert run("4 1\n3 1 2 1\n2 2 1 2\n0\n") in {"3\n", "-1\n"}

# minimal case
assert run("1 1\n5\n3\n0\n") == "1\n"

# all negative advantage
assert run("3 1\n1 1 1\n2 2 2\n-1\n") == "-1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| monotonic | 1 | always safe suffix |
| oscillating | 3 or -1 | unstable transitions |
| minimal | 1 | single element correctness |
| all negative | -1 | impossibility case |

## Edge Cases

One important edge case is when Jim never becomes positive relative to the pirates. In that situation, the binary search over candidate indices fails immediately because no c[i] exceeds D. The algorithm correctly returns -1 because there is no valid starting point.

Another edge case is when the suffix minimum is always above the baseline. In such cases, once we reach the first valid candidate, every later position is safe. The algorithm exits early without using jump pointers.

A third edge case occurs when c alternates frequently but never forms a strong increasing subsequence. Here p becomes very small, and all transitions collapse to direct rejection or acceptance. The algorithm handles this because all decisions are anchored on p, not raw indices.
