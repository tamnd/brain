---
title: "CF 102348E - Painting The Fence"
description: "We have a row of (n) fence planks and (m) colors. Color (i) is available exactly (ai) times, so every occurrence of that color must be used. Since the sum of all (ai) equals (n), the task is to arrange the colors into an array of length (n)."
date: "2026-08-14T02:11:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "E"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 187
verified: false
draft: false
---

[CF 102348E - Painting The Fence](https://codeforces.com/problemset/problem/102348/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We have a row of (n) fence planks and (m) colors. Color (i) is available exactly (a_i) times, so every occurrence of that color must be used. Since the sum of all (a_i) equals (n), the task is to arrange the colors into an array of length (n).

The restriction is local: whenever several consecutive planks have the same color, that run may contain at most (k) planks. The output can be any valid color array, while (-1) means that no such arrangement exists.

The upper bound (n\le 2\cdot10^5) rules out anything quadratic in (n). An (O(n^2)) construction could perform around (4\cdot10^{10}) operations in the worst case, far beyond a one-second limit. We want a solution close to linear, or at most (O(n\log n)), because the input itself contains only (O(n)) numbers.

The most dangerous edge case is a single color. For example,

```
1 1 1
1
```

has the valid output `1`, because the only run has length (1). A careless implementation that always looks for another color as a separator could incorrectly reject it.

The opposite case is when one color has too many planks. For example,

```
8 2 3
1 7
```

must produce `-1`. Seven copies of color (2) need at least three runs, because each run contains at most three copies. Separating three runs requires at least two planks of another color, but only one plank of color (1) exists. A construction that merely cuts color (2) into groups of three can silently leave two groups adjacent.

The boundary (a_i=k) also matters. For

```
4 2 2
2 2
```

a valid answer is `1 1 2 2`. A run of exactly (k) planks is allowed. Code that treats (k) as a strict upper bound would reject a valid arrangement.

A final subtle case is when a color needs several runs but its last run is shorter than (k). For

```
5 2 2
3 2
```

the arrangement `1 1 2 2 1` works. Color (1) is split into runs of lengths (2) and (1), not necessarily into equal-sized groups. Any construction that insists every group has exactly (k) elements is unnecessarily restrictive.

## Approaches

A direct brute-force approach would try to build the fence from left to right and, at every position, choose one of the colors whose remaining count is positive and whose use would not create a run longer than (k). In the worst case there are (m) possible choices at each of (n) positions, giving roughly (m^n) possible arrays. Even adding memoization over remaining counts does not help, because the state space can still be exponential in the number of colors. A simple backtracking implementation is therefore unusable.

The useful observation is that a color with (a_i) planks needs at least

[
r_i=\left\lceil\frac{a_i}{k}\right\rceil
]

separate runs. We can choose exactly that many runs and give every run at most (k) planks. The problem then becomes much simpler: arrange these runs so that two consecutive runs never have the same color.

Consider the color with the largest (a_i). It also has the largest (r_i), because the ceiling function above is monotonic. If this color needs (r) runs, there must be at least (r-1) planks of other colors to separate them. Consequently, a necessary condition is

[
r-1\le n-a_{\max}.
]

This condition is also sufficient. We split every color into exactly (\lceil a_i/k\rceil) chunks, then arrange the chunks using the standard greedy strategy for avoiding equal adjacent labels: repeatedly take a color with the largest number of unused chunks, but never choose the same color as the previous chunk when another color is available.

Why does this work? The dominant color has the largest number of chunks. The feasibility condition says that the remaining actual planks are sufficient to separate its chunks. Since every other color has no more chunks than the dominant color, the collection of chunks can be interleaved without putting equal colors next to each other.

A max-heap gives a clean implementation. Each heap entry stores a color and its number of remaining chunks. When a color is selected, we output one chunk from it, decrease its chunk count, and temporarily keep it aside so it cannot be selected immediately again. Then we select the next largest color. The chunk itself has size (k), except for the final chunk of a color, whose size is the remaining number of planks.

The brute-force works because it explicitly explores every possible coloring, but fails when the number of possibilities becomes exponential. The observation that only the separation of color runs matters lets us compress each color into a small number of chunks and solve the resulting arrangement greedily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(m^n)) in the worst case | (O(n+m)) | Too slow |
| Optimal | (O(n\log m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Read the color counts and find the largest count (a_{\max}). Let its color be (c). This color requires (r=\lceil a_{\max}/k\rceil) separate runs. If (r-1>n-a_{\max}), print (-1), because there are not enough non-(c) planks to separate those runs.
2. For every color (i), compute the minimum number of runs it needs as (r_i=\lceil a_i/k\rceil). Store ((r_i,i)) in a max-heap. We deliberately use the minimum possible number of runs because splitting a color into even more runs only creates extra adjacency constraints and is never needed.
3. Keep the remaining number of planks for every color. Initially this is exactly (a_i). When one run of color (i) is chosen, its size is (\min(k,\text{remaining}[i])). Append that many copies of (i) to the answer and decrease its remaining plank count.
4. Repeatedly remove the color with the largest number of unused runs from the heap. If it is different from the color used for the previous run, use it immediately. If it is the same, temporarily remove it and take the next heap entry instead.
5. After using a different color, put the previously blocked color back into the heap if it still has unused runs. The selected color is also returned if it still has another run. This makes every heap entry represent exactly the number of runs that have not yet been placed.
6. Continue until every run has been placed. Because consecutive runs always have different colors and every run contains at most (k) planks, the resulting plank array satisfies the required condition.

### Why it works

For each color (i), the algorithm divides (a_i) planks into exactly (\lceil a_i/k\rceil) runs, so no individual run can exceed (k). The only remaining danger is two runs of the same color becoming adjacent. The heap always chooses the color with the most remaining runs, except when that color was used immediately before, in which case another available color is selected. The largest run count belongs to the color with the largest (a_i), and the feasibility test guarantees that its required runs can all be separated by planks of other colors. Every other color requires no more runs than this dominant color, so the same separation argument applies to all colors. Thus the greedy arrangement can finish without creating equal adjacent runs.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))

    max_a = max(a)

    # The color with max_a planks needs this many runs.
    max_runs = (max_a + k - 1) // k

    # Its runs need at least max_runs - 1 separating planks.
    if max_runs - 1 > n - max_a:
        print(-1)
        return

    # remaining[i] is the number of individual planks of color i
    # that have not yet been put into the answer.
    remaining = a[:]

    # runs[i] is the number of chunks still needed for color i.
    # Python's heap is a min-heap, so store the negative count.
    heap = []
    for i, cnt in enumerate(a):
        runs = (cnt + k - 1) // k
        heapq.heappush(heap, (-runs, i))

    answer = []
    previous = -1

    while heap:
        neg_runs, color = heapq.heappop(heap)

        # We cannot put two runs of the same color next to each other.
        if color == previous:
            if not heap:
                print(-1)
                return

            neg_runs2, color2 = heapq.heappop(heap)

            # Put the blocked color back unchanged.
            heapq.heappush(heap, (neg_runs, color))

            neg_runs, color = neg_runs2, color2

        # Use one complete chunk of this color.
        take = min(k, remaining[color])
        answer.extend([color + 1] * take)
        remaining[color] -= take

        # One run has now been placed.
        runs_left = -neg_runs - 1

        if runs_left > 0:
            heapq.heappush(heap, (-runs_left, color))

        previous = color

    print(*answer)

