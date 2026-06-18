---
problem: 1323B
contest_id: 1323
problem_index: B
name: "Count Subrectangles"
contest_name: "Codeforces Round 626 (Div. 2, based on Moscow Open Olympiad in Informatics)"
rating: 1500
tags: ["binary search", "greedy", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 210
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2ded2f-7b30-83ec-ae4c-241598b69c4b
---

# CF 1323B - Count Subrectangles

**Rating:** 1500  
**Tags:** binary search, greedy, implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 30s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2ded2f-7b30-83ec-ae4c-241598b69c4b  

---

## Solution

## Problem Understanding

The matrix in this problem is not arbitrary. Every cell is determined by a simple outer-product rule: row i is either fully “active” or fully “inactive” depending on whether $a_i$ is 1 or 0, and column j is similarly controlled by $b_j$. A cell becomes 1 only when both its row and column are active.

So the grid is essentially a binary mask where all rows with $a_i = 0$ are completely zero, and all rows with $a_i = 1$ replicate the pattern of array $b$. This makes every row either identical to $b$ or entirely zero.

The task is to count how many axis-aligned subrectangles in this grid have area exactly $k$ and consist only of ones. A valid subrectangle must lie entirely inside rows where $a_i = 1$, and its column segment must lie entirely inside a contiguous region of ones in $b$.

The constraints force a linear or near-linear solution. Both $n$ and $m$ can reach 40,000, so any approach that tries to enumerate all rectangles or all row-column pairs is immediately infeasible. Even $O(nm)$ is far beyond limits, and even $O(n \sqrt{m})$ style approaches are risky unless carefully optimized. The structure of the matrix must be exploited.

A key edge case arises when either array is all zeros. In that case the matrix is entirely zero and the answer must be zero regardless of $k$. A naive approach that does not filter zero rows or zero columns early may still attempt to count subarrays and produce nonzero results.

Another subtle case occurs when $k = 1$. Then every individual cell containing a 1 is a valid subrectangle. If one incorrectly tries to enforce contiguous blocks of both dimensions without simplifying the structure, it is easy to overcomplicate or miscount.

Finally, when $k$ factors in many ways, a naive rectangle enumeration might double count factorizations of $k$ as height times width, which is the core structure we ultimately rely on.

## Approaches

A brute-force interpretation is straightforward: enumerate every possible subrectangle, compute its area, and check whether all cells are ones. To verify the all-ones condition, we would need to scan every cell in the rectangle. There are $O(n^2 m^2)$ rectangles, and each check costs up to $O(nm)$ in the worst case, which is completely infeasible.

Even if we optimize slightly by noticing that the matrix is structured, we still face too many rectangle candidates unless we use the product nature of $c_{i,j} = a_i b_j$.

The key observation is that a subrectangle is valid if and only if all chosen rows have $a_i = 1$ and the chosen columns lie entirely inside a segment of consecutive ones in $b$. Once we fix a block of consecutive ones in $b$, every column in that block behaves identically across rows. The problem reduces to combining two independent 1D structures: runs of ones in $a$ and runs of ones in $b$.

We first compress both arrays into consecutive segments of ones. For each segment length, we count how many subsegments of a given length exist. Then we use the fact that a rectangle of area $k$ must satisfy $height × width = k$, and both height and width must correspond to valid all-one segments in $a$ and $b$ respectively. We enumerate all factor pairs of $k$ and accumulate contributions.

This transforms the problem into counting subarrays of ones of certain lengths and matching them via divisors of $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 m^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n + m + \sqrt{k})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Scan array $a$ and compute, for every possible length $x$, how many subsegments of consecutive ones of length at least $x$ exist. This is done by identifying each run of ones and counting how many subsegments of a given length it contributes. The same is done for array $b$. This step is essential because only these runs can form valid rectangle dimensions.
2. For each run of ones of length $L$ in an array, it contributes $(L - x + 1)$ subsegments of length $x$, for every $x \le L$. We store this implicitly by recording run lengths rather than expanding explicitly.
3. Iterate over all divisors $h$ of $k$. For each divisor pair $(h, w)$ where $h × w = k$, interpret $h$ as a potential height (rows) and $w$ as a potential width (columns).
4. For each valid $h$, compute how many subsegments of ones in array $a$ have length at least $h$. This gives the number of possible vertical placements.
5. For the corresponding $w$, compute how many subsegments of ones in array $b$ have length at least $w$. This gives the number of possible horizontal placements.
6. Multiply these two counts and add to the answer. Each combination of a valid vertical segment and horizontal segment forms a unique all-ones rectangle of area $k$.

### Why it works

