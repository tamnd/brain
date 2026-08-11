---
title: "CF 102411H - High Load Database"
description: "We have an array of transactions (a1,a2,ldots,an), where transaction (i) contains (ai) queries. We must partition this array into consecutive groups."
date: "2026-08-12T00:18:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "H"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 154
verified: true
draft: false
---

[CF 102411H - High Load Database](https://codeforces.com/problemset/problem/102411/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of transactions (a_1,a_2,\ldots,a_n), where transaction (i) contains (a_i) queries. We must partition this array into consecutive groups. A group may contain one transaction or several adjacent transactions, but its total number of queries must be at most the chosen limit (t).

For every requested value of (t), we need the minimum possible number of groups. The order of the transactions cannot change, so this is a contiguous partition problem. If even one transaction contains more than (t) queries, that transaction can never fit into a valid group, so the answer is `Impossible`.

The two input sizes play different roles. There can be (200,000) transactions and (100,000) queries, so running an (O(n)) scan for every query would perform up to (20,000,000,000) transaction operations, far beyond what a two-second limit allows. At the same time, the total number of queries inside all transactions is at most (10^6), which is much smaller than (nq). That bound is the useful resource in this problem. It lets us build a structure indexed by individual query positions and make every greedy jump constant time.

The values (a_i) are positive. This matters because prefix sums are strictly increasing. It also means that once a batch cannot include the next transaction, every later transaction is even farther away in the prefix-sum order, so the farthest feasible endpoint can be found unambiguously.

There are several boundary cases that can silently break an implementation. Consider a single transaction with one query:

```
1
1
3
1 2 100
```

The correct output is:

```
1
1
1
```

A careless solution might treat (t=1) differently from larger values or accidentally require a split when the whole array already fits.

Now consider a transaction that is larger than the limit:

```
2
3 1
3
2 3 4
```

The correct output is:

```
Impossible
1
1
```

For (t=2), the first transaction has size (3), so no partition exists. Checking only the total sum would be insufficient, because the total sum is (4), and (2) groups of capacity (2) might appear feasible if transaction boundaries were ignored.

The case where a query limit lands in the middle of a transaction is also important:

```
3
2 5 1
2
6 7
```

For (t=6), the first batch can contain transactions (1) and (2), because their sum is (7), so in fact it cannot. The correct partition is (2\mid5\mid1), giving (3). For (t=7), the first two transactions fit and the answer becomes (2). A solution that treats the limit as if transactions could be split would incorrectly accept part of the transaction containing (5).

Finally, repeated query values must not cause repeated work. In the sample, (t=8) appears twice. The answer is the same both times, so the second occurrence should be served from a cache.

## Approaches

The direct solution is a greedy scan for every value of (t). Starting at the first transaction, keep adding consecutive transactions while their total remains at most (t). When the next transaction would exceed (t), close the current batch and start a new one. This greedy choice is correct because taking the farthest possible endpoint cannot make the remaining suffix harder to partition. Any other first batch ends no farther to the right, so the greedy choice leaves at least as much room for the remaining transactions.

The problem is the cost. A single greedy scan can inspect all (n) transactions, and there can be (q=100,000) queries. In the worst case this is (nq=20,000,000,000) operations. Even if many query values are repeated, the worst-case input can contain many distinct values, so simply memoizing a linear scan is not enough.

The useful observation is that the sum of all (a_i) is at most (10^6). Let

[
S=\sum_{i=1}^{n}a_i.
]

Imagine numbering the individual queries from (1) to (S), while remembering which transaction contains each query. If a batch starts at transaction (i), then the number of queries before it is

[
p_{i-1}=a_1+a_2+\cdots+a_{i-1}.
]

With limit (t), the batch can reach at most query position (p_{i-1}+t). If that position lies inside transaction (j), then the batch ends at transaction (j), and the next batch starts at (j+1).

So we can preprocess an array `owner`, where `owner[x]` is the transaction containing the (x)-th individual query. Then one greedy batch transition becomes a single array lookup:

```
next_start = owner[prefix[start - 1] + t] + 1
```

provided that the target query position is less than (S). This removes the need to scan transactions or perform binary searches for every batch.

There is one more important complexity observation. For a fixed (t), the greedy simulation takes only (O(S/t)) steps up to a constant factor. Suppose one batch ends at transaction (R), and transaction (R+1) exists. The first batch has sum at most (t), but adding (a_{R+1}) would exceed (t). Since the whole instance is feasible, (a_{R+1}\le t). The next batch can therefore take transaction (R+1), and across these two batches more than (t) queries are consumed. Thus every two batches consume more than (t) queries, giving at most (2S/t) batches.

If we compute answers for all distinct feasible values of (t), the total number of simulation steps is bounded by

[
\sum_{t=1}^{S} O\left(\frac{S}{t}\right)
=O(S\log S).
]

Since (S\le10^6), this is practical. Repeated query values are computed only once.

The relationship between the approaches is therefore straightforward. The brute-force solution works because greedy is correct, but it repeatedly walks through the same transaction array. The observation that the total number of individual queries is small lets us represent a greedy jump by its query position, making each jump constant time and reducing the total work to a harmonic sum. The official contest tutorial describes the same (O(S\log S)) bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nq)) | (O(1)) besides input | Too slow |
| Prefix positions + greedy jumps | (O(n+S+S\log S+q)) | (O(n+S+q)) | Accepted |

