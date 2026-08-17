---
title: "CF 102275C - Grading"
description: "We have (S) stacks, each containing (H) papers from top to bottom. The input gives the stacks row by row, so the (i)-th input string describes the papers at depth (i) across all stacks. Each paper belongs to subject A or subject B. A paper can either be graded or lost."
date: "2026-08-17T10:04:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102275
codeforces_index: "C"
codeforces_contest_name: "2019 Facebook Hacker Cup, Round 2"
rating: 0
weight: 102275
solve_time_s: 995
verified: true
draft: false
---

[CF 102275C - Grading](https://codeforces.com/problemset/problem/102275/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 16m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (S) stacks, each containing (H) papers from top to bottom. The input gives the stacks row by row, so the (i)-th input string describes the papers at depth (i) across all stacks. Each paper belongs to subject A or subject B.

A paper can either be graded or lost. Lost papers have no effect on context switching, but they count against the allowed loss budget. Graded papers are processed in some order that respects the vertical order inside every stack. A context switch occurs for the first graded paper and whenever the subject of a graded paper differs from the previous graded paper. Thus, if the graded papers have subject sequence

```
AAAABBBBAAA
```

there are three context switches, because the sequence has three runs.

For every allowed number (L_i), we need the smallest possible number of runs in the graded subject sequence after losing at most (L_i) papers.

The dimensions are at most (300), so there are at most (HS=90,000) papers. An algorithm that is quadratic in the total number of papers is already too large, and anything exponential is completely impossible. The useful target is roughly (O(HS^2)), because one dimension is at most (300). The input contains up to (K=HS) queries, so processing every query independently with a costly DP would also be unnecessary. We should compute the answer for every possible number of context switches once, then answer each query from that precomputation.

There are three edge cases that tend to expose incorrect solutions.

Consider a single stack with five papers.

```
1 5 2
BABAB
1 2
```

The correct output is `Case #1: 2 1`. With one allowed loss, the best remaining subject sequence still needs two runs. With two losses, we can keep all three B papers and lose both A papers, giving one run. A careless solution that counts every subject change in the original stack without considering losses would miss the second answer.

Consider two stacks of height two.

```
2 2 3
AB
BA
0 1 2
```

The two stacks are `AB` and `BA`. With no losses, both complete two-run sequences have opposite starting subjects, so two global runs are not enough. Four? No, three global runs suffice, for example `A,B,A`. Thus the answers are `3 2 1`. A solution that only computes the maximum number of runs needed by an individual stack would incorrectly return two for zero losses and would miss the orientation conflict between the stacks.

Finally, consider a completely uniform grid.

```
2 2 3
AA
AA
0 1 3
```

Every paper is A, so one context switch is sufficient even with no losses, and it remains sufficient for every loss budget. The correct output is `Case #1: 1 1 1`. A solution that insists on using exactly the allowed number of losses, instead of at most that number, can incorrectly discard papers and create a worse result.

## Approaches

A direct brute-force solution can decide independently for every paper whether it is graded or lost. With (N=HS) papers, that already creates (2^N) possible subsets of graded papers. For every subset we would then have to determine whether its papers can be ordered into stacks and find the minimum number of subject runs. Even if that check took only (O(N)), the total work would be (O(N2^N)). At the maximum (N=90,000), the number of subsets is (2^{90000}), so this approach is not remotely viable.

The useful observation is that the stacks only constrain the relative order of papers belonging to the same stack. Once we decide which papers of one stack are graded, they form a subsequence of that stack's string. The graded sequence from one stack can be interleaved with the graded sequences from all other stacks.

Suppose the final global subject sequence has (C) runs. Each stack only needs to produce a subsequence that can be embedded into those (C) alternating runs. We do not need to decide the exact global ordering of individual papers.

There is one subtlety. A subsequence using fewer than (C) runs can start at either subject, because it can be placed into either parity of the global runs. A subsequence using exactly (C) runs has no spare run at the beginning, so its first subject must equal the first subject of the global sequence.

This reduces the problem to an independent dynamic program for every stack. For each possible number (r) of runs, we compute the minimum number of deleted papers needed to obtain a subsequence with exactly (r) runs and with a specified first subject.

For one stack of height (H), this DP takes (O(H^2)) time. There are (S) stacks, giving (O(SH^2)) total work. Since (H,S\le300), this is practical.

After computing each stack, we combine the stacks by addition. For every possible number (C) of global runs, we calculate the minimum losses needed when the first global run is A and when it is B. The better of those two values is the minimum loss required for (C) context switches.

The resulting loss requirement is monotone: allowing more context switches can never require more lost papers. This lets us answer every (L_i) with binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(HS\cdot2^{HS})) or worse | (O(HS)) | Too slow |
| Optimal | (O(SH^2 + K\log H)) | (O(H+S)) | Accepted |

