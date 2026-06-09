---
title: "CF 1778C - Flexible String"
description: "We are given two equal-length strings, and we are allowed to modify the first string in a very specific way. Each time we change a character in the first string, the original character at that position gets “recorded” into a special set."
date: "2026-06-09T11:34:12+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "strings"]
categories: ["algorithms"]
codeforces_contest: 1778
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 848 (Div. 2)"
rating: 1600
weight: 1778
solve_time_s: 83
verified: true
draft: false
---

[CF 1778C - Flexible String](https://codeforces.com/problemset/problem/1778/C)

**Rating:** 1600  
**Tags:** bitmasks, brute force, strings  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two equal-length strings, and we are allowed to modify the first string in a very specific way. Each time we change a character in the first string, the original character at that position gets “recorded” into a special set. This set tracks which original characters we have ever overwritten, and its size is constrained by a limit $k$.

At the end of all modifications, we compare the modified first string with the second string. We count how many substrings are identical between them, and we want to maximize that count while ensuring that the number of distinct characters ever added to the recorded set does not exceed $k$.

A useful way to reinterpret the operation is that every position either keeps its original character or is “forgiven” by paying the cost of adding that character into the set. Once a character is in the set, all occurrences of that character can be freely modified without further cost.

The key structural observation is that the set constraint is global over characters, not positions. Since there are at most 10 distinct characters in the initial string, any decision is really about choosing which subset of these characters we are willing to “spend” budget on.

The constraints imply a combinatorial explosion over subsets is still feasible. With at most 10 characters, there are at most $2^{10} = 1024$ subsets, and $n$ over all test cases is $10^5$, so an $O(n \cdot 2^{10})$ solution is acceptable. Anything quadratic in $n$ would fail immediately.

A subtle edge case appears when $k = 0$. In this case, we cannot ever modify a character whose original value is different from the target alignment, meaning the answer depends only on positions where $a[i] = b[i]$. A naive approach that assumes we can freely overwrite mismatches would produce incorrect results here.

Another corner case occurs when $k$ is large enough to cover all distinct characters in $a$. Then we can effectively change any position without restriction, making the optimal result depend only on structural alignment with $b$, and any partial greedy logic that assumes local decisions may miss the global optimum.

## Approaches

A brute-force solution would try every way to choose which positions to modify and which characters end up in the forbidden set $Q$. For each configuration, we would simulate the final string and count matching substrings against $b$. This immediately becomes infeasible because even for fixed $k$, the number of subsets of positions is exponential in $n$, and substring counting itself is $O(n^2)$. The total complexity collapses under even small inputs.

The key simplification is to shift focus from positions to characters. Since the cost is incurred per distinct original character used in modifications, not per operation, the problem becomes selecting a subset of characters from the at most 10 available in $a$. Once a subset is fixed, we can treat all positions containing those characters as freely modifiable.

For any chosen subset, we can compute the best achievable number of matching substrings efficiently by reducing the problem to a binary classification over positions: at each index, either we force equality with $b[i]$ or we treat it as flexible and try to maximize contributions.

The crucial insight is that substring equality counting can be transformed into counting contributions over pairs $(l, r)$, which is equivalent to summing over runs where prefix constraints are satisfied. This leads to a standard reduction: instead of counting substrings directly, we compute how many positions are “good” in terms of whether prefix equality is maintained.

Because the character set is small, we iterate over all subsets of characters in $a$, simulate the resulting best alignment, and take the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential in $n$ | $O(n)$ | Too slow |
| Optimal | $O(n \cdot 2^{10})$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first compress the set of distinct characters in $a$, since only those matter in decisions. Let their count be $m \le 10$.

1. Assign each distinct character in $a$ an index from 0 to $m-1$. This allows us to represent any subset as a bitmask. The reason this works is that all operations depend only on whether a character is “activated” for modification, not on position-specific behavior.
2. Precompute an array that marks, for each position, whether $a[i]$ equals $b[i]$. This captures the baseline contribution without any modifications.
3. Iterate over all subsets of characters in $a$ using a bitmask. For each mask, interpret it as the set of characters we choose to include in $Q$. If the number of chosen characters exceeds $k$, we discard this mask immediately since it violates the constraint.
4. For a fixed mask, simulate the effect on each position: if $a[i]$ is in the mask, we can freely change it to match $b[i]$, so that position becomes “fixable”. If not, the position is locked and only contributes if already equal.
5. Convert the resulting array into a gain array where each position contributes 1 if it can be made equal to $b[i]$, otherwise 0. The problem reduces to counting how many substrings are fully supported by this array.
6. Compute the number of valid substrings by scanning left to right and maintaining the length of the current valid segment. Every time we extend a valid segment of length $L$, we add $L$ to the answer since all suffix substrings ending at that point are valid.
7. Track the maximum over all masks.

The core idea is that for a fixed choice of modifiable characters, validity becomes a simple contiguous structure problem over positions, and substring counting collapses into linear accumulation.

### Why it works

For any fixed subset of characters, each position independently becomes either fully correctable or permanently constrained. This independence ensures that substring validity depends only on whether all positions in the substring are correctable or already matching. The linear scan correctly counts all valid substrings because every valid ending position contributes exactly the number of valid starting positions within the current contiguous segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = input().strip()
        b = input().strip()

        # compress characters of a (at most 10 distinct)
        chars = list(set(a))
        m = len(chars)
        idx = {c: i for i, c in enumerate(chars)}

        # precompute equality
        eq = [1 if a[i] == b[i] else 0 for i in range(n)]

        ans = 0

        # iterate all subsets of characters in a
        for mask in range(1 << m):
            if mask.bit_count() > k:
                continue

            # build transformed validity array
            ok = [0] * n
            for i in range(n):
                if eq[i]:
                    ok[i] = 1
                else:
                    if mask & (1 << idx[a[i]]):
                        ok[i] = 1

            # count valid substrings in ok array
            cur = 0
            total = 0
            for i in range(n):
                if ok[i]:
                    cur += 1
                    total += cur
                else:
                    cur = 0

            ans = max(ans, total)

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first compresses the alphabet of $a$ because the entire decision space depends only on those characters. The bitmask loop enumerates all valid choices of characters to include in the modification set, pruning any mask that exceeds $k$.

For each mask, we build a binary array representing which positions can be made equal to $b$. A position is always good if it already matches; otherwise it becomes good only if its character is in the chosen mask. This directly encodes the effect of the operation constraints.

The substring counting step uses the standard technique for counting all-subarray contributions in a binary array: a contiguous run of length $L$ contributes $L(L+1)/2$ substrings, accumulated incrementally as a running sum.

## Worked Examples

Consider a simple case where $a = \texttt{abc}$, $b = \texttt{abd}$, and $k = 1$.

We enumerate masks over characters $\{a,b,c\}$.

| mask | allowed chars | valid array | total substrings |
| --- | --- | --- | --- |
| 000 | {} | 110 | 3 |
| 001 | {c} | 111 | 6 |
| 010 | {b} | 110 | 3 |
| 100 | {a} | 110 | 3 |

The best choice is masking character $c$, which allows full correction at position 3, yielding all substrings valid.

Now consider a case with no flexibility, $k=0$, $a=\texttt{abc}$, $b=\texttt{abd}$.

| mask | allowed chars | valid array | total substrings |
| --- | --- | --- | --- |
| 000 | {} | 110 | 3 |

No modifications are possible, so only positions already matching contribute, and the answer is fixed.

These examples show that the optimal mask selection directly determines which mismatches can be repaired, and substring counting is a deterministic consequence of that choice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 2^{m})$ | each subset recomputes a linear scan over $n$, with $m \le 10$ |
| Space | $O(n + m)$ | arrays for input, equality, and character mapping |