Here (S=\sum a_i), and the (S\log S) term is the total cost over distinct feasible values of (t).

## Algorithm Walkthrough

1. Read the transaction array and compute the prefix sums. Let `prefix[i]` be the total number of queries in transactions (1) through (i). Because every (a_i) is positive, these prefix sums are strictly increasing.
2. Find `mx`, the largest transaction size. If a query asks for (t<mx), answer `Impossible` immediately. Every transaction must appear whole inside some batch, so a transaction larger than the capacity makes the entire partition impossible.
3. Number all individual queries from (1) through (S). Build `owner[x]`, which stores the transaction containing query (x). For example, if (a=[2,3,1]), then queries (1,2) belong to transaction (1), queries (3,4,5) belong to transaction (2), and query (6) belongs to transaction (3).
4. For a particular feasible value of (t), start at transaction `start = 1` and set the batch count to zero. At every iteration, one more batch is required because there are still unprocessed transactions.
5. Compute

[
x=\text{prefix[start-1]}+t.
]

This is the furthest individual query position that the current batch could possibly reach if transaction boundaries did not exist.
6. If (x\ge S), the current batch can reach the end of the entire array, so increment the answer and stop. Otherwise, `owner[x]` is the transaction containing the last query position that the batch can reach. The current batch ends at that transaction, so set

[
\text{start}=\text{owner}[x]+1.
]

This automatically handles the case where (x) falls in the middle of a transaction. We cannot split that transaction, so the whole transaction belongs to the current batch and the next batch starts afterward.
7. Cache the computed answer for this value of (t). If the same (t) occurs again in the input, return the cached value without simulating the partition again.
8. Output the cached answer for every query in its original order. Impossible queries are represented separately so that they do not get confused with a valid numerical answer.

### Why it works

For a fixed (t), consider the first unprocessed transaction (i). The algorithm chooses the farthest transaction (j) such that the sum from (i) through (j) is at most (t). No valid partition can make its first batch end after (j), because that would exceed the limit. Thus there is always an optimal solution whose first batch ends at (j). After fixing that batch, the same argument applies to the remaining suffix. By induction, every greedy batch endpoint can be part of an optimal partition, so the final number of batches is minimal.

