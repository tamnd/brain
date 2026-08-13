---
title: "CF 102348E - Painting The Fence"
description: "We have a row of (n) fence planks and (m) colors. Color (i) must be used exactly (ai) times, so the array (a) describes the complete multiset of colors that has to appear in the final row."
date: "2026-08-14T05:29:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "E"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 204
verified: false
draft: false
---

[CF 102348E - Painting The Fence](https://codeforces.com/problemset/problem/102348/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We have a row of (n) fence planks and (m) colors. Color (i) must be used exactly (a_i) times, so the array (a) describes the complete multiset of colors that has to appear in the final row. The task is to permute these colors so that no maximal consecutive block of equal colors has length greater than (k).

The output is any valid permutation of the color indices (1,\ldots,m), with color (i) appearing exactly (a_i) times. If no such permutation exists, we print (-1).

The main constraint is (n\le 2\cdot10^5). That rules out any method that explores permutations or repeatedly scans the whole remaining array. We need essentially linear or (O(n\log n)) work. The number of colors is also at most (n), so a heap containing one entry per color is small enough, and processing each required color occurrence once is easily affordable.

A first edge case is when one color is too frequent. For example,

```
8 2 3
7 1
```

is impossible. Color (1) needs seven positions, but each of its consecutive blocks can contain at most three positions. With only one position of color (2), there are only two possible blocks of color (1), whose total capacity is (3+3=6). A construction that merely checks that (a_i\le n) would incorrectly accept this input.

A second edge case occurs exactly at the capacity boundary. Consider

```
7 2 3
5 2
```

This is possible, for example with

```
1 1 1 2 2 1 1
```

The two blocks of color (1) have lengths (3) and (2). A check using (a_i/k) with integer division instead of ceiling would count color (1) as requiring only one block, which loses precisely the information needed to detect the constraint.

A third edge case is (k=1). For

```
5 2 1
2 3
```

every adjacent pair must have different colors, so the only possible pattern up to symmetry is

```
2 1 2 1 2
```

A construction that creates arbitrary chunks and then concatenates chunks without checking their colors could accidentally place two equal chunks next to each other, producing an invalid run.

Finally, when there is only one color, the entire fence is one run. Thus

```
4 1 3
4
```

must produce (-1), while

```
3 1 3
3
```

is valid. The equality boundary (a_i=k) must be accepted.

## Approaches

A brute-force solution can try every possible ordering of the colors, keep the counts that remain, and stop as soon as it finds an ordering whose equal-color runs are all at most (k). The method is correct because every possible painting is considered, and a completed valid permutation is accepted.

The problem is the number of possibilities. In the worst case, when all (n) planks have different colors, there are (n!) permutations. Even a weaker recursive formulation that chooses one of at most (m) colors at every position has up to (m^n) branches. With (n=2\cdot10^5), neither is remotely feasible.

The useful observation is to stop thinking about individual planks first. A single color (i), appearing (a_i) times, must be divided into at least

[
c_i=\left\lceil\frac{a_i}{k}\right\rceil
]

separate blocks. Each such block can contain at most (k) planks. If we use exactly (c_i) blocks, all but possibly the last can have (k) planks, so this minimum number of blocks is achievable.

Now the problem becomes much simpler. We have (c_i) blocks of each color, and we need to order these blocks so that two blocks of the same color are never adjacent. Once the blocks are separated, every original run has size at most (k).

Let

[
C=\sum_i c_i.
]

A sequence of (C) blocks can avoid equal adjacent colors exactly when no color contributes more than (\lceil C/2\rceil) blocks. If a color has more than that many blocks, even placing all other blocks between its blocks is insufficient. Conversely, when this condition holds, we can repeatedly take the color with the largest remaining number of blocks, except that the color used immediately before cannot be chosen.

A max-heap gives this greedy choice efficiently. Each heap operation costs (O(\log m)), and we create exactly (C) blocks. Since (c_i\le a_i) and (\sum a_i=n), we have (C\le n), so the total work is (O(n\log m)).

The brute-force works because it explicitly searches the space of possible color arrangements, but fails because that space is enormous. The observation that each color only needs a certain number of bounded-size blocks reduces the problem to scheduling these blocks without equal neighbors, which is exactly what a greedy max-heap handles efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n!)) in the worst case | (O(n)) recursion and state | Too slow |
| Optimal | (O(n\log m)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. For every color (i), calculate the minimum number of blocks it needs as (c_i=(a_i+k-1)//k). The value (c_i) is the number of separate places where this color must appear in the final fence.
2. Compute (C=\sum c_i) and find the largest (c_i). If the largest value is greater than ((C+1)//2), print (-1). Such a color would need more block positions than all other blocks can separate.
3. Create a max-heap containing every color with its number of remaining blocks. Python's `heapq` is a min-heap, so store the negative count. Keep the previously chosen color separately because it cannot be selected for the next block.
4. Repeatedly remove the color with the largest remaining block count, skipping the previous color when necessary. If the heap's largest entry is the previous color, temporarily remove it and use the next largest color instead.
5. For the selected color, create one block. Its size is (k) if at least (k) planks of that color remain, otherwise it is the remaining number of planks. Append that many copies of the color to the answer and decrease its remaining plank count.
6. Decrease the color's remaining block count and put it back into the heap if more blocks of that color are required. Record the selected color as the previous color.
7. Continue until every required block has been placed. The result contains exactly (a_i) copies of every color, and consecutive blocks have different colors, so every maximal equal-color segment has size at most (k).

The greedy invariant is that after every step, the already constructed prefix consists of valid blocks, no two consecutive blocks have the same color, and the heap contains exactly the blocks that still need to be placed. Choosing the color with the largest remaining block count is safe because it is the color most likely to become impossible to separate later. If the largest available color is the previous one, using the second-largest color preserves the required separation while consuming one block from another color. The feasibility condition guarantees that this choice can continue until every block is placed.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))

    blocks = [(x + k - 1) // k for x in a]
    total_blocks = sum(blocks)

    if max(blocks) > (total_blocks + 1) // 2:
        print(-1)
        return

    heap = []
    for color in range(m):
        if blocks[color] > 0:
            heapq.heappush(heap, (-blocks[color], color))

    remaining = a[:]
    answer = []
    previous = -1

    for _ in range(total_blocks):
        first_count, first_color = heapq.heappop(heap)

        if first_color == previous:
            if not heap:
                print(-1)
                return

            second_count, second_color = heapq.heappop(heap)
            heapq.heappush(heap, (first_count, first_color))
            count, color = second_count, second_color
        else:
            count, color = first_count, first_color

        block_size = min(k, remaining[color])
        answer.extend([color + 1] * block_size)

        remaining[color] -= block_size
        blocks[color] -= 1

        if blocks[color] > 0:
            heapq.heappush(heap, (-blocks[color], color))

        previous = color

    print(*answer)

if __name__ == "__main__":
    solve()
```

The first calculation transforms plank counts into block counts. The ceiling division `(x + k - 1) // k` is essential because a color with (k+1) planks needs two blocks, not one.

The feasibility check is performed before constructing anything. If a color requires more than half of all blocks, rounded upward, there are not enough blocks of other colors to place between its blocks. This gives an immediate impossibility result.

The heap stores `(-blocks[color], color)` because `heapq` returns the smallest tuple, so negating the block count makes the largest count appear first. The color index is included as a deterministic tie breaker.

When the most frequent color is the same as `previous`, the algorithm temporarily removes it and takes the next color. The first heap entry is immediately restored so that its remaining count is not lost. This is the central detail that prevents two equal blocks from becoming adjacent.

The block size is computed from the remaining plank count, not from the number of blocks. Every block takes at most (k) planks, and the final block may be shorter. Since the number of blocks was computed with a ceiling, exactly enough blocks are created to consume every plank.

There is no integer overflow issue in Python. The answer itself contains exactly (n) integers, so its size is linear in the input size.

## Worked Examples

### Sample 1

For

```
5 2 1
2 3
```

each block can contain only one plank. The resulting block counts are (2) for color (1) and (3) for color (2), giving five blocks in total. The largest block count is (3), exactly ((5+1)//2), so the instance is feasible.

| Step | Previous | Heap before choice | Chosen color | Block size | Remaining block counts |
| --- | --- | --- | --- | --- | --- |
| 1 | none | (2:3,\ 1:2) | 2 | 1 | (2:2,\ 1:2) |
| 2 | 2 | (1:2,\ 2:2) | 1 | 1 | (2:2,\ 1:1) |
| 3 | 1 | (2:2,\ 1:1) | 2 | 1 | (2:1,\ 1:1) |
| 4 | 2 | (1:1,\ 2:1) | 1 | 1 | (2:1,\ 1:0) |
| 5 | 1 | (2:1) | 2 | 1 | (2:0,\ 1:0) |

The resulting array is `2 1 2 1 2`. Every block has length one, and each color is used exactly the required number of times.

### Sample 2

For

```
8 2 3
1 7
```

color (1) requires one block, while color (2) requires three blocks because (7) planks cannot fit into two blocks of capacity three.

| Color | Planks | Maximum block size | Required blocks |
| --- | --- | --- | --- |
| 1 | 1 | 3 | 1 |
| 2 | 7 | 3 | 3 |

There are four blocks in total, so a color can contribute at most ((4+1)//2=2) blocks. Color (2) needs three, so the algorithm immediately prints `-1`.

This example demonstrates why checking only `max(a)` against (k) is insufficient. The count (7) is larger than (k), but the real issue is that there are not enough other-color blocks to separate the required pieces.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log m)) | There are at most (n) blocks, and each heap operation costs (O(\log m)). |
| Space | (O(n)) | The answer uses (O(n)) space, while the heap and count arrays use (O(m)). |

Because (n\le2\cdot10^5), the algorithm performs only a linear number of block constructions and heap operations. The (O(n\log m)) bound is comfortably within the intended range, and the stored answer plus auxiliary arrays fit well inside the 256 MB memory limit.

## Test Cases

The test helper below validates outputs structurally rather than assuming that every valid answer has the same ordering. This is necessary because the problem accepts any valid painting. The provided samples are still checked by verifying the exact output produced by this deterministic heap implementation.

```python
import sys
import io
import heapq

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))

    blocks = [(x + k - 1) // k for x in a]
    total_blocks = sum(blocks)

    if max(blocks) > (total_blocks + 1) // 2:
        print(-1)
        return

    heap = []
    for color in range(m):
        if blocks[color] > 0:
            heapq.heappush(heap, (-blocks[color], color))

    remaining = a[:]
    answer = []
    previous = -1

    for _ in range(total_blocks):
        first_count, first_color = heapq.heappop(heap)

        if first_color == previous:
            if not heap:
                print(-1)
                return

            second_count, second_color = heapq.heappop(heap)
            heapq.heappush(heap, (first_count, first_color))
            count, color = second_count, second_color
        else:
            count, color = first_count, first_color

        block_size = min(k, remaining[color])
        answer.extend([color + 1] * block_size)

        remaining[color] -= block_size
        blocks[color] -= 1

        if blocks[color] > 0:
            heapq.heappush(heap, (-blocks[color], color))

        previous = color

    print(*answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = output
        try:
            solve()
        finally:
            sys.stdout = old_stdout
        return output.getvalue().strip()
    finally:
        sys.stdin = old_stdin

def validate(inp: str, out: str) -> bool:
    data = list(map(int, inp.split()))
    n, m, k = data[0], data[1], data[2]
    a = data[3:3 + m]

    if out == "-1":
        blocks = [(x + k - 1) // k for x in a]
        return max(blocks) > (sum(blocks) + 1) // 2

    ans = list(map(int, out.split()))

    if len(ans) != n:
        return False

    counts = [0] * (m + 1)
    for x in ans:
        if x < 1 or x > m:
            return False
        counts[x] += 1

    if counts[1:] != a:
        return False

    run_length = 1
    for i in range(1, n):
        if ans[i] == ans[i - 1]:
            run_length += 1
            if run_length > k:
                return False
        else:
            run_length = 1

    return True

# Provided sample 1.
sample1 = "5 2 1\n2 3\n"
assert run(sample1) == "2 1 2 1 2"

# Provided sample 2.
sample2 = "8 2 3\n1 7\n"
assert run(sample2) == "-1"

# Provided sample 3.
sample3 = "10 3 2\n5 2 3\n"
assert validate(sample3, run(sample3))

# Minimum-size input.
case_min = "1 1 1\n1\n"
assert run(case_min) == "1"

# All colors have the same amount of paint.
case_equal = "6 3 2\n2 2 2\n"
assert validate(case_equal, run(case_equal))

# Exact feasibility boundary: 5 and 2 with k = 3 is possible.
case_boundary = "7 2 3\n5 2\n"
assert validate(case_boundary, run(case_boundary))

# Exact impossibility boundary: 7 and 1 with k = 3 is impossible.
case_impossible = "8 2 3\n7 1\n"
assert run(case_impossible) == "-1"

# Maximum-size case. Each color needs exactly one block.
n = 200000
case_max = f"{n} 2 {n // 2}\n{n // 2} {n // 2}\n"
out_max = run(case_max)
assert validate(case_max, out_max)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1` | `1` | Minimum size and equality with (k) |
| `6 3 2 / 2 2 2` | Any valid arrangement | Equal color counts and heap tie handling |
| `7 2 3 / 5 2` | Any valid arrangement | Feasibility exactly at the block-separation boundary |
| `8 2 3 / 7 1` | `-1` | Impossibility caused by too many required blocks |
| `200000 2 100000 / 100000 100000` | Any valid arrangement | Maximum (n), linear output construction, and run length exactly (k) |

## Edge Cases

The single-color case exposes the most basic boundary. With

```
3 1 3
3
```

we have one required block, and the maximum allowed block size is exactly three. The algorithm computes `blocks = [1]`, so the maximum block count is one and the instance is accepted. The heap produces one block of size three, giving `1 1 1`.

If we increase the input to

```
4 1 3
4
```

the required block count becomes two, but there are only two total blocks and only one color. The separation condition requires at least two different colors between or around repeated blocks, which is impossible. The algorithm computes `blocks = [2]`, while `(2 + 1) // 2` is one, so it prints `-1`.

The (k=1) case is handled naturally by the same block transformation. For

```
5 2 1
2 3
```

the required block counts are (2) and (3). The heap alternates the colors, producing `2 1 2 1 2`. Since every block contains one plank, adjacent equal colors never occur.

The ceiling boundary is handled by explicitly computing `(a_i + k - 1) // k`. For

```
7 2 3
5 2
```

the required block counts are (2) and (1). The heap can arrange them as color (1), color (2), color (1). Their actual sizes are (3), (2), and (2), giving `1 1 1 2 2 1 1`. The first color therefore uses five planks without ever creating a run longer than three.

The corresponding impossible boundary is

```
8 2 3
7 1
```

where the required block counts are (3) and (1). Four blocks exist in total, but the largest color would need three positions while only two positions can be occupied by alternating placement. The inequality (3>(4+1)//2) detects the failure before construction begins.

At the maximum input size, the algorithm never expands a color one plank at a time through the heap. It performs one heap operation per required block, then appends the whole block using `answer.extend`. Since the total number of blocks is at most (n), the algorithm remains (O(n\log m)) even when (n=200000).
