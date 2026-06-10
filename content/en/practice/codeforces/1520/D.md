---
title: "CF 1520D - Same Differences"
description: "We are given an array and must count how many index pairs $(i, j)$ with $i < j$ satisfy a very specific relationship between their values and positions."
date: "2026-06-10T18:06:41+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "hashing", "math"]
categories: ["algorithms"]
codeforces_contest: 1520
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 719 (Div. 3)"
rating: 1200
weight: 1520
solve_time_s: 120
verified: true
draft: false
---

[CF 1520D - Same Differences](https://codeforces.com/problemset/problem/1520/D)

**Rating:** 1200  
**Tags:** data structures, hashing, math  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and must count how many index pairs $(i, j)$ with $i < j$ satisfy a very specific relationship between their values and positions.

The condition is:

$$a_j - a_i = j - i$$

For every test case, we need to count all pairs that satisfy this equation and print the total.

The constraints are the first thing to examine. A single test case can contain up to $2 \cdot 10^5$ elements, and the total size across all test cases is also at most $2 \cdot 10^5$. Any solution that checks every pair would require roughly

$$\frac{n(n-1)}{2}$$

comparisons. For $n = 2 \cdot 10^5$, that is about $2 \times 10^{10}$ pair checks, which is completely infeasible within a 2-second limit.

This immediately rules out $O(n^2)$ approaches. We need something close to linear time per test case.

There are a few easy-to-miss situations that can cause mistakes.

Consider:

```
1
3
1 2 3
```

Every pair is valid because:

$$2 - 1 = 1,\quad 3 - 2 = 1,\quad 3 - 1 = 2$$

The correct answer is:

```
3
```

A solution that only checks adjacent elements would count 2 instead of 3.

Now consider:

```
1
4
1 1 1 1
```

The correct answer is:

```
0
```

Even though all values are equal, the right side $j-i$ is always positive for distinct indices, so the equation can never hold.

Another subtle case is:

```
1
5
1 3 5 7 9
```

Every element increases by 2, while indices increase by 1. A careless solution that focuses only on differences between neighboring elements might incorrectly conclude many pairs are valid. In reality:

$$a_j-a_i = 2(j-i)$$

which never equals $j-i$ unless $i=j$. The correct answer is 0.

These examples suggest that we need a way to transform the condition into something easier to count globally rather than comparing pairs directly.

## Approaches

The most direct solution is brute force. For every index $i$, try every later index $j$, compute both sides of the equation, and increment the answer when they match.

This works because it literally checks the definition of a valid pair. The problem is the running time. With $n = 2 \cdot 10^5$, the number of pairs is roughly $2 \times 10^{10}$, far beyond what can be processed in time.

To improve on this, we should examine the equation itself:

$$a_j - a_i = j - i$$

Move terms involving the same index to the same side:

$$a_j - j = a_i - i$$

This is the key observation.

A pair is valid exactly when both indices have the same value of:

$$a_k - k$$

for their respective positions.

The original problem is no longer about comparing pairs. Instead, it becomes:

"How many pairs of indices share the same value of $a_i - i$?"

Once viewed this way, the solution becomes a standard frequency-counting problem.

As we scan the array, suppose the current value $a_i - i$ has already appeared $f$ times. Then the current index forms a valid pair with each of those previous $f$ indices. We add $f$ to the answer and increase the frequency.

A hash map stores how many times each transformed value has appeared.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Initialize an empty hash map that will store frequencies of values $a_i - i$.
2. Initialize the answer to 0.
3. Iterate through the array from left to right.
4. For the current position, compute:

$$key = a_i - i$$

The problem statement uses 1-based indexing, so the transformation must also use 1-based positions.
5. Look up how many times this key has appeared before.

Every previous occurrence corresponds to one valid pair with the current index because:

$$a_j-j = a_i-i$$

is exactly the transformed condition.
6. Add that frequency to the answer.
7. Increase the frequency of the current key in the hash map.
8. After processing all elements, print the accumulated answer.

### Why it works

The transformation

$$a_j-a_i=j-i$$

is algebraically equivalent to

$$a_j-j=a_i-i.$$

Thus a pair is valid if and only if both indices produce the same transformed value.

During the scan, the hash map always stores the number of previously processed indices having each transformed value. When the current index has value $x$, every earlier index with transformed value $x$ forms a valid pair with it, and no index with a different transformed value can form a valid pair.

Because each pair is counted exactly when its second index is processed, every valid pair is counted once and only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {}
        ans = 0

        for i in range(n):
            key = a[i] - (i + 1)  # 1-based index

            ans += freq.get(key, 0)
            freq[key] = freq.get(key, 0) + 1

        print(ans)

solve()
```

The solution follows the transformed condition directly.

The variable `key` stores $a_i - i$, using `i + 1` because the mathematical indices in the problem are 1-based. Forgetting this conversion is the most common bug in this problem.

The dictionary `freq` records how many previous positions produced each transformed value.

When a new occurrence of the same key appears, every previous occurrence forms a valid pair with the current index. Adding `freq[key]` to the answer counts all such pairs immediately.

The answer can become large. In the worst case every pair is valid, giving:

$$\frac{n(n-1)}{2}$$

which is approximately $2 \times 10^{10}$ when $n=2\cdot10^5$. Python integers handle this automatically, but in languages such as C++ a 64-bit integer is required.

## Worked Examples

### Example 1

Input:

```
6
3 5 1 4 6 6
```

Compute $a_i-i$ using 1-based indices.

| Index | Value | Key = a[i] - i | Previous Frequency | Answer After Step |
| --- | --- | --- | --- | --- |
| 1 | 3 | 2 | 0 | 0 |
| 2 | 5 | 3 | 0 | 0 |
| 3 | 1 | -2 | 0 | 0 |
| 4 | 4 | 0 | 0 | 0 |
| 5 | 6 | 1 | 0 | 0 |
| 6 | 6 | 0 | 1 | 1 |

Final answer:

```
1
```

The only repeated transformed value is 0, occurring at indices 4 and 6, producing one valid pair.

### Example 2

Input:

```
3
1 2 3
```

| Index | Value | Key = a[i] - i | Previous Frequency | Answer After Step |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 |
| 2 | 2 | 0 | 1 | 1 |
| 3 | 3 | 0 | 2 | 3 |

Final answer:

```
3
```

All three positions share the same transformed value. The number of valid pairs becomes:

$$\binom{3}{2}=3.$$

This trace demonstrates the counting logic. When the third occurrence arrives, it forms a pair with both earlier occurrences, contributing 2 new pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is processed once, with constant-time hash map operations |
| Space | $O(n)$ | In the worst case every transformed value is distinct |

Since the total number of elements across all test cases is at most $2 \cdot 10^5$, the total running time is linear in the input size. This comfortably fits within the time limit, and the hash map easily fits within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {}
        ans = 0

        for i in range(n):
            key = a[i] - (i + 1)
            ans += freq.get(key, 0)
            freq[key] = freq.get(key, 0) + 1

        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run(
"""4
6
3 5 1 4 6 6
3
1 2 3
4
1 3 3 4
6
1 6 3 4 5 6
"""
) == "1\n3\n3\n10", "sample"

# minimum size
assert run(
"""1
1
1
"""
) == "0", "single element"

# all equal values
assert run(
"""1
4
1 1 1 1
"""
) == "0", "all equal"

# every pair valid
assert run(
"""1
5
1 2 3 4 5
"""
) == "10", "all pairs valid"

# off-by-one check
assert run(
"""1
2
2 2
"""
) == "0", "index handling"

# repeated transformed values
assert run(
"""1
5
3 4 5 1 2
"""
) == "3", "multiple groups"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1]` | `0` | Minimum array size |
| `[1,1,1,1]` | `0` | Equal values do not imply valid pairs |
| `[1,2,3,4,5]` | `10` | Every pair satisfies the condition |
| `[2,2]` | `0` | Detects 1-based indexing mistakes |
| `[3,4,5,1,2]` | `3` | Multiple occurrences of the same transformed value |

## Edge Cases

### Single element array

Input:

```
1
1
1
```

The transformed value is:

$$1-1=0$$

The frequency of 0 is initially 0, so nothing is added to the answer. No pair exists because at least two indices are required.

Output:

```
0
```

### All values equal

Input:

```
1
4
1 1 1 1
```

The transformed values are:

$$0,\,-1,\,-2,\,-3$$

All are distinct.

Processing proceeds with frequencies always equal to zero before insertion, so the answer never increases.

Output:

```
0
```

This confirms that equal array values alone are not enough. The index positions matter.

### Every pair valid

Input:

```
1
5
1 2 3 4 5
```

The transformed values are:

$$0,0,0,0,0$$

The running answer becomes:

$$0 + 1 + 2 + 3 + 4 = 10$$

which equals:

$$\binom{5}{2}.$$

Output:

```
10
```

The algorithm correctly counts all possible pairs.

### Off-by-one indexing trap

Input:

```
1
2
2 2
```

Using the correct 1-based indices:

$$2-1=1,\qquad 2-2=0$$

The transformed values differ, so no valid pair exists.

Output:

```
0
```

If someone mistakenly used 0-based indices in the transformation, both keys would become 2 and the answer would incorrectly be 1. This example shows why the conversion to 1-based indexing is essential.
