# Renormalize 重整文件名

## 使用

```shell
> python src/main.py pattern pathname
```

1. `pattern`——重整后的文件名模式，如`作业-:id-:name`。

    `:`开头表占位符，例如`JamesClerk:name-:id`对于`{ name: 'Maxwell', id: '1831-06-13' }`会变成`JamesClerkMaxwell-1830-06-13`。

2. `pathname`——要重整的文件夹，例如`./作业/*`。

    用于[`glob.glob`的`pathname`参数](https://docs.python.org/3/library/glob.html#glob.glob)。

更多信息请`--help`。

```shell
> python src/main.py --help
```

## 配置（`config/`）

-   `entities.csv`——姓名等个人信息。

    必须有`name`。
