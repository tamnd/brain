---
title: "CF 102460J - Automatic Control Machine"
description: "Each machine has a set of features that must all be tested. A test dataset can detect some subset of those features, represented by a binary string of length (n). Choosing several datasets means taking the union of all features detected by those datasets."
date: "2026-08-08T10:18:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102460
codeforces_index: "J"
codeforces_contest_name: "2019-2020 ICPC Asia Taipei-Hsinchu Regional Contest"
rating: 0
weight: 102460
solve_time_s: 310
verified: true
draft: false
---

[CF 102460J - Automatic Control Machine](https://codeforces.com/problemset/problem/102460/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

Each machine has a set of features that must all be tested. A test dataset can detect some subset of those features, represented by a binary string of length \(n\). Choosing several datasets means taking the union of all features detected by those datasets. The task is to find the smallest number of datasets whose union contains every feature. If some feature is never detected by any dataset, the answer is \(-1\).

The constraints are deliberately asymmetric. There can be as many as 500 features, which is too many for a subset over features because \(2^{500}\) is completely infeasible. On the other hand, there are at most 15 test datasets. That makes \(2^m\), at most \(2^{15}=32768\), small enough to enumerate for every machine. The number of machines is also at most 10, so even processing all subsets for every machine is easily manageable.

A careless implementation can still fail on a few boundaries. Consider a single feature with one dataset that cannot test it:

```text
1
1 1
0
```

The correct answer is `-1`. A solution that initializes the answer to zero and only decreases it when it finds a solution can incorrectly print zero.

The opposite case is also useful:

```text
1
1 1
1
```

The correct answer is `1`, not zero. The empty subset covers no features, so it must never be treated as a valid solution.

Duplicate datasets do not provide any special advantage. For example:

```text
1
4 3
1111
1111
1111
```

The answer is `1`, because one dataset already covers everything. A solution that counts distinct coverage patterns instead of selected datasets could still get this case right, but algorithms that accidentally require different coverage from every chosen dataset can fail.

Finally, a feature may be covered only by combining several datasets. For example:

```text
1
3 2
100
011
```

The answer is `2`. Checking only whether some individual dataset covers all features would incorrectly report `-1`.

The official sample contains five machines and has outputs `1, 2, 4, 3, -1`. The complete binary strings are present in the original contest statement. citeturn2view0

## Approaches

The direct brute-force approach is to consider every subset of the \(m\) test datasets. For each subset, scan collection of datasets appears exactly once among the \(2^m\) subsets.

If the coverage is represented naively as a boolean array, processing one subset can take \(O(mn)\) time. In the worst case this gives

\[
O(2^m mn).
\]

With \(m=15\) and \(n=500\), that is roughly \(32768 \times 15 \times 500\), or about 246 million elementary feature checks per machine. Python would have little room for that under a two-second limit.

The key observation is that the small dimension is the number of datasets, not the number of features. We should enumerate subsets of datasets, but we should represent the set of covered features compactly.

Python integers are arbitrary-precision bitsets. We can turn each binary string into one integer, where bit \(j\) represents whether feature \(j\) is covered. Combining datasets is then simply bitwise OR. A union of 500 features fits into only a handful of machine words internally, and Python performs the OR operation in optimized native code.

There is one more useful improvement. When considering a subset, remove one selected dataset and reuse the coverage of the smaller subset. If `mask` is the current subset and `bit` is its lowest set bit, then

```text
coverage[mask] = coverage[mask without bit] | dataset[bit]
```

Each subset therefore needs only one integer OR operation instead of rebuilding its union from all selected datasets.

The brute-force approach works because every possible choice must be considered, but it fails because it repeatedly recomputes the same partial unions. The small value of \(m\) lets us keep the \(2^m\) search space, while bitsets and incremental subset construction make the work per subset tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | \(O(2^m mn)\) | \(O(n)\) | Too slow in Python |
| Optimal | \(O(2^m \lceil n/w\rceil)\) | \(O(2^m \lceil n/w\rceil)\) | Accepted |

Here \(w\) is the machine word size used internally by the bitset representation. Since \(n\le500\), it is effectively a small constant for this problem.

## Algorithm Walkthrough

1. Convert every dataset's binary string into an integer. Bit \(j\) is set exactly when dataset \(j\) can test the corresponding feature. Using integers means unioning two sets of tested features becomes a single bitwise OR.

2. Construct `full = (1 << n) - 1`. This integer has all \(n\) feature bits set, so a collection covers every feature exactly when its coverage integer equals `full`.

3. Allocate an array `coverage` of size \(2^m\). Entry `coverage[mask]` stores the union of all datasets selected by the subset represented by `mask`. The empty subset has `coverage[0] = 0`.

4. Enumerate every nonempty subset `mask`. Extract its lowest set bit with `mask & -mask`. The position of that bit identifies one dataset belonging to the subset.

5. Remove that dataset from the subset to obtain `previous = mask ^ bit`. The coverage of the current subset is then `coverage[previous] | datasets[index]`. This is the central reuse step, because the smaller subset has already been processed.

6. Whenever the resulting coverage equals `full`, compute `mask.bit_count()` and use it to update the minimum answer. Every subset is examined, so the smallest valid subset is guaranteed to be found.

7. If no subset reaches `full`, print `-1`. Otherwise print the smallest number of selected datasets found.

### Why it works

The invariant is that after processing a subset `mask`, `coverage[mask]` is exactly the union of all datasets selected by `mask`. This holds initially for the empty subset. For any nonempty subset, removing one selected dataset gives a smaller subset whose coverage is already correct, and OR-ing the removed dataset adds exactly the features it can test. Thus every subset gets its exact coverage. Since the algorithm examines every possible subset and accepts precisely those whose coverage contains every feature, the minimum recorded population count is exactly the minimum number of datasets required.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    answers = []

    for _ in range(T):
        n, m = map(int, input().split())

        datasets = []
        for _ in range(m):
            datasets.append(int(input().strip(), 2))

        full = (1 << n) - 1
        total_masks = 1 << m

        coverage = [0] * total_masks
        answer = m + 1

        for mask in range(1, total_masks):
            bit = mask & -mask
            index = bit.bit_length() - 1
            previous = mask ^ bit

            coverage[mask] = coverage[previous] | datasets[index]

            if coverage[mask] == full:
                count = mask.bit_count()
                if count < answer:
                    answer = count

        answers.append(str(answer if answer <= m else -1))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The input strings are converted with `int(string, 2)`. The leftmost character becomes a higher-order bit, but that does not matter because we only care whether every position is covered consistently across all datasets.

`full = (1 << n) - 1` creates exactly \(n\) one-bits. Since every dataset has exactly \(n\) characters, no irrelevant bit can appear above position \(n-1\).

The expression `mask & -mask` isolates the lowest selected dataset. `bit.bit_length() - 1` converts that isolated bit into the corresponding zero-based dataset index. `mask ^ bit` removes it, because that bit is guaranteed to be set in `mask`.

The array `coverage` has \(2^m\) entries, including the empty subset. Starting the enumeration at `1` avoids treating the empty subset as a solution. Since \(n>0\), the empty subset can never cover `full` anyway.

Python integers do not overflow, so a feature count of 500 requires no special numeric handling. The expensive work is performed by integer OR operations rather than Python-level loops over individual features.

## Worked Examples

The official sample begins with this machine:

```text
3 3
100
011
111
```

There are three datasets and three features. The complete sample gives this machine the answer `1`. citeturn2view0

| Mask | Selected datasets | Coverage | Count | Best |
|---:|---|---|---:|---:|
| 000 | none | 000 | 0 | not valid |
| 001 | dataset 1 | 100 | 1 | not valid |
| 010 | dataset 2 | 011 | 1 | not valid |
| 011 | datasets 1, 2 | 111 | 2 | 2 |
| 100 | dataset 3 | 111 | 1 | 1 |

The subset `011` proves that all three features are possible with two datasets. The later subset `100` shows that the third dataset alone already covers everything, so the optimum decreases to `1`.

The fifth machine in the official sample is:

```text
2 1
01
```

There is only one dataset, and it tests only the second feature. The first feature is impossible to test, so the answer is `-1`. citeturn2view0

| Mask | Selected datasets | Coverage | Count | Best |
|---:|---|---|---:|---:|
| 0 | none | 00 | 0 | not valid |
| 1 | dataset 1 | 01 | 1 | not valid |

No subset produces `11`, so the algorithm finishes with its initial sentinel value and prints `-1`. This demonstrates why impossibility must be handled separately from finding a minimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(T2^m\lceil n/w\rceil)\) | Each of the \(2^m\) subsets performs one bitwise OR and one bit count at most |
| Space | \(O(2^m\lceil n/w\rceil)\) | The coverage array stores one bitset for every dataset subset |

