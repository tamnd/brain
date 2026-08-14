---
title: "CF 102348E - Painting The Fence"
description: "We have a row of (n) fence planks and (m) colors. Color (i) is available for exactly (ai) planks, and the values sum to (n), so every unit of paint must be used."
date: "2026-08-14T11:51:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "E"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 844
verified: true
draft: false
---

[CF 102348E - Painting The Fence](https://codeforces.com/problemset/problem/102348/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of (n) fence planks and (m) colors. Color (i) is available for exactly (a_i) planks, and the values sum to (n), so every unit of paint must be used. We need to permute these color occurrences along the fence so that no maximal contiguous run of one color has length greater than (k).

The output is either such a length-(n) color array, using every color exactly (a_i) times, or (-1) if no valid arrangement exists.

The constraint (n \le 2\cdot 10^5) rules out anything that explores a large fraction of the possible permutations. Even (O(n^2)) would already mean around (4\cdot10^{10}) operations in the worst case. We need an essentially linear or (O(n\log n)) solution. A priority queue is appropriate because every position can be decided by taking the color with the largest remaining amount, while temporarily excluding the color that has reached the run limit.

There are several edge cases that can make a careless implementation fail. First, a color can be exactly at the feasibility boundary. For example,

```
6 2 3
5 1
```

is possible, with `1 1 1 2 1 1`. The run of color 1 has length exactly (3), so rejecting runs of length (k) instead of runs greater than (k) would incorrectly print (-1).

A second case is when the largest color is too large even though several other colors exist. For example,

```
8 2 3
7 1
```

is impossible. Seven copies of color 1 require at least three separate runs, but the single plank of color 2 can separate only two boundaries. A greedy implementation that simply starts placing the largest color without checking feasibility can eventually get stuck and needs to handle that situation correctly.

The smallest possible input is also special:

```
1 1 1
1
```

The only valid answer is `1`. There is no previous color and no possibility of a run violation, so initialization must not assume that the answer already contains a previous plank.

Finally, (k) can be larger than every useful run. For example,

```
5 2 5
4 1
```

is valid as `1 1 1 1 2`. When (k\ge n), the run restriction is effectively irrelevant, so the algorithm must not force unnecessary color changes.

## Approaches

A direct brute-force approach treats the fence as a permutation problem. At every plank we try every color whose remaining amount is positive, recursively continue, and reject a branch as soon as its current run exceeds (k). This is correct because every possible coloring is eventually considered, and a valid coloring is accepted.

The problem is the number of possible colorings. Even ignoring the fixed multiplicities, there are (m^n) sequences of (n) colors. Checking one complete sequence takes (O(n)), so a straightforward exhaustive search can take (O(nm^n)) time. With (m=n=2\cdot10^5), this worst-case bound is roughly (O(n^{n+1})), which is completely infeasible.

The useful observation is that we never care about the identities of positions that have not been filled yet. At each step, what matters is how many copies of every color remain, what color was used last, and how long the current run is. Among the available colors, the one with the largest remaining count is the most dangerous one. If we leave it unused while consuming smaller colors, its remaining copies become harder to place later.

That leads to a priority queue. We always take the color with the largest remaining count. If that color is different from the previous color, we can use it immediately. If it is the same color and the current run has already reached (k), we temporarily take the second-largest color instead. After using a color once, its remaining count is decreased and it is returned to the heap if copies remain.

There is also a simple feasibility condition. Suppose color (c) occurs (A) times. Since every run of (c) contains at most (k) copies, we need at least (\lceil A/k\rceil) separate runs of (c). Between those runs there must be at least (\lceil A/k\rceil-1) planks of other colors. Thus,

[
\left\lceil\frac{A}{k}\right\rceil \le n-A+1,
]

which is equivalent to

[
A \le k(n-A+1).
]

The hardest color is the one with the largest (A), so checking the maximum (a_i) is sufficient. This gives an immediate impossibility test before constructing the answer.

The brute-force works because it explores every possible ordering, but fails because there are exponentially many orderings. The observation that only the largest remaining color threatens to become impossible to place lets us make each decision greedily with a max-heap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm^n)) | (O(n+m)) | Too slow |
| Optimal | (O(n\log m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Read the color counts and find the largest count (A). If (A>k(n-A+1)), print (-1). The largest color alone already needs more separated runs than the other planks can provide.
2. Put every color with its remaining count into a max-heap. Python's `heapq` is a min-heap, so we store the negative count.
3. Keep `last`, the color used on the previous plank, and `run`, the length of its current consecutive run. Initially there is no previous color, so `last = -1` and `run = 0`.
4. At every position, remove the color with the largest remaining count from the heap.
5. If that color differs from `last`, use it. The new run length becomes (1).
6. If it equals `last` and `run < k`, use it again. Continuing the same color is preferable because it has the largest remaining count and the current run still has room.
7. If it equals `last` and `run = k`, it cannot be used now. Remove the next largest color from the heap and use that color instead. Return the blocked color to the heap unchanged. If no second color exists, the construction cannot continue.
8. Decrease the chosen color's remaining count. If it still has copies left, insert it back into the heap.
9. Repeat until all (n) planks are assigned.

### Why it works

The invariant is that after every constructed prefix, the heap contains exactly the unused copies of every color, while the prefix already satisfies the run-length limit. Whenever the most frequent remaining color is allowed to continue, using it is safe because postponing a color with a smaller remaining count cannot make that smaller color more difficult to place. Whenever the current run reaches (k), continuing it is forbidden, so any valid continuation must choose another color. Choosing the largest available alternative preserves the most constrained remaining resource.

The feasibility inequality guarantees that the largest color has enough nonmatching planks available to separate all of its required runs. The greedy choice always spends those separating colors only when a switch is forced, rather than wasting them while the current color can still legally continue. Consequently, if the initial feasibility condition holds, the heap construction can consume all copies without getting stuck.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))

    mx = max(a)

    if mx > k * (n - mx + 1):
        print(-1)
        return

    heap = []
    for color, count in enumerate(a, 1):
        heapq.heappush(heap, (-count, color))

    ans = []
    last = -1
    run = 0

    for _ in range(n):
        neg_count, color = heapq.heappop(heap)
        count = -neg_count

        if color == last and run == k:
            if not heap:
                print(-1)
                return

            neg_count2, color2 = heapq.heappop(heap)
            count2 = -neg_count2

            heapq.heappush(heap, (-count, color))

            color = color2
            count = count2
            run = 1
        else:
            if color == last:
                run += 1
            else:
                run = 1

        ans.append(color)
        count -= 1

        if count > 0:
            heapq.heappush(heap, (-count, color))

        last = color

    print(*ans)