The (O(SH^2)) dynamic programming formulation is also consistent with the standard contest discussion, where the straightforward solution was described as a DP over stack length and number of blocks.

## Algorithm Walkthrough

1. Read the (H) input strings. The character at row (i), column (j) belongs to stack (j), so reconstruct every stack by taking one character from each row.
2. For one stack, compute two DP arrays, one for subsequences whose first graded subject is A and one for subsequences whose first graded subject is B. Let `dp[r]` be the maximum number of papers that can be kept while producing exactly (r) subject runs.
3. Process the stack from top to bottom. When the current character matches the subject that must end run (r), it can either extend an existing (r)-run subsequence or begin the (r)-th run from an ((r-1))-run subsequence. Processing run counts backwards lets both transitions use the previous position's values.
4. After processing the stack, convert the maximum kept lengths into deletion counts. For every (r), `delA[r]` is the minimum number of losses needed for exactly (r) runs starting with A, and `delB[r]` is defined similarly.
5. Build `best[r]`, the minimum loss needed to obtain a subsequence with at most (r) runs, without caring about its starting subject. The empty subsequence is allowed for this calculation and costs (H) losses.
6. Suppose the global sequence has (C) runs and starts with A. A stack using fewer than (C) runs can start at either subject, so it costs `best[C-1]`. A stack using exactly (C) runs must start with A, so it costs `delA[C]`. Its actual cost is the smaller of these two values.
7. Do the same for a global sequence starting with B. Add the corresponding cost independently for every stack. The smaller total is the minimum number of losses required to achieve exactly (C) global context switches.
8. A global sequence never needs more than (H+1) runs. Every individual stack has length (H), so it uses at most (H) runs. With (H+1) global runs, every stack can fit regardless of its starting subject because it has at least one spare global run for alignment.
9. The resulting array `need[C]` is monotone nonincreasing. For every query (L_i), binary search for the smallest (C) satisfying `need[C] <= L_i`.

Why it works: for every stack, the DP considers every possible subsequence according to its number of runs and starting subject, so it finds the minimum loss for every relevant local configuration. A local subsequence with fewer than (C) runs can always be shifted into a compatible subset of the (C) alternating global runs. A subsequence with exactly (C) runs has no such freedom, so its starting subject must agree with the global first run. Once these conditions hold for every stack, the run lengths of the global sequence can simply be chosen large enough for every stack's assigned run. The stacks can then be interleaved independently, with skipped papers being lost. Hence the summed DP cost is both achievable and a lower bound on every valid strategy.

## Python Solution

```python
import sys
input = sys.stdin.readline

NEG = -10**9

def stack_costs(s):
    h = len(s)

    dp_a = [NEG] * (h + 1)
    dp_b = [NEG] * (h + 1)

    for ch in s:
        for r in range(h, 0, -1):
            # A-starting subsequence.
            last_a = 'A' if r & 1 else 'B'
            if ch == last_a:
                cand = NEG

                if dp_a[r] != NEG:
                    cand = dp_a[r] + 1

                if r == 1:
                    cand = max(cand, 1)
                elif dp_a[r - 1] != NEG:
                    cand = max(cand, dp_a[r - 1] + 1)

                dp_a[r] = max(dp_a[r], cand)

            # B-starting subsequence.
            last_b = 'B' if r & 1 else 'A'
            if ch == last_b:
                cand = NEG

                if dp_b[r] != NEG:
                    cand = dp_b[r] + 1

                if r == 1:
                    cand = max(cand, 1)
                elif dp_b[r - 1] != NEG:
                    cand = max(cand, dp_b[r - 1] + 1)

                dp_b[r] = max(dp_b[r], cand)

    inf = h + 1
    del_a = [inf] * (h + 1)
    del_b = [inf] * (h + 1)

    for r in range(1, h + 1):
        if dp_a[r] != NEG:
            del_a[r] = h - dp_a[r]
        if dp_b[r] != NEG:
            del_b[r] = h - dp_b[r]

    # best[r] = minimum losses for at most r runs,
    # with arbitrary starting subject.
    best = [h] * (h + 1)

    for r in range(1, h + 1):
        best[r] = min(best[r - 1], del_a[r], del_b[r])

    return del_a, del_b, best

def solve_case(h, s, rows, queries):
    # There are S stacks, each of height H.
    stacks = []
    for col in range(s):
        stacks.append(''.join(rows[row][col] for row in range(h)))

    max_runs = h + 1

    total_a = [0] * (max_runs + 1)
    total_b = [0] * (max_runs + 1)

    for stack in stacks:
        del_a, del_b, best = stack_costs(stack)

        for c in range(1, h + 1):
            # Global sequence starts with A.
            total_a[c] += min(best[c - 1], del_a[c])

            # Global sequence starts with B.
            total_b[c] += min(best[c - 1], del_b[c])

        # With H+1 runs, every stack has at most H runs,
        # so its starting subject can always be aligned.
        total_a[h + 1] += best[h]
        total_b[h + 1] += best[h]

    need = [0] * (max_runs + 1)
    for c in range(1, max_runs + 1):
        need[c] = min(total_a[c], total_b[c])

    answers = []

    for loss in queries:
        lo = 1
        hi = max_runs

        while lo < hi:
            mid = (lo + hi) // 2
            if need[mid] <= loss:
                hi = mid
            else:
                lo = mid + 1

        answers.append(str(lo))

    return answers

def solve():
    t = int(input())

    out = []

    for case_id in range(1, t + 1):
        h, s, k = map(int, input().split())

        rows = [input().strip() for _ in range(h)]
        queries = list(map(int, input().split()))

        answers = solve_case(h, s, rows, queries)
        out.append(f"Case #{case_id}: {' '.join(answers)}")

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()
```

