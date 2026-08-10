---
title: "CF 102399F - XOR \u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u0438\u0435"
description: "We maintain a dynamic set (A) of distinct integers, initially empty. After every insertion or deletion, we must determine how small the MEX can become after choosing some XOR mask (x) with (0 le x le k)."
date: "2026-08-10T17:12:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "F"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 762
verified: true
draft: false
---

[CF 102399F - XOR \u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u0438\u0435](https://codeforces.com/problemset/problem/102399/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 12m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a dynamic set (A) of distinct integers, initially empty. After every insertion or deletion, we must determine how small the MEX can become after choosing some XOR mask (x) with (0 \le x \le k).

For a fixed mask (x), the transmitted set is obtained by replacing every (a\in A) with (a\oplus x). Its MEX is the smallest non-negative integer (y) for which (y\notin{a\oplus x\in A}). We need the minimum of this MEX over every allowed (x).

All values fit into 20 bits, so there are only (2^{20}=1,048,576) possible values that can occur in (A). The number of updates is much larger, up to (200,000). This makes a solution that scans the whole value domain after every update impossible. Even (O(2^{20}q)) is about (2.1\cdot10^{11}) operations, far beyond what a two-second contest solution can afford. We need the preprocessing to depend on the fixed (20)-bit universe, while each update should cost at most logarithmic time.

There are several boundary cases that are easy to mishandle. The empty set is one of them. For example,

```
1 0
1 5
```

has output

```
0
```

because the transformed set is still empty, whose MEX is (0). A solution that assumes some transformed value exists would get this wrong.

Another important case is when every value from (0) through (k) is already in (A). For example,

```
3 2
1 0
1 1
1 2
```

has output

```
0
0
1
```

After the third update, every allowed XOR mask is (0,1,2), so none of them can immediately make (0) disappear. The answer becomes (1). A careless implementation that only checks whether (0) itself is absent from (A) misses the effect of XORing.

The upper boundary of the XOR range is also significant. If (k=2^{20}-1), every possible 20-bit value is an allowed mask. Since at most (200,000) values are present while there are (2^{20}) possible values, some value (z) is missing, and we can choose (x=z). Then (z\oplus x=0), so the answer is always (0). Forgetting that (x=k) is allowed creates an off-by-one error here.

Finally, the values in (A) do not have to be near zero. For example,

```
1 2
1 7
```

has output

```
0
```

because (0) is missing and choosing (x=0) already gives MEX (0). A solution that searches only around the currently stored values is unnecessary and can become incorrect.

## Approaches

The direct approach is to try every allowed mask (x). For each (x), we can construct or conceptually inspect the transformed set and find its MEX. If (|A|=n), its MEX is at most (n), so a straightforward implementation can test membership for (0,1,\ldots,n). In the worst case this costs (O((k+1)n)) per update. With (q=200,000), (k) close to (2^{20}), and (n) close to (200,000), the worst case is roughly

[
200,000\cdot1,048,576\cdot200,000
\approx 4.2\cdot10^{16}
]

membership checks. Even replacing the MEX calculation with a faster data structure does not save the approach, because trying all (2^{20}) masks after every update is already too expensive.

The key observation is to stop thinking about the MEX as something that must be calculated separately for every mask.

Fix a mask (x). Its MEX is the smallest (y) such that (y) does not belong to the transformed set. The condition (y\notin{a\oplus x\in A}) is equivalent to

[
y\oplus x\notin A.
]

Let

[
z=y\oplus x.
]

Then (z) is simply some value missing from (A), and

[
y=x\oplus z.
]

Consequently,

\min_{z\notin A}(x\oplus z).
]

Taking the best allowed (x),

\min_{z\notin A}\min_{0\le x\le k}(x\oplus z).
]

This changes the problem completely. For every possible value (z), define the static function

[
g(z)=\min_{0\le x\le k}(x\oplus z).
]

Then the answer is simply

[
\boxed{\min_{z\notin A}g(z)}.
]

The set (A) is dynamic, but (g) depends only on (k). We can preprocess the values (g(z)), count how many currently missing values have each possible (g), and maintain the smallest non-empty bucket.

There is one more useful bound. If (A) currently contains (n) values, every transformed set also contains (n) values, so its MEX is at most (n). Thus the final answer is at most (n\le q). We never need to maintain buckets with (g(z)>q).

