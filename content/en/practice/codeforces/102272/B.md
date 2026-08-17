---
title: "CF 102272B - \u0110\u1ebfm Th\u1ecf"
description: "Ta có một hàng gồm (N) con thỏ, con thứ (i) có giống được biểu diễn bởi số (typi). Với mỗi đoạn liên tiếp ([l,r]), điểm của đoạn là số lượng giống khác nhau xuất hiện trong các con thỏ từ vị trí (l) đến (r). Bài toán không yêu cầu tìm một đoạn tốt nhất."
date: "2026-08-17T11:13:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102272
codeforces_index: "B"
codeforces_contest_name: "HCW 19 Individual Day 1"
rating: 0
weight: 102272
solve_time_s: 143
verified: false
draft: false
---

[CF 102272B - \u0110\u1ebfm Th\u1ecf](https://codeforces.com/problemset/problem/102272/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Problem Understanding

Ta có một hàng gồm (N) con thỏ, con thứ (i) có giống được biểu diễn bởi số (typ_i). Với mỗi đoạn liên tiếp ([l,r]), điểm của đoạn là số lượng giống khác nhau xuất hiện trong các con thỏ từ vị trí (l) đến (r).

Bài toán không yêu cầu tìm một đoạn tốt nhất. Ta phải cộng điểm của tất cả các đoạn liên tiếp có thể chọn:

[
\sum_{1\le l\le r\le N} f(l,r).
]

Vì vậy, với mỗi đoạn, ta chỉ cần biết bao nhiêu giống khác nhau xuất hiện trong đoạn đó, rồi cộng tất cả các giá trị lại.

Giới hạn (N) lên tới (10^6), và tổng (N) của toàn bộ test không vượt quá (2\cdot10^6). Số đoạn liên tiếp đã là

[
\frac{N(N+1)}2,
]

tức khoảng (5\cdot10^{11}) khi (N=10^6). Chỉ riêng việc duyệt qua từng đoạn đã không thể thực hiện trong giới hạn thời gian. Một thuật toán (O(N^2)) cũng quá chậm, còn (O(N^3)) hoàn toàn không khả thi. Ta cần đưa thời gian xuống (O(N)) cho mỗi test, hoặc ít nhất là gần tuyến tính.

Giá trị (typ_i) có thể lên tới (10^9), nên không thể dùng một mảng có kích thước bằng giá trị giống. Ta cần một cấu trúc ánh xạ giống thỏ sang thông tin liên quan, chẳng hạn như dictionary.

Kết quả cũng có thể rất lớn. Với (N=10^6) và tất cả các con thỏ có giống khác nhau, mọi đoạn có điểm bằng độ dài của nó. Khi đó tổng là

[
1+2+\cdots+N
]

theo từng điểm bắt đầu, tương đương

[
\frac{N(N+1)(N+2)}6
=166667166667000000.
]

Giá trị này vượt xa giới hạn của số nguyên 32 bit. Python dùng số nguyên độ chính xác tùy ý nên không cần xử lý tràn số thủ công.

Một trường hợp biên khác là (N=1). Với input gồm một con thỏ như `5`, chỉ có đoạn ([1,1]), nên đáp án là (1). Cách triển khai dùng chỉ số sai hoặc khởi tạo tổng từ vị trí (0) có thể tạo ra kết quả sai.

Trường hợp tất cả các con thỏ cùng giống cũng dễ gây nhầm. Với `7 7 7`, có sáu đoạn nhưng mỗi đoạn chỉ chứa một giống, nên đáp án là (6), không phải số lượng phần tử đã được duyệt. Khi một giống xuất hiện lại, lần xuất hiện mới phải thay thế đóng góp của lần xuất hiện cũ.

Một lỗi khác thường xuất hiện ở lần xuất hiện đầu tiên của một giống. Với `1 2 1`, khi xử lý con thỏ thứ ba, giống `1` đã xuất hiện tại vị trí (1). Ta phải thay vị trí cuối của `1` từ (1) thành (3), chứ không cộng thêm một giống mới. Đáp án đúng là (9).

## Approaches

Cách trực tiếp nhất là xét từng đoạn ([l,r]), duyệt các phần tử trong đoạn và đưa giống của chúng vào một set. Kích thước của set sau khi duyệt xong chính là số giống khác nhau của đoạn, nên cách này đúng về mặt logic.

Tuy nhiên, tổng số phần tử phải kiểm tra qua tất cả các đoạn là

\frac{N(N+1)(N+2)}6.
]

