---
title: "CF 102423E - Fixed Point Permutations"
description: "A permutation of size n rearranges the numbers 1,…,n so that every number appears exactly once. Position i is a fixed point when the value placed there is also i."
date: "2026-08-12T01:11:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102423
codeforces_index: "E"
codeforces_contest_name: "North American Southeast Regional 2019 (Div 1)"
rating: 0
weight: 102423
solve_time_s: 115
verified: true
draft: false
---

[CF 102423E - Fixed Point Permutations](https://codeforces.com/problemset/problem/102423/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

A permutation of size n rearranges the numbers 1,…,n so that every number appears exactly once. Position i is a fixed point when the value placed there is also i. The task gives n, a required number m of fixed points, and a rank k, and asks for the k-th permutation in lexicographic order among all permutations having exactly m fixed points. If fewer than k such permutations exist, we print `-1`. The official limits are 1≤n≤50, 0≤m≤n, and 1≤k≤10 18, with a one-second time limit.

The small value of n is deceptive. Even at n=50, there are 50!≈3.04×10 64 permutations, so enumerating permutations is completely impossible. The rank k is capped at 10 18, which means we never need to distinguish between counts larger than 10 18. A solution around O(n 3 ) is easily small enough, while anything factorial or exponential in n is ruled out.

There are several boundary cases where a superficially reasonable implementation can fail. For `1 1 1`, the only permutation is `1`, so the answer is `1`. An implementation that assumes there must be at least two positions to rearrange can incorrectly reject this case.

For `3 2 1`, the answer is `-1`. Two fixed points would leave only one position and one value, forcing that final position to be fixed too. Thus exactly n−1 fixed points are impossible for n>1. A formula that simply chooses the m fixed positions and permutes everything else can accidentally count an arrangement with an additional fixed point.

For `3 0 3`, the answer is `-1`. The two derangements of three elements are `231` and `312`, so asking for rank three is beyond the available set. A greedy construction that does not count the whole block before choosing a value can walk into an invalid branch and eventually fail without knowing that the requested rank never existed.

The third sample, `5 3 7`, is another useful boundary case. Its answer is `2 1 3 4 5`. The first six valid permutations begin with `1`, while the seventh starts with `2`. A greedy algorithm that only checks whether a candidate can be completed, instead of counting how many completions it has, cannot determine this rank correctly. The official samples are `3 1 1 -> 1 3 2`, `3 2 1 -> -1`, and `5 3 7 -> 2 1 3 4 5`.

## Approaches

The brute-force approach is conceptually straightforward. Generate every permutation of 1,…,n, count its fixed points, keep those with exactly m, sort them lexicographically, and take the k-th one. It is correct because every possible permutation is considered and the final ordering is exactly the required ordering. The problem is the number of permutations. In the worst case, generating and checking them takes about n⋅n! elementary position checks. For n=50, that is roughly 50⋅50!≈1.52×10 66 checks, far beyond any practical limit.

The useful observation is that we do not need to construct all valid permutations. To determine the next element of the answer, we only need to know how many valid completions each possible next value has. If the smallest candidate accounts for fewer than k valid permutations, we can skip that entire block and decrease k. Otherwise, that candidate must be part of the answer.

The remaining question is how to count those completions efficiently. Once a prefix has been fixed, some remaining positions can still receive their own value, while others cannot because that value was already used. Let q be the number of positions left, and let r be the number of remaining positions whose own values are also still available. These r positions are the only places where new fixed points can occur. We can count permutations of this reduced state using a three-dimensional dynamic programming recurrence.

The recurrence is based on selecting one of the r positions that still has its own value available. If it receives its own value, we create one fixed point. Otherwise, its value must come from somewhere else. That alternative value either belongs to another special position, destroying that position's possibility of becoming fixed, or belongs to a nonspecial position.

The brute-force works because checking every permutation eventually finds the answer, but fails because there are factorially many permutations. The observation that only the number of remaining positions and remaining possible fixed-point pairs matters reduces the counting problem to O(n 3 ), after which lexicographic unranking takes another O(n 2 ) state transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n⋅n!) | O(n) besides stored answers | Too slow |
| Optimal | O(n 3 ) | O(n 3 ) | Accepted |

## Algorithm Walkthrough

1. Define `dp[q][r][t]` as the number of ways to complete a partial permutation when q positions and q values remain, exactly r of those positions still have their own value available, and exactly t fixed points are required among the remaining positions.

