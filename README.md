<p align="center">
    <img src="doc/logo.svg" height="200px" alt="logo" title="Answerable">
</p>
<h1 align="center">Answerable</h1>
<h3 align="center">Find questions on Stack Overflow suited for you</h3>
<p align="center">
	<a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-MIT-informational"></a>
	<img src="https://img.shields.io/github/repo-size/MiguelMJ/Answerable">
	<img src="https://img.shields.io/badge/python-3.8-informational">  
	<img src="https://img.shields.io/badge/documentation-To_do-important">  
</p>


Answerable is a Python program that learns from your answers in Stack Overflow and use them to find questions that you could answer.

**This project is still under development.**

## Features

- Get insights on your stack overflow profile without leaving the console.

  The first time you analyze your profile, it may take a while. This happens because each requests has a delay of two seconds the server, and it has to do at least one per answer you have answered. So if you have a long story. 

- Get the latest questions 
- It follows [respectful scraping methods](https://www.empiricaldata.org/dataladyblog/a-guide-to-ethical-web-scraping).

## Quick guide

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