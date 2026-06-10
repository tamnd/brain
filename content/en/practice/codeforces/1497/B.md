---
title: "CF 1497B - M-arrays"
description: "We are given a multiset of numbers and a modulus $m$. The task is to rearrange all numbers into as few sequences as possible, where each sequence must satisfy a local compatibility rule: whenever two consecutive elements appear in the same sequence, their sum must be divisible…"
date: "2026-06-10T21:44:17+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1497
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 708 (Div. 2)"
rating: 1200
weight: 1497
solve_time_s: 142
verified: false
draft: false
---

[CF 1497B - M-arrays](https://codeforces.com/problemset/problem/1497/B)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 2m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of numbers and a modulus $m$. The task is to rearrange all numbers into as few sequences as possible, where each sequence must satisfy a local compatibility rule: whenever two consecutive elements appear in the same sequence, their sum must be divisible by $m$.

Because we are allowed to permute elements arbitrarily inside each sequence, the only real constraint is how elements “fit” next to each other based on their remainders modulo $m$. If two numbers leave remainders $r$ and $s$, then they can be adjacent in some sequence exactly when $r + s \equiv 0 \pmod m$. This means each remainder $r$ is compatible only with its complement $m - r$, while remainder $0$ is compatible only with itself, and when $m$ is even, remainder $m/2$ is also self-compatible.

The goal is to split all elements into the minimum number of such valid sequences.

The constraint $n \le 10^5$ over all test cases forces us away from any strategy that tries all partitions or builds sequences explicitly. Any solution that even implicitly considers all pairings or tries backtracking will fail, since the search space grows exponentially with $n$. The structure of the problem suggests that only frequencies of remainders matter, not the actual arrangement of elements.

A subtle failure case for naive reasoning is assuming that pairing complementary remainders greedily always minimizes sequences. For example, if we try to always match as many $r$ with $m-r$ as possible and then start new sequences for leftovers without considering global structure, we may overestimate the number of sequences needed or build invalid constructions. Another common mistake is treating each pair of remainders independently without handling the special behavior of remainder $0$ and $m/2$.

## Approaches

A brute-force idea would attempt to actually construct sequences one by one. We could repeatedly pick an unused element, extend a sequence by greedily choosing any compatible unused element, and continue until no extension is possible, then start a new sequence. This is correct in principle because we are explicitly respecting the adjacency rule. However, each extension requires scanning for compatible unused elements, and in the worst case we may revisit elements many times. This leads to quadratic behavior, which is far beyond the limit when $n$ reaches $10^5$.

The key observation is that adjacency depends only on remainders, and each remainder $r$ interacts only with a single partner $m-r$. This reduces the problem to independent counting problems over each complementary pair of residues.

For a fixed pair $(r, m-r)$, we only care about how many elements of each type exist. Any valid sequence using only these two residues must alternate between them. This turns the problem into splitting two multisets into the minimum number of alternating sequences. The optimal structure emerges when we realize that imbalance between the two counts forces multiple sequences, since a single alternating sequence can absorb at most a difference of one between counts.

The special residues $0$ and, when $m$ is even, $m/2$, behave differently because they pair with themselves. For these, all elements can be placed into a single sequence since any adjacency is valid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force sequence construction | $O(n^2)$ | $O(n)$ | Too slow |
| Frequency-based remainder pairing | $O(n + m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We first compress the array into frequency counts of each remainder modulo $m$.

1. Compute an array `cnt` where `cnt[r]` stores how many numbers have remainder $r$. This removes all ordering information and keeps only what matters for adjacency feasibility.
2. Handle remainder $0$. If `cnt[0]` is nonzero, all such elements can be placed into a single valid sequence, since $0 + 0 \equiv 0 \pmod m$. This contributes either 0 or 1 sequence.
3. If $m$ is even, handle remainder $m/2$. All elements with this remainder are also mutually compatible, so they can be placed into a single sequence if they exist. This also contributes at most 1 sequence.
4. For each remainder $r$ from $1$ to $m-1$, pair it with $m-r$, but only process each pair once by enforcing $r < m-r$. For each such pair, we decide how many sequences are needed to accommodate both groups.
5. For a pair $(r, m-r)$, let $a = cnt[r]$ and $b = cnt[m-r]$. If both are zero, we skip it. Otherwise, the minimum number of alternating sequences needed is $\max(1, |a - b|)$. This captures the fact that a single alternating sequence can absorb as much balance as possible, and any leftover imbalance forces additional sequences.
6. Sum contributions from all independent groups to get the final answer.

### Why it works

Each sequence over a pair $(r, m-r)$ is an alternating chain, and within any single chain the difference between counts of the two residues is at most one. Therefore, a sequence can “absorb” balanced pairs efficiently, and only the excess of the dominant residue forces new sequences. Because different residue pairs do not interact, optimizing each pair independently produces a globally optimal decomposition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        
        cnt = [0] * m
        for x in a:
            cnt[x % m] += 1
        
        ans = 0
        
        if cnt[0] > 0:
            ans += 1
        
        if m % 2 == 0 and cnt[m // 2] > 0:
            ans += 1
        
        for r in range(1, m):
            s = m - r
            if r >= s:
                continue
            a1, a2 = cnt[r], cnt[s]
            if a1 == 0 and a2 == 0:
                continue
            ans += max(1, abs(a1 - a2))
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by building remainder frequencies, which is the only information relevant for feasibility. It then handles the two self-compatible residue classes separately, since they behave like independent single-group problems.

The loop over $r$ pairs each residue with its complement exactly once. The expression `max(1, abs(a1 - a2))` implements the key structural result for alternating sequences: even a heavily imbalanced pair still needs at least one sequence, and every extra unit of imbalance forces an additional sequence.

Care must be taken to skip double counting by ensuring $r < m-r$, otherwise each pair would be processed twice and the answer would be inflated.

## Worked Examples

### Example 1

Input:

```
n=6, m=4
a = [2, 2, 8, 6, 9, 4]
```

Remainders are:

```
0: 1 element (4)
1: 1 element (9)
2: 3 elements (2,2,8,6 → actually 4 elements mod 4 gives 0,2,2,2 depending; final counts matter)
3: 0 elements
```

| Step | Pair | Counts | Contribution |
| --- | --- | --- | --- |
| 1 | r=0 | cnt[0]=1 | +1 |
| 2 | r=1,3 | 1 vs 0 | max(1,1)=1 |
| 3 | r=2 (self when m even? m/2=2) | cnt[2]>0 | +1 |

Final answer is 3.

This shows how independent residue components each contribute separately and combine additively.

### Example 2

Input:

```
n=5, m=3
a = [1, 2, 2, 1, 1]
```

Remainders:

```
0: 0
1: 3
2: 2
```

| Step | Pair | Counts | Contribution |
| --- | --- | --- | --- |
| 1 | r=1,2 | 3 vs 2 | max(1,1)=1 |

Final answer is 1.

This demonstrates a fully connected alternating structure where imbalance is small enough to be absorbed into a single sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ per test | Counting remainders takes linear time in input size, and pairing residues is linear in $m$ |
| Space | $O(m)$ | Frequency array for residues |

The total constraints ensure $\sum n + \sum m \le 10^5$, so this linear approach easily fits within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, m = map(int, input().split())
            a = list(map(int, input().split()))
            cnt = [0] * m
            for x in a:
                cnt[x % m] += 1

            ans = 0
            if cnt[0] > 0:
                ans += 1
            if m % 2 == 0 and cnt[m // 2] > 0:
                ans += 1

            for r in range(1, m):
                s = m - r
                if r >= s:
                    continue
                a1, a2 = cnt[r], cnt[s]
                if a1 == 0 and a2 == 0:
                    continue
                ans += max(1, abs(a1 - a2))

            out.append(str(ans))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""4
6 4
2 2 8 6 9 4
10 8
1 1 1 5 2 4 4 8 6 7
1 1
666
2 2
2 4
""") == """3
6
1
1"""

# all equal values
assert run("""1
5 3
3 3 3 3 3
""") == "1"

# single element
assert run("""1
1 7
10
""") == "1"

# no pairing possible
assert run("""1
4 5
1 1 1 1
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all samples | 3 6 1 1 | correctness on mixed structure |
| all equal values | 1 | self-complement collapse |
| single element | 1 | minimal non-empty sequence |
| uniform residue | 4 | maximal splitting due to imbalance |

## Edge Cases

For remainder $0$, the algorithm correctly assigns a single sequence whenever it exists, because all such elements are mutually compatible. Even if there are many zeros, they do not force multiple sequences since no alternating constraint is violated.

For remainder $m/2$ when $m$ is even, the same reasoning applies. Although it may look like a pairing problem, every pair of identical residues is valid, so all elements can be chained into one sequence regardless of count.

For highly imbalanced complementary pairs, the expression $\max(1, |a-b|)$ ensures that even when one residue dominates, at least one sequence is formed for the usable overlap, while the remaining excess is correctly forced into separate singleton or partially filled sequences.
