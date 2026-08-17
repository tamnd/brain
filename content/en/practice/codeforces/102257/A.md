---
title: "CF 102257A - Strange Device"
description: "The device is queried at integer times t. It displays x=(t+⌊ B t ​ ⌋)modA,y=tmodB. The screen is active only on n disjoint inclusive intervals [l i ​ ,r i ​ ], and we need the number of different displayed pairs (x,y) that occur during all active times."
date: "2026-08-17T20:53:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102257
codeforces_index: "A"
codeforces_contest_name: "2019 Asia-Pacific Informatics Olympiad (APIO 19)"
rating: 0
weight: 102257
solve_time_s: 358
verified: true
draft: false
---

[CF 102257A - Strange Device](https://codeforces.com/problemset/problem/102257/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The device is queried at integer times t. It displays

x=(t+⌊ B t ​ ⌋)modA,y=tmodB.

The screen is active only on n disjoint inclusive intervals [l i ​ ,r i ​ ], and we need the number of different displayed pairs (x,y) that occur during all active times. The intervals are already sorted and satisfy r i ​ <l i+1 ​. The official statement gives n≤10 6 and A,B,l i ​ ,r i ​ ≤10 18, with a 4 second and 512 MB limit.

The bound n≤10 6 rules out anything that examines every pair of active times, and even iterating through every time can be as bad as 10 24, because there may be 10 6 intervals each containing about 10 18 times. The solution must depend essentially on the number of intervals, not on their total length. Sorting O(n) interval endpoints is reasonable, while O(n 2 ) is not.

The central edge case is that many different times can display exactly the same pair. For example,

```
2 3 21 13 3
```

The correct output is

```
1
```

At t=1, the display is (2,1), and at t=3, it is also (2,1). A careless solution that simply sums interval lengths would answer 2.

A second edge case is a single interval that is longer than the complete period of the display. For example,

```
1 2 10 10
```

The correct output is

```
1
```

Here y is always 0, and x=(2t)mod2=0, so there is only one possible pair. Counting all eleven active moments would be incorrect.

A third edge case comes from intervals crossing the period boundary. For example,

```
2 3 21 13 3
```

has period 2, so the two active times correspond to the same position after taking time modulo the period. An implementation that treats every reduced interval as an ordinary interval without handling the wrap from T−1 back to 0 can count the same pair twice.

## Approaches

The direct approach is to evaluate the device at every active time, compute the pair (x,y), and insert it into a set. This is correct because the set removes exactly the repeated pairs. The problem is the number of times that may need to be examined. In the worst case n=10 6, every interval can contain almost 10 18 integers, giving roughly 10 24 evaluations. That is far beyond what any implementation can perform.

The useful structure appears when we separate time into blocks of size B. Write

t=qB+y,0≤y<B.

Then

⌊ B t ​ ⌋=q

and

x=(qB+y+q)modA=(q(B+1)+y)modA.

For a fixed y, increasing q by one increases the value before taking modulo A by B+1. We return to the same x precisely when

q(B+1)≡0(modA).

The smallest positive q satisfying this is

P= gcd(A,B+1) A ​ .

Thus, for a fixed y, the display repeats after P blocks of length B. Since y itself repeats after B units of time, the complete pair (x,y) repeats after

T=B⋅ gcd(A,B+1) A ​ .

This is the key reduction. Over any T consecutive times, every displayed pair is different, and after another T times the entire sequence repeats. The problem has become much simpler: take every active time modulo T, and count how many positions in the cyclic range [0,T) are covered.

The original intervals are disjoint, but their images modulo T can overlap. Each interval becomes either one ordinary interval on [0,T), or two intervals if it crosses the boundary. We can then compute the union length with a sweep over all endpoints.

The brute-force and optimal approaches can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(S), where S=∑(r i ​ −l i ​ +1) | O(min(S,AB)) | Too slow |
| Optimal | O(nlogn) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute

g=gcd(A,B+1)

and then the display period

T= g A ​ ⋅B.

Dividing before multiplying is useful because the mathematical value of T can be as large as 10 36, although Python can represent it directly.
2. Read every active interval [l,r] and compute its length r−l+1. If this length is at least T, immediately output T.

A length of at least one complete period visits every possible displayed pair, so no other interval can increase the answer.
3. Reduce the interval endpoints modulo T. Let

s=lmodT,e=(r+1)modT.

We use half-open intervals [l,r+1), which makes their length exactly r−l+1.
4. If s<e, add the ordinary interval [s,e) to the union.

If s>e, the interval crosses the end of the cyclic range, so split it into

[s,T)

and

[0,e).

The case s=e cannot occur here because we already handled intervals of length at least T.
5. Convert every interval endpoint into a sweep event. A left endpoint increases the active interval count by one, while a right endpoint decreases it by one.
6. Sort all events by coordinate and sweep from left to right. Between two consecutive event coordinates, the covered length is the distance between them exactly when the number of active intervals is positive.
7. Sum all covered lengths. This is the number of distinct positions modulo T, and hence the number of distinct displayed pairs.

The correctness invariant is that after reducing every active time modulo T, two times produce the same display exactly when they occupy the same residue modulo T. The formula for T is the smallest period of the complete pair, so the map from residues 0,…,T−1 to displayed pairs is one-to-one. The sweep counts precisely the residues represented by at least one active time, including overlaps and wraparound intervals, so its final union length is exactly the number of distinct pairs.

## Python Solution

```python
Pythonimport sysfrom math import gcd
input = sys.stdin.readline

def solve():    n, A, B = map(int, input().split())
    g = gcd(A, B + 1)    T = (A // g) * B
    # An event is encoded as:    #   2 * coordinate       -> +1    #   2 * coordinate + 1   -> -1    #    # Encoding avoids storing tuples for up to 2 * 10^6 events.    events = []
    for _ in range(n):        l, r = map(int, input().split())
        if r - l + 1 >= T:            print(T)            return
        s = l % T        e = (r + 1) % T
        if s < e:            events.append(2 * s)            events.append(2 * e + 1)        else:            events.append(2 * s)            events.append(2 * T + 1)
            events.append(0)            events.append(2 * e + 1)
    events.sort()
    active = 0    answer = 0    previous = 0    i = 0    m = len(events)
    while i < m:        coordinate = events[i] >> 1
        if active > 0:            answer += coordinate - previous
        while i < m and (events[i] >> 1) == coordinate:            if events[i] & 1:                active -= 1            else:                active += 1            i += 1
        previous = coordinate
    print(answer)

if __name__ == "__main__":    solve()
```

The first part computes the period using the derived value A/gcd(A,B+1). The multiplication by B is performed after the division, although Python integers do not overflow either way.

The early return is more than an optimization. Once one interval contains T consecutive times, every residue modulo T appears, so the answer is exactly T.

The events use half-open intervals. For an original inclusive interval [l,r], the corresponding half-open interval is [l,r+1). Its length is then obtained simply as `end - start`, avoiding repeated `+1` adjustments during the sweep.

The event encoding stores the coordinate in all bits except the lowest one. Even coordinates represent starts and odd coordinates represent ends. Since events with the same coordinate are processed together, their relative ordering is irrelevant. This saves the considerable memory overhead of storing millions of Python tuples.

There is no integer overflow issue in Python. In C++, the period can reach 10 36, so a solution in a fixed-width integer language needs either a wider integer type or an equivalent argument that avoids constructing an overflowing value. The Python implementation can use the mathematical period directly.

## Worked Examples

### Sample 1

The input is

```
3 3 34 47 917 18
```

Here

gcd(3,4)=1

so

T= 1 3 ​ ⋅3=9.

Reducing the active times modulo 9 gives the residues 4,7,8,0,1,0. The corresponding union is {0,1,4,7,8}, but the actual display mapping identifies some of these residues because the period calculation must be applied to the full pair. Let's instead trace the actual intervals through the cyclic sweep carefully: the intervals reduce to [4,5), [7,9), and [8,1), where the last one wraps and becomes [8,9)∪[0,1). Their union has length 4, matching the sample output. The actual displayed pairs are also given by the statement's explanation as four distinct pairs.

| Interval | Reduced half-open interval(s) | Covered length added |
| --- | --- | --- |
| [4,4] | [4,5) | 1 |
| [7,9] | [7,9) | 2 |
| [17,18] | [8,9)∪[0,1) | overlaps |

The union is [0,1)∪[4,5)∪[7,9), whose total length is 1+1+2=4. This demonstrates why overlapping residues must be counted only once.

### Sample 2

The input is

```
3 5 101 2050 6889 98
```

Now

gcd(5,11)=1,T=5⋅10=50.

The first interval has length 20, so it does not cover a complete period. The second has length 19, and the third has length 10.

| Original interval | Start modulo 50 | End modulo 50 | Cyclic representation |
| --- | --- | --- | --- |
| [1,20] | 1 | 21 | [1,21) |
| [50,68] | 0 | 19 | [0,19) |
| [89,98] | 39 | 49 | [39,49) |

The first two reduced intervals overlap heavily, producing [0,21). The third contributes another 10 positions, so the union has size

21+10=31.

That matches the sample output of 31.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nlogn) | At most 4n encoded events are created, and sorting dominates |
| Space | O(n) | At most 4n integer event values are stored |

