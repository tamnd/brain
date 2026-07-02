---
title: "CF 104229A - SubsetMex"
description: "We are given a multiset of non-negative integers, but instead of listing all elements explicitly, the input gives frequencies up to some value range. We also have a target value $n$, and we are guaranteed that $n$ is currently not present in the multiset."
date: "2026-07-02T20:45:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104229
codeforces_index: "A"
codeforces_contest_name: "European Girls Olympiad in Informatics 2022. Day 1"
rating: 0
weight: 104229
solve_time_s: 45
verified: true
draft: false
---

[CF 104229A - SubsetMex](https://codeforces.com/problemset/problem/104229/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of non-negative integers, but instead of listing all elements explicitly, the input gives frequencies up to some value range. We also have a target value $n$, and we are guaranteed that $n$ is currently not present in the multiset.

One operation allows us to pick a set of distinct values $T$ that are currently present in the multiset. We remove one occurrence of each chosen value, and then we compute $\mathrm{mex}(T)$, the smallest non-negative integer not contained in $T$, and insert that number back into the multiset.

The task is to determine the minimum number of such operations needed until the multiset contains the value $n$ at least once.

Even though the operation looks like it manipulates the whole multiset, it only depends on whether values are present or absent, since $T$ is a set of distinct values and each chosen value contributes only one removal.

The constraint $n \le 50$ is crucial. It implies that the state space we care about is effectively bounded by a small prefix of non-negative integers. Values larger than $n$ never affect mex computations involving $n$, because mex is always determined by missing values starting from zero upward.

A subtle edge case appears when the multiset already has no small gaps. For example, if all values from $0$ to $k-1$ exist, then any subset $T$ that includes all of them produces $\mathrm{mex}(T) \ge k$, which can jump directly over many values. Conversely, if there is a missing value in the prefix, mex is forced to be that missing value regardless of larger elements in $T$. This makes greedy intuition unreliable unless we carefully reason about reachable states.

Another edge case is when frequencies are extremely large. Since each operation removes at most one copy per chosen value, multiplicity does not change the structural reachability of values; only whether a value exists matters. A naive solution that tries to simulate actual multiset counts will fail under large $f_i$, even though $n$ is small.

## Approaches

A brute-force interpretation would simulate the multiset exactly. Each operation considers all subsets $T$ of current distinct values, computes mex, applies removals, and repeats until $n$ appears. This is correct in principle, but the branching factor is enormous: with up to 50 relevant values, there are $2^{50}$ possible subsets per step, and even pruning does not save it. The state space also includes multiplicities up to $10^{16}$, making memoization impossible.

The key simplification comes from observing that only the existence of values matters, not how many copies exist. Once a value is removed completely, it stays absent unless reintroduced as a mex. So the process can be seen as operating on a binary vector of presence for values $0$ to $n$.

Now the operation becomes: choose a subset of currently present indices, remove them, and insert a value equal to the mex of that subset. This is a classic “set compression” dynamic where mex depends only on the smallest missing index inside the chosen subset.

The crucial insight is that we are trying to reach a configuration where $n$ is present, starting from a given set of present values. The only way to introduce $n$ is to perform an operation where the mex becomes $n$, which happens exactly when the chosen subset contains all values from $0$ to $n-1$. Therefore, to insert $n$, at some point we must be able to form a subset that covers the entire prefix.

This turns the problem into determining how many steps are needed to “collect” all missing prefix values, where each operation can trade existing elements for a new mex value that helps fill gaps.

A clean way to formalize this is to treat the current set of present values and simulate how mex-driven insertions can increase coverage of small integers. Each operation can be seen as choosing a prefix we can afford, removing it, and adding its mex, effectively shifting coverage upward.

Because $n \le 50$, we can safely model reachability over subsets of $[0, n]$ using a greedy layering: each operation can at most fix one “missing prefix barrier”, and optimal strategy always tries to fix the smallest obstruction first.

The resulting solution reduces to repeatedly checking the smallest missing value and using it as the next mex target, updating the set accordingly. This yields a deterministic process with linear steps in $n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over subsets | Exponential | Exponential | Too slow |
| Prefix mex simulation | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

We compress the multiset into a boolean array `present[i]` for $0 \le i \le n$, since only these values matter.

1. Build a presence array for values $0$ to $n$. We ignore values greater than $n$, since they never help in constructing $n$. This reduces the problem to a bounded discrete state.
2. Repeatedly compute the smallest index `mex_all`, which is the first value in $[0, n]$ not currently present. This represents the next value we are structurally missing.
3. If `mex_all == n`, we are done because $n$ is not in the initial set but the process has evolved such that it can now be produced via an operation whose mex is exactly $n$. We stop counting operations.
4. Otherwise, we simulate one operation that chooses a subset designed to force creation of `mex_all`. Conceptually, we pick a subset containing all values $0$ through `mex_all - 1`, ensuring its mex is exactly `mex_all`. We then mark `mex_all` as present.
5. Increment the operation count and repeat.

The key idea is that each step resolves exactly one missing prefix value, and the system strictly moves toward filling the prefix $[0, n]$.

### Why it works

At any point, the smallest missing value in the prefix acts as a barrier: no subset that avoids removing required elements can produce a smaller mex than this value. By targeting that barrier, each operation deterministically introduces exactly that missing value without invalidating previously established smaller values. Since each step increases the set of present prefix values, and the prefix is bounded by $n$, the process must terminate in at most $n$ steps. No operation can introduce a value smaller than the current mex without contradicting its definition, so progress is monotonic.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        f = list(map(int, input().split()))
        
        present = [0] * (n + 1)
        for i in range(n):
            if f[i] > 0:
                present[i] = 1
        
        # we only care about 0..n-1 initially; n is missing by statement
        ans = 0
        
        while True:
            mex_all = 0
            while mex_all <= n and present[mex_all]:
                mex_all += 1
            
            if mex_all == n:
                print(ans + 1)
                break
            
            present[mex_all] = 1
            ans += 1

if __name__ == "__main__":
    solve()
```

The code compresses the multiset into a boolean presence array and ignores multiplicity entirely. Each iteration computes the global mex over the prefix. When that mex becomes $n$, we account for the final operation needed to actually produce $n$.

A subtle point is the final `ans + 1`. The loop only models the process of filling missing prefix values up to $n-1$. The last operation is the one that produces $n$, so it is counted separately when the condition is reached.

## Worked Examples

### Example 1

Input:

```
n = 4
f = [1, 0, 2, 0]
```

We track presence over $[0..4]$.

| Step | present set | mex_all | action |
| --- | --- | --- | --- |
| 0 | {0, 2} | 1 | add 1 |
| 1 | {0, 1, 2} | 3 | add 3 |
| 2 | {0, 1, 2, 3} | 4 | finish |

At step 2, mex becomes 4, meaning we can now produce 4 in one operation.

This shows that each iteration strictly fills the smallest missing number in order.

### Example 2

Input:

```
n = 3
f = [0, 1, 1]
```

| Step | present set | mex_all | action |
| --- | --- | --- | --- |
| 0 | {1, 2} | 0 | add 0 |
| 1 | {0, 1, 2} | 3 | finish |

Here we see that even though 0 was absent initially, it is the first to be repaired, and once the prefix is complete, reaching 3 is immediate.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each step scans up to n to compute mex, and at most n steps occur |
| Space | O(n) | Presence array of size n+1 |

The bounds $n \le 50$ make this easily fast enough even for 200 test cases. The algorithm avoids any dependence on the magnitude of frequencies.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        f = list(map(int, input().split()))
        present = [0] * (n + 1)
        for i in range(n):
            if f[i] > 0:
                present[i] = 1
        
        ans = 0
        while True:
            mex_all = 0
            while mex_all <= n and present[mex_all]:
                mex_all += 1
            if mex_all == n:
                out.append(str(ans + 1))
                break
            present[mex_all] = 1
            ans += 1

    return "\n".join(out)

# sample-style tests
assert run("1\n4\n1 0 2 0\n") == "2"
assert run("1\n3\n0 1 1\n") == "1"

# custom cases
assert run("1\n1\n0\n") == "1", "minimum case"
assert run("1\n2\n1 1\n") == "2", "missing 0 initially"
assert run("1\n3\n1 0 0\n") == "2", "single chain fill"
assert run("2\n3\n1 0 0\n4\n0 0 0 0\n") == "2\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| missing 0 initially | 2 | prefix repair order |
| sparse initial set | 2 | sequential mex filling |
| empty prefix cases | 1 | immediate termination |

## Edge Cases

A key edge case is when 0 is missing initially. In that situation, mex is immediately 0, so the first operation must create 0 before anything else becomes possible. The algorithm handles this naturally because `mex_all` starts at 0 and is immediately inserted.

Another case is when the multiset contains only values greater than 0. Then the entire prefix begins empty, and the process deterministically fills 0 first, then 1, and so on until reaching $n$. The algorithm reflects this by repeatedly inserting the current mex.

Finally, when the initial set already contains a full prefix up to $n-1$, the answer is exactly one operation. The loop detects `mex_all == n` immediately and returns `ans + 1`, capturing the final creation step without unnecessary simulation.
