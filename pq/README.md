## MaxPQ

最大堆的简单实现。用于寻找序列中前 K 个最大的元素。

```python
from pq import MaxPQ

max_pq = MaxPQ(max_size=5, key=lambda x: x['n'])

for _ in range(100):
    max_pq.add({
        'n': random.randint(0, 10000)
    })

print(max_pq.values())

# 输出
[{'n': 9864}, {'n': 9530}, {'n': 9472}, {'n': 9404}, {'n': 9359}]
```

`max_size` 指定堆的大小。`key` 用来获取比较的值。
