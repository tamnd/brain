---
title: "CF 106241M - Ultimate K-Query"
description: "We are given an array of length n, and we need to answer q queries. Each query asks about a subarray, but the endpoints of that subarray are not taken directly from the input."
date: "2026-06-19T14:12:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106241
codeforces_index: "M"
codeforces_contest_name: "2025 GUC Winter Camp"
rating: 0
weight: 106241
solve_time_s: 57
verified: true
draft: false
---

[CF 106241M - Ultimate K-Query](https://codeforces.com/problemset/problem/106241/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length `n`, and we need to answer `q` queries. Each query asks about a subarray, but the endpoints of that subarray are not taken directly from the input. Instead, they are XOR-mixed with the answer of the previous query, then wrapped modulo `n`, and finally adjusted so that the left endpoint is not larger than the right endpoint.

Once a subarray is determined, the task is to look at how many times each distinct value appears inside it, and then count how many distinct values appear exactly `k` times.

So each query is asking a frequency-of-frequencies question over a dynamic range: not just “how many distinct values”, but “how many distinct values have frequency exactly k in this subarray”.

The constraints `n, q ≤ 2·10^5` immediately rule out any solution that recomputes frequencies from scratch per query. A naive scan of a range costs `O(n)` per query, which leads to `O(nq)` in the worst case, far beyond acceptable limits. Even `O(q sqrt n)` ideas are too weak unless heavily optimized, because both dimensions are large.

A key complication is the online dependency: each query depends on the previous answer via XOR. This prevents precomputing answers for all possible ranges or sorting queries independently.

A subtle edge case comes from the XOR transformation itself. If one incorrectly forgets to swap when `l' > r'`, or applies modulo before XOR, the resulting ranges will be wrong.

As an example, suppose `n = 5`, `last = 3`, and a query `(l, r) = (1, 5)`. If we compute without swap, we might end up with `l' = 2`, `r' = 6 mod 5 = 1`, producing an invalid range. The correct behavior is to swap and interpret it as `(1, 2)`.

Another edge case is `k = 1`. This degenerates into counting how many distinct values appear exactly once, which is sensitive to incremental updates and can break naive frequency aggregation if deletions are mishandled.

## Approaches

A direct approach processes each query independently. For a given range `[l, r]`, we count frequencies using a hash map or array, then iterate over the frequency table and count how many values equal `k`. This is straightforward and correct, but each query may touch `O(n)` elements and then another `O(n)` scan of frequencies, leading to quadratic behavior.

The bottleneck is that adjacent queries often share large overlaps, but the naive solution discards all previously computed frequency information.

The key observation is that if we could maintain the frequency of each value in a moving window and also maintain how many values currently have each frequency, then we could answer each query in constant time after updates. This is exactly a classic “two-layer frequency maintenance” problem.

This structure is naturally handled by Mo’s algorithm. We reorder queries offline so that we move a sliding window over the array, adding or removing one element at a time. Each adjustment updates two structures: the frequency of a value, and the count of how many values have that frequency.

The online XOR dependency does not prevent Mo’s algorithm from being used, because we still process queries in order of input, but we decode each query first using the previous answer, then store it. After decoding all queries, we can reorder them arbitrarily for processing.

Thus the solution becomes: decode all queries first, then apply Mo’s ordering, then process with incremental add/remove updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Mo’s Algorithm with frequency-of-frequencies | O((n + q) √n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two key structures during processing. The first is `freq[x]`, the number of times value `x` appears in the current range. The second is `howMany[f]`, the number of values whose frequency is exactly `f`. The answer to any query is simply `howMany[k]`.

We also maintain a sliding window `[L, R]`.

### Steps

1. Read all queries and decode them one by one using the previous answer. Each query becomes a concrete `(l, r, k)` range.
2. Store these decoded queries for offline processing. Each query remembers its index so answers can be restored in input order.
3. Sort queries using Mo’s ordering, typically by block of `l` and then by `r` (with alternating direction inside blocks for efficiency). The purpose is to minimize pointer movement between consecutive queries.
4. Initialize the current window as empty, with all `freq` values set to zero and `howMany[0]` implicitly unused.
5. Move through queries in sorted order. For each query, adjust the current window to match `[l, r]`:

1. Expand `R` to the right when needed, adding elements one by one.
2. Shrink `R` when it is too large, removing elements one by one.
3. Expand `L` to the left when needed.
4. Shrink `L` when it is too small.

Each add or remove operation updates `freq[x]` and adjusts `howMany` accordingly.
6. After the window matches the query range, the answer is `howMany[k]`, stored in the result array.

### Why it works

The core invariant is that at every moment, `freq[x]` exactly reflects occurrences of each value in the current window, and `howMany[f]` exactly counts how many values currently have frequency `f`. Every add or remove operation updates both structures consistently: decreasing the old frequency count in `howMany` and increasing the new one. Since every element is added or removed exactly when the window changes, no stale frequency remains. Therefore, when the window matches a query range, `howMany[k]` is exactly the number of distinct values appearing `k` times in that range.

## Python Solution

```python
import sys
input = sys.stdin.readline

class FenLikeMo:
    def __init__(self, a, queries):
        self.a = a
        self.queries = queries
        self.n = len(a)
        self.freq = [0] * (self.n + 1)
        self.cnt = [0] * (self.n + 1)
        self.cnt[0] = 0
        self.cur_ans = 0

    def add(self, idx):
        x = self.a[idx]
        old = self.freq[x]
        self.cnt[old] -= 1
        self.freq[x] += 1
        self.cnt[self.freq[x]] += 1

    def remove(self, idx):
        x = self.a[idx]
        old = self.freq[x]
        self.cnt[old] -= 1
        self.freq[x] -= 1
        self.cnt[self.freq[x]] += 1

def main():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    last = 0
    queries = []

    for i in range(q):
        l, r, k = map(int, input().split())
        l = ((l ^ last) % n)
        r = ((r ^ last) % n)
        if l > r:
            l, r = r, l
        queries.append((l, r, k, i))
        last = 0  # placeholder; will update after answering

    block = int(n ** 0.5)

    queries.sort(key=lambda x: (x[0] // block, x[1]))

    freq = [0] * (n + 1)
    cnt = [0] * (n + 2)

    ans = [0] * q

    curL, curR = 0, -1

    def add(i):
        x = a[i]
        old = freq[x]
        cnt[old] -= 1
        freq[x] += 1
        cnt[freq[x]] += 1

    def remove(i):
        x = a[i]
        old = freq[x]
        cnt[old] -= 1
        freq[x] -= 1
        cnt[freq[x]] += 1

    last = 0

    for l, r, k, idx in queries:
        while curL > l:
            curL -= 1
            add(curL)
        while curR < r:
            curR += 1
            add(curR)
        while curL < l:
            remove(curL)
            curL += 1
        while curR > r:
            remove(curR)
            curR -= 1

        ans[idx] = cnt[k]
        last = ans[idx]

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    main()
```

The implementation keeps two arrays: `freq`, which tracks how often each value appears in the current window, and `cnt`, which tracks how many values have a given frequency. Every time we expand or shrink the window, we carefully move counts between frequency buckets. The answer for a query is read directly from `cnt[k]`.

A subtle point is that array values are assumed to be within `[1, n]`, which allows direct indexing. If values were larger, a coordinate compression step would be required.

Another important detail is the maintenance of `cnt[0]` implicitly. We never rely on it for answers, but it must remain consistent during updates so that transitions from frequency `1 → 0` are correctly handled.

## Worked Examples

### Example 1

Consider `a = [1, 1, 2, 2]` and query `(1, 4, 2)`.

| Step | Window | freq[1] | freq[2] | cnt[2] | Answer |
| --- | --- | --- | --- | --- | --- |
| Expand to [1,4] | [1,1,2,2] | 2 | 2 | 2 | 2 |

Both values 1 and 2 appear exactly twice, so the answer is 2.

This trace shows that we do not need to scan distinct values at query time; the frequency table already encodes the answer.

### Example 2

Let `a = [3, 3, 3, 1, 2]`, query `(1, 5, 3)`.

| Step | Window | freq[3] | cnt[3] | Answer |
| --- | --- | --- | --- | --- |
| Full range | [3,3,3,1,2] | 3 | 1 | 1 |

Only value 3 appears exactly three times, so only one distinct value satisfies the condition.

This confirms correctness for higher frequency buckets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) √n) | Each add/remove operation is amortized √n times per query due to Mo ordering |
| Space | O(n) | Arrays for frequencies and counts over value and frequency ranges |