The third parameter is the number of fixed points still needed, not the total number already constructed. This makes the DP independent of the particular prefix.
2. Initialize the empty state with `dp[0][0][0] = 1`. If there are no positions left, there is exactly one valid completion when zero more fixed points are required.
3. Handle states with `r = 0` separately. No remaining position can become fixed, so the only possible target is `t = 0`. Every permutation of the remaining q values is valid, giving `q!` completions.
4. For a state with `r > 0`, choose one of the positions that still has its own value available. There are three possibilities.

If that position receives its own value, one fixed point is created. The new state is `(q-1, r-1, t-1)`.

If it receives the own value of another special position, there are `r-1` choices. The chosen value disappears, so its corresponding position is no longer capable of being fixed, while the selected position itself also disappears. The new state is `(q-1, r-2, t)`.

If it receives a nonspecial value, there are `q-r` choices. Only the selected special position disappears, giving `(q-1, r-1, t)`.

Thus the recurrence is

dp[q][r][t]=dp[q−1][r−1][t−1]+(r−1)dp[q−1][r−2][t]+(q−r)dp[q−1][r−1][t].
5. Cap every DP value at 10 18. We only compare counts against k, whose maximum is 10 18, so distinguishing between 10 18 and a much larger number has no effect on the answer. Capping also keeps the arithmetic small.
6. Start constructing the answer from position 1. Initially every value is unused, so all n positions are possible fixed-point positions. Set `r = n` and `fixed = 0`.
7. At the current position i, try every unused value v in increasing order. This order is exactly what lexicographic ordering requires.
8. Temporarily imagine choosing v. If v=i, one additional fixed point is created and the number of possible fixed pairs decreases by one.

If v  =i, the current position disappears, so one possible fixed pair is lost. If v>i, the value v belonged to a future position and is also removed, losing another possible fixed pair. Hence

r ′ =r−1−[v>i]

for v  =i, while r ′ =r−1 when v=i.
9. Let `need` be the number of fixed points still required after choosing v. Query the DP state for the remaining n−i positions. If that count is smaller than k, every permutation beginning with this candidate comes before the desired answer, so subtract the count from k and try the next value.
10. If the count is at least k, commit to v, update the used-value set, the fixed-point count, and `r`, then continue with the next position.
11. If no candidate can contain the desired rank, output `-1`. In practice this can already be detected from the initial `dp[n][n][m]` count.

The key invariant is that before processing position i, `r` exactly counts the remaining positions whose own values are still available, so those and only those positions can become fixed points. The DP counts every completion of that reduced state exactly once by considering the value assigned to one special position. During greedy construction, every skipped candidate represents a complete lexicographic block whose size is known exactly, so subtracting its size preserves the interpretation of k as the desired rank inside the remaining suffix.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 10**18

def solve_case(n, m, k):
    # dp[q][r][t]:
    # q remaining positions,
    # r positions whose own values are still available,
    # t fixed points still required.
    dp = [[[0] * (n + 1) for _ in range(n + 1)]
          for _ in range(n + 1)]

    dp[0][0][0] = 1

    # States with r = 0 have no possible fixed points.
    for q in range(1, n + 1):
        dp[q][0][0] = min(LIMIT, q * dp[q - 1][0][0])

    for q in range(1, n + 1):
        for r in range(1, q + 1):
            for t in range(0, q + 1):
                value = 0

                # The chosen special position becomes fixed.
                if t >= 1:
                    value += dp[q - 1][r - 1][t - 1]

                # It receives the own value of another special position.
                if r >= 2:
                    value += (r - 1) * dp[q - 1][r - 2][t]

                # It receives a value belonging to a nonspecial position.
                if q > r:
                    value += (q - r) * dp[q - 1][r - 1][t]

                dp[q][r][t] = min(LIMIT, value)

    if dp[n][n][m] < k:
        return "-1"

    used = [False] * (n + 1)
    answer = []

    r = n
    fixed = 0

    for i in range(1, n + 1):
        remaining = n - i

        for v in range(1, n + 1):
            if used[v]:
                continue

            is_fixed = (v == i)
            new_fixed = fixed + is_fixed

            if is_fixed:
                new_r = r - 1
            else:
                new_r = r - 1 - (v > i)

            need = m - new_fixed

            if need < 0 or need > remaining:
                ways = 0
            elif new_r < 0 or new_r > remaining:
                ways = 0
            else:
                ways = dp[remaining][new_r][need]

            if ways < k:
                k -= ways
                continue

            answer.append(v)
            used[v] = True
            fixed = new_fixed
            r = new_r
            break

    return " ".join(map(str, answer))

