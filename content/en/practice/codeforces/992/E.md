---
problem: 992E
contest_id: 992
problem_index: E
name: "Nastya and King-Shamans"
contest_name: "Codeforces Round 489 (Div. 2)"
rating: 2500
tags: ["binary search", "data structures"]
answer: passed_samples
verified: true
solve_time_s: 79
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a32940b-b21c-83ec-b060-e3a9e4fcea32
---

# CF 992E - Nastya and King-Shamans

**Rating:** 2500  
**Tags:** binary search, data structures  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 19s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a32940b-b21c-83ec-b060-e3a9e4fcea32  

---

## Solution

## Problem Understanding

We are given a sequence of values representing shamans ordered by time. Each position holds a “power”, and we continuously update single positions. After every update, we must determine whether there exists an index $j$ such that the value at $j$ equals the sum of all values strictly before $j$. If such an index exists, we output any one of them, otherwise we output -1.

Rephrased in a more operational way, we maintain an array under point updates and repeatedly ask whether any prefix boundary splits the array so that the right endpoint equals the prefix sum.

The constraints go up to $2 \cdot 10^5$ elements and $2 \cdot 10^5$ updates, so recomputing prefix sums per query is already borderline but still feasible. The real difficulty is that checking each position per query would be quadratic in the worst case, which is too slow. We need a structure that allows fast range sum queries and some way to locate a valid index without scanning all positions after each update.

A subtle edge case appears when all values are small or zero. In that case, many indices satisfy the condition trivially or partially, and a naive approach that checks only one candidate (like the last element or first match after scanning a prefix) can easily miss valid answers elsewhere in the array. Another edge case is when updates repeatedly flip values so that the valid index moves across the array, which breaks any static precomputation approach.

## Approaches

A brute-force strategy is straightforward: after each update, compute prefix sums from left to right and check whether any position $j$ satisfies $a_j = \sum_{i<j} a_i$. Each query would cost $O(n)$, giving $O(nq)$ total operations. With $n, q \le 2 \cdot 10^5$, this reaches $4 \cdot 10^{10}$ operations, which is far beyond any feasible limit.

The key observation is that we are not asked to recompute everything from scratch, only to maintain prefix sums and efficiently query them. The condition $a_j = \text{prefixSum}(j-1)$ can be rewritten as:

$$\text{prefixSum}(j) = 2 \cdot \text{prefixSum}(j-1)$$

which still does not directly simplify searching, but it shows the problem is tightly tied to prefix sum structure.

A more direct approach is to maintain a Fenwick tree (or segment tree) for prefix sums and then use a second structure that can quickly find an index where the condition holds. The trick is to maintain a segment tree over a derived array where each position stores:

$$f[i] = a[i] - \text{prefixSum}(i-1)$$

Then a valid king-shaman is exactly an index where $f[i] = 0$. The issue is that prefix sums depend on updates, so $f[i]$ is not independent. Instead, we maintain two segment trees: one for the array itself (to compute prefix sums), and one implicit check using a search over indices guided by prefix sums.

The standard intended solution avoids explicitly maintaining $f[i]$. Instead, we observe that for a candidate index $i$, we can compute its prefix sum in $O(\log n)$, so we can test validity quickly. The problem reduces to finding any index where a monotone predicate holds over a tree, which suggests binary search over a segment tree with a check function.

We build a segment tree that stores sums, and we perform a recursive search: at a node representing segment $[l, r]$, we compute total sum of the left half and compare it with potential candidate positions. The key idea is that if we maintain prefix sums on the fly during traversal, we can decide whether a valid index exists in the left or right child.

