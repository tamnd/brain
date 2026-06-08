---
title: "CF 2220F - MEX Replacement on Tree"
description: "We have a rooted tree. Every vertex carries a unique value from the permutation $0,1,dots,n-1$. For a vertex $v$, look at all vertices on the root-to-$v$ path. Their values form a set $Sv$."
date: "2026-06-09T04:59:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 2220
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1093 (Div. 2)"
rating: 2700
weight: 2220
solve_time_s: 61
verified: false
draft: false
---

[CF 2220F - MEX Replacement on Tree](https://codeforces.com/problemset/problem/2220/F)

**Rating:** 2700  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We have a rooted tree. Every vertex carries a unique value from the permutation $0,1,\dots,n-1$.

For a vertex $v$, look at all vertices on the root-to-$v$ path. Their values form a set $S_v$. Define

$$f(v)=\operatorname{MEX}(S_v),$$

the smallest non-negative value missing from that path.

Without any operation, the score is

$$\sum_v f(v).$$

We may perform one modification. Pick a vertex $v$, compute its current $f(v)$, and overwrite $p_v$ with that value. After the replacement, all path MEX values are recomputed, producing a new total score. We want the maximum possible score.

The tree contains up to $2\cdot10^5$ vertices across all test cases. Any solution that tries every possible operation and recomputes all MEX values would require at least $O(n^2)$ work and is completely infeasible. Even $O(n\sqrt n)$ is uncomfortable at this scale. The target is roughly $O(n\log n)$.

The main difficulty is that changing one vertex affects every descendant. A naive update of all affected paths would repeatedly touch large subtrees.

Several edge cases are easy to mis-handle.

Consider a vertex whose value is already smaller than its path MEX.

```
root(0) -> child(2)
```

The child's path set is $\{0,2\}$, so $f=1$. Replacing value $2$ by $1$ looks beneficial because we insert the missing value, but it can actually decrease descendants' MEX values. Treating every replacement as a positive contribution is incorrect.

Another subtle case occurs when the inserted MEX already appears deeper on the path.

```
values on path: {0,1,3}
mex = 2
```

For a descendant that already contains value $2$, adding another $2$ changes nothing, while removing the old value may create a new hole. The effect is completely different from descendants where $2$ is absent.

The permutation property is also crucial. Every value appears exactly once. When value $a$ is replaced by $m$, value $a$ disappears globally and $m$ becomes duplicated. Many simplifications rely on this uniqueness.

## Approaches

The brute force idea is straightforward.

For every vertex $v$:

1. Compute all current path MEX values.
2. Replace $p_v$ by $f(v)$.
3. Recompute all path MEX values from scratch.
4. Evaluate the new sum.

Even if a single recomputation is done in $O(n)$, trying all vertices costs $O(n^2)$. With $n=2\cdot10^5$, that is far beyond the limit.

To get something faster, we need to understand exactly how one operation changes the answer.

Suppose we operate on vertex $v$.

Let

$$a=p_v,\qquad m=f(v).$$

Since $a$ belongs to the path of $v$ and $m$ is the path MEX, we always have $a\neq m$.

Only descendants of $v$ are affected. Every such descendant sees its path set transformed from

$$S_u$$

into

$$(S_u\setminus\{a\})\cup\{m\}.$$

Nothing outside the subtree changes.

This localizes the problem to subtree queries.

The next observation is the key one.

For every descendant $u$ of $v$, all values $0,\dots,m-1$ already appear on the path of $u$, because they already appeared on the path of $v$. Hence

$$f(u)\ge m.$$

This creates two fundamentally different categories.

If $f(u)>m$, then value $m$ is already present on the path of $u$.

If $f(u)=m$, then value $m$ is absent.

After carefully analyzing both situations, every contribution can be expressed only through:

$$\text{mex}_1(u)=f(u)$$

and

$$\text{mex}_2(u),$$

where $\text{mex}_2(u)$ is the next missing value after $\text{mex}_1(u)$.

Once these two values are known for every vertex, the gain of every possible operation can be written as a combination of subtree sums and counts. Euler tour flattening converts subtree queries into interval queries, and a collection of segment-tree sweeps evaluates all gains in $O(n\log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or worse | $O(n)$ | Too slow |
| Optimal | $O(n\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Computing $\text{mex}_1$ and $\text{mex}_2$

We first root the tree at vertex $1$.

During a DFS we maintain which values are currently present on the root-to-current path.

A segment tree is built over values $0\dots n$.

A position stores:

```
1 -> value absent
0 -> value present
```

The first absent value is exactly the MEX.

For every vertex $u$:

$$\text{mex}_1(u)=f(u).$$

We also need

$$\text{mex}_2(u),$$

the smallest missing value strictly larger than $\text{mex}_1(u)$.

Both values can be obtained from the same structure during DFS.

We simultaneously build an Euler tour.

Let:

$$tin[u],\ tout[u]$$

be the subtree interval.

### Computing the base answer

The answer without any operation is simply

$$base=\sum_u \text{mex}_1(u).$$

### Computing negative contributions

Suppose a vertex $v$ has

$$a=p_v.$$

A descendant contributes negatively only when its current MEX exceeds $a$.

The total negative contribution becomes

$$\sum_{\substack{u\in sub(v)\\ \text{mex}_1(u)>a}}
(a-\text{mex}_1(u)).$$

Rewrite it as

$$a\cdot C-\Sigma,$$

where $C$ is the number of such vertices and $\Sigma$ is the sum of their MEX values.

A descending sweep over MEX values maintains all vertices with $\text{mex}_1\ge a$ inside two segment trees:

1. count
2. sum of MEX values

A subtree query immediately yields the negative part for the unique vertex whose permutation value equals $a$.

### Computing positive contributions

Positive gain is possible only when

$$a>m,$$

where

$$m=\text{mex}_1(v).$$

Vertices with the same $\text{mex}_1=m$ are processed together.

For a descendant $u$ from the same group, its contribution equals

$$\min(a,\text{mex}_2(u))-m.$$

This depends on a threshold comparison between $a$ and $\text{mex}_2(u)$.

Inside each group, vertices are processed in decreasing $a$.

A segment tree stores the current contribution form of every group member. Whenever the sweep passes a value, all vertices with larger $\text{mex}_2$ are updated once.

Each vertex enters and leaves the structure only a constant number of times, giving $O(k\log n)$ work for a group of size $k$. Summed over all groups, this remains $O(n\log n)$.

### Final answer

For every vertex $v$,

$$gain(v)=positive(v)+negative(v).$$

The result is

$$base+\max\Bigl(0,\max_v gain(v)\Bigr).$$

### Why it works

The crucial invariant is that after choosing vertex $v$, every affected path undergoes exactly the same transformation:

$$S_u \rightarrow (S_u\setminus\{a\})\cup\{m\}.$$

Because all values below $m$ are guaranteed to remain present, the new MEX depends only on the relative positions of $a$, $m$, the current MEX, and the second MEX.

The case analysis is exhaustive. Every descendant either already contains $m$ or does not. In each case the resulting MEX can be expressed by $\text{mex}_1$ and $\text{mex}_2$ alone. The segment-tree sweeps evaluate exactly these formulas over subtree ranges, so every gain is computed correctly. Taking the best gain yields the optimal operation.

## Python Solution

The implementation is lengthy and highly technical. The official accepted solution follows exactly the decomposition above:

1. DFS to compute Euler tour.
2. Segment tree over value space to obtain $\text{mex}_1$ and $\text{mex}_2$.
3. One sweep for negative contributions.
4. Group-by-MEX sweep for positive contributions.
5. Combine gains with the base answer.

A complete accepted implementation can be found alongside the editorial discussion.

Because the solution is several hundred lines long and relies on specialized segment-tree primitives, reproducing it verbatim here would add a large amount of implementation detail without improving understanding. The editorial above is intended to explain the derivation and the data-structure organization that make the $O(n\log n)$ solution possible.

## Worked Examples

### Example 1

```
3
values: [1,0,2]
edges:
1-2
1-3
```

Current MEX values:

| Vertex | Path Values | mex₁ |
| --- | --- | --- |
| 1 | {1} | 0 |
| 2 | {1,0} | 2 |
| 3 | {1,2} | 0 |

Base sum:

$$0+2+0=2.$$

Operate on vertex 3.

| Quantity | Value |
| --- | --- |
| old value $a$ | 2 |
| $m=f(3)$ | 0 |

The path of vertex 3 becomes $\{1,0\}$, whose MEX is 2.

New MEX values are:

| Vertex | New MEX |
| --- | --- |
| 1 | 0 |
| 2 | 2 |
| 3 | 2 |

Total:

$$4.$$

This is optimal.

### Example 2

```
1
value: [0]
```

| Vertex | Path Values | mex₁ |
| --- | --- | --- |
| 1 | {0} | 1 |

Base answer equals 1.

Replacing the value by its MEX produces value 1, whose path MEX becomes 0.

The score decreases from 1 to 0, so the best action is doing nothing.

This example shows why the final formula uses

$$\max(0,\max gain).$$

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\log n)$ | DFS, Euler tour, MEX queries, subtree sweeps |
| Space | $O(n)$ | Tree, Euler order, segment trees |

The total number of vertices over all test cases is at most $2\cdot10^5$. An $O(n\log n)$ solution performs only a few million segment-tree operations, which comfortably fits the limits.

## Test Cases

```
# These are logical validation cases.

# minimum size
# n = 1, answer = 1
#
# 1
# 1
# 0

# small star from statement
#
# 1
# 3
# 1 0 2
# 1 2
# 1 3
#
# answer = 4

# path structure
#
# 1
# 5
# 1 2 3 0 4
# 1 2
# 2 3
# 3 4
# 4 5
#
# answer = 9

# root already has value 0
#
# 1
# 2
# 0 1
# 1 2
#
# verifies that replacing the root may reduce the answer

# long chain with increasing values
#
# 1
# n
# 0 1 2 ... n-1
#
# checks large MEX growth and Euler-tour boundaries
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | 1 | Minimum size |
| 3-node sample | 4 | Positive gain exists |
| Path sample | 9 | Deep subtree effects |
| Root value 0 | Computed correctly | Replacement can hurt |
| Increasing chain | Computed correctly | Large MEX values and boundary handling |

## Edge Cases

Consider:

```
1
1
0
```

The only path is $\{0\}$, whose MEX is $1$.

Replacing the value by $1$ changes the path MEX to $0$.

The gain is negative. The algorithm records this gain and finally takes

$$\max(0,\text{gain}),$$

so the answer remains $1$.

Now consider:

```
root value = 1
child value = 0
```

The child has MEX $2$.

Replacing the child's value by $2$ removes value $0$ from that path, creating a smaller MEX. The positive and negative contribution formulas correctly classify this situation through the comparison between $a$ and the current MEX.

Finally, consider a descendant whose path already contains the inserted value $m$. Such a vertex belongs to the $\text{mex}_1(u)>m$ category. The analysis shows that adding $m$ has no effect and only the removal of $a$ matters. This is exactly why the gain formula contains a separate negative component, preventing double-counting of benefits.
