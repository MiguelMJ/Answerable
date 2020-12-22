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

___This project is still under development.___

**Table of contents**

<span id="toc"></span>

  - [Quick guide](#Quick-guide24)
  - [Commands](#Commands51)
    - [`summary`](#`summary`54)
    - [`tags`](#`tags`58)
    - [`answers`](#`answers`62)
    - [`questions`](#`questions`66)
    - [`save`](#`save`70)
        - [The `.config` file](#The-`.config`-file74)
        - [Where to get the user ID and tags file](#Where-to-get-the-user-ID-and-tags-file78)
  - [To do](#To-do100)

<h2 id="Quick-guide24">Quick guide</h2> 
[[TOC](#toc)]

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

<h2 id="Commands51">Commands</h2> 
[[TOC](#toc)]

<h3 id="`summary`54">`summary`</h3> 

...

<h3 id="`tags`58">`tags`</h3> 

...

<h3 id="`answers`62">`answers`</h3> 

...

<h3 id="`questions`66">`questions`</h3> 

...

<h3 id="`save`70">`save`</h3> 

Take the options `-u|--user` and `-t|--tags` and save their information to a `.config` file. 

<h5 id="The-`.config`-file74">The `.config` file</h5> 

The most probable thing is that you will be using this program with your user, repeteadly. For this reason, instead of having to call Answerable always with the `-u|--user` and `-t|--tags`, you can save them to this file and the following executions will read them from it.

<h5 id="Where-to-get-the-user-ID-and-tags-file78">Where to get the user ID and tags file</h5> 

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

<h2 id="To-do100">To do</h2> 
[[TOC](#toc)]

- [x] Use `argparse` to interpret the CLI options.
- [ ] Implement all commands.
- [ ] Test and improve the learning models.
- [ ] Complete documentation.
- [ ] Adapt behaviour for users with authentication token.

**Low priority**

- [ ] Include the rest of the Stack Exchange communitites.
- [ ] Make a GUI.