The remaining task is to calculate (g(z)) quickly. This can be done in constant time using the binary representations of (z) and (k).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(q^2 2^{20})) in the worst case | (O(q)) | Too slow |
| Optimal | (O(2^{20}+q\log q)) | (O(q)) | Accepted |

## Algorithm Walkthrough

1. Rewrite the desired answer as

[
\min_{z\notin A}g(z),
\qquad
g(z)=\min_{0\le x\le k}(z\oplus x).
]

This works because for a fixed (x), every missing value (z) of (A) corresponds bijectively to the missing value (y=z\oplus x) of (A\oplus x).
2. Observe that (g(z)=0) whenever (z\le k), because we can simply choose (x=z).

Hence all values (0,1,\ldots,k) belong to the same bucket (g=0).
3. For (z>k), compare (z) and (k) from the most significant bit downwards. At their highest differing bit, (z) has (1) and (k) has (0), because (z>k).

An allowed (x) cannot keep that bit equal to (z), so the XOR must contain that bit. After fixing it, the lower bits become the same problem with the lower parts of (z) and (k).
4. Let

[
d=z\oplus k.
]

The bits where (z) and (k) differ and (k) contains (1) are exactly the set bits of

[
d\mathbin{&}k.
]

If the highest such bit is (r), the greedy process stops there, because at that bit (z) has (0) and (k) has (1), so the chosen (x) has already become strictly smaller than (k). All lower bits can then be matched freely.

Therefore, if `bad = d & k`, then

[
g(z)=(d\mathbin{&}\neg k)
\mathbin{&}
\left(-2^{\operatorname{bit_length}(bad)}\right).
]

If `bad` is zero, there is no such stopping bit, so

[
g(z)=d\mathbin{&}\neg k.
]
5. Precompute how many values (z\in[0,2^{20})) have each (g(z)\le q). Values with larger (g(z)) can be ignored because the answer can never exceed (q).

Initially every value (z) is missing from (A), so these counts describe the complete missing set.
6. Maintain a min-heap containing all possible bucket values from (0) through (q). Alongside it, maintain `cnt[v]`, the number of currently missing (z) with (g(z)=v).

When a value is inserted into (A), its bucket loses one missing value. When it is deleted from (A), its bucket gains one missing value.
7. After every update, remove heap entries whose bucket count is zero. The smallest remaining heap value is exactly

[
\min_{z\notin A}g(z),
]

which is the required minimum possible MEX.

The invariant is that `cnt[v]` always equals the number of values currently absent from (A) whose best possible XOR with an allowed mask is exactly (v). The heap represents the candidate bucket indices, while zero-count buckets are discarded lazily. Thus the heap minimum is always the smallest (g(z)) among all missing (z), which by the transformation above is exactly the answer to the original problem.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

LIMIT = 1 << 20

def solve():
    q, k = map(int, input().split())

    cnt = [0] * (q + 1)

    # Every z in [0, k] has g(z) = 0.
    cnt[0] = k + 1

    not_k = ~k

    # For z > k, compute g(z) in O(1).
    for z in range(k + 1, LIMIT):
        d = z ^ k
        bad = d & k

        g = d & not_k

        if bad:
            # Keep only bits strictly above the highest bit of bad.
            g &= -(1 << bad.bit_length())

        if g <= q:
            cnt[g] += 1

    # Initially every bucket is a candidate.
    heap = list(range(q + 1))
    heapq.heapify(heap)

    # True means that this bucket currently has an entry in the heap.
    in_heap = [True] * (q + 1)

    def get_g(z):
        if z <= k:
            return 0

        d = z ^ k
        bad = d & k

        g = d & not_k

        if bad:
            g &= -(1 << bad.bit_length())

        return g

    ans = []

    for _ in range(q):
        typ, z = map(int, input().split())
        g = get_g(z)

        if g <= q:
            if typ == 1:
                # z becomes present, so it is no longer missing.
                cnt[g] -= 1
            else:
                # z becomes missing again.
                if cnt[g] == 0 and not in_heap[g]:
                    heapq.heappush(heap, g)
                    in_heap[g] = True
                cnt[g] += 1

        while cnt[heap[0]] == 0:
            v = heapq.heappop(heap)
            in_heap[v] = False

        ans.append(str(heap[0]))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The preprocessing starts with `cnt[0] = k + 1`, because every value from (0) through (k) has XOR distance zero from the allowed interval. Only values greater than (k) need the bitwise formula.