Với (N=10^6), con số này khoảng (1.67\cdot10^{17}). Ngay cả nếu mỗi thao tác set chỉ mất (O(1)), lượng công việc này vẫn quá lớn. Một biến thể tốt hơn là cố định (l), rồi tăng (r) và duy trì set, nhưng vẫn có (O(N^2)) đoạn phải xét, khoảng (5\cdot10^{11}) đoạn trong trường hợp lớn nhất.

Ta cần thay đổi cách đếm. Thay vì xét từng đoạn và hỏi đoạn đó có bao nhiêu giống, hãy cố định điểm phải (r) và tính tổng điểm của tất cả các đoạn kết thúc tại (r).

Xét một giống cụ thể. Gọi (p) là vị trí xuất hiện cuối cùng của giống đó trong đoạn tiền tố (1,\ldots,r). Một đoạn ([l,r]) chứa giống này khi và chỉ khi (l\le p). Có đúng (p) lựa chọn cho (l), từ (1) đến (p). Vì vậy, giống này đóng góp chính xác (p) vào tổng điểm của tất cả các đoạn kết thúc tại (r).

Đây là mấu chốt của bài toán. Với mỗi (r), nếu biết vị trí xuất hiện cuối cùng của mọi giống đã gặp, tổng điểm của tất cả các đoạn kết thúc tại (r) đơn giản là tổng các vị trí cuối đó.

Khi chuyển từ (r-1) sang (r), chỉ có giống của con thỏ tại vị trí (r) thay đổi vị trí xuất hiện cuối cùng. Nếu giống này chưa từng xuất hiện, ta thêm (r) vào tổng. Nếu nó từng xuất hiện cuối cùng ở vị trí (p), ta thay (p) bằng (r), tức tổng tăng thêm (r-p). Như vậy mỗi phần tử chỉ được xử lý một lần.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) nếu duyệt lại từng đoạn | (O(N)) | Too slow |
| Duy trì set cho từng điểm bắt đầu | (O(N^2)) | (O(N)) | Too slow |
| Optimal | (O(N)) trung bình | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Duyệt các con thỏ từ trái sang phải. Dùng dictionary `last` để lưu vị trí xuất hiện cuối cùng của mỗi giống.
2. Duy trì biến `current`, là tổng vị trí xuất hiện cuối cùng của tất cả các giống đã xuất hiện trong đoạn tiền tố hiện tại.

Nếu đang ở vị trí (r), `current` chính là tổng điểm của mọi đoạn có dạng ([l,r]). Lý do là mỗi giống có vị trí cuối cùng (p), và nó xuất hiện trong đúng (p) đoạn kết thúc tại (r), tương ứng với (l=1,\ldots,p).
3. Khi gặp giống `x` ở vị trí (r), kiểm tra `last[x]`.

Nếu `x` chưa xuất hiện, giống này chưa có đóng góp trong `current`, nên ta cộng (r).

Nếu `x` đã xuất hiện cuối cùng ở vị trí (p), đóng góp cũ của nó là (p), còn đóng góp mới là (r). Vì vậy ta chỉ cần cộng (r-p) vào `current`.
4. Cập nhật `last[x] = r`. Sau thao tác này, dictionary phản ánh chính xác vị trí cuối cùng của từng giống trong prefix (1,\ldots,r).
5. Cộng `current` vào đáp án. `current` là tổng điểm của tất cả các đoạn kết thúc tại (r), nên cộng nó qua mọi (r) sẽ thu được tổng điểm của toàn bộ các đoạn.
6. Lặp lại cho đến vị trí (N), rồi in đáp án.

### Why it works

Sau khi xử lý vị trí (r), với mỗi giống xuất hiện trong prefix (1,\ldots,r), dictionary lưu vị trí xuất hiện cuối cùng (p). Một đoạn ([l,r]) chứa giống đó chính xác khi (l\le p), nên giống đó xuất hiện trong đúng (p) đoạn kết thúc tại (r). Do đó `current` bằng tổng số lần xuất hiện của tất cả các giống trên toàn bộ các đoạn kết thúc tại (r), cũng chính là tổng số giống khác nhau của những đoạn đó. Khi cộng `current` vào đáp án ở mọi (r), mỗi cặp ((l,r)) được tính đúng một lần và mỗi giống trong đoạn được tính đúng một lần.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    answers = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        last = {}
        current = 0
        answer = 0

        for r, x in enumerate(a, 1):
            old = last.get(x)

            if old is None:
                current += r
            else:
                current += r - old

            last[x] = r
            answer += current

        answers.append(str(answer))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