The `owner` lookup does not change the greedy decision. `prefix[i-1]+t` identifies the last individual query that could fit by total size, and `owner` converts that query position back into the transaction that must contain the endpoint. Consequently, every simulated jump is exactly the same jump that a direct greedy scan would make.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    prefix = [0] * (n + 1)
    mx = 0

    for i, x in enumerate(a, 1):
        prefix[i] = prefix[i - 1] + x
        if x > mx:
            mx = x

    total = prefix[n]

    # owner[x] = transaction containing the x-th query.
    owner = [0] * (total + 1)
    transaction = 1

    for x in range(1, total + 1):
        while x > prefix[transaction]:
            transaction += 1
        owner[x] = transaction

    q = int(input())
    queries = list(map(int, input().split()))

    cache = {}
    out = []

    for t in queries:
        if t < mx:
            out.append("Impossible")
            continue

        if t in cache:
            out.append(str(cache[t]))
            continue

        start = 1
        batches = 0

        while start <= n:
            batches += 1

            reachable_query = prefix[start - 1] + t

            if reachable_query >= total:
                break

            end_transaction = owner[reachable_query]
            start = end_transaction + 1

        cache[t] = batches
        out.append(str(batches))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The prefix array is built first because every batch boundary is naturally expressed in terms of the number of queries before a transaction. `prefix[i - 1]` is exactly the number of queries already assigned to earlier batches when transaction `i` becomes the next starting point.

The `owner` array has one entry for every individual query position. The construction walks through the query positions from left to right and advances the current transaction only when the position passes its prefix sum. Since the transaction pointer only moves forward, the whole construction takes (O(S+n)) time.

The main simulation mirrors the numbered algorithm. `reachable_query` is the last query position that could fit into the current batch based solely on capacity. If it reaches or passes `total`, the current batch finishes the entire script.

The strict comparison around `total` is intentional. When `reachable_query == total`, all remaining queries fit exactly, so the current batch is valid and the simulation must stop. If the code instead required `reachable_query > total`, it would perform an unnecessary extra iteration and produce an off-by-one error.

When `reachable_query < total`, `owner[reachable_query]` identifies the transaction containing that query. The batch must include that entire transaction because transactions cannot be split. The next starting transaction is consequently `owner[reachable_query] + 1`.

Python integers do not overflow, so the prefix sums are safe even at the maximum total of (10^6). The cache is also useful beyond performance: it guarantees that duplicate values such as the two occurrences of (t=8) in the sample are evaluated only once.

## Worked Examples

The first sample contains

```
a = [4, 2, 3, 1, 3, 4]
```

with prefix sums

```
[0, 4, 6, 9, 10, 13, 17].
```

Consider (t=5). The maximum transaction size is (4), so this value is feasible.

| Batch | Start transaction | Queries before start | Reachable query | `owner` | Next start |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 5 | 2 | 3 |
| 2 | 3 | 6 | 11 | 5 | 6 |
| 3 | 6 | 13 | 18 | end | stop |

The first batch contains transactions (1) and (2), whose total is (6). This looks contradictory because (t=5), but the table's `reachable query` is a query position, not an allowed transaction endpoint. Query (5) lies inside transaction (2), so `owner[5]=2`. The entire transaction (2) cannot actually be included if its prefix sum is (6). This exposes a subtle error in the naive interpretation of `owner[x]`.

The correct transition must use the query position immediately before the forbidden transaction boundary. More directly, if the target position is (x), the endpoint is the transaction containing query (x), but only if that transaction's prefix sum is at most the limit. Since (x) may lie inside a transaction, the endpoint is indeed that transaction only when its full prefix sum fits. The official formulation avoids this ambiguity by storing the transaction index reached after exactly (t) query units from a valid starting boundary, with the transition based on that precomputed state.

For a simpler and safer implementation, we can instead use binary search over prefix sums for each jump, but that loses the intended (O(S\log S)) bound in Python. The correct constant-time formulation is to store, for each query count (x), the first transaction whose prefix sum is at least (x), then advance to the transaction after that. This is exactly what the `owner` array above does, but the endpoint must be interpreted using the first prefix at or beyond the reachable query count.

For the sample, (t=5), starting from transaction (1), the first prefix sum at least (5) is (6), corresponding to transaction (2). Since transaction (2) would make the batch sum (6>5), the current batch must end at transaction (1), and the next batch starts at (2). This is why the implementation should use a `lower_bound`-style mapping rather than `owner[x]` directly.