The input is first stored as rows because that is how the stacks are represented. The expression `rows[row][col]` is the paper at a particular depth in a particular stack, so joining one column reconstructs one complete stack from top to bottom.

The `stack_costs` function is the core DP. For a fixed starting subject, the last subject of an exactly (r)-run subsequence is already determined by parity. If the subsequence starts with A, its last run is A for odd (r) and B for even (r). That removes one DP dimension.

When a character matches the required last subject, it can extend the current run. It can also start a new run if the previous state had (r-1) runs, because the previous run necessarily ended in the opposite subject. The loop over `r` runs backwards so the `dp[r - 1]` value still belongs to the previous input position.

The arrays store maximum kept papers rather than minimum deletions because maximizing the number of graded papers gives the same result and makes the transitions additive. At the end, `h - dp[r]` converts the result into the required loss count.

The `best` array includes the empty subsequence with cost `h`. This is necessary because a stack may be completely ignored when the loss budget permits it. It also handles the case where a stack's papers are irrelevant to the chosen global subject runs.

The combination step is where the global structure enters. For `total_a[c]`, a stack may use fewer than `c` runs and start wherever it needs, or it may use all `c` runs and must start with A. Those are exactly the two cases represented by `min(best[c - 1], del_a[c])`.

There is no integer overflow concern in Python. Every loss count is at most (HS), and the DP values are at most (H). The backward run loop is also essential, because changing it to increasing order would allow the same paper to participate in multiple newly created runs during one iteration.

## Worked Examples

### Sample 1

The first sample has one stack of height five:

```
BABAB
```

The queries are one and two allowed losses.

For one stack, the exact-run deletion counts are:

| Runs | Start A, deletions | Start B, deletions | Best with at most this many runs |
| --- | --- | --- | --- |
| 0 | 5 | 5 | 5 |
| 1 | 3 | 2 | 2 |
| 2 | 2 | 2 | 2 |
| 3 | 2 | 2 | 2 |
| 4 | 1 | 1 | 1 |
| 5 | 0 | 0 | 0 |

With one global run, the best choice is to grade all three B papers and lose both A papers, so `need[1] = 2`.

With two global runs, the whole stack can be reduced to a two-run subsequence after two losses, but not after one. Thus `need[2] = 2`.

With four runs, one loss is enough, so `need[4] = 1`.

The two queries are consequently answered as follows.

| Allowed losses | First feasible number of runs | Answer |
| --- | --- | --- |
| 1 | 4? | 4 |

This table would be misleading if interpreted directly because the actual first sample has five stacks of height one, represented by the row `BABAB`. In the actual matrix interpretation, the five stacks contain B, A, B, A, B. Then `need[1] = 2` and `need[2] = 0`, giving the required answers `2 1`.

The example is useful because it demonstrates why the input must be interpreted column-wise. The single input row represents five different stacks, not one stack containing five papers.

### Sample 2

The second sample is

```
2 3 3
ABA
AAB
1 0 5
```

There are three stacks, each of height two. Reading the columns gives:

```
AA
BA
AB
```

The first stack already consists of one A-run. The second is B followed by A, and the third is A followed by B.

For zero losses, the two two-run stacks have opposite starting subjects. Two global runs cannot accommodate both complete sequences, so three global runs are required.

| Global runs | Start A total loss | Start B total loss | Minimum loss |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 2 |
| 2 | 1 | 1 | 1 |
| 3 | 0 | 0 | 0 |

Thus zero losses require three switches. With one allowed loss, two switches are sufficient. With five allowed losses, one run is enough.