`last` lưu vị trí xuất hiện cuối cùng của mỗi giống, đúng với bước 1 và bước 3 của thuật toán. Dictionary được dùng vì giá trị giống có thể lên tới (10^9), nên không thể dùng trực tiếp một mảng chỉ số theo `typ`.

Biến `current` được cập nhật trước khi cộng vào `answer`. Ở vị trí (r), nó phải mô tả các đoạn kết thúc đúng tại (r), không phải các đoạn kết thúc tại (r-1).

Biểu thức `current += r - old` là phần dễ sai nhất. Nếu một giống trước đó xuất hiện tại `old`, các đoạn có (l\le old) đã chứa giống này trước khi thêm phần tử thứ (r). Các lựa chọn mới là (l=old+1,\ldots,r), có đúng (r-old) lựa chọn, nên đóng góp tăng đúng lượng đó.

Với lần xuất hiện đầu tiên, `old` không tồn tại và giống mới đóng góp (r), vì mọi đoạn ([l,r]) với (l\le r) đều chứa nó.

Chỉ số `r` bắt đầu từ (1) nhờ `enumerate(a, 1)`. Điều này làm cho vị trí cuối cùng có thể dùng trực tiếp làm số lượng lựa chọn của (l), tránh phải cộng hoặc trừ (1) ở nhiều nơi.

Python không bị giới hạn số nguyên 64 bit, nên `answer` có thể chứa kết quả lớn nhất mà không cần kiểu dữ liệu đặc biệt.

Một chi tiết về input là đề cho tổng (N) trên tất cả test không quá (2\cdot10^6). Vì vậy việc đọc từng test và xử lý tuyến tính là phù hợp. Dictionary cũng được tạo mới cho từng test để không giữ dữ liệu của test trước.

## Worked Examples

### Sample case 1

Với mảng `1 2 3`, mỗi con thỏ có một giống riêng. Ta có các trạng thái sau:

| (r) | `x` | `last` sau cập nhật | `current` | `answer` |
| --- | --- | --- | --- | --- |
| 1 | 1 | `{1: 1}` | 1 | 1 |
| 2 | 2 | `{1: 1, 2: 2}` | 3 | 4 |
| 3 | 3 | `{1: 1, 2: 2, 3: 3}` | 6 | 10 |

Ở vị trí 1 có một đoạn kết thúc tại 1 và nó chứa một giống, nên `current = 1`. Sang vị trí 2, có hai giống với vị trí cuối lần lượt là 1 và 2, nên tổng là (3). Sang vị trí 3, tổng là (1+2+3=6). Cộng lại được (1+3+6=10), đúng sample.

### Sample case 2

Với mảng `1 2 2 3`, trạng thái chi tiết là:

| (r) | `x` | `old` | `current` sau cập nhật | `answer` |
| --- | --- | --- | --- | --- |
| 1 | 1 | chưa có | 1 | 1 |
| 2 | 2 | chưa có | 3 | 4 |
| 3 | 2 | 2 | 4 | 8 |
| 4 | 3 | chưa có | 7 | 15 |

Ở (r=3), giống `2` xuất hiện lại. Trước đó vị trí cuối của nó là 2, nên đóng góp của giống `2` đổi từ 2 thành 3. Vì vậy `current` tăng đúng (3-2=1), từ 3 thành 4.

Ở (r=4), giống `3` xuất hiện lần đầu và đóng góp thêm 4. `current` trở thành (1+3+4=8). Tổng cuối cùng là (1+3+4+8=16), đúng kết quả mẫu.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) trung bình | Mỗi con thỏ thực hiện một lần tra cứu và cập nhật dictionary |
| Space | (O(N)) | Dictionary có nhiều nhất một phần tử cho mỗi giống khác nhau |

