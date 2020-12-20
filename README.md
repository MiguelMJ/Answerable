<p align="center">
    <img src="doc/logo.svg" height="200px" alt="logo" title="Answerable">
</p>
<h1 align="center">Answerable</h1>
<h3 align="center">Find questions on Stack Overflow suited for you</h3>
<p align="center">
	<a href="LICENSE">
        <img alt="license" src="https://img.shields.io/badge/license-MIT-informational">
    </a>
	<img alt="repo-size" src="https://img.shields.io/github/repo-size/MiguelMJ/Answerable">
	<img alt="python3.8" src="https://img.shields.io/badge/python-3.8-informational">  
	<img alt="doc-to-do" src="https://img.shields.io/badge/documentation-To_do-important">
	<a href="https://github.com/psf/black">
        <img alt="code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
</p>
Answerable is a Python program that learns from your answers in Stack Overflow and use them to recommend you questions that you could answer.

**This project is still under development.**

## Features

- Get insights on your stack overflow profile without leaving the console.

- Get the latest questions and sort them by their similarity to questions you have already answered.

## Quick guide

_For now this is a reference for implementation, not its actual behaviour._

**Save your user**

```
python answerable.py -s ID [SOURCE-FILE]
```
**Execute command**

```
python answerable.py [-u ID] [--no-ansi] COMMAND
```
- Commands
  - `summary [-r] [-l LIMIT] [-t LENGTH] [-k reputation|votes]`
  - `tags [-r] [-l LIMIT] [-k reputation|name|count|ratio]`
  - `answers [-r] [-f FIRST] [-l LIMIT] [-k reputation|name|votes|value]`
  - `questions [-a] [-l LIMIT]`

- Options

| Option      | Details                                                      |
| ----------- | ------------------------------------------------------------ |
| `-s`        | Save the user ID and, optionally, their tags from the downloaded source file to the `data/user.json` file. |
| `-u`        | Specify the user ID. If no data has been saved before with the `-s` option, then this option is obligatory. |
| `--no-ansi` | Don't display color.                                         |
| `-r`        | Reverse information order. It has no effect `questions`.     |
| `-l`        | Limit the number of items displayed.                         |
| `-k`        | Order the items displayed to a given key. It has no effect in `questions` . |
| `-t`        | Truncate titles with a max length in `summary`               |
| `-a`        | Search through all the new questions, without tag filter. If the user tags haven't been saved before with the `-s` option, then this  option is on by default. |

# To do

- Interpret the arguments using `argparse`.
- Test and improve the learning models.
- Make more documentation.