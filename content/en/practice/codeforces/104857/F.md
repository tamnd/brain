---
title: "CF 104857F - Colorful Balloons"
description: "We are given a sequence of balloon colors, where each balloon has a color represented by a short lowercase string. The task is to determine whether there exists a color that appears strictly more than half of the total number of balloons. If such a color exists, we output it."
date: "2026-06-28T10:55:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104857
codeforces_index: "F"
codeforces_contest_name: "The 2023 ICPC Asia Hefei Regional Contest (The 2nd Universal Cup. Stage 12: Hefei)"
rating: 0
weight: 104857
solve_time_s: 36
verified: true
draft: false
---

[CF 104857F - Colorful Balloons](https://codeforces.com/problemset/problem/104857/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of balloon colors, where each balloon has a color represented by a short lowercase string. The task is to determine whether there exists a color that appears strictly more than half of the total number of balloons. If such a color exists, we output it. Otherwise, we output the failure string “uh-oh”.

The structure is essentially about dominance in a multiset of strings. We are not asked to list frequencies or compute anything else beyond identifying whether a strict majority element exists and, if so, returning it.

The input size goes up to 100000 strings, each up to length 10. This immediately suggests that any algorithm that compares every pair of strings or repeatedly scans the entire list for each candidate will be too slow. A solution that counts frequencies in linear time using hashing is appropriate, since the total number of operations will be on the order of 100000 insertions and lookups, which is well within typical limits.

A subtle edge case arises when no color crosses the 50% threshold. For example, if the input is three distinct colors like red, blue, yellow, each appearing once, no output color qualifies and the answer must be “uh-oh”. Another edge case is when exactly half the balloons are of one color. For instance, in n = 4, if a color appears exactly 2 times, it does not satisfy the strict “more than half” requirement, so it should not be accepted.

Another important case is when multiple colors exist but one barely crosses the threshold, such as 5 balloons with counts red = 3, green = 2. Only the dominant color is valid, even though others may be frequent.

## Approaches

A direct approach is to count occurrences of each color by scanning the entire list and, for each distinct color, recomputing its frequency by another scan. This would require O(n) work per color, leading to O(n^2) in the worst case when all colors are distinct. With n up to 100000, this is far too slow.

The key observation is that we only care about frequencies aggregated over identical strings. Once we maintain a frequency map while reading input, we can determine the maximum frequency in a single pass. This reduces the problem to counting and then checking whether the maximum count exceeds n/2.

An alternative perspective is that this is a classic majority element problem over strings. While algorithms like Boyer-Moore majority vote exist, they are unnecessary here because a hash map provides a simpler and equally efficient solution given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Counting per Color | O(n^2) | O(1) | Too slow |
| Frequency Map | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a dictionary that stores how many times each color appears while reading the input.

1. Initialize an empty hash map to store frequencies of colors. This allows constant-time updates and queries per string on average.
2. Read each balloon color one by one and increment its count in the map. This ensures that by the end of input processing, we have complete frequency information without needing extra passes.
3. Track the color with the highest frequency as we update the map. This avoids scanning the map afterward and keeps the solution strictly linear.
4. After processing all colors, compare the maximum frequency against n divided by 2. If it is strictly greater, output the corresponding color.
5. Otherwise, output “uh-oh”.

The reason we use a strict comparison is critical: equality with half does not satisfy the problem condition.

### Why it works

At any point during processing, the frequency map exactly reflects the number of occurrences seen so far for each color. The color with maximum frequency at the end is therefore the global maximizer over the entire dataset. Since the condition for correctness depends only on whether a single value exceeds n/2, identifying the maximum frequency is sufficient to decide the answer. No other structural property of the sequence matters.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    freq = {}
    best_color = ""
    best_count = 0

    for _ in range(n):
        c = input().strip()
        freq[c] = freq.get(c, 0) + 1

        if freq[c] > best_count:
            best_count = freq[c]
            best_color = c

    if best_count > n // 2:
        print(best_color)
    else:
        print("uh-oh")

if __name__ == "__main__":
    solve()
```

The solution maintains a dictionary `freq` to count occurrences. The variable `best_count` tracks the largest frequency seen so far, and `best_color` remembers which color achieved it. This avoids a second pass over the dictionary.

A common mistake is using `>= n // 2` instead of `> n // 2`, which incorrectly accepts colors that appear exactly half the time. Another potential pitfall is forgetting to strip newline characters when reading strings, which would cause identical colors to be treated as different keys.

## Worked Examples

### Example 1

Input:

```
5
red
green
red
red
blue
```

| Step | Color | freq(red) | freq(green) | freq(blue) | best_color | best_count |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | red | 1 | 0 | 0 | red | 1 |
| 2 | green | 1 | 1 | 0 | red | 1 |
| 3 | red | 2 | 1 | 0 | red | 2 |
| 4 | red | 3 | 1 | 0 | red | 3 |
| 5 | blue | 3 | 1 | 1 | red | 3 |

The final maximum frequency is 3, and n/2 is 2.5, so red is strictly more than half and is printed.

### Example 2

Input:

```
3
red
blue
yellow
```

| Step | Color | freq(red) | freq(blue) | freq(yellow) | best_color | best_count |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | red | 1 | 0 | 0 | red | 1 |
| 2 | blue | 1 | 1 | 0 | red | 1 |
| 3 | yellow | 1 | 1 | 1 | red | 1 |

Here the maximum frequency is 1, while n/2 is 1.5, so no valid majority exists and the output is “uh-oh”.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each balloon is processed once with O(1) average dictionary operations |
| Space | O(k) | k distinct colors stored in the hash map, worst case k = n |

The constraints allow up to 100000 balloons, so a linear scan with hashing is comfortably efficient. Memory usage is also safe since each string is short and only distinct colors are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""5
red
green
red
red
blue
""") == "red"

# sample 2
assert run("""3
red
blue
yellow
""") == "uh-oh"

# all same
assert run("""4
a
a
a
a
""") == "a"

# exactly half (invalid)
assert run("""4
a
a
b
b
""") == "uh-oh"

# single element
assert run("""1
abc
""") == "abc"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same | a | full dominance case |
| split half | uh-oh | strict majority condition |
| single element | abc | minimal boundary case |

## Edge Cases

One edge case is when all colors are distinct. The frequency map still records each color once, but no value exceeds n/2. For input:

```
4
a
b
c
d
```

the algorithm tracks each frequency as 1, and since 1 is not greater than 2, it correctly outputs “uh-oh”.

Another case is when the majority exists but appears in non-consecutive positions. For example:

```
7
x
y
x
z
x
x
y
```

The frequency of x becomes 4, exceeding 7/2 = 3.5. Even though occurrences are scattered, the map aggregates correctly, and the algorithm outputs x.