Vì tổng (N) của tất cả test không vượt quá (2\cdot10^6), tổng số thao tác là tuyến tính theo kích thước input. Đây là sự khác biệt quyết định so với (O(N^2)), vốn có thể phải xử lý hàng trăm tỷ đoạn khi (N=10^6). Bộ nhớ (O(N)) cũng nằm trong giới hạn 512 MB với cách lưu một vị trí cuối cho mỗi giống.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    answers = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        last = {}
        current = 0
        answer = 0

        for r, x in enumerate(a, 1):
            old = last.get(x)

            if old is None:
                current += r
            else:
                current += r - old

            last[x] = r
            answer += current

        answers.append(str(answer))

    sys.stdout.write("\n".join(answers))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    try:
        solve()
        return output.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run(
    """2
3
1 2 3
4
1 2 2 3
"""
) == "10\n16\n", "provided samples"

# Minimum size
assert run(
    """1
1
5
"""
) == "1\n", "single rabbit"

# All rabbits have the same type
assert run(
    """1
3
7 7 7
"""
) == "6\n", "all equal"

# Repeated type with a gap
assert run(
    """1
3
1 2 1
"""
) == "9\n", "repeated type"

# Large answer and all distinct types
assert run(
    """1
5
1 2 3 4 5
"""
) == "35\n", "all distinct"

# Maximum-size test, all equal
n = 1_000_000
expected = n * (n + 1) // 2
inp = "1\n" + str(n) + "\n" + ("7 " * (n - 1)) + "7\n"
assert run(inp) == str(expected) + "\n", "maximum N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 5` | `1` | Kích thước nhỏ nhất và xử lý biên của vị trí đầu tiên |
| `1 / 3 / 7 7 7` | `6` | Cùng một giống xuất hiện liên tục, kiểm tra việc thay thế vị trí cuối |
| `1 / 3 / 1 2 1` | `9` | Giống xuất hiện lại sau một khoảng cách, kiểm tra `r - old` |
| `1 / 5 / 1 2 3 4 5` | `35` | Tất cả giống khác nhau, kiểm tra tổng đóng góp tăng dần |
| (N=10^6), tất cả bằng `7` | `500000500000` | Giới hạn lớn nhất, thời gian tuyến tính và khả năng xử lý đáp án lớn |

## Edge Cases

Với (N=1), input

```
1
1
5
```

dictionary ban đầu rỗng. Tại (r=1), giống `5` chưa xuất hiện nên `current` tăng từ 0 lên 1. Sau đó `answer` cũng trở thành 1. Chỉ có một đoạn ([1,1]), và nó chứa đúng một giống, nên kết quả là `1`.

Với tất cả các con thỏ cùng giống, chẳng hạn

```
1
3
7 7 7
```

tại (r=1), `current=1`. Tại (r=2), vị trí cũ của `7` là 1 nên `current` tăng (2-1=1), trở thành 2. Tại (r=3), nó tăng (3-2=1), trở thành 3. Tổng là (1+2+3=6). Mỗi đoạn chỉ có một giống, và có tổng cộng sáu đoạn, nên kết quả khớp.

Với giống xuất hiện lại sau một khoảng cách, xét

```
1
3
1 2 1
```

sau vị trí 1, `current=1`. Sau vị trí 2, hai giống có vị trí cuối là 1 và 2, nên `current=3`. Tại vị trí 3, giống `1` có vị trí cuối cũ là 1 và vị trí mới là 3. Đóng góp của nó tăng từ 1 lên 3, nên `current` tăng thêm 2, thành 5. Tổng đáp án là (1+3+5=9). Điều này cũng tương ứng trực tiếp với các điểm của sáu đoạn, lần lượt là (1,2,2,1,2,1).

Với tất cả giống khác nhau và (N=5),

```
1
5
1 2 3 4 5
```

`current` lần lượt là (1,3,6,10,15), vì ở mỗi prefix mọi vị trí cuối đều khác nhau. Đáp án là (35), đúng với tổng độ dài của tất cả các đoạn. Trường hợp này kiểm tra rằng thuật toán không vô tình xem các giống mới là chỉ đóng góp 1, trong khi một giống xuất hiện lần đầu tại vị trí (r) thực tế đóng góp (r) đoạn kết thúc tại (r).

Với (N=10^6) và tất cả giống đều bằng `7`, dictionary chỉ chứa một phần tử trong suốt quá trình chạy. Mỗi vị trí chỉ thực hiện một lần tra cứu và một lần cập nhật, nên vẫn là (O(N)). `current` lần lượt tăng 1 ở mỗi bước và đáp án cuối cùng là

500000500000.
]

Trường hợp này vừa kiểm tra giới hạn kích thước input, vừa kiểm tra việc không dùng (O(N^2)) bộ nhớ hay thời gian khi số lượng giống khác nhau rất nhỏ.
