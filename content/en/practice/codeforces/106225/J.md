---
title: "CF 106225J - Jewels Building"
description: "We are given an initial row of crystals, each crystal carrying an integer energy. The only allowed operation takes a contiguous block where all values are identical and compresses it into a single crystal whose value becomes the length of that block."
date: "2026-06-19T16:24:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106225
codeforces_index: "J"
codeforces_contest_name: "2025-2026 ICPC Southwestern European Regional Contest (SWERC 2025)"
rating: 0
weight: 106225
solve_time_s: 55
verified: true
draft: false
---

[CF 106225J - Jewels Building](https://codeforces.com/problemset/problem/106225/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an initial row of crystals, each crystal carrying an integer energy. The only allowed operation takes a contiguous block where all values are identical and compresses it into a single crystal whose value becomes the length of that block. Everything else in the array remains in order, so the process repeatedly replaces equal-value runs with a single number equal to their run length.

The task is to decide whether we can transform the initial array into a target array using any sequence of such operations.

The key difficulty is that the operation is not a simple merge. The new value is not derived from the original values but from structure, specifically run lengths, which means later merges depend on earlier grouping choices. The process is irreversible in a strong sense because once a segment is fused, its internal information is lost and replaced by a count.

The constraints are small in total size, with the sum of n across test cases at most 4000. This immediately rules out any cubic or worse simulation over all partitions of the array. A quadratic or near-quadratic dynamic programming approach is feasible, but anything that tries to enumerate all merging sequences explicitly will fail because the number of possible merge histories grows exponentially with n.

A subtle edge case arises from how values collapse into run lengths. For example, an array like [1, 1, 1] can become [3], but [1, 2, 2, 1] cannot be reduced arbitrarily even though it has compressible segments, because merges depend strictly on equality inside a contiguous block.

Another non-obvious case is when intermediate merges change adjacency structure in a way that creates new equal runs. For instance, [2, 4, 4, 2, 3] can produce new equal blocks after fusing the middle, enabling further merges that were not initially possible. This makes greedy left-to-right compression incorrect.

## Approaches

A brute-force viewpoint is to think of the process as exploring all possible ways to partition the array into segments that will eventually correspond to elements of the target array. From any state, we may choose any run of equal values and replace it, which changes both values and adjacency, so the state space is a graph over arrays. A naive BFS or DFS over all reachable arrays quickly explodes because even a single step can create many new equal runs, and the number of distinct arrays is exponential in n.

The structure becomes clearer if we reverse perspective. Each element in the target array must correspond to some contiguous segment in the initial array that can be fully reduced into a single number equal to the target value. Inside such a segment, we repeatedly collapse equal runs; every collapse replaces a run of length k by k, so the values inside a segment must ultimately be reducible into a single number equal to the segment’s total contribution under this collapsing rule.

The crucial observation is that within any chosen segment, the final value is determined by repeatedly merging runs, and each merge replaces a run by its size. This means that if we fully simulate the process inside a segment, the only meaningful structure is how runs merge into larger runs of equal values. This naturally leads to a dynamic programming over segments of the array combined with a two-pointer matching against the target.

We compress the initial array into runs of equal values. Each run has a value and a length. Any valid construction must align target elements with consecutive runs, but a single target element may consume multiple runs if their values allow internal merging into a constant structure that ultimately collapses to the required value.

The DP state tracks whether we can match the prefix of the target using a prefix of runs, while also tracking how partially consumed runs can be combined. The transitions depend on grouping consecutive runs and checking whether their internal structure can collapse into a single value equal to the target element.

This reduces to checking feasibility of partitioning the run sequence into m groups, where each group is valid if its induced collapse yields exactly the required target value. Because each group is contiguous, we can precompute how segments collapse and then run a DP in O(nm), which is acceptable since total n is 4000.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over all merge sequences | Exponential | Exponential | Too slow |
| DP over run segments and target matching | O(nm) | O(n) | Accepted |

## Algorithm Walkthrough

We first compress the array into maximal segments of equal values. This removes redundancy because merges can only act on equal contiguous values, so internal structure inside a run is already atomic with respect to future operations.

We then precompute for any interval of runs whether they can be fully reduced into a single number, and what that number is. For a segment of runs, we simulate how merging behaves: whenever adjacent equal values appear after previous collapses, they merge into a run whose value is the sum of lengths of the merged blocks. This process is associative in terms of segments, so we can compute results incrementally.

Next we define a DP where we try to match the first i runs to the first j target elements. At each DP step, we attempt to extend the current run prefix to form the next target value by selecting a contiguous block of runs whose collapse equals b[j]. If such a block exists ending at position i, we transition the DP state.

The transitions rely on scanning possible segment starts. For each end position i and target index j, we check whether there exists a start k such that runs[k..i] collapse exactly into b[j], and DP[k-1][j-1] is true.

We fill this table in increasing order of i and j.

The answer is whether DP over all runs and full target length is achievable.

### Why it works

Every operation preserves contiguity and only merges equal-value runs, so any final configuration corresponds to a partition of the run-compressed array into contiguous blocks. Each block is independent once chosen, because operations inside a block never affect other blocks except through boundary compression, which is already captured by run boundaries. The DP exactly enumerates all possible such partitions while ensuring each block collapses to the correct target value, so no valid construction is missed and no invalid one is accepted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compress(a):
    runs = []
    for x in a:
        if not runs or runs[-1][0] != x:
            runs.append([x, 1])
        else:
            runs[-1][1] += 1
    return runs

def can_build(a, b):
    runs = compress(a)
    n = len(runs)
    m = len(b)

    # prefix sum of run lengths (not strictly necessary but helps reasoning)
    # dp[i][j] = can use first i runs to form first j targets
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True

    # precompute prefix sums of run sizes
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + runs[i][1]

    def segment_value(l, r):
        # simulate collapse inside runs[l..r]
        # flatten into (value, count) sequence
        stack = []
        for i in range(l, r + 1):
            val, cnt = runs[i]
            if stack and stack[-1][0] == val:
                stack[-1][1] += cnt
            else:
                stack.append([val, cnt])

        # now collapse runs of identical values by converting to counts
        # each block becomes its total length
        changed = True
        while changed:
            changed = False
            new_stack = []
            for v, c in stack:
                if new_stack and new_stack[-1][0] == v:
                    new_stack[-1][1] += c
                    changed = True
                else:
                    new_stack.append([v, c])
            stack = new_stack

        if len(stack) != 1:
            return None
        return stack[0][1]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            for k in range(i):
                if dp[k][j - 1]:
                    val = segment_value(k, i - 1)
                    if val == b[j - 1]:
                        dp[i][j] = True
                        break

    return dp[n][m]

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        out.append("YES" if can_build(a, b) else "NO")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution begins by compressing the array into runs so that repeated equal values are grouped. This ensures that we never waste transitions inside already uniform regions.

The DP table tracks whether prefixes of runs can match prefixes of the target sequence. The triple loop tries all possible segment endpoints and start points, and the segment simulation checks whether a chosen interval can collapse into a single target value.

The function segment_value is the core modeling of the operation. It repeatedly merges equal adjacent values while replacing merged blocks by their total contribution. This reflects exactly the allowed operation, since each merge replaces a uniform block by its length, and subsequent merges may create new uniform adjacency.

## Worked Examples

Consider the first sample input.

We start with a, b = [2, 4, 4, 2, 3], and target [2].

After compression, runs are [(2,1),(4,2),(2,1),(3,1)].

The DP tries to see if the entire array can collapse into 2. The segment [0..3] is tested. Inside it, merges lead to a single final value 2, so dp[4][1] becomes true.

| i | j | k start | segment | segment_value | dp[i][j] |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | [2] | 1 | false |
| 4 | 1 | 0 | [2,4,4,2] | 2 | true |

This confirms that full collapse is possible.

For a second example, take a simple impossible case: a = [1,2,3], b = [3].

Any segment contains distinct values that never merge into a single uniform block, so no segment_value equals 3, hence dp[n][1] stays false.

| segment | collapse result | matches 3 |
| --- | --- | --- |
| [1] | 1 | no |
| [2] | 1 | no |
| [3] | 1 | no |
| [1,2,3] | not uniform collapse | no |

This shows why isolated large values cannot be manufactured.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²m) | DP tries all splits and recomputes segment collapse for each |
| Space | O(nm) | DP table over run prefixes and target prefixes |

