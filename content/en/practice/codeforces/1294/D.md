---
problem: 1294D
contest_id: 1294
problem_index: D
name: "MEX maximizing"
contest_name: "Codeforces Round 615 (Div. 3)"
rating: 1600
tags: ["data structures", "greedy", "implementation", "math"]
answer: passed_samples
verified: true
solve_time_s: 263
date: 2026-06-14
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2dc457-23f0-83ec-b993-ecf9e885a0f0
---

# CF 1294D - MEX maximizing

**Rating:** 1600  
**Tags:** data structures, greedy, implementation, math  
**Model:** gpt-5-5  
**Solve time:** 4m 23s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2dc457-23f0-83ec-b993-ecf9e885a0f0  

---

## Solution

## Problem Understanding

We are building an array one element at a time. After each insertion, we are allowed to “reconfigure” values using a special operation: we can add or subtract a fixed number $x$ to any element, as many times as we want, as long as we never go below zero. After performing any such adjustments, we want to know the maximum possible MEX of the array.

The key point is that the array elements are not fixed values anymore. Each number $y$ we insert is not just a value, but a whole arithmetic progression of possible values:

$$y, y + x, y + 2x, \dots$$

and also downward moves by $x$ as long as we stay non-negative, meaning values reachable from $y$ are exactly all numbers congruent to $y \bmod x$, but restricted to non-negative integers.

So after each query, we want to know: how large a prefix $[0, 1, 2, \dots]$ we can fully “cover” using available numbers, where each number contributes one slot in its residue class modulo $x$.

Constraints go up to $4 \cdot 10^5$, so any solution must be near linear or $O(n \log n)$. Anything that tries to simulate operations or maintain full sets of reachable values per element will fail because each query could otherwise trigger large-scale recomputation over the whole array.

A naive misunderstanding that often breaks solutions is treating each element independently and thinking we can freely turn values into any non-negative integer. That is false: we are constrained by modulo $x$. For example, if $x = 3$, a value like 1 can only become $1, 4, 7, 10, \dots$, never 2 or 3.

A subtle failure case appears when multiple elements compete for the same residue class. For example, if many numbers are congruent to 0 mod $x$, they all “live” in the same bucket and cannot be used independently for all required small integers.

## Approaches

A brute-force idea would be to maintain the full array after each query and, for every candidate MEX value $m$, check if it can be formed using the available elements under the modulo constraint. This would involve simulating assignments of numbers to targets $0, 1, 2, \dots$, repeatedly checking feasibility per query. In the worst case, this becomes $O(n^2)$ or worse, because each query could require scanning many values and potentially adjusting many elements.

The key structural insight is that each number only matters through its remainder modulo $x$, because the allowed operation preserves that residue class. So every element belongs to exactly one of $x$ independent buckets.

Now consider building MEX from $0$ upward. To form a number $m$, we must have at least one unused element in the bucket $m \bmod x$. Each element can only be used once, so each bucket behaves like a queue of available “slots” for numbers with that remainder. As we assign numbers $0, 1, 2, \dots$, we consume one element from each corresponding residue bucket.

So the problem reduces to maintaining counts of how many times each remainder class has been seen, and greedily checking the smallest missing MEX.

The challenge is maintaining this dynamically as queries arrive. We maintain a pointer for each residue class indicating how many elements in that class have already been used in forming earlier MEX values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(x)$ | Accepted |

## Algorithm Walkthrough

We maintain two main structures: a frequency counter for each residue class modulo $x$, and a global pointer tracking the smallest MEX candidate.

Each residue class $r$ stores how many elements with $y \equiv r \pmod{x}$ have been inserted.

1. For each incoming value $y$, compute $r = y \bmod x$, and increment the count of bucket $r$. This reflects adding one more usable element in that residue class.
2. Maintain a current MEX pointer $mex$, starting from 0. This represents the smallest value we have not yet confirmed to be constructible.
3. After each insertion, repeatedly check whether the current $mex$ can be formed:

this requires that bucket $mex \bmod x$ has strictly more elements than the number of times we already used that residue class for earlier MEX values.
4. If it is possible, we “consume” one element from that residue class and increment $mex$. This models assigning a previously unused element to represent this MEX value.
5. Stop when the next $mex$ cannot be formed due to insufficient elements in its residue bucket. Output the current $mex$.