For such a value, `d = z ^ k` records exactly the positions where the two numbers differ. The expression `d & ~k` keeps the differing positions where (k) has a zero, which are the positions that necessarily contribute to the minimum XOR. If `bad = d & k` is nonzero, its highest set bit identifies the first lower position where (z) has zero and (k) has one. The expression `-(1 << bad.bit_length())` clears every bit below that position.

The update itself needs only one calculation of (g(z)). An insertion decrements its bucket because the value stops being missing. A deletion increments its bucket because the value becomes missing again.

The heap is lazy. A bucket is not immediately removed when its count becomes zero. Instead, the cleanup loop removes zero-count buckets only when they reach the top. The `in_heap` array prevents unnecessary duplicate heap entries when a bucket becomes non-empty again.

All arithmetic is integer-only. Python integers have no overflow issue here, and all relevant values fit comfortably inside the 20-bit domain.

## Worked Examples

For Sample 1, (k=2). The relevant values of (g) are

[
g(0)=g(1)=g(2)=0,
\quad
g(3)=1,
\quad
g(4)=g(5)=g(6)=4,
\quad
g(7)=5.
]

The trace is:

| Step | Operation | Changed value | (g(z)) | Missing count of (g=0) | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | add 1 | 1 | 0 | 2 | 0 |
| 2 | add 0 | 0 | 0 | 1 | 0 |
| 3 | add 2 | 2 | 0 | 0 | 1 |
| 4 | remove 1 | 1 | 0 | 1 | 0 |
| 5 | add 3 | 3 | 1 | 0 | 0 |
| 6 | add 1 | 1 | 0 | 0 | 4 |
| 7 | add 4 | 4 | 4 | 0 | 4 |
| 8 | remove 3 | 3 | 1 | 0 | 1 |

The third operation is the first point where all values (0,1,2) are present. The zero bucket becomes empty, so the heap advances to (g=1), corresponding to the missing value (3). At the sixth operation, value (1) is inserted again, so the missing values no longer contain any element with (g=0) or (g=1). The next available bucket is (g=4).

For Sample 2, (k=1). Here (g(0)=g(1)=0), while (g(2)=g(3)=2).

| Step | Operation | Changed value | (g(z)) | Missing count of (g=0) | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | add 2 | 2 | 2 | 2 | 0 |
| 2 | add 1 | 1 | 0 | 1 | 0 |
| 3 | add 3 | 3 | 2 | 1 | 0 |
| 4 | remove 2 | 2 | 2 | 1 | 0 |
| 5 | add 0 | 0 | 0 | 0 | 2 |

The final operation fills the last missing value from the allowed interval, namely (0). The smallest remaining bucket is then (g=2), produced by the missing value (2), giving the final answer (2).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(2^{20}+q\log q)) | Each possible 20-bit value is processed once during preprocessing, and every update performs one heap operation plus lazy cleanup. |
| Space | (O(q)) | The bucket counts, heap, and auxiliary heap-state array all have size (O(q)). |

The fixed value domain contains only (1,048,576) numbers, so the preprocessing is practical. The dynamic part performs only (O(\log q)) heap work per update, giving roughly (200,000\log_2 200,000) heap-level operations. The algorithm never constructs a trie or segment tree over the full (2^{20}) domain, which keeps the Python memory usage small.

## Test Cases

