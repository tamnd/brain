---
title: "CF 2033E - Sakurako, Kosuke, and the Permutation"
description: "We are given a permutation of numbers from 1 to n. We are allowed to repeatedly swap any two positions. After performing some swaps, we want the permutation to satisfy a structural condition on every index i."
date: "2026-06-08T11:43:07+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dfs-and-similar", "dsu", "graphs", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2033
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 981 (Div. 3)"
rating: 1400
weight: 2033
solve_time_s: 78
verified: true
draft: false
---

[CF 2033E - Sakurako, Kosuke, and the Permutation](https://codeforces.com/problemset/problem/2033/E)

**Rating:** 1400  
**Tags:** brute force, data structures, dfs and similar, dsu, graphs, greedy, math  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of numbers from 1 to n. We are allowed to repeatedly swap any two positions. After performing some swaps, we want the permutation to satisfy a structural condition on every index i.

At each position i, the value either already sits in its own place, meaning p[i] = i, or it forms a mutual pairing with its correct position, meaning if p[i] = x then p[x] must equal i. So every element is either a fixed point or part of a 2-cycle. No longer cycles are allowed in the final arrangement.

The task is to compute the minimum number of swaps required to transform the given permutation into any permutation that satisfies this condition.

The constraints matter strongly here. The total n across all test cases is up to 10^6, which rules out anything quadratic per test. Any solution that attempts to simulate swaps or repeatedly fix cycles by scanning arrays would fail. We need a linear or near-linear decomposition approach per test case.

A subtle failure case for naive thinking is assuming every cycle can be fixed independently with a fixed formula without considering how swaps interact globally. For example, in a 3-cycle like [2, 3, 1], one might incorrectly think it can be repaired in 1 swap, but it actually requires 2 swaps to break it into valid fixed points or 2-cycles.

Another subtle case is a mixture of cycles, such as multiple disjoint cycles of different lengths. A greedy local fix per cycle must still sum correctly over the entire structure.

## Approaches

A direct brute-force approach would try to simulate swaps until the permutation becomes valid. After each swap, we would scan all indices and check whether every position satisfies the condition. Each scan costs O(n), and in the worst case we may need O(n) swaps, leading to O(n^2) per test case, which is far too large for n up to 10^6.

The key observation is that the final structure is extremely constrained: every connected component in the permutation graph must become either a fixed point or a pair. This immediately suggests working in terms of cycles of the permutation.

Each permutation can be decomposed into disjoint cycles. Inside a cycle of length k, we must decide how many swaps are needed to transform it into valid structure. The critical insight is that swaps do not mix cycles unless we intentionally break them, so each cycle contributes independently to the answer.

For a cycle of length 1, nothing is needed. For a cycle of length 2, it is already valid as a mutual pair. For any cycle of length k ≥ 3, we must break it into valid pairs and fixed points using swaps. The optimal strategy is to reduce each such cycle using k - 1 swaps worth of structure, but more precisely, every cycle of length k contributes floor((k - 1) / 2) swaps after optimal pairing behavior emerges from swap decomposition.

This problem is equivalent to counting how many swaps are needed to convert each cycle into a set of 1-cycles and 2-cycles. Each swap can fix at most two misplaced elements inside a cycle, which leads directly to a pairing interpretation.

After decomposing into cycles, we accumulate the cost per cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Cycle simulation / brute swaps | O(n^2) | O(n) | Too slow |
| Cycle decomposition counting pairs | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a visited array and iterate through all indices from 1 to n. Each unvisited index starts a new cycle traversal.
2. Traverse the permutation starting from this index until we return to a visited node. Collect the size of the cycle. This step isolates independent structural components, which is necessary because swaps inside one cycle do not affect another.
3. For each discovered cycle, compute its contribution to the answer. If the cycle length is 1 or 2, it contributes 0 swaps. If the cycle length is k ≥ 3, it contributes floor((k - 1) / 2). This comes from pairing elements optimally within the cycle using swaps, where each swap resolves two misplaced positions in the best achievable arrangement.
4. Sum contributions over all cycles and output the result.

### Why it works

The permutation can be decomposed uniquely into disjoint cycles, and swaps only affect elements within cycles unless explicitly used to merge cycles. However, merging cycles never improves optimality because the target structure also decomposes into independent fixed points and 2-cycles. Thus each original cycle can be solved independently.

Inside a cycle of length k, the best we can do is convert it into valid fixed points and 2-cycles. Each swap can reduce the number of unresolved elements by at most 2, so the lower bound is determined by how many pairs we can form, which yields floor((k - 1) / 2). Since this bound is achievable by constructive rearrangement, summing over cycles gives the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        
        visited = [False] * (n + 1)
        ans = 0

        for i in range(1, n + 1):
            if not visited[i]:
                cur = i
                cycle_len = 0
                while not visited[cur]:
                    visited[cur] = True
                    cycle_len += 1
                    cur = p[cur - 1]

                if cycle_len >= 3:
                    ans += (cycle_len - 1) // 2

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first builds cycles using a standard permutation traversal. Each position is visited exactly once, ensuring linear complexity. The conversion from cycle to answer uses the derived formula directly, avoiding any simulation of swaps.

The important implementation detail is indexing: the permutation is 1-based in logic but stored 0-based, so every transition uses p[cur - 1].

## Worked Examples

### Example 1

Input:

```
n = 5
p = [2, 3, 4, 5, 1]
```

| Start | Cycle traversal | Cycle size | Contribution |
| --- | --- | --- | --- |
| 1 | 1 → 2 → 3 → 4 → 5 → 1 | 5 | (5-1)//2 = 2 |

Final answer: 2

This shows a single large cycle decomposes into two required swap operations.

### Example 2

Input:

```
n = 4
p = [2, 3, 4, 1]
```

| Start | Cycle traversal | Cycle size | Contribution |
| --- | --- | --- | --- |
| 1 | 1 → 2 → 3 → 4 → 1 | 4 | (4-1)//2 = 1 |

Final answer: 1

This confirms that even-length cycles are not automatically valid and still require pairing operations.

These traces highlight that the only structure that matters is cycle length, not the specific labels inside the cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once during cycle decomposition |
| Space | O(n) | Visited array and input storage |

The algorithm fits comfortably within limits because the total number of elements across test cases is 10^6, so linear traversal is optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        p = list(map(int, sys.stdin.readline().split()))
        vis = [False]*(n+1)
        ans = 0
        for i in range(1,n+1):
            if not vis[i]:
                cur = i
                cnt = 0
                while not vis[cur]:
                    vis[cur] = True
                    cnt += 1
                    cur = p[cur-1]
                if cnt >= 3:
                    ans += (cnt-1)//2
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""6
5
1 2 3 4 5
5
5 4 3 2 1
5
2 3 4 5 1
4
2 3 4 1
3
1 3 2
7
2 3 1 5 6 7 4
""") == """0
0
2
1
0
2"""

# custom cases
assert run("""1
1
1
""") == "0"

assert run("""1
3
1 2 3
""") == "0"

assert run("""1
3
2 3 1
""") == "1"

assert run("""1
6
2 1 4 3 6 5
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 identity | 0 | smallest valid case |
| identity permutation | 0 | no swaps needed |
| 3-cycle | 1 | minimal non-trivial cycle |
| all 2-cycles | 0 | already valid structure |

## Edge Cases

A single-element cycle like p[i] = i contributes nothing. The traversal immediately marks it visited and skips contribution, matching the requirement that fixed points are already valid.

A two-element cycle like [2, 1] is already a valid mutual pair. The cycle length is 2, so the formula contributes zero, and no swaps are performed.

A long odd cycle such as [2, 3, 4, 5, 1] produces a cycle length of 5. The algorithm contributes 2 swaps, which corresponds to repeatedly fixing two misplaced elements per swap until only valid structures remain.

A disjoint union of cycles demonstrates independence. For example, [2, 1, 4, 3, 5] splits into cycles of sizes 2, 2, and 1, all contributing zero, confirming that the algorithm does not incorrectly mix components.
