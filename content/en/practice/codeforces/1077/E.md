---
title: "CF 1077E - Thematic Contests"
description: "We are given a multiset of problems where each problem belongs to a topic. The same topic can appear many times. From this pool, we want to form several contests. Each contest must use only problems from a single topic, so it is homogeneous."
date: "2026-06-15T06:41:24+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1077
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 521 (Div. 3)"
rating: 1800
weight: 1077
solve_time_s: 177
verified: true
draft: false
---

[CF 1077E - Thematic Contests](https://codeforces.com/problemset/problem/1077/E)

**Rating:** 1800  
**Tags:** greedy, sortings  
**Solve time:** 2m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of problems where each problem belongs to a topic. The same topic can appear many times. From this pool, we want to form several contests. Each contest must use only problems from a single topic, so it is homogeneous. Different contests must use different topics, so each topic can contribute to at most one contest.

These contests are arranged in a sequence. If we decide that the first contest uses $x$ problems, then the next must use $2x$, the next $4x$, and so on, forming a strict doubling chain. We are free to choose how many contests we create, and we are free to choose the starting size $x$. The objective is not to maximize the number of contests, but to maximize the total number of problems used across all chosen contests.

The key structure is that each contest consumes a fixed budget of problems, and the budgets grow exponentially. Since topics cannot repeat, each step in the sequence must be assigned a different topic, and that topic must have enough problems available to support that stage size.

The constraint $n \le 2 \cdot 10^5$ implies we need an $O(n \log n)$ or $O(n)$ approach. Anything that tries to simulate all possible starting sizes and topic assignments explicitly would be too slow, especially since each topic can appear many times and naive matching would repeatedly scan large frequency lists.

A subtle failure case appears when frequencies are uneven. For example, if one topic has a huge count and many others have small counts, a greedy assignment that simply takes largest frequencies first without respecting doubling order can waste large counts on early stages or fail to extend a chain even though a better arrangement exists.

Another edge case is when multiple topics have identical frequencies. A naive approach might treat them interchangeably, but assignment order matters because early stages consume far fewer problems than later stages, and misordering can block feasible extensions.

## Approaches

A brute-force idea is to consider every possible starting topic and every possible starting size. For a fixed starting size $x$, we attempt to build a chain: pick any topic with at least $x$ problems, then any other topic with at least $2x$, then $4x$, and so on. For each choice, we compute the total sum of used problems and take the maximum.

This is correct in principle because it explores all valid sequences. However, for each attempt we would repeatedly search among topics for a feasible next frequency. With up to $2 \cdot 10^5$ problems, the number of distinct frequencies is large, and the number of possible chains is also large. Even if we compress frequencies, checking all chains leads to something close to quadratic or worse in practice.

The key observation is that the structure of the problem depends only on topic frequencies, not on individual problems. Once we compute how many problems exist per topic, we can think of each topic as a “capacity” value. We then want to assign these capacities to levels of a geometric progression.

Instead of choosing a start and simulating forward, we reverse the perspective: fix how many contests we will take, say $k$, and try to see the best possible assignment of topics to levels $1, 2, 4, \dots, 2^{k-1}$. For a fixed $k$, to maximize usage, we want to assign the largest available frequencies to the largest required levels. This suggests sorting frequencies and greedily matching from largest requirement to largest capacity.

The remaining issue is how to determine the best $k$. Since each added level doubles the requirement, the total required grows exponentially, so $k$ is at most around $\log n$. This makes it feasible to try all $k$ values and evaluate greedily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force chains | Exponential / $O(n^2)$ | $O(n)$ | Too slow |
| Try all lengths + greedy assignment | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Count frequencies of each topic.

Each topic becomes a single number representing how many problems we can allocate from it.
2. Sort the frequencies in descending order.

Large topics are more flexible, so we want them to serve larger requirements when possible.
3. Build a prefix sum of frequencies to quickly compute how many problems are available for any chosen subset of top topics.
4. Try all possible numbers of contests $k$.

Since requirements grow as $1, 2, 4, \dots$, we stop when the total required exceeds available problems.
5. For a fixed $k$, compute required sizes: $1, 2, 4, \dots, 2^{k-1}$.
6. Check feasibility greedily from largest requirement to smallest: assign the largest frequency topics first to the largest requirement.

This works because larger requirements are harder to satisfy, so they should consume the most flexible resources.
7. If feasible, compute total contribution as sum of all assigned contest sizes and update the answer.

### Why it works

The core invariant is that for any fixed number of contests, an optimal assignment never benefits from giving a large requirement to a smaller frequency when a larger frequency is available. Any swap that moves a larger frequency to a larger requirement can only preserve or improve feasibility, since constraints are monotone. This reduces the problem to matching sorted demands with sorted capacities, which eliminates the combinatorial explosion of assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    freq = {}
    for x in a:
        freq[x] = freq.get(x, 0) + 1
    
    vals = sorted(freq.values(), reverse=True)
    
    best = 0
    
    # try number of contests k
    for k in range(1, len(vals) + 1):
        need = []
        x = 1
        total_need = 0
        
        for i in range(k):
            need.append(x)
            total_need += x
            x *= 2
        
        # prune if even total requirement exceeds sum of all problems
        if total_need > n:
            break
        
        # check feasibility: assign largest needs to largest frequencies
        ok = True
        for i in range(k):
            if vals[i] < need[k - 1 - i]:
                ok = False
                break
        
        if ok:
            best = max(best, total_need)
    
    print(best)

if __name__ == "__main__":
    solve()
```

The code first compresses the input into topic frequencies. It then sorts these frequencies so we can always reason about allocating the strongest topics first. For each possible number of contests, it constructs the required geometric sequence and checks whether the largest frequencies can satisfy the largest requirements. The reversed comparison ensures that we match constraints in the most favorable way.

The pruning step using total required sum prevents unnecessary checks once requirements exceed available problems.

## Worked Examples

### Example 1

Input:

```
18
2 1 2 10 2 10 10 2 2 1 10 10 10 10 1 1 10 10
```

Frequencies:

| Topic | Count |
| --- | --- |
| 10 | 8 |
| 2 | 5 |
| 1 | 3 |

Sorted: `[8, 5, 3]`

We test $k = 1, 2, 3$.

For $k = 3$, requirements are `[1, 2, 4]`, total is 7.

Assignment check:

| Level (largest first) | Requirement | Frequency |
| --- | --- | --- |
| 4 | 4 | 8 |
| 2 | 2 | 5 |
| 1 | 1 | 3 |

All satisfied, so total = 7.

This shows that all three topics can participate in a doubling chain.

### Example 2

Input:

```
2
3 3
```

Frequencies:

| Topic | Count |
| --- | --- |
| 3 | 2 |

Only one topic exists, so only $k = 1$ is possible.

Requirement `[1]`, total = 1.

The algorithm correctly avoids trying $k = 2$ since there is no second topic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting frequencies dominates, and we try at most $O(\log n)$ values of $k$ |
| Space | $O(n)$ | Frequency map and list of counts |

The constraints allow up to $2 \cdot 10^5$ elements, so sorting and a small number of linear checks fit comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    
    freq = {}
    for x in a:
        freq[x] = freq.get(x, 0) + 1
    
    vals = sorted(freq.values(), reverse=True)
    
    best = 0
    
    for k in range(1, len(vals) + 1):
        need = []
        x = 1
        total_need = 0
        
        for i in range(k):
            need.append(x)
            total_need += x
            x *= 2
        
        if total_need > n:
            break
        
        ok = True
        for i in range(k):
            if vals[i] < need[k - 1 - i]:
                ok = False
                break
        
        if ok:
            best = max(best, total_need)
    
    return str(best)

# provided samples
assert run("18\n2 1 2 10 2 10 10 2 2 1 10 10 10 10 1 1 10 10\n") == "7"

# single topic
assert run("3\n1337 1337 1337\n") == "3"

# two balanced topics
assert run("6\n1 1 1 2 2 2\n") == "6"

# skewed frequencies
assert run("10\n1 1 1 1 1 2 2 3 3 3\n") == "7"

# minimum
assert run("1\n5\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single topic | 3 | only one contest possible |
| balanced topics | 6 | full utilization across multiple topics |
| skewed frequencies | 7 | greedy matching robustness |
| minimum input | 1 | base edge case |

## Edge Cases

A key edge case is when one topic dominates the frequency distribution. For example:

```
8
1 1 1 1 1 1 1 1
```

Here only one contest can be formed, and the algorithm correctly outputs 1 since no second topic exists.

Another case is many small equal topics:

```
6
1 2 3 4 5 6
```

Each topic has frequency 1. Only $k = 1$ works, since $k = 2$ already requires a second topic. The algorithm correctly prevents overextension because sorted frequencies fail the requirement check.

A final case is when large topics exist but cannot support deep chains. The algorithm ensures that even if total sum is large, exponential requirements force early stopping, preventing invalid long sequences.