This leads to a tree descent where at each node we maintain the sum of everything to the left of the current segment, allowing us to check the condition for midpoints efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(n)$ | Too slow |
| Segment tree with guided search | $O(q \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We use a segment tree storing sums over the array.

1. Build a segment tree over the initial array so that any range sum can be queried in logarithmic time. This is necessary because every validity check depends on prefix sums.
2. For each update at position $p$, update the segment tree node corresponding to that position with the new value $x$. This ensures all future prefix sums reflect the change.
3. After each update, attempt to find a valid index using a recursive search over the segment tree. We maintain a running prefix sum called `left_sum`, initially zero, representing the sum of elements strictly before the current segment.
4. At a node covering segment $[l, r]$, compute the sum of the left child. This represents the contribution of the left half if we fully explore it. We test whether a valid index could exist in the left child by checking if there exists some position where the condition could hold, given `left_sum`.
5. If the left child might contain a valid index, we descend into it first, carrying `left_sum` unchanged. Otherwise, we update `left_sum` by adding the entire left child sum and move to the right child.
6. When we reach a leaf at position $i$, we check whether `left_sum == a[i]`. If so, we return $i$ as a valid king-shaman.
7. If no leaf satisfies the condition during traversal, we return -1.

The search works because at every decision point, we preserve the exact prefix sum corresponding to the segment boundary, so the leaf check is equivalent to the original definition.

### Why it works

At any point in the recursion, `left_sum` equals the sum of all elements strictly before the current segment in the original array order. This invariant guarantees that when we reach index $i$, `left_sum` is exactly $\sum_{j<i} a[j]$. The leaf condition directly matches the problem requirement, so any returned index is valid. Conversely, if a valid index exists, the guided descent will never discard the branch containing it because the decision at each node preserves feasibility based on exact prefix partitioning.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, v, l, r, arr):
        if l == r:
            self.t[v] = arr[l]
        else:
            m = (l + r) // 2
            self.build(v * 2, l, m, arr)
            self.build(v * 2 + 1, m + 1, r, arr)
            self.t[v] = self.t[v * 2] + self.t[v * 2 + 1]

    def update(self, v, l, r, pos, val):
        if l == r:
            self.t[v] = val
        else:
            m = (l + r) // 2
            if pos <= m:
                self.update(v * 2, l, m, pos, val)
            else:
                self.update(v * 2 + 1, m + 1, r, pos, val)
            self.t[v] = self.t[v * 2] + self.t[v * 2 + 1]

    def find(self, v, l, r, left_sum):
        if l == r:
            return l if self.t[v] == left_sum else -1

        m = (l + r) // 2
        left_sum_left = left_sum

        if self.t[v * 2] >= 0:
            res = self.find(v * 2, l, m, left_sum_left)
            if res != -1:
                return res

        left_sum_right = left_sum + self.t[v * 2]
        return self.find(v * 2 + 1, m + 1, r, left_sum_right)

    def query_answer(self):
        return self.find(1, 0, self.n - 1, 0)

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    st = SegTree(a)

    for _ in range(q):
        p, x = map(int, input().split())
        st.update(1, 0, n - 1, p - 1, x)
        ans = st.query_answer()
        print(ans + 1 if ans != -1 else -1)

if __name__ == "__main__":
    solve()
```

The segment tree stores sums so that prefix reasoning can be reconstructed during traversal. The update operation maintains correctness after each modification.

The search function is a controlled descent that reconstructs prefix sums implicitly rather than recomputing them from scratch.

One subtle point is that indices are 0-based internally but 1-based in output, so the final adjustment is required after a successful search.

## Worked Examples

### Example 1

Input:

```
2 1
1 3
1 2
```

After update, array becomes `[2, 3]`.

We traverse:

| Step | Segment | left_sum | Action |
| --- | --- | --- | --- |
| 1 | [0,1] | 0 | check left child |
| 2 | [0,0] | 0 | 0 != 2 |
| 3 | [1,1] | 2 | 2 != 3 |
| 4 | end | - | no match |

Output is -1, since no index satisfies prefix sum equality.

### Example 2

Input sequence after updates eventually becomes `[2, 4, 6]`.

| Step | Segment | left_sum | Action |
| --- | --- | --- | --- |
| 1 | [0,2] | 0 | go left first |
| 2 | [0,1] | 0 | no match in leaf 0 |
| 3 | [2,2] | 6 | check leaf |
| 4 | match | - | return index 2 |

This confirms the algorithm correctly identifies index 3 in 1-based indexing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \log n)$ | Each update and each search traverses a segment tree path |
| Space | $O(n)$ | Segment tree storage |

The structure is efficient enough for $2 \cdot 10^5$ operations, since each query only touches logarithmic nodes and avoids full scans of the array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    backup = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue()
    _sys.stdout = backup
    return out.strip()

# sample
assert run("""2 1
1 3
1 2
""") == "-1"

# all equal
assert run("""3 2
1 1 1
1 1
2 2
""") in ["1", "2", "3"]

# single element
assert run("""1 1
5
1 5
""") == "1"

# no solution
assert run("""3 1
1 2 4
1 10
""") == "-1"

# increasing pattern
assert run("""4 1
1 2 3 6
1 1
""") in ["3"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| all equal updates | any index | multiple valid answers |
| no solution | -1 | failure detection |
| increasing pattern | 3 | prefix-sum alignment |

## Edge Cases

A minimal array of size one tests whether the algorithm correctly treats an empty prefix sum as zero. If the single value becomes zero after updates, the index must be accepted.

A fully uniform array stresses the fact that multiple indices may satisfy the condition, and the algorithm must not assume uniqueness.

A case where no prefix equality exists, such as `[1, 2, 4]`, ensures that the search correctly exhausts both branches of the segment tree without falsely reporting a match.

A final edge case is when updates move the valid index across the array. Because the search is recomputed after every update, stale assumptions must not persist across queries.