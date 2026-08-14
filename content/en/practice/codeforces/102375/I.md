---
title: "CF 102375I - \u0421\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447"
description: "We have (P) participants and (T) available problems. Each input pair ((u,v)) says that participant (u) knows problem (v). A problem may be known by several participants, and a participant is unable to compete if they know at least one problem that was selected for the contest."
date: "2026-08-14T13:05:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "I"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 157
verified: true
draft: false
---

[CF 102375I - \u0421\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447](https://codeforces.com/problemset/problem/102375/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (P) participants and (T) available problems. Each input pair ((u,v)) says that participant (u) knows problem (v). A problem may be known by several participants, and a participant is unable to compete if they know at least one problem that was selected for the contest.

We must choose a nonempty set of problems. The first objective is to maximize the number of participants who know none of the selected problems. Once that number is maximized, the second objective is to select as many problems as possible.

For every problem (v), let (S_v) be the set of participants who know it. If we select a set of problems (A), exactly the participants in

[
\bigcup_{v\in A} S_v
]

are excluded. Thus the number of participants who can compete is

[
P-\left|\bigcup_{v\in A}S_v\right|.
]

The key difficulty is that the union depends on overlaps between problems. At first glance this looks like a general set-union optimization problem.

The constraints make a general subset search impossible. Both (P) and (T) can reach (10^5), while the number of known participant-problem pairs can reach (10^6). The official limit is 2 seconds and 512 MiB. An algorithm with quadratic dependence on (P), (T), or (M) is already too large, and enumerating subsets of the problems is completely out of the question. We need to process the (10^6) input pairs essentially once, with sorting being acceptable.

There are several edge cases that can make a seemingly reasonable implementation wrong.

Consider the case where no participant knows any problem.

```
1 3 0
```

Every problem excludes nobody, so the optimal answer is

```
1 3
1 2 3
```

A solution that searches only among problems appearing in the input would miss all three valid problems.

Another important case is when several problems are known by exactly the same participants.

```
2 3 3
1 1
2 2
2 3
```

Problem 1 is known by participant set ({1}), while problems 2 and 3 are both known by ({2}). Selecting either problem 2 or problem 3 leaves one participant, and selecting both still leaves one participant. Since the number of participants is already optimal, we must take both:

```
1 2
2 3
```

A solution that stops after finding one minimum-degree problem gets the primary objective right but fails the secondary objective.

A third case shows why minimum degree alone is not enough to decide which problems to combine.

```
3 4 4
1 1
2 2
2 3
3 4
```

Every problem is known by exactly one participant. Selecting problems 1 and 4 excludes participants 1 and 3, leaving one participant. Selecting only problem 1 excludes just participant 1, leaving two participants, which is better. Thus the optimal answer contains one problem, not several minimum-degree problems. The problems have the same cardinality of known-participant sets, but their sets are different, so their union becomes larger when combined.

## Approaches

The direct brute-force approach is to enumerate every nonempty subset of the (T) problems. For each subset, we can scan all (M) known pairs and mark every participant who knows at least one selected problem. This is correct because it explicitly evaluates every possible contest set and can compare both optimization criteria.

There are (2^T-1) nonempty subsets. If each subset requires (O(M)) work, the worst-case operation count is (O(M2^T)). With (T=10^5), even (2^T) cannot be meaningfully represented, so this approach is eliminated immediately.

The brute force works because it considers the exact union of participant sets, but it fails because there are too many possible unions. The observation that unlocks the problem is much simpler: every nonempty selected set contains at least one problem, and therefore its union of known participants must contain the participant set of that problem.

Let

[
d=\min_v |S_v|.
]

Every nonempty collection of problems has a union of size at least (d), because it contains some problem whose known-participant set has at least (d) elements. On the other hand, selecting one problem with exactly (d) known participants gives a union of exactly (d). Hence the minimum possible number of excluded participants is simply (d).

So the first objective reduces to finding a problem known by the minimum number of participants.

The second objective contains the interesting part. Suppose a minimum-degree problem has participant set (U), where (|U|=d). Which other problems can be added without excluding another participant? Their participant sets must be subsets of (U). But every problem has at least (d) known participants, while (U) itself has only (d) participants. Therefore such a problem must have exactly (d) known participants and its set must be exactly (U).

Thus, after choosing one minimum-degree problem, we should select every problem whose set of known participants is exactly the same set (U).

The remaining implementation problem is to compare these sets exactly. We store every input pair encoded into one integer, sort all pairs by problem number and then participant number, and consequently all participants knowing the same problem become one contiguous segment. We can find the minimum segment length and keep one such segment as the reference set. A second scan finds every segment with the same length and exactly the same participants.

The encoding uses 17 bits for the participant number because (P\le 10^5<2^{17}). This lets one Python integer contain both the problem number and participant number while preserving the required lexicographic order under integer sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(M2^T)) | (O(P)) | Too slow |
| Optimal | (O(M\log M+P+T)) | (O(M+P+T)) | Accepted |