if __name__ == "__main__":
    solve()
```

The first part computes the largest color count and converts it into the number of runs that color must occupy. The expression `(max_a + k - 1) // k` is the integer form of (\lceil a_{\max}/k\rceil), so it avoids floating-point arithmetic.

The feasibility check compares the number of required gaps, `max_runs - 1`, with the number of planks belonging to all other colors, `n - max_a`. Equality is allowed because exactly enough separator planks can exist.

The heap stores run counts rather than individual planks. This is the key compression in the implementation. A color with (10^5) planks does not need (10^5) heap entries, it needs only (\lceil10^5/k\rceil) runs represented by one entry.

When a run is selected, `take = min(k, remaining[color])` handles both full chunks and the final partial chunk. The code decreases the number of remaining runs by exactly one, not by `take`, because a run is the logical unit being arranged.

The `previous` variable prevents equal-colored runs from becoming adjacent. If the heap's largest entry has the same color as `previous`, the code takes the next best color and pushes the blocked color back. The feasibility condition guarantees that this situation cannot occur when there is no alternative color unless the construction is genuinely impossible.

All color indices in the internal arrays are zero-based, while the required output uses one-based color indices. The expression `color + 1` performs that conversion only when writing the answer.

No integer overflow is possible in Python. The answer contains exactly (n) integers, and each plank is appended once.