The correctness rests on the separability of the matrix structure. Every valid rectangle must lie entirely inside a run of ones in $a$ and a run of ones in $b$. Within such a run, every cell is guaranteed to be 1 due to the multiplicative construction. Conversely, any choice of a row segment of length $h$ inside a run of ones in $a$ and a column segment of length $w$ inside a run of ones in $b$ produces a valid rectangle of ones. Since area is exactly $k$, only factor pairs of $k$ matter, and each valid rectangle corresponds uniquely to one such pair. No overcounting occurs because each rectangle is uniquely determined by its row interval and column interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_segments(arr):
    n = len(arr)
    res = {}
    i = 0
    while i < n:
        if arr[i] == 0:
            i += 1
            continue
        j = i
        while j < n and arr[j] == 1:
            j += 1
        length = j - i
        for x in range(1, length + 1):
            res[x] = res.get(x, 0) + (length - x + 1)
        i = j
    return res

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    cntA = count_segments(a)
    cntB = count_segments(b)

    ans = 0
    h = 1
    while h * h <= k:
        if k % h == 0:
            w = k // h
            if h in cntA and w in cntB:
                ans += cntA[h] * cntB[w]
            if h != w and w in cntA and h in cntB:
                ans += cntA[w] * cntB[h]
        h += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first compresses each array into contributions of all possible segment lengths. The function `count_segments` expands each run of ones into a frequency table where key `x` represents how many subsegments of ones of length exactly `x` exist.

Then the main solver iterates over divisor pairs of `k`. Each pair defines a rectangle shape. We check whether both arrays can support those dimensions and multiply the number of placements.

A subtle point is handling symmetry when $h × w = k$. We must avoid double counting when $h = w$, so we explicitly check the diagonal case. Another subtle point is that `cntA[x]` represents counts of segments of length exactly $x$, which already encodes how many valid starting positions exist.

## Worked Examples

### Example 1

Input:

```
3 3 2
1 0 1
1 1 1
```

Array analysis:

| Step | A segments | B segments | k factor |
| --- | --- | --- | --- |
| 1 | runs: [1], [1] | run: [3] | (1,2), (2,1) |
| 2 | cntA[1]=2 | cntB[1]=3, cntB[2]=2 | evaluate pairs |

For (h=1, w=2), we take 1-row strips in A and 2-column strips in B. For (h=2, w=1), we take 2-row segments in A (none exist, so zero) and 1-column segments in B.

The only contributing configuration is height 1 with width 2, producing 4 valid rectangles.

This shows how the answer depends on counting placements rather than raw geometry.

### Example 2 (all ones)

Input:

```
2 3 2
1 1
1 1 1
```

| Step | A runs | B runs | contribution |
| --- | --- | --- | --- |
| (1,2) | 2 rows | 2 subarrays of length 2 | 2×2 |
| (2,1) | 1 subarray of length 2 | 3 subarrays of length 1 | 1×3 |

Total becomes 4 + 3 = 7 valid rectangles.

This confirms that multiple factor pairs contribute independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m + \sqrt{k})$ | One linear scan per array plus divisor enumeration |
| Space | $O(n + m)$ | Stores segment contributions up to run lengths |

The algorithm fits easily within constraints because both arrays are processed in linear time, and $k$ up to $n \cdot m$ still yields at most about 200 divisors in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def count_segments(arr):
        n = len(arr)
        res = {}
        i = 0
        while i < n:
            if arr[i] == 0:
                i += 1
                continue
            j = i
            while j < n and arr[j] == 1:
                j += 1
            length = j - i
            for x in range(1, length + 1):
                res[x] = res.get(x, 0) + (length - x + 1)
            i = j
        return res

    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    cntA = count_segments(a)
    cntB = count_segments(b)

    ans = 0
    h = 1
    while h * h <= k:
        if k % h == 0:
            w = k // h
            if h in cntA and w in cntB:
                ans += cntA[h] * cntB[w]
            if h != w and w in cntA and h in cntB:
                ans += cntA[w] * cntB[h]
        h += 1

    return str(ans)

# provided sample
assert run("3 3 2\n1 0 1\n1 1 1\n") == "4"

# all zeros
assert run("3 3 2\n0 0 0\n0 0 0\n") == "0"

# single row
assert run("1 5 2\n1\n1 1 1 1 1\n") == "4"

# single column
assert run("5 1 2\n1 1 1 1 1\n1\n") == "4"

# all ones square
assert run("2 3 2\n1 1\n1 1 1\n") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | 0 | early elimination correctness |
| single row | 4 | horizontal-only counting |
| single column | 4 | vertical-only counting |
| full ones | 7 | combined factor pair handling |

## Edge Cases

For an all-zero array, the segment table is empty and no divisor pair contributes. For example:

```
3 3 2
0 0 0
0 0 0
```

Both `cntA` and `cntB` are empty, so every lookup fails and the answer remains zero. The algorithm correctly avoids counting any rectangles.

For a single long run:

```
1 5 3
1
1 1 1 1 1
```

Here `cntA[1]=1`, `cntB[3]=3`, `cntB[1]=5`, etc. Only factor pairs of 3 contribute, specifically (1,3) and (3,1). The algorithm multiplies valid placements correctly without needing any 2D enumeration.

For uneven factor structure like k = 6, both (2,3) and (3,2) contribute independently, and symmetry handling ensures no duplication when h = w.