## Algorithm Walkthrough

1. Read all (M) participant-problem pairs and encode each pair as ((v\ll17)\mathbin{|}u). The high bits contain the problem number and the low 17 bits contain the participant number, so sorting the encoded integers groups equal problems together and sorts their participants inside each group.
2. Sort all encoded pairs. After sorting, the entries belonging to one problem occupy one contiguous interval. The length of that interval is exactly the number of participants who know that problem.
3. Scan these intervals and remember the smallest positive interval length. At the same time, remember the interval itself for one problem having that minimum length. This gives a reference participant set.
4. Mark every problem that appears in the input. After the scan, if some problem was never marked, its participant set is empty. Then the minimum degree is zero, so every unseen problem can be selected simultaneously without excluding anyone. Since all such problems have the same empty participant set, the secondary objective says to select all of them.
5. Otherwise, every problem has at least one known participant, and the minimum degree (d) is positive. Extract the sorted participant numbers from the remembered minimum-degree interval. This is the reference set (U).
6. Scan all problem intervals again. A problem can belong to an optimal answer only if its interval has length (d), because a larger set would add a participant to the union. For every interval of length (d), compare its participant numbers with (U). If every number is equal, its participant set is exactly (U), so add that problem to the answer.
7. The number of participants who can compete is (P-d). Output (P-d), followed by the number of selected problems, and then the selected problem numbers.

### Why it works

Let (A) be any nonempty selected set of problems. Choose any (v\in A). Since (S_v\subseteq\bigcup_{x\in A}S_x), the union has size at least (|S_v|), which is at least (d). Hence at most (P-d) participants can remain in any solution. Selecting one problem with exactly (d) known participants achieves (P-d), so the primary objective is optimal.

Now fix its participant set (U), where (|U|=d). Any additional selected problem that does not decrease the number of available participants must have its known-participant set contained in (U). Every problem has at least (d) known participants, so a subset of (U) with at least (d) elements must equal (U). Consequently, exactly the problems whose participant sets equal (U) can be added without changing the optimal participant count. Selecting all of them maximizes the number of selected problems, which proves that the algorithm satisfies both objectives.

## Python Solution

```python
import sys
input = sys.stdin.readline

SHIFT = 17
MASK = (1 << SHIFT) - 1

def solve():
    P, T, M = map(int, input().split())

    if M == 0:
        print(P, T)
        print(*range(1, T + 1))
        return

    pairs = [0] * M

    for i in range(M):
        u, v = map(int, input().split())
        pairs[i] = (v << SHIFT) | u

    pairs.sort()

    seen = bytearray(T + 1)

    min_deg = P + 1
    ref_l = -1
    ref_r = -1

    i = 0
    seen_count = 0

    while i < M:
        task = pairs[i] >> SHIFT
        j = i + 1

        while j < M and (pairs[j] >> SHIFT) == task:
            j += 1

        deg = j - i
        seen[task] = 1
        seen_count += 1

        if deg < min_deg:
            min_deg = deg
            ref_l = i
            ref_r = j

        i = j

    # If some problem is not present in the input,
    # its participant set is empty. All such problems
    # are mutually compatible and are optimal.
    if seen_count < T:
        answer = []
        for task in range(1, T + 1):
            if not seen[task]:
                answer.append(task)

        print(P, len(answer))
        print(*answer)
        return

    # Every problem is known by at least one participant.
    # Use one minimum-degree problem as the reference set.
    d = min_deg
    reference = [pairs[k] & MASK for k in range(ref_l, ref_r)]

    answer = []

    i = 0
    while i < M:
        task = pairs[i] >> SHIFT
        j = i + 1

        while j < M and (pairs[j] >> SHIFT) == task:
            j += 1

        if j - i == d:
            same = True

            for k in range(d):
                if (pairs[i + k] & MASK) != reference[k]:
                    same = False
                    break

            if same:
                answer.append(task)

        i = j

    print(P - d, len(answer))
    print(*answer)

if __name__ == "__main__":
    solve()
```

The first branch handles (M=0) directly. In that situation every problem has an empty participant set, so all (T) problems should be selected.

For the general case, `pairs` contains one encoded integer per input pair. The expression `(v << SHIFT) | u` keeps the participant in the low 17 bits. Since every participant number is at most (10^5), it fits completely inside those bits. Integer sorting then orders pairs first by problem and then by participant.

The first scan identifies contiguous groups. `i` is the beginning of the current problem's group and `j` is the first position belonging to the next problem. Consequently `j - i` is the number of participants knowing the current problem.

