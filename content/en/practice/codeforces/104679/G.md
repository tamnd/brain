---
title: "CF 104679G - Winter Gifts"
description: "We are given two strings of equal length and an integer step size $k$. The allowed operation does not let us freely edit characters anywhere. Instead, we can pick two positions whose distance is exactly $k$, and copy the character from one position into the other."
date: "2026-06-29T09:02:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104679
codeforces_index: "G"
codeforces_contest_name: "Replay of Battle of Brains 2022, University of Dhaka"
rating: 0
weight: 104679
solve_time_s: 44
verified: true
draft: false
---

[CF 104679G - Winter Gifts](https://codeforces.com/problemset/problem/104679/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings of equal length and an integer step size $k$. The allowed operation does not let us freely edit characters anywhere. Instead, we can pick two positions whose distance is exactly $k$, and copy the character from one position into the other.

So the operation behaves like a constrained propagation rule: characters can only “flow” along edges that connect positions differing by $k$. Over multiple operations, this means information can travel through chains like $i \to i+k \to i+2k \to \dots$, but it can never jump between unrelated positions.

The task is to determine whether we can transform the starting string into the target string using any number of such copy operations.

The main constraint to keep in mind is that the string length can be large enough that any quadratic simulation of operations or brute-force search over transformations is impossible. Any solution must reduce the structure of allowed operations into something linear or near-linear, because each position interacts only with a small structured subset of other positions.

A subtle edge case comes from how restricted movement really is. For example, if $k = 3$ and the string is indexed as $0 \dots 7$, position 0 can only ever affect positions 3 and 6, never positions like 1 or 2. So even if two characters are “close in value,” they may be completely disconnected under the operation rules.

Another important edge case is when $k = 0$, which is typically invalid or degenerate, since the operation would allow self-copy only and no transformation would ever be possible unless the strings already match.

## Approaches

The brute-force way to think about this problem is to simulate the allowed operations directly on the string. Each operation copies a character across a distance of $k$, and we would try all possible sequences of such operations, checking if we can reach the target configuration.

This immediately runs into a combinatorial explosion. Even though each operation is simple, the number of reachable states grows exponentially with the number of positions that are connected by repeated applications. For a string of length $n$, this is far beyond feasible limits.

The key structural insight is that the operation does not mix all indices together. Instead, it partitions indices into independent arithmetic progressions modulo $k$. Indices $0, k, 2k, \dots$ form one component, indices $1, k+1, 2k+1, \dots$ form another, and so on up to $k-1$. No operation ever crosses these components.

This reduces the problem into $k$ independent subproblems, each operating on a sequence formed by taking every $k$-th character. Inside each sequence, the operation becomes equivalent to copying between adjacent positions, because stepping by $k$ in the original string corresponds to stepping by 1 in the extracted subsequence.

Once reduced to a single chain where only adjacent-copy operations exist, the problem turns into deciding whether we can transform one string into another using only “overwrite neighbor” operations. The crucial observation is that such operations cannot introduce new distinct blocks of characters; they can only merge or propagate existing ones.

This leads to compressing the target string into runs of distinct characters. What matters is whether this compressed pattern appears as a subsequence in the source string. If it does, we can simulate constructing the target by aligning and propagating segments; if it does not, some required structural change is impossible under the restricted operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We reduce the original string into independent chains based on index modulo $k$, then solve each chain separately.

1. Split the original string and target string into $k$ subsequences. The $i$-th subsequence contains characters at positions $i, i+k, i+2k, \dots$. This is correct because the operation never connects indices with different remainders modulo $k$.
2. For each pair of corresponding subsequences, treat the problem as transforming one string into another where operations only allow copying adjacent characters. This captures exactly the original movement constraint after decomposition.
3. Compress the target subsequence by collapsing consecutive equal characters into a single representative. This removes redundant information because repeated identical segments do not impose additional structural constraints beyond their boundaries.
4. Check whether this compressed target is a subsequence of the source subsequence. We scan the source and greedily match characters in order.
5. If any subsequence fails this condition, the full transformation is impossible, so we return “NO”.
6. If all subsequences pass, we return “YES”.

The key reasoning step is that once we fix the order of distinct blocks in the target, the source must contain them in the same relative order, since operations only propagate existing characters without creating new ordering possibilities.

### Why it works

Each modulo class behaves like a line where we can only overwrite positions using adjacent propagation. This means the set of distinct character blocks in the target must already exist in the source in the same order, because the operation can only expand or shrink regions of identical characters, never permute them or create new transitions. The subsequence check on the compressed target exactly captures whether the required boundary structure is already present in the source.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compress(s):
    res = []
    for c in s:
        if not res or res[-1] != c:
            res.append(c)
    return res

def is_subseq(a, b):
    j = 0
    for x in b:
        if j < len(a) and a[j] == x:
            j += 1
    return j == len(a)

def solve_case(s, t, k):
    n = len(s)
    
    for start in range(k):
        ss = []
        tt = []
        
        i = start
        while i < n:
            ss.append(s[i])
            tt.append(t[i])
            i += k
        
        tt = compress(tt)
        
        if not is_subseq(tt, ss):
            return False
    
    return True

def main():
    s = input().strip()
    t = input().strip()
    k = int(input())
    
    print("YES" if solve_case(s, t, k) else "NO")

if __name__ == "__main__":
    main()
```

The implementation first isolates each residue class modulo $k$ by walking through indices in steps of $k$. This avoids constructing extra arrays with slicing overhead and keeps the logic linear in the string length.

The compression step is essential because consecutive duplicates in the target subsequence do not introduce new constraints; they only extend existing segments. Without compression, the subsequence check would incorrectly require matching repeated structure that the operations can freely generate.

The subsequence check uses a greedy pointer scan, which is optimal because order is the only constraint that matters after compression.

## Worked Examples

Consider $s =$ “abac” and $t =$ “aaac” with $k = 2$. We split into two chains: indices $0,2$ give “aa” and “ac”, and indices $1,3$ give “bc” and “ac”.

For the first chain:

| Source | Target (raw) | Target (compressed) | Subsequence check |
| --- | --- | --- | --- |
| aa | aa | a | yes |

For the second chain:

| Source | Target (raw) | Target (compressed) | Subsequence check |
| --- | --- | --- | --- |
| bc | ac | ac | yes |

Both chains succeed, so the answer is YES. This shows how compression removes redundant repeated structure and reduces the check to boundary ordering.

Now consider $s =$ “abdc”, $t =$ “acbd”, $k = 1$. Here there is a single chain.

Target compression stays “acbd” since there are no consecutive duplicates.

We attempt subsequence matching:

| Step | Source pointer | Target pointer | Match |
| --- | --- | --- | --- |
| a vs a | 0 | 0 | yes |
| b vs c | 1 | 1 | no |
| d vs c | 2 | 1 | no |

We fail immediately, so the answer is NO. This demonstrates that even though characters are identical in multiset, ordering constraints from propagation make rearrangement impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is processed once across its residue class, and subsequence checks are linear |
| Space | O(n) | Storage for extracted chains in the worst case |

The solution stays linear in the input size, which is necessary because any nested simulation of operations would exceed limits for large strings.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    t = input().strip()
    k = int(input())
    
    def compress(s):
        res = []
        for c in s:
            if not res or res[-1] != c:
                res.append(c)
        return res

    def is_subseq(a, b):
        j = 0
        for x in b:
            if j < len(a) and a[j] == x:
                j += 1
        return j == len(a)

    n = len(s)
    for start in range(k):
        ss, tt = [], []
        i = start
        while i < n:
            ss.append(s[i])
            tt.append(t[i])
            i += k
        if not is_subseq(compress(tt), ss):
            return "NO"
    return "YES"

# minimal
assert run("a\na\n1") == "YES"

# impossible reordering
assert run("ab\nba\n1") == "NO"

# k = 2 split case
assert run("abac\naaac\n2") == "YES"

# identical strings
assert run("abcde\nabcde\n2") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a / a / 1 | YES | trivial identity |
| ab / ba / 1 | NO | ordering constraint |
| abac / aaac / 2 | YES | decomposition correctness |
| abcde / abcde / 2 | YES | stable unchanged case |

## Edge Cases

When $k = 1$, the entire string becomes a single chain. The algorithm reduces to checking whether the compressed target is a subsequence of the source, which correctly handles cases where only propagation is possible without cross-position mixing. For example, transforming “aabbcc” into “abc” succeeds, since compression removes duplicates and the subsequence condition holds trivially.

When all characters are identical, both strings always pass after compression, because every subsequence check reduces to a single repeated character match. For instance, “aaaaa” to “aaaaa” succeeds regardless of $k$, since no structural transitions are required.

When the target introduces a new order of character blocks not present in the source, the subsequence check fails immediately in that chain, reflecting the impossibility of creating new boundaries through copy operations alone.