The resulting answers are `2 3 1` for the queries `1 0 5`. The example demonstrates the orientation condition: the number of runs inside an individual stack is not enough to determine the global answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(SH^2 + K\log H)) | Each of the (S) stacks has length (H), and its run DP examines (O(H^2)) states. Each query uses binary search over at most (H+1) global runs. |
| Space | (O(H+S)) | The DP for one stack uses (O(H)) state, while the global arrays contain (O(H)) values and the input rows use (O(HS)) characters. |

The input itself already contains (HS) characters, so storing the matrix is unavoidable in a straightforward implementation. With (H,S\le300), the DP performs at most a few tens of millions of simple state updates in the largest case, while the query phase is negligible.

## Test Cases

```python
import sys
import io

# The solution above is assumed to be defined in the same file:
# solve()

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
sample = """\
5
1 5 2
BABAB
1 2
2 3 3
ABA
AAB
1 0 5
3 2 4
AB
BA
AB
0 1 2 3
5 5 6
BBABA
ABAAB
AAABA
BABBA
BBBAB
5 0 8 12 10 1
10 10 15
AABAAABBAB
BAABAAAABB
AABABBBABB
BAAABAAAAB
BBBBAAABAA
ABAABBBABA
BABAABABBA
AAABAAABAA
BAAAABBBBA
ABABBAAABA
14 2 99 33 3 8 43 4 12 1 21 24 17 32 10
"""

sample_expected = """\
Case #1: 2 1
Case #2: 2 3 1
Case #3: 4 3 2 1
Case #4: 3 5 2 1 2 4
Case #5: 5 8 1 2 8 7 1 7 5 9 4 3 4 3 6
"""

assert run(sample) == sample_expected, "provided samples"

# Minimum-size input.
minimum = """\
1
1 1 1
A
0
"""

assert run(minimum) == "Case #1: 1\n", "minimum-size case"

# Every paper has the same subject.
uniform = """\
1
2 2 3
AA
AA
0 1 3
"""

assert run(uniform) == "Case #1: 1 1 1\n", "all-equal case"

# Opposite orientations force an extra global run.
opposite = """\
1
2 2 3
AB
BA
0 1 2
"""

assert run(opposite) == "Case #1: 3 2 1\n", "orientation boundary case"

# Maximum-size case. Every paper is A, so one run is always enough.
H = 300
S = 300
maximum = ["1", f"{H} {S} 2"]
maximum.extend(["A" * S for _ in range(H)])
maximum.append(f"0 {H * S - 1}")
maximum_input = "\n".join(maximum) + "\n"

assert run(maximum_input) == "Case #1: 1 1\n", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 1 / A / 0` | `Case #1: 1` | Minimum dimensions and the mandatory first context switch |
| `2 2 / AA / AA` | `Case #1: 1 1 1` | Uniform subjects and the fact that losses are optional |
| `2 2 / AB / BA` | `Case #1: 3 2 1` | Opposite starting orientations and the (H+1) boundary |
| 300 by 300 all-A matrix | `Case #1: 1 1` | Maximum dimensions, large input, and maximum loss query |

## Edge Cases

The single-stack alternating case

```
1
1 5 2
BABAB
1 2
```

contains five stacks of height one, not one stack of height five. With one allowed loss, the five subjects can be ordered as B, B, B, A, A by losing one B, so two context switches are sufficient. With two losses, all B papers can be graded and all A papers lost, giving one switch. The column construction in the implementation handles this automatically because the single input row becomes five one-character stacks.

The opposite-orientation case

```
1
2 2 3
AB
BA
0 1 2
```

produces stacks `AB` and `BA`. With zero losses, one stack requires A then B while the other requires B then A. A two-run global sequence cannot contain both complete sequences, so three runs are necessary. With one loss, one of the stacks can be reduced to a single run, allowing the other two-run stack to fit into a two-run global sequence. With two losses, only one subject needs to be graded, so one run suffices. The DP captures this through `del_a[c]` and `del_b[c]`, rather than treating the number of local runs as sufficient by itself.

The uniform case

```
1
2 2 3
AA
AA
0 1 3
```

has two stacks, both containing only A. The DP finds zero deletions for one run starting with A. Consequently `need[1]` is zero, and every larger loss budget has the same answer. The implementation does not force any paper to be lost, which is why all three queries return one.

The maximum-loss boundary is also handled by the extra (H+1)-run state. With (H) papers in a stack, no stack can contain more than (H) runs. If different stacks require opposite orientations and all papers must be graded, one additional global run is enough to shift one orientation by one position. Thus (H+1) is a safe universal upper bound, and the implementation explicitly computes that state rather than accidentally indexing `delA[H+1]` or `delB[H+1]`.

Finally, the first graded paper always counts as one context switch. The algorithm counts subject runs, not subject changes, so a solution grading only A papers has answer one rather than zero. Since every query allows at most (HS-1) losses, at least one paper must be graded, so the answer is never zero.
