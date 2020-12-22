<p align="center">
    <img src="doc/logo.svg" height="200px" alt="logo" title="Answerable">
</p>
<h1 align="center">Answerable</h1>
<h3 align="center">Stack Overflow unanswered questions recommendation system</h3>
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
**Display summary of your top 5 answers**

```
python answerable.py summary -l 5 -k reputation
```

**Get recommendations from the latest questions**

```
python answerable.py questions
```

**See all options**

```
python answerable.py -h
```

## To do

- Implement all commands
- Test and improve the learning models.
- Make more documentation.