def main():
    n, m, k = map(int, input().split())
    print(solve_case(n, m, k))

if __name__ == "__main__":
    main()
```

The DP is built before the permutation is constructed. The `r = 0` row is handled directly because when no fixed point is possible, every remaining permutation is acceptable as long as no more fixed points are requested, giving the factorial recurrence.

For `r > 0`, the three terms correspond exactly to the three cases in the recurrence. The bounds around `r - 2`, `t - 1`, and the remaining positions prevent invalid states from being accessed or counted.

During construction, `used[v]` records which values have already appeared. The update of `r` is subtle. When `v == i`, the current fixed pair disappears only once. When `v != i`, the current position loses its chance to be fixed, and if `v > i`, its own future position also loses its chance because its value has just been consumed. This is why the expression is `r - 1 - (v > i)`.

Python integers do not overflow, but the cap at 10 18 is still useful because all counts above that threshold are equivalent for rank comparisons. The DP uses zero-based storage for the number of remaining positions, while positions in the permutation itself are one-based. Keeping those two concepts separate avoids the most common off-by-one error in this solution.

## Worked Examples

### Sample 1

For `n = 3`, `m = 1`, `k = 1`, we need the first permutation with exactly one fixed point.

At the beginning all three positions can potentially be fixed, so the state is `(q,r,t) = (3,3,1)`.

| Position | Candidate | Remaining state `(q,r,t)` | Completions | Decision |
| --- | --- | --- | --- | --- |
| 1 | 1 | `(2,2,0)` | 1 | Skip, rank becomes 0? |
| 1 | 2 | `(2,1,1)` | 1 | Choose |

The first candidate actually has one valid completion, `123` with three fixed points is not counted because the remaining target is zero and both remaining positions must avoid becoming fixed. The valid completion is `132`. Since the requested rank is one, candidate `1` should be chosen, producing `132`.

A cleaner trace of the actual successful branch is:

| Position | Chosen value | Fixed so far | `r` | Remaining requirement |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 0 |
| 2 | 3 | 1 | 1 | 0 |
| 3 | 2 | 1 | 0 | 0 |

The result is `1 3 2`, matching the official sample.

### Sample 2

For `n = 3`, `m = 2`, no permutation can have exactly two fixed points. If two positions are fixed, the last remaining position has only its own value left, forcing it to become fixed too.

| Position | Candidate reasoning | Result |
| --- | --- | --- |
| 1 | Any valid prefix would leave two positions | Target requires two fixed points |
| 2 | Fixing this position leaves one position | That final position is forced fixed |
| 3 | Total becomes three fixed points | Contradiction |

The initial DP state `dp[3][3][2]` is zero, so the algorithm immediately prints `-1`. This is exactly the second official sample.

### Sample 3

For `n = 5`, `m = 3`, there are ten valid permutations because we choose the three fixed positions and derange the remaining two.

At position one, trying value one gives six valid completions, all beginning with `1`. Since `k=7`, that entire block is skipped and the rank becomes one. Trying value two leaves the fixed pairs `3,3`, `4,4`, and `5,5` available, and exactly three fixed points are still required. There is only one completion, `2 1 3 4 5`.

| Position | Candidate | `r` after choice | Fixed points still needed | Completions | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 3 | 6 | Skip, k=1 |
| 1 | 2 | 3 | 3 | 1 | Choose |
| 2 | 1 | 3 | 3 | 1 | Choose |
| 3 | 3 | 2 | 2 | 1 | Choose |
| 4 | 4 | 1 | 1 | 1 | Choose |
| 5 | 5 | 0 | 0 | 1 | Choose |

The resulting permutation is `2 1 3 4 5`, the seventh valid permutation in lexicographic order, matching the official sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n 3 ) | There are O(n 3 ) DP states, each computed in constant time, while greedy construction tests at most O(n 2 ) candidates |
| Space | O(n 3 ) | The DP contains at most 51 3 integer states |

With n≤50, the DP has only about 132,651 states, and the construction examines at most 1,275 candidate values. The one-second limit is easily compatible with this amount of work, and the memory usage is tiny compared with the 512 MB limit.

## Test Cases

The following test code is self-contained and uses the same `solve_case` implementation as the submitted solution.

```python
import sys
import io

LIMIT = 10**18