if __name__ == "__main__":
    solve()
```

The feasibility check uses the maximum count only. For a color with (A) copies, at least (\lceil A/k\rceil) runs are necessary, and the (n-A) other planks provide at most (n-A+1) possible run slots. Since the inequality becomes harder as (A) grows, checking the maximum count covers every color.

The heap stores pairs `(-count, color)` so that the smallest heap value corresponds to the largest remaining count. Color indices are stored explicitly because two colors can have the same count and still need to remain distinguishable.

The special branch where `color == last and run == k` is the key boundary condition. The current color has already occupied exactly (k) consecutive positions, so using it one more time would create a run of length (k+1). We temporarily remove it, select the next best color, and put the blocked color back unchanged.

When a selected color has one copy left, decrementing its count produces zero and it is simply not pushed back. Since the input guarantees that the total of all counts is (n), exactly (n) successful selections are needed.

Python integers do not overflow, and the largest product in the feasibility test is at most (n^2), around (4\cdot10^{10}), which Python handles directly.

## Worked Examples

### Sample 1

The input is

```
5 2 1
2 3
```

Here (k=1), so equal colors may never be adjacent. The largest count is (3), and

[
3 \le 1(5-3+1)=3,
]

so the instance is exactly at the feasibility boundary.

| Position | Heap before choice | Last | Run | Chosen color | Remaining chosen count |
| --- | --- | --- | --- | --- | --- |
| 1 | `(3,2), (2,1)` | none | 0 | 2 | 2 |
| 2 | `(2,1), (2,2)` | 2 | 1 | 1 | 1 |
| 3 | `(2,2), (1,1)` | 1 | 1 | 2 | 1 |
| 4 | `(1,1), (1,2)` | 2 | 1 | 1 | 0 |
| 5 | `(1,2)` | 1 | 1 | 2 | 0 |

The resulting coloring is `2 1 2 1 2`. Because (k=1), every step is forced to switch colors, and the feasibility inequality tells us that color 2 has exactly enough separating planks.

### Sample 2

The input is

```
8 2 3
1 7
```

The largest color has (A=7) copies. Its required number of runs is

[
\left\lceil\frac{7}{3}\right\rceil=3.
]

But there is only one plank of the other color, so at most two runs of color 1 can be separated. Equivalently,

[
7 > 3(8-7+1)=6.
]

The algorithm rejects the instance before constructing anything.

| Value | State |
| --- | --- |
| (n) | 8 |
| (k) | 3 |
| Largest count (A) | 7 |
| Maximum possible separated capacity | (3(8-7+1)=6) |
| Feasible? | No |
| Output | `-1` |

This demonstrates why the feasibility check must use `n - A + 1`, rather than simply counting how many other colors exist. A single other plank creates at most two separated groups of the dominant color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log m)) | Every plank causes a constant number of heap operations, each taking (O(\log m)). |
| Space | (O(n+m)) | The answer contains (n) colors and the heap contains at most (m) color entries. |

With (n\le2\cdot10^5), the algorithm performs only a logarithmic amount of heap work per plank. The memory usage is linear, so it comfortably fits the 256 MB limit.

## Test Cases

Because a valid output is not unique, the test harness should not compare successful outputs to one fixed string. Instead, it checks that the output has the right number of planks, uses every color the required number of times, and never creates a run longer than (k). For impossible cases, an exact `-1` comparison is appropriate.

```python
import sys
import io
import heapq

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))

    mx = max(a)

    if mx > k * (n - mx + 1):
        print(-1)
        return

    heap = []
    for color, count in enumerate(a, 1):
        heapq.heappush(heap, (-count, color))

    ans = []
    last = -1
    run = 0

    for _ in range(n):
        neg_count, color = heapq.heappop(heap)
        count = -neg_count

        if color == last and run == k:
            if not heap:
                print(-1)
                return

            neg_count2, color2 = heapq.heappop(heap)
            count2 = -neg_count2

            heapq.heappush(heap, (-count, color))

            color = color2
            count = count2
            run = 1
        else:
            if color == last:
                run += 1
            else:
                run = 1

        ans.append(color)
        count -= 1

        if count > 0:
            heapq.heappush(heap, (-count, color))

        last = color

    print(*ans)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