```python
import io
import sys
import heapq

LIMIT = 1 << 20

def run(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    q = int(next(it))
    k = int(next(it))

    cnt = [0] * (q + 1)
    cnt[0] = k + 1

    not_k = ~k

    for z in range(k + 1, LIMIT):
        d = z ^ k
        bad = d & k
        g = d & not_k

        if bad:
            g &= -(1 << bad.bit_length())

        if g <= q:
            cnt[g] += 1

    heap = list(range(q + 1))
    heapq.heapify(heap)
    in_heap = [True] * (q + 1)

    def get_g(z):
        if z <= k:
            return 0

        d = z ^ k
        bad = d & k
        g = d & not_k

        if bad:
            g &= -(1 << bad.bit_length())

        return g

    out = []

    for _ in range(q):
        typ = int(next(it))
        z = int(next(it))
        g = get_g(z)

        if g <= q:
            if typ == 1:
                cnt[g] -= 1
            else:
                if cnt[g] == 0 and not in_heap[g]:
                    heapq.heappush(heap, g)
                    in_heap[g] = True
                cnt[g] += 1

        while cnt[heap[0]] == 0:
            v = heapq.heappop(heap)
            in_heap[v] = False

        out.append(str(heap[0]))

    return "\n".join(out)

# Provided sample 1
assert run(
    """8 2
1 1
1 0
1 2
2 1
1 3
1 1
1 4
2 3
"""
) == """0
0
1
0
0
4
4
1""", "sample 1"

# Provided sample 2
assert run(
    """5 1
1 2
1 1
1 3
2 2
1 0
"""
) == """0
0
0
0
2""", "sample 2"

# Minimum-size case.
assert run(
    """1 0
1 0
"""
) == """1""", "minimum case"

# Boundary case: every 20-bit value is an allowed XOR mask.
# With only two stored values, many values remain missing, so the answer is 0.
assert run(
    """2 1048575
1 0
1 1048575
"""
) == """0
0""", "maximum k"

# Off-by-one case around k.
assert run(
    """3 2
1 0
1 1
1 2
"""
) == """0
0
1""", "complete allowed interval"

# Repeated insertion and deletion of the same value.
assert run(
    """4 0
1 1
2 1
1 1
2 1
"""
) == """0
0
0
0""", "toggle same value"

# Maximum number of updates, alternating the same value.
# The answer is always 0 because k = 0 and value 0 is never inserted.
q = 200000
parts = [f"{q} 0"]
for i in range(q):
    parts.append("1 1" if i % 2 == 0 else "2 1")

large_input = "\n".join(parts) + "\n"
large_output = run(large_input).split()

assert len(large_output) == q, "maximum q length"
assert all(x == "0" for x in large_output), "maximum q values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0`, add `0` | `1` | Smallest possible input and the first positive answer |
| `k = 1048575`, add two values | `0`, `0` | Maximum mask boundary |
| Add `0,1,2` with `k=2` | `0,0,1` | Exact transition when the whole allowed interval becomes present |
| Toggle `1` repeatedly with `k=0` | `0,0,0,0` | Correct insertion and deletion of the same value |
| (q=200000), alternating `1` and `2` on value `1` | 200000 zeros | Maximum update count and lazy heap behavior |

## Edge Cases

When (A) is empty, every value is missing. In particular, values (0) through (k) are missing, so their bucket is (g=0). The heap immediately reports (0), matching the fact that the MEX of an empty transformed set is (0).

For

```
1 0
1 0
```

the only allowed mask is (x=0), and the transformed set is ({0}), so the answer is (1). The algorithm starts with one missing value in bucket (g=0), then insertion of (0) makes that bucket empty. The next missing value has (g=1), so the heap reports (1).

For

```
3 2
1 0
1 1
1 2
```

the initial zero bucket contains (0,1,2). Each insertion removes one of these values from the missing set. After the third insertion, its count reaches zero. The smallest remaining bucket is (g(3)=1), so the output is (1).

For the maximum mask boundary,

```
2 1048575
1 0
1 1048575
```

the allowed masks cover the entire 20-bit universe. There are still many missing values, and any missing (z) itself is an allowed mask. Choosing (x=z) gives (z\oplus z=0), so (g(z)=0). The bucket (0) therefore remains non-empty and the answer stays (0).

The off-by-one distinction between (x\le k) and (x<k) is handled by the condition `z <= k`. If (z=k), choosing (x=k) gives XOR (0), so (g(k)=0). Excluding (k) would incorrectly move this value into a positive bucket.

The formula for (z>k) also handles cases where the first forced XOR bit is not the only contributing bit. With (k=2) and (z=7), binary representations are (010) and (111). The minimum is (7\oplus2=5), not (4). Here `d = 5`, `bad = 0`, so the formula keeps both contributing bits and obtains (g(7)=5). With (z=5), we have `d = 7` and `bad = 2`, whose highest bit is the stopping bit. The lower contribution is cleared, giving (g(5)=4). These cases are exactly why using only the highest differing bit would be incorrect.