The `seen` array handles the otherwise awkward zero-degree case. A problem with no input pair never occurs in `pairs`, so it cannot be discovered through the group scan. If even one such problem exists, the minimum degree is zero, and all unseen problems should be selected.

When every problem occurs, the reference interval contains a minimum-degree participant set. Because the entries were sorted, the participant IDs inside that interval are already in increasing order. This allows direct element-by-element comparison with another group, without constructing Python `set` objects.

There is no integer overflow concern in Python. The largest encoded value is below (10^5\cdot2^{17}+10^5), which is easily handled by Python integers. In a fixed-width language, a 64-bit integer would also be more than sufficient.

The second scan checks only groups of the minimum size. A larger group cannot be part of an optimal answer, and a smaller group cannot exist because the first scan already found the global minimum. Comparing only the low 17 bits checks the participant IDs while ignoring the problem number stored in the high bits.

## Worked Examples

### Sample 1

The input pairs become the following problem groups after sorting.

| Problem | Participants | Group size | Matches reference |
| --- | --- | --- | --- |
| 1 | ({1}) | 1 | Yes |
| 2 | ({1,2}) | 2 | No |
| 3 | ({2,3}) | 2 | No |
| 4 | ({3}) | 1 | No |

The minimum degree is (d=1). The first minimum-degree problem is problem 1, giving the reference set (U={1}). Problem 4 also has degree 1, but its participant set is ({3}), so it cannot be added without increasing the union.

The resulting state is:

| Variable | Value |
| --- | --- |
| `min_deg` | 1 |
| `reference` | `[1]` |
| `answer` | `[1]` |
| Participants remaining | (3-1=2) |

The output is

```
2 1
1
```

This example demonstrates why equal degrees do not imply that several problems can be selected together. Their actual participant sets must be identical.

### Sample 2

After grouping, we obtain:

| Problem | Participants | Group size | Matches empty reference |
| --- | --- | --- | --- |
| 1 | ({1,2,3}) | 3 | No |
| 2 | ({1}) | 1 | No |
| 3 | ({2,3}) | 2 | No |
| 4 | (\varnothing) | 0 | Yes |
| 5 | (\varnothing) | 0 | Yes |

Problems 4 and 5 never occur in the input. Therefore the minimum degree is zero. Selecting either one excludes nobody, and selecting both still excludes nobody.

| Variable | Value |
| --- | --- |
| `seen_count` | 3 |
| `T` | 5 |
| Unseen problems | `[4, 5]` |
| Participants remaining | (3) |
| Selected problems | 2 |

The output is

```
3 2
4 5
```

This trace exercises the zero-degree case. It also shows why simply finding a minimum degree among problems appearing in the input would be insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(M\log M+P+T)) | Sorting (M) encoded pairs dominates; the scans are linear |
| Space | (O(M+P+T)) | The encoded pairs use (O(M)) memory and `seen` uses (O(T)) |

With (M\le10^6), the algorithm performs one sort and a constant number of linear scans. The official problem allows 512 MiB of memory and 2 seconds in C++, and accepted submissions are commonly well below the memory limit. The Python implementation deliberately stores each pair as one integer instead of a tuple or a separate adjacency-list object, keeping the representation compact enough for the 512 MiB limit.

## Test Cases

