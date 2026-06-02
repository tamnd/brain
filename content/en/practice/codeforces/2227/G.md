---
title: "CF 2227G - Drowning"
description: "Ta có một mảng số nguyên dương. Một phép giảm chọn ba phần tử liên tiếp sao cho phần tử giữa nhỏ hơn tổng hai phần tử hai bên. Khi đó bộ ba $$(c{i-1},ci,c{i+1})$$ được thay bằng một giá trị duy nhất $$x=c{i-1}-ci+c{i+1}.$$ Mỗi lần thực hiện, độ dài mảng giảm đi đúng 2."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 2227
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1096 (Div. 3)"
rating: 0
weight: 2227
solve_time_s: 177
verified: false
draft: false
---

[CF 2227G - Drowning](https://codeforces.com/problemset/problem/2227/G)

**Rating:** -  
**Tags:** binary search, data structures, math  
**Solve time:** 2m 57s  
**Verified:** no  

## Solution
## Problem Understanding

Ta có một mảng số nguyên dương. Một phép giảm chọn ba phần tử liên tiếp sao cho phần tử giữa nhỏ hơn tổng hai phần tử hai bên. Khi đó bộ ba

$$(c_{i-1},c_i,c_{i+1})$$

được thay bằng một giá trị duy nhất

$$x=c_{i-1}-c_i+c_{i+1}.$$

Mỗi lần thực hiện, độ dài mảng giảm đi đúng 2.

Một đoạn con được gọi là tốt nếu có thể áp dụng các phép giảm nhiều lần để cuối cùng chỉ còn lại đúng một phần tử. Nhiệm vụ là đếm bao nhiêu đoạn con của mảng ban đầu là tốt.

Điểm khó nằm ở chỗ định nghĩa của phép biến đổi có vẻ rất cục bộ, nhưng số cách thực hiện lại khổng lồ. Với $n$ lên tới $2\cdot 10^5$, tổng $n$ trên tất cả test cũng đạt $2\cdot 10^5$, nên mọi lời giải dạng xét từng đoạn con rồi mô phỏng đều không khả thi. Ta cần một đặc trưng toàn cục cho phép nhận biết ngay một đoạn con có tốt hay không.

Một tình huống dễ bỏ sót là các đoạn có độ dài chẵn. Vì mỗi phép giảm làm độ dài giảm đúng 2, tính chẵn lẻ của độ dài không bao giờ thay đổi. Muốn kết thúc ở độ dài 1 thì độ dài ban đầu bắt buộc phải là số lẻ.

Ví dụ với mảng:

```
[1, 1]
```

không có cách nào giảm xuống một phần tử dù mọi giá trị đều nhỏ.

Một tình huống khác là đoạn dài 3. Khi đó chỉ có đúng một phép có thể thực hiện, nên điều kiện trở thành:

```
a1 + a3 > a2
```

Ví dụ:

```
[10, 20, 10]
```

không tốt vì $10+10=20$, không phải bất đẳng thức nghiêm.

Điều nguy hiểm nhất là nghĩ rằng chỉ cần tồn tại một bước hợp lệ là đủ. Chẳng hạn:

```
[100, 1, 1]
```

có một phép hợp lệ và sau khi giảm sẽ còn một phần tử. Đoạn này tốt. Nhưng để xử lý các đoạn dài lớn hơn, ta cần một tiêu chuẩn mạnh hơn nhiều.

## Approaches

Ý tưởng brute force tự nhiên nhất là xét mọi đoạn con. Với mỗi đoạn có độ dài lẻ, ta thử tất cả các chuỗi phép giảm có thể xảy ra để kiểm tra xem có thể về một phần tử hay không.

Cách này đúng vì nó duyệt toàn bộ không gian trạng thái. Vấn đề là số trạng thái tăng theo cấp số nhân. Chỉ riêng việc có $O(n^2)$ đoạn con đã khiến bài toán không thể xử lý ở $n=2\cdot10^5$.

Điểm đột phá nằm ở việc quan sát một đại lượng bất biến.

Định nghĩa tổng luân phiên:

$$S(c)=c_1-c_2+c_3-c_4+\cdots$$

Khi thay

$$(c_{i-1},c_i,c_{i+1})$$

bởi

$$x=c_{i-1}-c_i+c_{i+1},$$

đóng góp của ba phần tử này trong tổng luân phiên chính xác bằng đóng góp của phần tử mới. Vì thế tổng luân phiên không đổi sau mọi phép biến đổi.

Nếu một mảng được giảm thành một phần tử dương duy nhất, thì tổng luân phiên cuối cùng chắc chắn dương. Do bất biến, tổng luân phiên ban đầu cũng phải dương. Đây là điều kiện cần.

Điều bất ngờ là điều kiện đó cũng là điều kiện đủ. Ta có thể chứng minh rằng với một mảng độ dài lẻ, nếu tổng luân phiên dương thì luôn tồn tại ít nhất một phép hợp lệ. Sau khi thực hiện phép đó, tổng luân phiên vẫn dương, và ta tiếp tục quy nạp cho tới khi còn một phần tử.

Vì thế một đoạn con là tốt khi và chỉ khi:

1. Độ dài của nó là lẻ.
2. Tổng luân phiên của nó dương.

Lúc này bài toán trở thành đếm các đoạn con độ dài lẻ có tổng luân phiên dương.

Ta đưa tổng luân phiên về dạng prefix sum và đếm các cặp chỉ số bằng Fenwick Tree sau khi nén tọa độ.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential hoặc tệ hơn $O(n^3)$ | Rất lớn | Too slow |
| Optimal | $O(n\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Bước 1

Xây dựng prefix alternating sum:

$$pref[0]=0$$

$$pref[i]=a_1-a_2+a_3-\cdots+(-1)^{i-1}a_i.$$

Khi đó mọi tổng luân phiên của đoạn con đều có thể tính từ hai giá trị prefix.

### Bước 2

Xét một đoạn con $[l,r]$ có độ dài lẻ.

Độ dài lẻ tương đương với $l$ và $r$ cùng parity.

Nếu $l$ lẻ:

$$alt(l,r)=pref[r]-pref[l-1].$$

Ta cần:

$$pref[r]>pref[l-1].$$

Nếu $l$ chẵn:

$$alt(l,r)=pref[l-1]-pref[r].$$

Ta cần:

$$pref[r]<pref[l-1].$$

### Bước 3

Đặt:

$$p=l-1.$$

Khi đó:

Nếu $r$ lẻ thì $p$ là chẵn và ta cần

$$pref[p]<pref[r].$$

Nếu $r$ chẵn thì $p$ là lẻ và ta cần

$$pref[p]>pref[r].$$

Bài toán trở thành đếm các cặp $(p,r)$ với parity xác định và bất đẳng thức trên giá trị prefix.

### Bước 4

Nén tọa độ toàn bộ giá trị $pref[i]$.

Giá trị có thể lớn tới khoảng $2\cdot10^{14}$, nhưng chỉ có $n+1$ giá trị khác nhau cần xét.

### Bước 5

Duy trì hai Fenwick Tree.

Fenwick thứ nhất lưu các prefix ở chỉ số chẵn.

Fenwick thứ hai lưu các prefix ở chỉ số lẻ.

Khi đang xử lý vị trí $r$:

Nếu $r$ lẻ, cần số lượng chỉ số chẵn trước đó có:

$$pref[p]<pref[r].$$

Đó là truy vấn đếm phần tử nhỏ hơn giá trị hiện tại trong Fenwick chẵn.

Nếu $r$ chẵn, cần số lượng chỉ số lẻ trước đó có:

$$pref[p]>pref[r].$$

Ta lấy:

$$\text{tổng phần tử lẻ đã thấy} - \text{số phần tử}\le pref[r].$$

### Bước 6

Sau khi cộng đóng góp của vị trí $r$, chèn $pref[r]$ vào Fenwick tương ứng với parity của $r$.

### Why it works

Tổng luân phiên là bất biến của mọi phép giảm. Một đoạn con tốt bắt buộc có tổng luân phiên dương và độ dài lẻ. Ngược lại, với độ dài lẻ, nếu tổng luân phiên dương thì luôn tồn tại một phép hợp lệ, nên có thể quy nạp giảm dần tới độ dài 1. Vì vậy điều kiện "độ dài lẻ và tổng luân phiên dương" là tương đương với "đoạn con tốt".

Biến đổi sang mảng prefix cho phép biểu diễn tổng luân phiên của mọi đoạn bằng quan hệ giữa hai giá trị prefix. Fenwick Tree đếm chính xác số cặp chỉ số thỏa bất đẳng thức tương ứng, nên tổng số cặp đếm được chính là số đoạn con tốt.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        n = self.n
        while idx <= n:
            self.bit[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pref = [0] * (n + 1)

        for i in range(1, n + 1):
            if i & 1:
                pref[i] = pref[i - 1] + a[i - 1]
            else:
                pref[i] = pref[i - 1] - a[i - 1]

        vals = sorted(set(pref))
        m = len(vals)

        def get_id(x):
            return 1 + __import__("bisect").bisect_left(vals, x)

        even_bit = Fenwick(m)
        odd_bit = Fenwick(m)

        even_cnt = 0
        odd_cnt = 0

        ans = 0

        idx0 = get_id(pref[0])
        even_bit.add(idx0, 1)
        even_cnt = 1

        for r in range(1, n + 1):
            pos = get_id(pref[r])

            if r & 1:
                ans += even_bit.sum(pos - 1)
            else:
                ans += odd_cnt - odd_bit.sum(pos)

            if r & 1:
                odd_bit.add(pos, 1)
                odd_cnt += 1
            else:
                even_bit.add(pos, 1)
                even_cnt += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

Phần đầu tiên xây dựng mảng `pref`, chính là tổng luân phiên của tiền tố.

Sau đó ta nén tọa độ vì các giá trị prefix có thể rất lớn. Fenwick Tree chỉ cần biết thứ tự tương đối giữa các giá trị nên nén tọa độ là đủ.

Hai Fenwick Tree được tách theo parity của chỉ số prefix. Đây là chi tiết quan trọng nhất. Điều kiện của bài toán không chỉ phụ thuộc vào giá trị prefix mà còn phụ thuộc vào parity của hai đầu đoạn con.

Với chỉ số lẻ, ta đếm số prefix chẵn trước đó nhỏ hơn giá trị hiện tại. Với chỉ số chẵn, ta đếm số prefix lẻ trước đó lớn hơn giá trị hiện tại.

Mọi phép tính đều dùng số nguyên 64 bit. Trong Python điều này tự động an toàn.

## Worked Examples

### Example 1

```
a = [10, 20, 10]
```

Prefix:

$$pref=[0,10,-10,0]$$

| r | pref[r] | Parity of r | Query result | Total answer |
| --- | --- | --- | --- | --- |
| 1 | 10 | Odd | 1 | 1 |
| 2 | -10 | Even | 1 | 2 |
| 3 | 0 | Odd | 1 | 3 |

Kết quả là 3.

Ba đoạn tốt chính là ba đoạn độ dài 1. Đoạn `[10,20,10]` có tổng luân phiên bằng 0 nên không được tính.

### Example 2

```
a = [1,1,1,1,1]
```

Prefix:

$$[0,1,0,1,0,1]$$

| r | pref[r] | Parity | Query result | Total |
| --- | --- | --- | --- | --- |
| 1 | 1 | Odd | 1 | 1 |
| 2 | 0 | Even | 1 | 2 |
| 3 | 1 | Odd | 2 | 4 |
| 4 | 0 | Even | 2 | 6 |
| 5 | 1 | Odd | 3 | 9 |

Đáp án cuối cùng là 9.

Ví dụ này cho thấy những đoạn độ dài 3 và độ dài 5 đều được đếm chính xác thông qua điều kiện tổng luân phiên dương.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Nén tọa độ và mỗi prefix thực hiện vài thao tác Fenwick |
| Space | $O(n)$ | Prefix, mảng nén và Fenwick |

Tổng $n$ trên tất cả test chỉ là $2\cdot10^5$. Với độ phức tạp $O(n\log n)$, số thao tác thực tế nằm rất xa giới hạn thời gian 2 giây.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    from bisect import bisect_left

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, val):
            while idx <= self.n:
                self.bit[idx] += val
                idx += idx & -idx

        def sum(self, idx):
            res = 0
            while idx > 0:
                res += self.bit[idx]
                idx -= idx & -idx
            return res

    data = io.StringIO(inp)
    t = int(data.readline())
    out = []

    for _ in range(t):
        n = int(data.readline())
        a = list(map(int, data.readline().split()))

        pref = [0]
        cur = 0
        for i, x in enumerate(a, start=1):
            cur += x if i & 1 else -x
            pref.append(cur)

        vals = sorted(set(pref))
        m = len(vals)

        even = Fenwick(m)
        odd = Fenwick(m)

        even_cnt = 1
        odd_cnt = 0

        p0 = bisect_left(vals, pref[0]) + 1
        even.add(p0, 1)

        ans = 0

        for r in range(1, n + 1):
            pos = bisect_left(vals, pref[r]) + 1

            if r & 1:
                ans += even.sum(pos - 1)
            else:
                ans += odd_cnt - odd.sum(pos)

            if r & 1:
                odd.add(pos, 1)
                odd_cnt += 1
            else:
                even.add(pos, 1)
                even_cnt += 1

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run(
"""4
3
10 20 10
5
1 1 1 1 1
4
5 1 5 1
1
100
"""
) == "3\n9\n5\n1"

# custom cases
assert run(
"""1
1
7
"""
) == "1"

assert run(
"""1
2
1 1
"""
) == "2"

assert run(
"""1
3
1 100 1
"""
) == "3"

assert run(
"""1
5
2 2 2 2 2
"""
) == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[7]` | `1` | Kích thước nhỏ nhất |
| `[1,1]` | `2` | Đoạn độ dài chẵn không được tính |
| `[1,100,1]` | `3` | Tổng luân phiên không dương |
| `[2,2,2,2,2]` | `9` | Nhiều prefix trùng nhau |

## Edge Cases

### Độ dài chẵn

Input:

```
1
2
1 1
```

Không có phép nào làm độ dài 2 trở thành độ dài 1 vì mỗi lần chỉ giảm đi đúng 2 phần tử. Thuật toán cũng không đếm đoạn `[1,1]` vì điều kiện parity của hai đầu đoạn không được thỏa.

Kết quả:

```
2
```

chỉ gồm hai đoạn đơn.

### Tổng luân phiên bằng 0

Input:

```
1
3
10 20 10
```

Tổng luân phiên của cả đoạn là:

$$10-20+10=0.$$

Điều kiện cần là phải dương, nên đoạn độ dài 3 không được tính. Thuật toán chỉ đếm ba đoạn độ dài 1.

Kết quả:

```
3
```

### Tổng luân phiên dương nhưng có vẻ khó giảm

Input:

```
1
5
1 1 1 1 1
```

Tổng luân phiên của toàn bộ đoạn là:

$$1-1+1-1+1=1.$$

Điều kiện lý thuyết khẳng định đoạn này tốt. Thật vậy:

```
[1,1,1,1,1]
→ [1,1,1]
→ [1]
```

Thuật toán đếm chính xác đoạn độ dài 5 cùng các đoạn độ dài 3 và độ dài 1, cho đáp án 9.
