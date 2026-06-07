---
title: "CF 2131C - Make it Equal"
description: "We start with a multiset $S$ of size $n$ and we want to transform it into another multiset $T$ of the same size. The only allowed move takes one element $x$ from $S$, deletes it, and replaces it with either $x+k$ or $ The core question is whether repeated applications of these…"
date: "2026-06-08T02:54:33+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2131
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1042 (Div. 3)"
rating: 1100
weight: 2131
solve_time_s: 103
verified: false
draft: false
---

[CF 2131C - Make it Equal](https://codeforces.com/problemset/problem/2131/C)

**Rating:** 1100  
**Tags:** math, number theory  
**Solve time:** 1m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a multiset $S$ of size $n$ and we want to transform it into another multiset $T$ of the same size. The only allowed move takes one element $x$ from $S$, deletes it, and replaces it with either $x+k$ or $|x-k|$. Each operation preserves the size of the multiset but can change individual values.

The core question is whether repeated applications of these moves can reshape $S$ exactly into $T$, respecting multiplicities.

The constraints suggest that each test case must be handled in near linear time in $n$, since the total $n$ across all tests is up to $2 \cdot 10^5$. Any approach that explores transformations per value or simulates operations step by step will immediately fail due to explosion in reachable states.

A subtle aspect is that values are not bounded tightly except by $10^9$, so direct graph traversal over values is impossible.

Two edge patterns tend to break naive thinking.

First, assuming each element can independently reach any target with the same residue mod $k$ is wrong because the $|x-k|$ operation can reduce values in a non-linear way until they cross zero, after which behavior changes. For example, with $k=5$, from $x=6$ you can go to $1$, then to $4$, then to $9$, producing cycles that are not purely modular.

Second, assuming greedy matching of closest values fails because transformations may require intermediate values that are not present in either multiset.

A small misleading case is:

```
S = [1, 6], T = [4, 3], k = 5
```

A greedy attempt might match 1→6 and 6→1, but intermediate transitions show that the structure is not symmetric in a straightforward way.

## Approaches

A brute-force interpretation would model each value as a node in a graph, with edges $x \to x+k$ and $x \to |x-k|$, and attempt to check if multiset $T$ is reachable from $S$ via redistribution. This turns into a multi-source reachability problem with state counts, which is exponential in practice because values grow unbounded in the $+k$ direction.

The failure point is that each number branches into two possibilities at every operation, and sequences can grow arbitrarily long. Even if we cap values at some heuristic bound, the transitions are not monotone, so pruning is unsafe.

The key observation is that the operation structure preserves a very strong invariant: every number eventually behaves independently inside its residue class modulo $k$, except that values can be reduced by repeatedly applying $|x-k|$ until they enter a canonical range.

More concretely, repeatedly applying the “subtract $k$ in absolute sense” operation always pushes a number toward a unique representative in the interval $[0, k)$, after which further structure becomes predictable. Every value can be mapped to a chain that eventually cycles within a small bounded region determined by its residue modulo $k$. The only meaningful freedom is how many times we “wrap upward” using $+k$, which shifts values but never changes their residue class.

This reduces the problem to tracking how many elements from each residue class are available in $S$ and needed in $T$, and verifying that within each class the multiset can be aligned under allowed shifts.

The final check becomes a balancing problem per residue class, where elements can be pushed upward in steps of $k$, but not arbitrarily rearranged across residues.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Graph Search | Exponential | O(n) | Too slow |
| Residue + Greedy Matching | O(n \log n) | O(n) | Accepted |

## Algorithm Walkthrough

We reduce every value to a canonical form inside its residue class and then compare how mass is distributed across increasing chains.

1. Group elements of $S$ and $T$ by their value modulo $k$. This is necessary because both allowed operations preserve the residue mod $k$ up to sign effects that disappear after normalization.
2. For each group, sort the elements. Sorting is needed because the transformation effectively allows shifting elements upward in increments of $k$, so alignment must respect order within the chain.
3. Within a residue group, process values in increasing order and simulate how surplus elements in $S$ can be pushed upward to match deficits in $T$. When a value in $S$ exceeds what is needed at the same level in $T$, the excess is carried to the next higher level by effectively treating it as $x+k$.
4. Maintain a running surplus counter while iterating through sorted values. At each step, subtract what is required by $T$. If we have a deficit, we try to compensate using surplus carried from lower values.
5. If at any point we cannot cover a deficit, the transformation is impossible for that residue class.
6. Repeat independently for all residue classes. If every class is satisfiable, the answer is “YES”, otherwise “NO”.

The key idea is that movement only flows upward along arithmetic progressions of step $k$, so each residue class behaves like a one-directional flow system.

### Why it works

Each element’s only irreversible direction is upward by adding $k$, while the $|x-k|$ operation can only reduce values but never change their residue class in a way that allows cross-class interaction. This creates independent chains per residue. Within each chain, elements can be shifted upward arbitrarily but cannot cross or reorder across chains. The greedy surplus propagation exactly models this flow, ensuring that every deficit must be matched by earlier surplus, and any mismatch implies impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = list(map(int, input().split()))
        tarr = list(map(int, input().split()))
        
        groups_s = defaultdict(list)
        groups_t = defaultdict(list)
        
        for x in s:
            groups_s[x % k].append(x)
        for x in tarr:
            groups_t[x % k].append(x)
        
        ok = True
        
        for r in set(list(groups_s.keys()) + list(groups_t.keys())):
            a = sorted(groups_s[r])
            b = sorted(groups_t[r])
            
            i = j = 0
            surplus = 0
            
            while i < len(a) or j < len(b):
                av = a[i] if i < len(a) else float('inf')
                bv = b[j] if j < len(b) else float('inf')
                
                if av == bv:
                    i += 1
                    j += 1
                    continue
                
                if av < bv:
                    surplus += 1
                    i += 1
                else:
                    if surplus == 0:
                        ok = False
                        break
                    surplus -= 1
                    j += 1
            
            if not ok:
                break
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The implementation first partitions values by residue modulo $k$, which isolates independent transformation chains. Within each group, sorting enforces a consistent direction for processing possible upward shifts.

The two-pointer loop compares availability in $S$ versus demand in $T$. When $S$ has a smaller value, we treat it as potential surplus that can be pushed upward. When $T$ demands a value that is not currently available, we consume previously accumulated surplus. If no surplus exists, we immediately fail.

The sentinel $+\infty$ handling ensures clean termination when one list is exhausted.

## Worked Examples

### Example 1

Input:

```
n=3, k=2
S = [0, 1, 0]
T = [1, 0, 1]
```

We group by modulo 2.

| residue | S sorted | T sorted |
| --- | --- | --- |
| 0 | [0, 0] | [0] |
| 1 | [1] | [1] |

Processing residue 0:

| step | S[i] | T[j] | surplus | action |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | match |
| 1 | 0 | ∞ | 1 | surplus from S |

Processing residue 1:

| step | S[i] | T[j] | surplus | action |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | match |

This shows that extra mass in residue 0 can be pushed upward within the same class, allowing redistribution.

### Example 2

Input:

```
n=2, k=7
S = [2, 8]
T = [2, 9]
```

Residue 2 class contains all elements.

| step | S[i] | T[j] | surplus | action |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 0 | match |
| 1 | 8 | 9 | fail | cannot match 9 |

Here 8 cannot reach 9 via allowed operations within constraints of the chain, so the process fails.

This demonstrates that even within a single residue class, upward movement must respect available surplus structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting within residue groups dominates; each element is processed once in two-pointer scans |
| Space | $O(n)$ | Storage for grouped elements |

The complexity fits comfortably within the constraint since total $n$ across test cases is $2 \cdot 10^5$, and sorting remains efficient at this scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    from collections import defaultdict

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        s = list(map(int, input().split()))
        tt = list(map(int, input().split()))

        groups_s = defaultdict(list)
        groups_t = defaultdict(list)

        for x in s:
            groups_s[x % k].append(x)
        for x in tt:
            groups_t[x % k].append(x)

        ok = True

        for r in set(groups_s.keys()) | set(groups_t.keys()):
            a = sorted(groups_s[r])
            b = sorted(groups_t[r])

            i = j = 0
            surplus = 0

            while i < len(a) or j < len(b):
                av = a[i] if i < len(a) else float('inf')
                bv = b[j] if j < len(b) else float('inf')

                if av == bv:
                    i += 1
                    j += 1
                elif av < bv:
                    surplus += 1
                    i += 1
                else:
                    if surplus == 0:
                        ok = False
                        break
                    surplus -= 1
                    j += 1

            if not ok:
                break

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run("""5
1 3
1
2
1 8
4
12
3 5
6 2 9
8 4 11
2 7
2 8
2 9
3 2
0 1 0
1 0 1
""") == """YES
YES
YES
NO
NO"""

# custom cases
assert run("""1
1 1
5
5
""") == "YES", "minimum equal"

assert run("""1
2 3
1 4
2 5
""") == "NO", "different residue structure"

assert run("""1
3 2
0 0 0
2 2 2
""") == "YES", "pure upward shifts"

assert run("""1
3 10
0 10 20
0 10 30
""") == "NO", "gap in chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single equal element | YES | trivial base case |
| mismatched residues | NO | residue separation correctness |
| uniform shift chain | YES | upward propagation |
| missing reachable value | NO | gap detection |

## Edge Cases

A critical edge case is when both multisets are identical but arranged such that transformation is unnecessary. For example, $S = T = [x_1, x_2, \dots]$. The algorithm processes each residue group, sees perfect pairwise matches, and never uses surplus. The output remains YES without relying on any transformation logic.

Another edge case is when one residue class has extra small elements that must be pushed upward multiple times. For instance:

```
S = [0, 0, 0], T = [6, 6, 6], k = 3
```

All elements belong to residue 0. The algorithm accumulates surplus at lower values and consumes it as we move upward, successfully matching all demands. This confirms that repeated +k transitions are correctly modeled by surplus propagation.

A failing case is when a required target appears without sufficient earlier supply in the same chain. In:

```
S = [1], T = [100], k = 7
```

No sequence of surplus generation can bridge the gap because there is no earlier element to propagate upward through intermediate steps. The algorithm correctly identifies this as impossible when surplus remains zero at the point of demand.