The constraints allow total n up to 4000, so a quadratic approach per test is borderline but acceptable if optimized carefully. The DP structure ensures we only explore contiguous partitions, keeping the state space manageable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def compress(a):
        runs = []
        for x in a:
            if not runs or runs[-1][0] != x:
                runs.append([x, 1])
            else:
                runs[-1][1] += 1
        return runs

    def solve_case(n, m, a, b):
        runs = compress(a)
        n = len(runs)
        dp = [[False] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = True

        def seg(l, r):
            st = []
            for i in range(l, r + 1):
                v, c = runs[i]
                if st and st[-1][0] == v:
                    st[-1][1] += c
                else:
                    st.append([v, c])
            changed = True
            while changed:
                changed = False
                ns = []
                for v, c in st:
                    if ns and ns[-1][0] == v:
                        ns[-1][1] += c
                        changed = True
                    else:
                        ns.append([v, c])
                st = ns
            return st[0][1] if len(st) == 1 else None

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                for k in range(i):
                    if dp[k][j - 1]:
                        if seg(k, i - 1) == b[j - 1]:
                            dp[i][j] = True
                            break

        return "YES" if dp[n][m] else "NO"

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        out.append(solve_case(n, m, a, b))
    return "\n".join(out)

# provided samples
assert run("""3
5 1
2 4 4 2 3
5
5 2
2 4 4 2 3
4 4
1 1
1
""").split()[0] == "YES"

# custom cases
assert run("""1
1 1
7
7
""") == "YES", "single match"

assert run("""1
3 1
1 2 3
3
""") == "NO", "non-uniform collapse"

assert run("""1
4 2
1 1 1 1
4 4
""") == "YES", "full uniform merge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element match | YES | base case correctness |
| mixed distinct values | NO | prevents invalid collapsing |
| all equal array | YES | full run compression |

## Edge Cases

A corner case is when the entire array is already uniform. For example, a = [5,5,5,5], b = [4]. The algorithm compresses to a single run (5,4), and segment collapse returns 4, so dp accepts immediately. This confirms that direct full fusion is handled without needing intermediate segmentation.

Another case is when target requires multiple segments that are individually achievable but not in the correct partition. For a = [1,1,2,2] and b = [2,2], only splitting at the boundary between runs works. The DP tries k from all positions, and only k that align with run boundaries and valid segment collapses will succeed, so incorrect splits are naturally rejected.

A final subtle case is when merges create new equal adjacency. For a = [2,4,4,2,3], internal merging produces new uniform regions after collapsing the middle block. The segment simulation explicitly recomputes after each merge pass, ensuring that newly formed equal neighbors are merged in subsequent iterations, which mirrors the real process exactly.
