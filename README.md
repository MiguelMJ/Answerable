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
	<a href="https://github.com/psf/black">
        <img alt="code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
</p>

Answerable is a Python program that learns from your answers in Stack Overflow and use them to recommend you questions that you could answer.

**This project is still under development.**

## Features

- Get insights on your Stack Overflow profile without leaving the console.

- Get the latest questions and sort them by their similarity to questions you have already answered.

## Quick guide

- **Save your user**

	```
	python answerable.py -s ID [SOURCE-FILE]
	```
	
- **Display summary of your top 5 answers**

	```
	python answerable.py summary -l 5 -k reputation
	```

- **Get recommendations from the latest questions**

	```
	python answerable.py questions
	```

- **See all options**

	```
	python answerable.py -h
	```

## Commands

### `summary`

...

### `tags`

...

### `answers`

...

### `questions`

...

### `save`

Take the options `-u|--user` and `-t|--tags` and save their information to a `.config` file. 

##### The `.config` file

The most probable thing is that you will be using this program with your user, repeteadly. For this reason, instead of having to call Answerable always with the `-u|--user` and `-t|--tags`, you can save them to this file and the following executions will read them from it.

##### Where to get the user ID and tags file

You can find your id in the url of your profile, that has the following form:

```
https://stackoverflow.com/users/{id}/{name}
```

The tags file requires few extra steps. The reason is that, for now, I won't be implementing the use of the authentication_token for the Stack Exchange API, and to obtain the tags the program must scrap the page. However, this page is private, so you must download. This should be simple. 

1. Go to the following page:

   ```
   view-source:https://stackoverflow.com/users/tag-notifications/{id}
   ```

2. Select all (`Ctrl+A`).

3. Copy and paste in a new file in your system.

   That will be the tags file.

## To do

- [x] Use `argparse` to interpret the CLI options.
- [ ] Implement all commands.
- [ ] Test and improve the learning models.
- [ ] Complete documentation.
- [ ] Adapt behaviour for users with authentication token.

**Low priority**

- [ ] Include the rest of the Stack Exchange communitites.
- [ ] Make a GUI.