def validate(inp: str, out: str):
    data = list(map(int, inp.split()))
    n, m, k = data[0], data[1], data[2]
    a = data[3:3 + m]

    assert out != "-1"

    ans = list(map(int, out.split()))
    assert len(ans) == n

    cnt = [0] * (m + 1)

    last = -1
    run = 0

    for color in ans:
        assert 1 <= color <= m
        cnt[color] += 1

        if color == last:
            run += 1
        else:
            last = color
            run = 1

        assert run <= k

    for color in range(1, m + 1):
        assert cnt[color] == a[color - 1]

# Provided samples
sample1 = """\
5 2 1
2 3
"""
out = run(sample1)
validate(sample1, out)

sample2 = """\
8 2 3
1 7
"""
assert run(sample2) == "-1", "sample 2"

sample3 = """\
10 3 2
5 2 3
"""
out = run(sample3)
validate(sample3, out)

# Minimum-size input
case1 = """\
1 1 1
1
"""
assert run(case1) == "1", "minimum-size case"

# Exact feasibility boundary
case2 = """\
6 2 3
5 1
"""
out = run(case2)
validate(case2, out)

# All counts equal
case3 = """\
12 3 4
4 4 4
"""
out = run(case3)
validate(case3, out)

# Maximum-size input
case4 = "200000 2 100000\n100000 100000\n"
out = run(case4)
validate(case4, out)

# Just beyond the feasibility boundary
case5 = """\
8 2 3
7 1
"""
assert run(case5) == "-1", "impossible boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1` | `1` | Minimum size and initialization with no previous color |
| `6 2 3 / 5 1` | Any valid coloring, such as `1 1 1 2 1 1` | Exact boundary where a run of length (k) is allowed |
| `12 3 4 / 4 4 4` | Any valid coloring | Equal color frequencies and ties in the heap |
| `200000 2 100000 / 100000 100000` | Any valid coloring | Maximum (n), large heap operations, and runs exactly at (k) |
| `8 2 3 / 7 1` | `-1` | Feasibility inequality and impossible dominant color |

## Edge Cases

For the minimum input

```
1 1 1
1
```

the maximum count is (1), and the feasibility test gives (1\le1(1-1+1)). The heap contains only color 1, which is selected once. Since there is no previous color, the run starts at (1), and the output is exactly `1`.

For the exact boundary case

```
6 2 3
5 1
```

the dominant color has five copies. It needs two runs because (\lceil5/3\rceil=2), and the single copy of color 2 is enough to separate them. The greedy construction takes color 1 three times, switches to color 2 when the run reaches (3), then takes color 1 twice. The result is `1 1 1 2 1 1`, whose longest run has length exactly (3).

For equal frequencies,

```
12 3 4
4 4 4
```

every color has the same priority in the heap. The heap's color index breaks ties consistently, so the construction can produce four copies of one color, followed by four of another and four of the third. Each run has length (4), exactly the allowed maximum.

For the impossible boundary,

```
8 2 3
7 1
```

the dominant color needs at least three runs, while one other plank can separate at most two such runs. The inequality becomes (7\le6), which is false, so the algorithm prints `-1` immediately. No partial construction is needed, and there is no risk of reporting a prefix that cannot be completed.

The case (k=1) is handled by the same logic. Every time the previous color is at the top of the heap, `run == k` is already true, so the algorithm must select a different color. The feasibility condition reduces to (A\le n-A+1), the familiar requirement that the most frequent color must have enough other elements to separate all of its copies.