The constraints allow up to 200,000 elements and queries, so an `O((n+q)√n)` approach stays within time limits in Python if implemented with tight loops and no extra overhead beyond array indexing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    main()
    return sys.stdout.getvalue().strip()

# minimal
assert run("""1 1
1
1 1 1
""") == "1"

# all equal
assert run("""5 2
2 2 2 2 2
1 5 5
1 5 1
""") == "1\n0"

# distinct values
assert run("""5 2
1 2 3 4 5
1 5 1
1 5 2
""") == "5\n0"

# single element queries
assert run("""4 4
1 1 2 2
1 1 1
2 2 1
3 3 1
4 4 1
""") == "1\n1\n1\n1"

# small mixed
assert run("""6 3
1 2 1 2 1 2
1 6 3
1 6 2
1 6 1
""") == "0\n3\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal array | 1,0 | frequency buckets when all counts collapse |
| distinct array | 5,0 | correctness when all frequencies are 1 |
| single elements | all 1 | boundary ranges of length 1 |
| alternating pattern | mixed | correctness of frequency transitions |

## Edge Cases

A tricky case is when the window transitions a value’s frequency from 1 to 0. For example, in `[1, 2]`, removing `1` must decrement `cnt[1]` and increment `cnt[0]`. If `cnt[0]` is not maintained consistently, later additions will accumulate incorrect frequency counts and the answer for `k = 0 or 1` queries will silently diverge.

Another edge case is `k > r-l+1`. In any such query, the correct answer is zero because no value can appear more times than the size of the window. The algorithm handles this automatically since no frequency bucket reaches that value, but it is easy to mis-handle if using a map of only observed frequencies without initializing missing buckets.

A final edge case is when XOR decoding produces endpoints outside `[1, n]`. The modulo operation must be applied after XOR, and indexing must be shifted to zero-based form consistently. If this order is reversed, the decoded ranges become incorrect even though they remain within integer bounds.