With \(m\le15\), there are at most 32768 subsets per machine. With only 500 features, each bitset is very small. Even across all 10 machines, this is comfortably within the stated memory limit, and the operations are much smaller than the naive \(O(2^m mn)\) implementation.

## Test Cases

The following test harness uses the same `solve` function as the submitted solution. The official sample is included exactly as published in the contest statement. citeturn2view0

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    T = int(input())
    answers = []

   
        answer = m + 1

        for mask in range(1, total_masks):
            bit = mask & -mask
            index = bit.bit_length() - 1
            previous = mask ^ bit

            coverage[mask] = coverage[previous] | datasets[index]

            if coverage[mask] == full:
                answer = min(answer, mask.bit_count())

        answers.append(str(answer if answer <= m else -1))

    sys.stdout.write("\n".join(answers))

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

# Official sample
sample = """\
5
3 3
100
011
111
5 6
10000
01001
01110
00111
10110
00101
6 7
000010
011000
100100
001000
000010
010000
110001
7 6
1001001
1001000
0001101
0010110
0110011
0100001
2 1
01
"""

assert run(sample) == """\
1
2
4
3
-1
""".strip(), "official sample"

# Minimum-size solvable case
assert run("""\
1
1 1
1
""") == "1", "single feature covered by one dataset"