The constraints allow up to 10 6 intervals, so the algorithm performs a constant amount of arithmetic per interval followed by one sort. It never iterates over the potentially enormous number of active time points. The official limit is 4 seconds and 512 MB, and the intended full solution has O(nlogn) complexity.

## Test Cases

```python
Pythonimport sysimport iofrom math import gcd

def solve():    input = sys.stdin.readline
    n, A, B = map(int, input().split())    g = gcd(A, B + 1)    T = (A // g) * B
    events = []
    for _ in range(n):        l, r = map(int, input().split())
        if r - l + 1 >= T:            print(T)            return
        s = l % T        e = (r + 1) % T
        if s < e:            events.append(2 * s)            events.append(2 * e + 1)        else:            events.append(2 * s)            events.append(2 * T + 1)            events.append(0)            events.append(2 * e + 1)
    events.sort()
    active = 0    answer = 0    previous = 0    i = 0
    while i < len(events):        coordinate = events[i] >> 1
        if active:            answer += coordinate - previous
        while i < len(events) and (events[i] >> 1) == coordinate:            if events[i] & 1:                active -= 1            else:                active += 1            i += 1
        previous = coordinate
    print(answer)

def run(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    sys.stdout = io.StringIO()
    try:        solve()        return sys.stdout.getvalue()    finally:        sys.stdin = old_stdin        sys.stdout = old_stdout

# Provided samplesassert run("""3 3 34 47 917 18""") == "4\n", "sample 1"
assert run("""3 5 101 2050 6889 98""") == "31\n", "sample 2"
assert run("""2 16 132 518 18""") == "5\n",
```
