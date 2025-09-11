一级标题
===
我展示的是二级标题
---
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
![alt text](image.png)
Markdown 段落没有特殊的格式，直接编写文字就好，段落的换行是使用两个以上空格加上回车。  
当然也可以在段落后面使用一个空行来表示重新开始一个段落。

*斜体文本*
_斜体文本_
**粗体文本**
__粗体文本__
***粗斜体文本***
___粗斜体文本___
![alt text](image-1.png =200x300)
你可以在一行中用三个以上的星号、减号、底线来建立一个分隔线，行内不能有其他东西。你也可以在星号或是减号中间插入空格。下面每种写法都可以建立分隔线：

---

***

* * *

*****

- - -

----------

## ~~删除线~~
## <u>下划线</u>

啦啦啦 [^jiaozhu]。
[^jiaozhu]: sjkdhfsdh

创建脚注格式类似这样 [^RUNOOB]。

[^RUNOOB]: 这是一个标注

## 列表（+,-,*随意即可，注意空格）可嵌套
### 1无序
+ 第一个
    1. 第一个
        - 第一个
        - 第二个
        - 第三个
    2. 第二个
        1. 第一个
        * 第二个
        3. 第三个
    3. 第三个
- 第二个
* 第三个
### 2有序
1. 第一个
2. 第二个
3. 第三个

> 测试区块引用
>> 测试区块引用
## 代码
 
` for(int i=0;i<n;i++) `

    for(int i=0;i<n;i++){
        printf("hello world")
    }


这是一个链接 [链接](https://www.runoob.com)
直接写链接<https://www.runoob.com>
[oi wiki](https://oi-wiki.org/)
这个链接用 1 作为网址变量 [Google][1]
这个链接用 runoob 作为网址变量 [Runoob][runoob]
然后在文档的结尾为变量赋值（网址）

  [1]: http://www.google.com/
  [runoob]: http://www.runoob.com/

| 左对齐aaa | 右对齐aaaa | aa居中对齐aaa |
| :-----| ----: | :----: |
| 单元格 | 单元格 | 单元格 |
| 单元格 | 单元格 | 单元格 |

## 公式
Markdown Preview Enhanced 使用 KaTeX 或者 MathJax 来渲染数学表达式。

KaTeX 拥有比 MathJax 更快的性能，但是它却少了很多 MathJax 拥有的特性。你可以查看 KaTeX supported functions/symbols 来了解 KaTeX 支持那些符号和函数。

默认下的分隔符：

\$...\$ 或者 \(...\) 中的数学表达式将会在行内显示。
\$\$...\$\$ 或者 \[...\] 或者 ```math 中的数学表达式将会在块内显示。

$ f(x)=sin(x)+10-cos(x) $

$$
\begin{Bmatrix}
   a & b \\
   c & d
\end{Bmatrix}
$$
$$
\begin{CD}
   A @>a>> B \\
@VbVV @AAcA \\
   C @= D
\end{CD}
$$