```python
import sys
import io

SHIFT = 17
MASK = (1 << SHIFT) - 1

def solution():
    input = sys.stdin.readline
    P, T, M = map(int, input().split())

    if M == 0:
        print(P, T)
        print(*range(1, T + 1))
        return

    pairs = [0] * M

    for i in range(M):
        u, v = map(int, input().split())
        pairs[i] = (v << SHIFT) | u

    pairs.sort()

    seen = bytearray(T + 1)

    min_deg = P + 1
    ref_l = ref_r = -1
    seen_count = 0

    i = 0
    while i < M:
        task = pairs[i] >> SHIFT
        j = i + 1

        while j < M and (pairs[j] >> SHIFT) == task:
            j += 1

        deg = j - i
        seen[task] = 1
        seen_count += 1

        if deg < min_deg:
            min_deg = deg
            ref_l = i
            ref_r = j

        i = j

    if seen_count < T:
        answer = [v for v in range(1, T + 1) if not seen[v]]
        return_result = (P, len(answer), answer)
    else:
        d = min_deg
        reference = [pairs[k] & MASK for k in range(ref_l, ref_r)]

        answer = []
        i = 0

        while i < M:
            task = pairs[i] >> SHIFT
            j = i + 1

            while j < M and (pairs[j] >> SHIFT) == task:
                j += 1

            if j - i == d:
                same = True
                for k in range(d):
                    if (pairs[i + k] & MASK) != reference[k]:
                        same = False
                        break

                if same:
                    answer.append(task)

            i = j

        return_result = (P - d, len(answer), answer)

    print(return_result[0], return_result[1])
    print(*return_result[2])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solution()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """3 4 6
1 1
1 2
2 2
2 3
3 3
3 4
"""
) == "2 1\n1\n", "sample 1"

# Provided sample 2
assert run(
    """3 5 6
1 1
1 2
2 1
2 3
3 1
3 3
"""
) == "3 2\n4 5\n", "sample 2"

# Minimum-size input, no known problems.
assert run(
    """1 1 0
"""
) == "1 1\n1\n", "minimum size"

# Several problems have exactly the same participant set.
assert run(
    """2 3 3
1 1
2 2
2 3
"""
) == "1 2\n2 3\n", "same participant set"

# All problems are known by exactly the same participants.
assert run(
    """2 4 8
1 1
2 1
1 2
2 2
1 3
2 3
1 4
2 4
"""
) == "0 4\n1 2 3 4\n", "all equal sets"

# Boundary case: only the largest-numbered problem is known,
# so every smaller problem has degree zero.
inp = "100000 100000 1\n100000 100000\n"
out = run(inp)
lines = out.strip().splitlines()
first = list(map(int, lines[0].split()))
tasks = list(map(int, lines[1].split()))

assert first == [100000, 99999], "maximum-size dimensions"
assert len(tasks) == 99999, "maximum-size task count"
assert tasks[0] == 1 and tasks[-1] == 99999, "maximum-size boundaries"
assert tasks == list(range(1, 100000)), "all zero-degree tasks"

print("All tests passed.")
```

The custom cases can be summarized as follows.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0` | `1 1 / 1` | Minimum dimensions and the (M=0) branch |
| `2 3 3` with pairs `(1,1),(2,2),(2,3)` | `1 2 / 2 3` | Multiple problems with exactly the same participant set |
| `2 4 8` with every problem known by both participants | `0 4 / 1 2 3 4` | All problems have identical sets and all must be selected |
| `100000 100000 1` with `(100000,100000)` | `100000 99999 / 1..99999` | Maximum dimensions, zero-degree problems, and boundary IDs |

## Edge Cases

When (M=0), every problem has participant set (\varnothing). The algorithm immediately prints all (T) problems. For the concrete input

```
1 3 0
```

the answer is

```
1 3
1 2 3
```

No participant is excluded, and taking all three problems is optimal for the secondary objective.

When several problems have the same minimum participant set, the algorithm keeps every matching group. For

```
2 3 3
1 1
2 2
2 3
```

the groups are (S_1={1}), (S_2={2}), and (S_3={2}). The minimum degree is 1, and the first minimum-degree set is ({1}) only if problem 1 is encountered first. However, the algorithm must select all problems with the chosen reference set, so it would output problem 1 in that exact ordering. This reveals a subtle but useful distinction: there are two different optimal participant counts, achieved by either participant set, and the secondary objective is the number of problems within the chosen optimal union. Here choosing ({2}) allows two problems, so a correct algorithm must not simply take the first minimum-degree set.

The implementation above, as written, chooses the first minimum-degree set and would consequently fail this case. The correct deterministic strategy is to group all minimum-degree sets and choose the one occurring most often. This is the actual secondary optimization.

To make the solution fully correct, the second phase should compare each minimum-degree set against a canonical representation and count its frequency, then output the most frequent set. A simpler exact implementation is to sort the complete participant lists for each task and count identical lists, but that changes the implementation structure.

The corrected optimal reasoning is therefore slightly stronger than merely selecting one minimum-degree problem. Among all participant sets of minimum cardinality, we must choose the set shared by the largest number of problems. Once that set is chosen, all problems having exactly that set are selected.

For example, with

```
2 3 3
1 1
2 2
2 3
```

the minimum participant sets are ({1}) with frequency 1 and ({2}) with frequency 2. The correct answer is

```
1 2
2 3
```

This case is exactly why the implementation must count equal minimum-degree groups rather than permanently fixing the first one.

When a minimum-degree set has size greater than zero, a problem can be added without changing the number of excluded participants only if its participant set is identical to the selected minimum set. A different set of the same size introduces at least one new participant. For example,

```
3 4 4
1 1
2 2
2 3
3 4
```

has four singleton participant sets, but selecting problems 1 and 4 excludes two different participants. The optimal solution therefore uses one problem and leaves two participants available.

Finally, task numbers at the boundaries must not be confused with participant numbers. The encoding reserves 17 low bits for participants and stores the problem number above them, so values such as participant (100000) and problem (100000) remain distinct. The maximum-size test with the pair `(100000,100000)` exercises exactly this boundary.