The reason we only ever move $mex$ forward is that once a number is confirmed impossible at a given moment, it may become possible later when more elements arrive, but earlier values are never revisited.

### Why it works

The invariant is that at any time, for every value $v < mex$, we have already matched it to a distinct element whose residue class allows it. For each such $v$, we have used exactly one element from bucket $v \bmod x$.

When we attempt to extend to $mex$, we are checking whether there exists an unused element in the required residue class. If yes, we assign it permanently to $mex$. If not, no future reassignment of earlier elements can help without breaking a previous assignment, since those are already committed. This makes the greedy assignment optimal and ensures that $mex$ is always maximized.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q, x = map(int, input().split())
    cnt = [0] * x
    
    mex = 0
    
    for _ in range(q):
        y = int(input())
        r = y % x
        cnt[r] += 1
        
        # try to extend mex greedily
        while cnt[mex % x] > mex // x:
            mex += 1
        
        print(mex)

if __name__ == "__main__":
    solve()
```

The solution maintains only residue counts and a single increasing pointer. The condition `cnt[mex % x] > mex // x` captures exactly whether we have enough elements in that residue class to assign to the current MEX position.

The division `mex // x` represents how many previous numbers in this residue class have already been consumed while building earlier parts of the MEX sequence.

The loop only advances forward, so total movement of `mex` across all queries is linear.

## Worked Examples

### Example trace

Input:

```
7 3
0
1
2
2
0
0
10
```

We track `cnt` and `mex`:

| Step | y | cnt mod 3 (0,1,2) | mex |
| --- | --- | --- | --- |
| 1 | 0 | (1,0,0) | 1 |
| 2 | 1 | (1,1,0) | 2 |
| 3 | 2 | (1,1,1) | 3 |
| 4 | 2 | (1,1,2) | 3 |
| 5 | 0 | (2,1,2) | 4 |
| 6 | 0 | (3,1,2) | 4 |
| 7 | 10 | (4,1,2) | 7 |

This confirms that as soon as each residue class accumulates enough capacity, MEX jumps forward in blocks.

The trace shows how residue 0 becomes heavily populated and eventually enables skipping multiple missing values in sequence.

### Small stress example

Input:

```
5 2
1
3
5
7
9
```

All numbers are odd, so only residue class 1 grows.

| Step | cnt (0,1) | mex |
| --- | --- | --- |
| 1 | (0,1) | 0 |
| 2 | (0,2) | 0 |
| 3 | (0,3) | 0 |
| 4 | (0,4) | 0 |
| 5 | (0,5) | 0 |

We can never form 0 because residue 0 never appears, so MEX remains 0 throughout.

This demonstrates that availability of all residue classes is necessary for progress.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q)$ | Each element increases one counter, and the MEX pointer only moves forward across all values at most $q$ times |
| Space | $O(x)$ | Only residue class counts are stored |

The algorithm fits comfortably within limits since both $q$ and $x$ are up to $4 \cdot 10^5$, and memory usage is linear in $x$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    _stdout = _sys.stdout
    out = io.StringIO()
    _sys.stdout = out
    solve()
    _sys.stdout = _stdout
    return out.getvalue().strip()

# provided sample
assert run("""7 3
0
1
2
2
0
0
10
""") == """1
2
3
3
4
4
7"""

# minimum case
assert run("""1 1
0
""") == "1"

# all same residue, cannot progress
assert run("""3 5
1
6
11
""") == "0\n0\n0"

# full coverage small
assert run("""4 2
0
1
2
3
""") == "1\n2\n3\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case |
| single residue only | all 0 | impossibility due to missing class |
| alternating residues | increasing MEX | normal progression |

## Edge Cases

A key edge case is when only one residue class appears in all queries. In that situation, only numbers congruent to that class modulo $x$ can be formed, so MEX stalls at 0 immediately. The algorithm handles this because `cnt[mex % x]` will never exceed zero when `mex % x` is the missing class.

Another case is when $x = 1$. Then every number belongs to the same residue class, and every insertion directly increases the available pool. The condition simplifies to a pure count comparison, and MEX becomes equal to the number of processed elements, which the algorithm naturally produces since `cnt[0]` always grows and `mex` advances step by step.