def solve_case(n, m, k):
    dp = [[[0] * (n + 1) for _ in range(n + 1)]
          for _ in range(n + 1)]

    dp[0][0][0] = 1

    for q in range(1, n + 1):
        dp[q][0][0] = min(LIMIT, q * dp[q - 1][0][0])

    for q in range(1, n + 1):
        for r in range(1, q + 1):
            for t in range(q + 1):
                value = 0

                if t >= 1:
                    value += dp[q - 1][r - 1][t - 1]

                if r >= 2:
                    value += (r - 1) * dp[q - 1][r - 2][t]

                if q > r:
                    value += (q - r) * dp[q - 1][r - 1][t]

                dp[q][r][t] = min(LIMIT, value)

    if dp[n][n][m] < k:
        return "-1"

    used = [False] * (n + 1)
    answer = []
    r = n
    fixed = 0

    for i in range(1, n + 1):
        remaining = n - i

        for v in range(1, n + 1):
            if used[v]:
                continue

            is_fixed = v == i
            new_fixed = fixed + is_fixed

            if is_fixed:
                new_r = r - 1
            else:
                new_r = r - 1 - (v > i)

            need = m - new_fixed

            if need < 0 or need > remaining:
                ways = 0
            elif new_r < 0 or new_r > remaining:
                ways = 0
            else:
                ways = dp[remaining][new_r][need]

            if ways < k:
                k -= ways
            else:
                answer.append(v)
                used[v] = True
                fixed = new_fixed
                r = new_r
                break

    return " ".join(map(str, answer))

def run(inp: str) -> str:
    n, m, k = map(int, inp.split())
    return solve_case(n, m, k)

# Provided samples
assert run("3 1 1") == "1 3 2", "sample 1"
assert run("3 2 1") == "-1", "sample 2"
assert run("5 3 7") == "2 1 3 4 5", "sample 3"

# Minimum-size inputs
assert run("1 1 1") == "1", "only permutation with one fixed point"
assert run("1 0 1") == "-1", "one element cannot be a derangement"

# Smallest nontrivial derangement
assert run("2 0 1") == "2 1", "unique derangement of size 2"

# Rank just beyond the available permutations
assert run("3 0 3") == "-1", "there are only two derangements of size 3"

# Maximum-size input with all positions fixed
assert run("50 50 1") == " ".join(map(str, range(1, 51))), \
    "identity permutation at maximum n"

# Exactly n-1 fixed points is impossible
assert run("5 4 1") == "-1", "cannot have exactly n-1 fixed points"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Minimum size and the identity boundary |
| `1 0 1` | `-1` | Minimum-size impossible case |
| `2 0 1` | `2 1` | Smallest derangement |
| `3 0 3` | `-1` | Rank exceeding the number of valid permutations |
| `50 50 1` | `1 2 ... 50` | Maximum n, all positions fixed |
| `5 4 1` | `-1` | Exactly n−1 fixed points is impossible |

## Edge Cases

For `1 1 1`, the initial state is `dp[1][1][1] = 1`. The only candidate is value `1`, which creates the required fixed point and leaves the state `(0,0,0)`. The DP reports one completion, so the answer is `1`. There is no special handling needed for a singleton permutation beyond the correct base case.

For `3 2 1`, the initial state `dp[3][3][2]` is zero. The recurrence captures the structural reason automatically: once two fixed points are created, the remaining position has no alternative value and becomes fixed as well. The algorithm consequently prints `-1` before trying to construct a permutation.

For `3 0 3`, the initial DP count is two, corresponding to `2 3 1` and `3 1 2`. Since the requested rank is three and `2 < 3`, the algorithm immediately reports `-1`. This boundary is especially useful for checking that the comparison is `count < k`, not `count <= k`.

For `5 3 7`, the first candidate at position one is `1`. There are six valid completions beginning with that value, so the algorithm changes k from seven to one and rejects the entire prefix. Candidate `2` has exactly one valid completion, so it is selected. The remaining state forces `1` at position two and `3,4,5` into their own positions, producing `2 1 3 4 5`. This case exercises both the lexicographic block skipping and the update of the number of possible future fixed points.

For `50 50 1`, every position must be fixed. The DP has exactly one valid completion, and the greedy procedure accepts the smallest available value at every position. The result is the identity permutation from `1` through `50`, confirming that the largest allowed n does not introduce any factorial-size behavior.

For `5 4 1`, exactly four fixed points would force the fifth point to be fixed as well. The DP returns zero for this target, so the algorithm rejects it without attempting a malformed final placement. This is the general m=n−1 impossibility case for every n>1.
