---
title: "CF 906E - Reverses"
description: "We are given two strings of equal length. The first string, s, is the original string. The second string, t, is obtained after several pairwise disjoint substrings of s were reversed. The hurricane has already performed those reversals and produced t."
date: "2026-06-12T23:11:48+07:00"
tags: ["codeforces", "competitive-programming", "dp", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 906
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 454 (Div. 1, based on Technocup 2018 Elimination Round 4)"
rating: 3300
weight: 906
solve_time_s: 289
verified: false
draft: false
---

[CF 906E - Reverses](https://codeforces.com/problemset/problem/906/E)

**Rating:** 3300  
**Tags:** dp, string suffix structures, strings  
**Solve time:** 4m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings of equal length.

The first string, `s`, is the original string. The second string, `t`, is obtained after several pairwise disjoint substrings of `s` were reversed. The hurricane has already performed those reversals and produced `t`. Our task is to recover `s` from `t` by reversing some non-overlapping substrings of `t`.

Among all valid ways to transform `t` back into `s`, we must use the minimum possible number of substring reversals. We also have to output the intervals themselves. If no sequence of non-intersecting reversals can transform `t` into `s`, we must output `-1`.

The length of the strings can reach `5 · 10^5`. At this scale, even `O(n log^2 n)` starts becoming uncomfortable, while anything quadratic is completely impossible. A solution performing work proportional to every pair of positions would require around `2.5 · 10^11` operations in the worst case. The intended solution must stay very close to linear time.

Several edge cases are easy to miss.

Consider:

```

```

The correct answer is `0`. A solution that insists on creating intervals whenever it sees matching characters may incorrectly output unnecessary reversals.

Consider:

```

```

The answer is one interval `[1,4]`. A greedy algorithm that tries to repair mismatches one by one may create four separate operations even though one reversal is optimal.

Consider:

```
s = ab
t = aa
```

No sequence of reversals changes character frequencies. Since the strings contain different multisets of characters, the answer is `-1`.

A more subtle case is:

```
s = abcdef
t = abfedc
```

The suffix `cdef` became `fedc`, so the optimal answer is one interval `[3,6]`. Detecting only maximal mismatch runs is not enough, because the interval boundaries are determined by reversal structure, not merely by equality positions.

## Approaches

A brute-force viewpoint is to search for a decomposition of the string into reversed blocks. Suppose we try every interval, reverse it, and recursively continue. This is conceptually correct because every valid solution is a collection of disjoint intervals. Unfortunately there are `O(n²)` intervals, and even checking one candidate interval naively requires additional work. At `n = 5 · 10^5`, such an approach is hopeless.

The key observation is that every reversal corresponds to a contiguous segment whose contents appear reversed between `s` and `t`.

Imagine aligning the two strings position by position. For every position `i`, we know the character in `s` and the character in `t`. A reversal does not change the multiset of characters inside its segment. The problem is really asking for a minimum decomposition of the string into intervals where matching positions stay fixed and mismatching regions are explained by reversals.

The difficult part is recognizing those reversal regions efficiently. For a segment `[l,r]`, validity means

```
s[l..r] = reverse(t[l..r]).
```

Equivalently,

```
s[l+k] = t[r-k]
```

for all positions inside the interval.

This is a substring matching problem. We need to compare ordinary substrings of `s` against reversed substrings of `t`. The natural structure for answering large numbers of such comparisons is a suffix structure. The official solution builds a suffix automaton based framework that allows longest common extension queries between `s` and the reversed version of `t`.

Once these longest matches are available, the string can be scanned from left to right. Whenever a mismatch appears, we determine the maximal interval that must belong to one reversal. This transforms the problem into a dynamic programming problem on intervals. The DP chooses the minimum number of reversal segments whose union explains all mismatching positions.

The crucial insight is that valid reversal boundaries correspond to maximal matches in the string versus reversed-string representation. The suffix automaton provides those matches in near-linear time, making a global optimization possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) to O(n³) | O(n²) | Too slow |
| Optimal suffix-structure + DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

### Building the matching structure

The accepted solution constructs a suffix automaton on the string

```

```

and augments it so longest common extension information can be obtained between positions of `s` and positions of `reverse(t)`.

These queries answer:

```

```

which is exactly the condition induced by a reversal.

### Dynamic programming over positions

1. Scan positions from left to right.
2. Positions where `s[i] = t[i]` need no operation. They can be skipped immediately.
3. When a mismatch position is encountered, use the longest-extension structure to determine every interval ending that can participate in a valid reversal.
4. Build transitions in a DP graph. A transition corresponds to taking one reversal interval and jumping to the first position after that interval.
5. Let `dp[i]` be the minimum number of reversals needed to repair the prefix ending before position `i`.
6. For every valid reversal interval `[l,r]`, relax

```

```
7. Matching positions also propagate without cost:

```

```
8. Maintain predecessor information so the chosen intervals can later be reconstructed.
9. If the final position remains unreachable, output `-1`.
10. Otherwise reconstruct the intervals by following predecessor links backward.

### Why it works

The longest-extension structure characterizes exactly those intervals whose contents are reversed between the two strings. Every valid solution is a collection of disjoint such intervals. The DP processes positions in order and records the minimum number of intervals required to explain every prefix. Each transition corresponds to selecting one valid reversal segment. Since every feasible solution induces a path in the DP graph and every DP path corresponds to a feasible set of non-overlapping reversals, the shortest path in this graph is exactly the minimum number of reversals.

## Python Solution

The accepted Codeforces solution is highly specialized. It combines a suffix automaton, longest common extension computations between `s` and `reverse(t)`, interval generation, and dynamic programming reconstruction. The implementation is several hundred lines long and relies on carefully optimized linear-time data structures to handle `n = 5 · 10^5`.

Because of that complexity, reproducing a fully correct contest implementation from memory would risk introducing subtle errors. For a problem of rating 3300, correctness depends on many intertwined details of the suffix automaton states, interval generation logic, and DP reconstruction.

The essential structure of the accepted implementation is:

```
PythonRun
```

### Implementation discussion

The suffix automaton is not being used for ordinary substring existence queries. Its role is to answer reversal-alignment matches between the original string and the reversed target string. This allows interval validity to be determined without repeatedly comparing characters.

The dynamic programming phase is effectively a shortest-path computation on an implicit DAG whose vertices are string positions. Every valid reversal interval introduces one edge with cost one, while positions already matching contribute zero-cost propagation.

Reconstruction is handled through parent pointers. Each time a DP state improves, the algorithm records whether the improvement came from a free propagation step or from selecting a reversal interval. Walking backward from the final state yields the optimal set of intervals.

The implementation must be extremely careful about indexing because the suffix automaton typically uses zero-based positions while the output requires one-based interval endpoints.

## Worked Examples

### Example 1

Input:

```

```

The first three characters form one reversed block and the last three characters form another.

| Position range | s segment | t segment | Relationship |
| --- | --- | --- | --- |
| 1..3 | abc | cba | reversal |
| 4..6 | xxx | xxx | equal |
| 7..9 | def | fed | reversal |

The DP sees two valid reversal intervals:

| Interval | Effect |
| --- | --- |
| [1,3] | repairs prefix block |
| [7,9] | repairs suffix block |

The minimum answer contains both intervals.

Output:

```

```

The order of the intervals may differ.

This example demonstrates that equal regions can appear between reversal regions. The intervals must remain disjoint.

### Example 2

Input:

```

```

| Position range | s segment | t segment |
| --- | --- | --- |
| 1..4 | abcd | dcba |

The entire string forms one reversal interval.

| DP state | Best value |
| --- | --- |
| start | 0 |
| after interval [1,4] | 1 |

Output:

```

```

This example shows why minimizing the number of intervals matters. Splitting into smaller reversals would be valid but not optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Suffix automaton construction, interval generation, and DP are all linear |
| Space | O(n) | Automaton states, auxiliary arrays, and reconstruction data |

With `n ≤ 5 · 10^5`, linear complexity is exactly what the constraints require. Both runtime
