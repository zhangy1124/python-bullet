# awk - 快闪

### 内建变量

- NR：已输入记录的条数。 (行数量)
- FNR: 当前记录数，与NR不同的是，这个值会是各个文件自己的行号。
- NF：当前记录中域的个数。记录中最后一个域可以以$NF的方式引用。 (每一行记录个数)
- FILENAME：当前输入文件的文件名。
- FS：“域分隔符”，用于将输入记录分割成域。其默认值为“空白字符”，即空格和制表符。FS可以替换为其它字符，从而改变域分隔符。
- RS：当前的“记录分隔符”。默认状态下，输入的每行都被作为一个记录，因此默认记录分隔符是换行符。
- OFS：“输出域分隔符”，即分隔print命令的参数的符号。其默认值为空格。
- ORS：“输出记录分隔符”，即每个print命令之间的符号。其默认值为换行符。
- OFMT：“输出数字格式”（Format for numeric output），其默认值为"%.6g"。


### 格式化输出

```bash
awk '{ printf "%+8s\n", $1 }' test.log
或
awk '$5 ~ /S|D/ { print $5 }' test.txt
取反
awk '$5 !~ /S/ { print $5 }' test.txt

awk '/S/ { print $5 }' test.txt
awk '!/S/ { print $5 }' test.txt
```

### 过滤记录

```bash
awk '$3 == 0' test.log
awk '$2 > 3 || $5 == "DGRAM" { printf "%2s %s\n", NR, $6 }' test.txt
```

### 指定分割符

```bash
awk 'BEGIN { fS=":" } { print $1 }' test.log
awk -F: '{ print $1 }' test.log
以上两种方式等价

指定多个分隔符
awk -F '[;:]'

指定输出分隔符
awk  -F: '{print $1,$3,$6}' OFS="\t" /etc/passwd
```

### 字符串匹配

```bash
awk '$5 ~ /S/ { print $5 }' test.txt
```

### awk脚本

```awk
#!/usr/bin/awk -f
# -f参数告诉awk将该文件作为awk的程序文件，然后即可运行该程序。

# awk函数
function plus(a, b) {
    return a + b
}

BEGIN {
    # 函数调用
    print plus(1, 2)
}
```