Since $m \le 10$, the number of subsets is at most 1024, making the solution comfortably fast for $n \le 10^5$ across all test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = input().strip()
        b = input().strip()

        chars = list(set(a))
        idx = {c:i for i,c in enumerate(chars)}
        eq = [1 if a[i]==b[i] else 0 for i in range(n)]

        best = 0
        for mask in range(1<<len(chars)):
            if mask.bit_count() > k:
                continue
            ok = [0]*n
            for i in range(n):
                if eq[i] or (mask & (1<<idx[a[i]])):
                    ok[i]=1
            cur = ans = 0
            for v in ok:
                if v:
                    cur += 1
                    ans += cur
                else:
                    cur = 0
            best = max(best, ans)

        out.append(str(best))
    return "\n".join(out)

# sample checks (abbreviated style)
assert run("1\n3 1\nabc\nabd\n") == "6"
assert run("1\n3 0\nabc\nabd\n") == "3"
assert run("1\n3 10\nabc\nabd\n") == "6"
assert run("1\n4 1\nabcd\naxcb\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 0 abc abd | 3 | no modifications allowed |
| 3 1 abc abd | 6 | optimal single-character repair |
| 4 1 abcd axcb | 6 | nontrivial mismatch structure |

## Edge Cases

When $k = 0$, the mask loop only allows the empty set, so the algorithm reduces to scanning the original equality array. On input $a=\texttt{abc}$, $b=\texttt{abd}$, the valid array is $110$, producing exactly 3 substrings, matching the expected behavior.

When $k$ is large, for example $k \ge m$, the full mask becomes valid and turns every position into a potentially correctable one. For $a=\texttt{xbb}$, $b=\texttt{xcd}$, selecting all characters ensures all positions can be aligned, producing the maximal substring count.