# Minimum-size impossible case
assert run("""\
1
1 1
0
""") == "-1", "single feature is never covered"

# All datasets are identical, but one already covers everything
assert run("""\
1
4 3
1111
1111
1111
""") == "1", "duplicate full-coverage datasets"

# Coverage requires combining datasets
assert run("""\
1
3 2
100
011
""") == "2", "two datasets are necessary"

# Maximum m, with every dataset identical
max_case = "1\n1 15\n" + "1\n" * 15
assert run(max_case) == "1", "maximum number of datasets"

# Maximum n, one dataset covers every feature
max_n_case = "1\n500 1\n" + "1" * 500 + "\n"
assert run(max_n_case) == "1", "maximum number of features"
```

| Test input | Expected output | What it validates |
|---|---:|---|
| `1 / 1 1 / 1` | `1` | Smallest solvable instance |
| `1 / 1 1 / 0` | `-1` | Smallest impossible instance |
| Three identical `1111` datasets | `1` | Duplicate datasets and minimum selection |
| `100` and `011` | `2` | Coverage that requires combining datasets |
| One feature and 15 identical datasets | `1` | Maximum \(m\) boundary |
| One dataset containing 500 ones | `1` | Maximum \(n\) boundary |

## Edge Cases

For the single-feature solvable case

```text
1
1 1
1
```

the full mask is `1`. The empty subset has coverage `0`, while subset `1` has coverage `1`, so the answer becomes `1`. The implementation never accidentally accepts the empty subset.

For the single-feature impossible case

```text
1
1 1
0
```

the full mask is again `1`, but the only nonempty subset has coverage `0`. No subset reaches the full mask, so the sentinel remains `m + 1` and the output is `-1`.

For duplicate full-coverage datasets

```text
1
4 3
1111
1111
1111
```

each dataset is already equal to `full`. The first single-dataset subset reaches full coverage and gives an answer of `1`. Additional identical datasets cannot improve it because no valid solution can use fewer than one dataset.

For a case requiring combination,

```text
1
3 2
100
011
```

the first dataset covers feature 1, the second covers features 2 and 3, and neither individual subset reaches `111`. The subset containing both datasets produces `111` and has population count `2`, giving the correct answer.

For the maximum number of datasets, \(m=15\), the algorithm enumerates exactly 32768 subsets. That is the largest search space permitted by the input. The subset representation uses 15 bits, so no special handling is needed when extracting the lowest set bit or counting selected datasets.

For the maximum number of features, \(n=500\), `full` contains 500 one-bits and every dataset becomes a 500-bit Python integer. Python's arbitrary-precision integers handle this directly, so there is no fixed-width overflow boundary to manage.