## Worked Examples

### Sample 1

For

```
5 2 1
2 3
```

color (2) has three planks and (k=1), so it needs three runs. There are two planks of color (1), exactly enough to separate those three runs.

The initial chunk counts are (r_1=2) and (r_2=3).

| Step | Heap run counts | Previous | Selected color | Chunk size | Answer prefix |
| --- | --- | --- | --- | --- | --- |
| 0 | (2:3,\ 1:2) | none | 2 | 1 | 2 |
| 1 | (1:2,\ 2:2) | 2 | 1 | 1 | 2 1 |
| 2 | (2:2,\ 1:1) | 1 | 2 | 1 | 2 1 2 |
| 3 | (1:1,\ 2:1) | 2 | 1 | 1 | 2 1 2 1 |
| 4 | (2:1) | 1 | 2 | 1 | 2 1 2 1 2 |

Every run has length one, so the maximum run length is exactly (k=1). The construction also uses both copies of color (1) and all three copies of color (2).

### Sample 2

For

```
8 2 3
1 7
```

color (2) has seven planks. Since (k=3), it requires

[
\left\lceil\frac{7}{3}\right\rceil=3
]

runs.

| Value | Meaning |
| --- | --- |
| (a_{\max}) | 7 |
| (k) | 3 |
| Required runs | 3 |
| Required separators | 2 |
| Other-color planks | 1 |
| Result | (-1) |

The three runs would need at least two non-color-(2) planks between them. Only one such plank exists, so no arrangement can satisfy the run-length limit. The algorithm rejects the instance before constructing anything.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log m)) | There are at most (n) runs, and each heap operation costs (O(\log m)). |
| Space | (O(n+m)) | The answer uses (O(n)) space, while the count arrays and heap use (O(m)) space. |

With (n\le2\cdot10^5), the algorithm performs only a logarithmic amount of heap work for each constructed run and scans the input once. This fits comfortably within the (256) MB memory limit and is suitable for the one-second constraint in Python with buffered input and output.

## Test Cases

The output is not unique, so asserting one exact coloring would be incorrect for most valid cases. The test harness below instead parses the program's output and checks the actual requirements: every color count must be correct and no equal-colored run may exceed (k).

