---
title: "CF 102739H - \u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430 \u0435\u0434\u044b"
description: "The problem asks us to answer many range queries on a sequence of delivery companies. During the day, the companies of arriving couriers are recorded as an array a."
date: "2026-08-01T22:17:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102739
codeforces_index: "H"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2020.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102739
solve_time_s: 115
verified: true
draft: false
---

[CF 102739H - \u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430 \u0435\u0434\u044b](https://codeforces.com/problemset/problem/102739/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem asks us to answer many range queries on a sequence of delivery companies. During the day, the companies of arriving couriers are recorded as an array `a`. For each colleague, we are given an interval of this array representing the time period when that colleague could have ordered food. We must find a company number that appears the most times inside that interval. If several companies have the same maximum frequency, any of them is accepted.

The array length and the number of queries can both reach `100000`, while company identifiers can be as large as `10^9`. The large identifier range means we cannot use the company number directly as an array index, so compression is needed. The size of `n` and `q` rules out checking every element of every interval. A solution that scans each query independently can perform around `10^10` operations in the worst case, which is far beyond what a one second limit allows. We need a method where the total amount of movement through the array is close to `n * sqrt(n)`.

A common mistake is to handle ties incorrectly. The answer is not required to be unique. For example:

```
5
1 2 1 2 3
1
1 4
```

The correct output can be either `1` or `2`, because both appear twice. A solution that assumes the first maximum found is always stable can fail after removing elements from a data structure.

Another edge case is a query containing a single element:

```
3
7 8 9
1
2 2
```

The answer must be `8`. Implementations that initialize the current maximum frequency to zero and forget to add the first element correctly may return an invalid value.

A third case is when one company dominates after many updates:

```
6
5 1 5 2 5 3
1
1 6
```

The answer must be `5`. A lazy update strategy that only increases the current maximum but does not repair it after deletions can keep an outdated frequency and produce a wrong answer.

## Approaches

The direct approach is to process each query separately. For an interval `[l, r]`, we scan all positions between `l` and `r`, count occurrences of every company, and select the largest count. This is correct because it examines exactly the elements that belong to the query. The problem is the repeated work. If all queries cover the whole array, each query costs `O(n)`, giving `O(nq)`, which becomes `10^10` operations for the maximum input size.

The structure of the problem is that queries only ask about frequencies in ranges, and neighboring queries often overlap heavily. Instead of rebuilding frequency information from zero every time, we can reorder the queries and maintain one moving window. This is the idea behind Mo's algorithm.

Mo's algorithm divides the array into blocks of roughly size `sqrt(n)`. Queries are sorted by their left block and then by their right endpoint. When moving from one query to the next, we only add or remove the positions that changed. The maintained window always contains exactly the current query interval, so the frequency table is always ready.

The remaining challenge is maintaining the most frequent company while elements enter and leave the window. We keep a frequency array for compressed company identifiers and another array telling how many companies currently have each frequency. When removing elements, if the current maximum frequency disappears, we decrease it until some company exists with that frequency.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O((n + q)√n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compress all company identifiers into consecutive integers. The original values are saved separately so that the final answer can be converted back.
2. Choose a block size around `sqrt(n)` and sort queries by Mo's ordering. Queries with smaller left blocks come first, and inside one block, right endpoints are ordered increasingly. This minimizes how far the current interval has to move overall.
3. Maintain the current interval with two pointers. Initially the interval is empty. When the left or right boundary changes, add or remove the corresponding array position.
4. When adding a company, increase its frequency. Update the number of companies having that frequency and raise the current maximum if necessary.
5. When removing a company, decrease its frequency. Update the frequency counters. If the previous maximum frequency no longer exists, lower the maximum until a valid frequency remains.
6. For every processed query, choose any company whose frequency equals the current maximum frequency and store its original identifier.

The invariant is that after every pointer movement, the frequency table describes exactly the elements inside the current interval. The second structure guarantees that the stored maximum frequency is always a frequency that actually appears in the window. Since the answer is chosen only from companies having that frequency, every produced answer is a valid mode of the requested range.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    values = sorted(set(arr))
    comp = {v: i for i, v in enumerate(values)}
    a = [comp[x] for x in arr]

    q = int(input())
    queries = []
    for i in range(q):
        l, r = map(int, input().split())
        queries.append((l - 1, r - 1, i))

    block = int(n ** 0.5) + 1

    queries.sort(
        key=lambda x: (
            x[0] // block,
            x[1] if (x[0] // block) % 2 == 0 else -x[1]
        )
    )

    freq = [0] * len(values)
    freq_count = [0] * (n + 1)

    answers = [0] * q
    current_max = 0
    best = -1

    def add(x):
        nonlocal current_max, best
        old = freq[x]
        if old:
            freq_count[old] -= 1
        new = old + 1
        freq[x] = new
        freq_count[new] += 1
        if new > current_max:
            current_max = new
            best = x

    def remove(x):
        nonlocal current_max, best
        old = freq[x]
        freq_count[old] -= 1
        new = old - 1
        freq[x] = new
        if new:
            freq_count[new] += 1
        if old == current_max and freq_count[old] == 0:
            current_max -= 1
            while current_max and freq_count[current_max] == 0:
                current_max -= 1
            if current_max:
                for i, f in enumerate(freq):
                    if f == current_max:
                        best = i
                        break

    left = 0
    right = -1

    for l, r, idx in queries:
        while left > l:
            left -= 1
            add(a[left])
        while right < r:
            right += 1
            add(a[right])
        while left < l:
            remove(a[left])
            left += 1
        while right > r:
            remove(a[right])
            right -= 1

        answers[idx] = values[best]

    print("\n".join(map(str, answers)))

if __name__ == "__main__":
    solve()
```

The compression step replaces large company numbers with small indexes, which allows constant time access to frequency arrays. The original numbers remain in `values`, so the output still uses the identifiers from the input.

The `queries` sorting order is the main part of Mo's algorithm. The alternating direction for the right endpoint reduces unnecessary pointer movement between neighboring blocks.

The `freq` array stores the current occurrence count of every compressed company. The `freq_count` array answers a different question: whether a particular frequency currently exists. This avoids rebuilding all frequencies after every removal.

Python integers do not overflow, so frequency values are safe. The important boundary detail is that the maintained interval is inclusive on both sides, so adding and removing operations must happen in the correct order when moving pointers.

## Worked Examples

For the sample:

```
5
2 4 2 4 5
3
1 3
3 4
1 5
```

the trace is:

| Query | Current range | Frequencies | Maximum frequency | Answer |
| --- | --- | --- | --- | --- |
| [1,3] | 2 4 2 | 2:2, 4:1 | 2 | 2 |
| [3,4] | 2 4 | 2:1, 4:1 | 1 | 2 |
| [1,5] | 2 4 2 4 5 | 2:2, 4:2, 5:1 | 2 | 4 |

The example demonstrates the tie rule. The second query contains two companies with the same frequency, so either one is valid.

A second example:

```
4
9 9 1 9
2
2 3
1 4
```

| Query | Current range | Frequencies | Maximum frequency | Answer |
| --- | --- | --- | --- | --- |
| [2,3] | 9 1 | 9:1, 1:1 | 1 | 9 |
| [1,4] | 9 9 1 9 | 9:3, 1:1 | 3 | 9 |

This trace shows that expanding the interval correctly accumulates previous frequency information instead of recomputing it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q)√n) | Mo's ordering limits the total pointer movement |
| Space | O(n) | Frequency arrays, compressed values, and stored queries |

With `100000` elements and queries, the number of pointer changes is acceptable for the intended constraints. The memory usage is linear and fits easily inside the limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out

    solve()

    sys.stdin = old
    sys.stdout = old_out
    return out.getvalue()

assert run("""5
2 4 2 4 5
3
1 3
3 4
1 5
""") in ("2\n2\n4\n", "2\n4\n4\n", "2\n2\n2\n", "4\n2\n4\n")

assert run("""1
100
1
1 1
""") == "100\n"

assert run("""6
7 7 7 3 3 2
3
1 6
4 5
6 6
""") == "7\n3\n2\n"

assert run("""5
1 2 3 4 5
2
1 5
2 4
""") in (
    "1\n2\n", "1\n3\n", "1\n4\n", "2\n2\n",
    "3\n2\n", "4\n2\n", "5\n2\n"
)

assert run("""5
8 8 8 8 8
2
1 3
3 5
""") == "8\n8\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | `100` | Minimum size interval handling |
| One dominant company | `7`, `3`, `2` | Frequency updates after moving windows |
| All distinct values | Any element from the range | Tie handling |
| All equal values | `8` | Maximum frequency tracking |

## Edge Cases

The tie case is handled because the algorithm only searches for a company with the current maximum frequency. It never assumes that a particular company must win. For:

```
5
1 2 1 2 3
1
1 4
```

the maintained frequencies are `1:2` and `2:2`, so either company can be returned.

For a single-element query:

```
3
7 8 9
1
2 2
```

Mo's algorithm expands the empty window by adding only position `2`. The frequency of `8` becomes one, and the maximum frequency becomes one, so the returned answer is exactly `8`.

For a dominant value after many updates:

```
6
5 1 5 2 5 3
1
1 6
```

the final frequency table contains `5:3`, while every other company has frequency one. The maintained maximum becomes three, and the algorithm returns `5`. The same logic works even if removals temporarily decrease the winner's frequency, because the frequency counters repair the maximum value before answering the next query.
