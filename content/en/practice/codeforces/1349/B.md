---
title: "CF 1349B - Orac and Medians"
description: "We are given several independent queries. Each query provides a sequence of integers and a target value $k$. We are allowed to repeatedly choose any contiguous segment of the sequence and replace every element in that segment with the median of that segment."
date: "2026-06-11T14:35:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1349
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 641 (Div. 1)"
rating: 2000
weight: 1349
solve_time_s: 159
verified: true
draft: false
---

[CF 1349B - Orac and Medians](https://codeforces.com/problemset/problem/1349/B)

**Rating:** 2000  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 2m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent queries. Each query provides a sequence of integers and a target value $k$. We are allowed to repeatedly choose any contiguous segment of the sequence and replace every element in that segment with the median of that segment. The median is defined as the middle element after sorting the segment, with the lower middle chosen when the length is even.

The question is whether it is possible, after applying any number of such segment operations, to make the entire array equal to $k$.

The key difficulty is that each operation is highly non-local: a single segment operation overwrites many positions at once, and the value written depends on the order statistics of that segment rather than sums or extrema. This makes the problem feel like it could require tracking many possible states, but the constraints rule that out. With total $n \le 10^5$, any solution that simulates operations or explores segments explicitly will fail, since even checking all segments is already quadratic.

A common subtle failure case comes from assuming that the median operation can “create” new values freely. For example, if $k$ does not appear initially, one might still hope to construct it by mixing smaller and larger values. This is incorrect because every value produced by an operation must already be one of the elements in the chosen segment. The median is always an existing element of that segment.

Another misleading situation is when $k$ exists in the array but seems “trapped”. For instance, even if $k$ is present, it is not always possible to spread it to the whole array depending on how values are distributed around it.

## Approaches

A brute-force interpretation would try to model all reachable arrays. From any current array, we could try every segment, compute its median, apply the operation, and continue. This creates an enormous branching process. Each step considers $O(n^2)$ segments, and each transformation changes the state space in a way that quickly explodes beyond tractability. Even for small $n$, this approach becomes infeasible because the number of reachable states grows exponentially.

The key insight is that we do not need to simulate the process at all. Instead, we ask what structural conditions must hold for the final state to be achievable. Since every operation replaces a segment with one of its existing values (the median), no operation can introduce a value that was not already present. This immediately implies that if the final array is all $k$, then $k$ must already exist in the initial array.

The second observation is about when $k$ can “spread”. To expand a region of $k$ using median operations, we need to find segments whose median becomes $k$. That requires the segment to be balanced around $k$, meaning it must contain values on both sides of $k$. If all elements except $k$ lie strictly on one side, then no segment can produce new $k$-dominant regions beyond what already exists.

So the problem reduces to checking whether the array contains $k$, and whether the distribution around $k$ is not one-sided.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over states | Exponential | Exponential | Too slow |
| Structural condition check | $O(n)$ per test | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

We process each query independently.

1. Scan the array to determine whether $k$ exists. If it does not exist, we can immediately conclude it is impossible to obtain an array consisting entirely of $k$. This follows from the fact that medians are always drawn from existing elements in the chosen segment.
2. Compute whether there exists at least one element strictly smaller than $k$.
3. Compute whether there exists at least one element strictly larger than $k$.
4. If every element is already equal to $k$, we return “YES” because no operation is needed.
5. Otherwise, we return “YES” only if both a smaller-than-$k$ and a larger-than-$k$ element exist. If one side is missing, we return “NO”.

The intuition behind the last step is that to propagate $k$ beyond its initial occurrences, we need segments where $k$ can act as the median after rebalancing values. Such rebalancing requires values on both sides of $k$. If the array lies entirely on one side of $k$, then every median stays on that same side, and $k$ cannot become dominant everywhere.

### Why it works

The median operation never introduces new values outside the selected segment, so $k$ must be present initially. Once $k$ exists, the only way to expand its influence is through segments whose median evaluates to $k$, which requires the presence of values both smaller and larger than $k$. If the array is one-sided relative to $k$, every segment median also stays one-sided, preventing any further structural change toward a uniform $k$ array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        has_k = False
        has_less = False
        has_greater = False
        
        for x in a:
            if x == k:
                has_k = True
            elif x < k:
                has_less = True
            else:
                has_greater = True
        
        if not has_k:
            print("NO")
        elif all(x == k for x in a):
            print("YES")
        else:
            if has_less and has_greater:
                print("YES")
            else:
                print("NO")

if __name__ == "__main__":
    solve()
```

The implementation separates the array into three logical categories relative to $k$: equal, smaller, and larger. The presence check for $k$ is necessary because without an initial occurrence, no sequence of median operations can introduce it.

The final decision logic follows directly from the structural characterization: either the array is already uniform, or it must contain values on both sides of $k$ to allow any propagation beyond the initial occurrences.

## Worked Examples

### Example 1

Input:

```
5 3
1 5 2 6 1
```

We track key conditions:

| Step | has_k | has_less | has_greater | Decision |
| --- | --- | --- | --- | --- |
| Scan array | False | True | True | NO |

Since $k = 3$ does not appear anywhere, no operation can ever introduce it. Every median is chosen from existing segment values, so the value 3 is unreachable.

### Example 2

Input:

```
3 2
1 2 3
```

| Step | has_k | has_less | has_greater | Decision |
| --- | --- | --- | --- | --- |
| Scan array | True | True | True | YES |

Here $k$ exists, and there are values on both sides of it. This allows construction of segments whose medians stabilize at 2, enabling propagation until the whole array becomes uniform.

This demonstrates that having both sides around $k$ is sufficient even in small arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per query | Each element is scanned once to classify relative to $k$ |
| Space | $O(1)$ | Only a few boolean flags are stored |

The total $n$ across all test cases is $10^5$, so a linear scan per query easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        has_k = False
        has_less = False
        has_greater = False

        for x in a:
            if x == k:
                has_k = True
            elif x < k:
                has_less = True
            else:
                has_greater = True

        if not has_k:
            out.append("NO")
        elif all(x == k for x in a):
            out.append("YES")
        else:
            out.append("YES" if (has_less and has_greater) else "NO")

    return "\n".join(out)

# provided samples
assert run("""5
5 3
1 5 2 6 1
1 6
6
3 2
1 2 3
4 3
3 1 2 3
10 3
1 2 3 4 5 6 7 8 9 10
""") == """NO
YES
YES
NO
YES"""

# all equal
assert run("""1
4 7
7 7 7 7
""") == "YES"

# missing k
assert run("""1
5 10
1 2 3 4 5
""") == "NO"

# one-sided distribution
assert run("""1
5 3
1 2 3 3 3
""") == "NO"

# two-sided around k
assert run("""1
5 3
1 3 4 5 2
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | YES | already solved state |
| missing k | NO | impossibility due to absence of k |
| one-sided | NO | cannot propagate k without both sides |
| two-sided | YES | sufficient condition for propagation |

## Edge Cases

One edge case is when $n = 1$. The array is already uniform, so the answer depends only on whether that single value equals $k$. If it does, the answer is trivially “YES”, otherwise “NO”.

Another case is when all values are strictly less than $k$ or strictly greater than $k$. Even if $k$ appears somewhere in the array, losing one side of the value spectrum prevents any median operation from stabilizing around $k$ in new regions, which blocks full propagation.

A final subtle case is when $k$ exists but is not “central” in the distribution. If every value is on one side of $k$, then every segment median stays on that side, so no operation can expand the influence of (k` beyond isolated positions.