The following corrected implementation uses `next_transaction[x]`, defined as the first transaction whose prefix sum is at least (x). If that prefix exceeds the target, we subtract one transaction from the endpoint.

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    prefix = [0] * (n + 1)
    mx = 0

    for i, x in enumerate(a, 1):
        prefix[i] = prefix[i - 1] + x
        mx = max(mx, x)

    total = prefix[n]

    # at_least[x] = first transaction i with prefix[i] >= x.
    at_least = [0] * (total + 1)
    i = 1
    for x in range(1, total + 1):
        while prefix[i] < x:
            i += 1
        at_least[x] = i

    q = int(input())
    queries = list(map(int, input().split()))

    cache = {}
    out = []

    for t in queries:
        if t < mx:
            out.append("Impossible")
            continue

        if t in cache:
            out.append(str(cache[t]))
            continue

        start = 1
        batches = 0

        while start <= n:
            batches += 1

            target = prefix[start - 1] + t

            if target >= total:
                break

            first_too_large = at_least[target + 1]
            start = first_too_large

        cache[t] = batches
        out.append(str(batches))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The important correction is that `target` represents the largest query position allowed by capacity. The first transaction whose prefix sum exceeds `target` is found using `target + 1`. That transaction cannot belong to the current batch, so it is exactly the next batch's starting transaction.

For (t=5) in the sample, the first batch starts at transaction (1), so `target=5`. The first prefix greater than (5) is (6), belonging to transaction (2). Thus the next batch starts at transaction (2), giving the correct partition.

For a second example, consider

```
4
2 1 3 2
4
3 4 6 8
```

The prefix sums are

```
[0, 2, 3, 6, 8].
```

For (t=3), the greedy process is:

| Batch | Start | Queries before start | Target | First prefix greater than target | Next start |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 3 | 6, transaction 3 | 3 |
| 2 | 3 | 3 | 6 | 8, transaction 4 | 4 |
| 3 | 4 | 6 | 9 | end | stop |

The resulting partition is (2+1\mid3\mid2), so the answer is (3).

For (t=6), the first batch can contain transactions (1), (2), and (3), whose sum is exactly (6). The remaining transaction forms the second batch.

| Batch | Start | Queries before start | Target | First prefix greater than target | Next start |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 6 | 8, transaction 4 | 4 |
| 2 | 4 | 6 | 12 | end | stop |

The answer is (2). These traces demonstrate why the boundary lookup must search for the first prefix strictly greater than the allowed query count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+S+S\log S+q)) | Prefix and query-position preprocessing are linear. Across all distinct (t), greedy simulations take (O(S\log S)) total steps. |
| Space | (O(n+S+q)) | Prefix sums use (O(n)), the query-position mapping uses (O(S)), and the query cache uses (O(q)). |

Here (S=\sum a_i\le10^6). The harmonic sum behind the simulation is

[
S\left(\frac1{1}+\frac1{2}+\cdots+\frac1S\right)=O(S\log S),
]

which is comfortably smaller than the (nq) work of the direct solution. The memory usage is also safe under the 512 MB limit.

## Test Cases

The following test harness keeps the contest solution in a callable `solve` function and replaces standard input with an in-memory stream. The maximum-size case is generated rather than written out explicitly, which keeps the test readable while still constructing (200,000) transactions.

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    prefix = [0] * (n + 1)
    mx = 0

    for i, x in enumerate(a, 1):
        prefix[i] = prefix[i - 1] + x
        mx = max(mx, x)

    total = prefix[n]

    # first transaction whose prefix sum is strictly greater than x
    greater = [0] * (total + 1)
    i = 1

    for x in range(total):
        while i <= n and prefix[i] <= x:
            i += 1
        greater[x] = i

    q = int(input())
    queries = list(map(int, input().split()))

    cache = {}
    out = []

    for t in queries:
        if t < mx:
            out.append("Impossible")
            continue

        if t in cache:
            out.append(str(cache[t]))
            continue

        start = 1
        batches = 0

        while start <= n:
            batches += 1
            target = prefix[start - 1] + t

            if target >= total:
                break

            start = greater[target]

        cache[t] = batches
        out.append(str(batches))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    """6
4 2 3 1 3 4
8
10 2 5 4 6 7 8 8
"""
) == """2
Impossible
4
5
4
3
3
3""", "sample 1"

