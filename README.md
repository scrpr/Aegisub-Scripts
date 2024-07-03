# Aegisub-Scripts

My typesetting scripts made for aegisub.

## Pangu.lua

Paranoid text spacing.

为什么你们就是不能加个空格呢.lua

会自动在中文字符和半角的英文、数字、符号之间插入空白。插入的空白长度为1/2个半角空格。

> [!NOTE]
> 由于使用`\fscx`控制长度，插入的标签可能会覆盖原有已存在标签。

## Katakana_fullwidth

Convert half-width katakanas to full-width, useful for Japanese tv-broadcasting captions.

将半角片假名转换为全角片假名。

## ASS Pre-translation

A simple script for the translation of ASS files with the use of LLMs.
使用LLM翻译ASS字幕。

### Installation

```bash
pip install path/to/pretranslation
```

### Usage

```bash
ass-pretrans [file]
```

**可选参数 Available options**
+ `-t` 设置最大Token数 Max token
+ `-m` 设置模型名称，默认为gpt-3.5-turbo Model name, defaults to gpt 3.5 turbo
+ `-c` 设置上下文信息 Context background
+ `-k` 设置关键词 Keywords
+ `--openai-key` 设置OPENAI API KEY
+ `--openai-url` 设置OPENAI BASE URL
+ `--moonshot-key` 设置Moonshot API KEY
+ `--sakura-key` 设置SakuraLLM KEY 由于Sakura多为本地部署，该项经常不检查
+ `--sakura-url` 设置SakuraLLM BASE URL

**输出 Output**

同文件夹下以`_{models}.ass`结尾的文件。