```python
import sys
import io
import heapq

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n, m, k = map(int, sys.stdin.readline().split())
        a = list(map(int, sys.stdin.readline().split()))

        max_a = max(a)
        max_runs = (max_a + k - 1) // k

        if max_runs - 1 > n - max_a:
            print(-1)
            return sys.stdout.getvalue().strip()

        remaining = a[:]
        heap = []

        for i, cnt in enumerate(a):
            runs = (cnt + k - 1) // k
            heapq.heappush(heap, (-runs, i))

        answer = []
        previous = -1

        while heap:
            neg_runs, color = heapq.heappop(heap)

            if color == previous:
                if not heap:
                    print(-1)
                    return sys.stdout.getvalue().strip()

                neg_runs2, color2 = heapq.heappop(heap)
                heapq.heappush(heap, (neg_runs, color))

                neg_runs, color = neg_runs2, color2

            take = min(k, remaining[color])
            answer.extend([color + 1] * take)
            remaining[color] -= take

            runs_left = -neg_runs - 1
            if runs_left > 0:
                heapq.heappush(heap, (-runs_left, color))

            previous = color

        print(*answer)
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def run(inp: str) -> str:
    return solve_data(inp)

def validate(inp: str, out: str):
    data = list(map(int, inp.split()))
    n, m, k = data[:3]
    a = data[3:3 + m]

    tokens = out.split()

    if tokens == ["-1"]:
        max_a = max(a)
        required_runs = (max_a + k - 1) // k
        assert required_runs - 1 > n - max_a, (
            "Solution rejected a feasible instance"
        )
        return

    assert len(tokens) == n, "Wrong number of colors"
    ans = list(map(int, tokens))

    assert all(1 <= x <= m for x in ans), "Invalid color index"

    counts = [0] * m
    for x in ans:
        counts[x - 1] += 1

    assert counts == a, "Color counts do not match the input"

    run_length = 0
    previous = -1

    for x in ans:
        if x == previous:
            run_length += 1
        else:
            previous = x
            run_length = 1

        assert run_length <= k, "A color run is longer than k"

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

# Minimum-size instance
case4 = """\
1 1 1
1
"""
out = run(case4)
validate(case4, out)

# Boundary case: a run may have exactly k elements.
case5 = """\
4 2 2
2 2
"""
out = run(case5)
validate(case5, out)

# Large single-color case. It is valid because every run has length at most k.
case6 = """\
200000 1 200000
200000
"""
out = run(case6)
validate(case6, out)

# Off-by-one feasibility boundary:
# 7 copies need exactly 3 runs when k = 3,
# and two other planks are exactly enough separators.
case7 = """\
9 3 3
7 1 1
"""
out = run(case7)
validate(case7, out)

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1` | Any valid single `1` | Minimum size and the single-color case |
| `4 2 2 / 2 2` | Any arrangement such as `1 1 2 2` | A run of exactly (k) is legal |
| `200000 1 200000 / 200000` | (200000) copies of `1` | Maximum (n), maximum chunk size, and one-color handling |
| `9 3 3 / 7 1 1` | Any valid arrangement | Exact feasibility boundary, where the dominant color needs exactly two separators |

## Edge Cases

For the single-color input

```
1 1 1
1
```

the maximum color count is (1), so `max_runs` is (1). The required number of separators is (0), and there are (0) other planks. The feasibility test passes, the heap contains one run, and the answer is `1`.

For the impossible dominant-color case

```
8 2 3
1 7
```

the maximum count is (7), giving `max_runs = 3`. The algorithm needs `3 - 1 = 2` separators, but `n - max_a = 1`. Since (2>1), it immediately prints `-1`. No greedy construction is attempted because no construction could possibly succeed.

For the exact-(k) boundary

```
4 2 2
2 2
```

both colors require one run. The heap can choose either color first and then the other, producing `1 1 2 2`. The first run has length exactly (2), which is allowed, so an implementation must use `<= k`, not `< k`.

For the exact feasibility boundary

```
9 3 3
7 1 1
```

color (1) needs three runs of sizes (3,3,1). The two other colors provide exactly two separating planks. A possible result is `1 1 1 2 1 1 1 3 1`. The three color-(1) runs have lengths (3), (3), and (1), while colors (2) and (3) each appear once. The separator count is exactly sufficient, so the algorithm must accept this instance rather than using a strict inequality.

For a color whose count is not divisible by (k), the final chunk is shorter. With

```
5 2 2
3 2
```

the chunks are (1,1) of sizes (2,1), and (2) of size (2). The heap arranges these chunks without equal adjacent colors, for example as `1 1 2 2 1`. The final chunk of color (1) has size (1), demonstrating why the construction uses `min(k, remaining[color])` rather than always appending exactly (k) planks.