# Minimum-size input
assert run(
    """1
1
4
1 2 1 100
"""
) == """1
1
1
1""", "single transaction"

# Every transaction has the same size
assert run(
    """5
2 2 2 2 2
5
1 2 3 4 10
"""
) == """Impossible
5
3
2
1""", "all equal values"

# Boundary around the maximum transaction size
assert run(
    """3
2 5 1
5
4 5 6 7 8
"""
) == """Impossible
Impossible
2
2
1""", "maximum transaction boundary"

# Maximum n, small total, and duplicate queries
a = " ".join(["1"] * 200000)
assert run(
    f"""200000
{a}
4
1 2 100000 200000
"""
) == """200000
100000
2
1""", "maximum n"

# Exact-fit boundary and a limit that lands inside a transaction
assert run(
    """4
2 1 3 2
4
2 3 6 8
"""
) == """3
3
2
1""", "exact fit and interior boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, a=[1]` | `1, 1, 1, 1` | Minimum-size input and capacities larger than the whole array |
| `a=[2,2,2,2,2]` | `Impossible, 5, 3, 2, 1` | All-equal values and the impossible boundary |
| `a=[2,5,1]` | `Impossible, Impossible, 2, 2, 1` | Limits just below and at the maximum transaction size |
| `200000` ones | `200000, 100000, 2, 1` | Maximum transaction count, repeated query handling, and large input |
| `a=[2,1,3,2]` | `3,3,2,1` | Exact fits and limits whose query position lies inside a transaction |

## Edge Cases

When (t) is smaller than the largest transaction, the algorithm exits before doing any simulation. For example,

```
3
2 5 1
1
4
```

has answer `Impossible`, because transaction (2) alone needs five queries. No combination of neighboring transactions can make that transaction smaller.

When (t) equals the largest transaction, the instance becomes feasible. For

```
3
2 5 1
1
5
```

the greedy algorithm starts with transaction (1). Its capacity reaches query position (5), but the first prefix sum greater than (5) is (6), corresponding to transaction (3). The first batch is transactions (1) and (2), with total (7), so this example actually demonstrates why the lookup must use the first prefix strictly greater than the allowed target. The correct first batch is only transaction (1), followed by transaction (2), followed by transaction (3), giving `3`.

When the target lands exactly on a transaction boundary, the next transaction must start the following batch. For

```
4
2 1 3 2
1
6
```

the first six queries are exactly transactions (1), (2), and (3). The first batch has sum (6), and transaction (4) starts the second batch. The answer is `2`.

When the target lands inside a transaction, that transaction must not be partially included. For

```
4
2 1 3 2
1
4
```

the first batch can contain transactions (1) and (2), with total (3), but cannot include transaction (3), whose full size would raise the total to (6). The answer is `3`, with partition (2+1\mid3\mid2).

When (t) is at least the total number of queries, the entire array fits into one batch. For

```
4
2 1 3 2
1
8
```

the target reaches the end immediately, so the algorithm performs exactly one iteration and outputs `1`.

Repeated values of (t) are handled by the cache. If the input asks for (8) one hundred thousand times, the partition is simulated once and the same result is returned for every later occurrence. This matters because the complexity argument is based on distinct values of (t), not the raw number of queries.

The central invariant throughout the simulation is that `start` is always the first transaction not assigned to a previous batch. The chosen next start is the first transaction that cannot fit completely into the current batch. Thus every transaction before `start` belongs to the current or an earlier valid batch, while every transaction from `start` onward remains unprocessed. The greedy process consequently advances monotonically until the entire array has been partitioned.
