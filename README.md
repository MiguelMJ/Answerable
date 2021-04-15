<p align="center">
    <img src="doc/logo.svg" height="200px" alt="logo" title="Answerable">
</p>
<h1 align="center">Answerable</h1>
<h3 align="center">Recommendation system for Stack Overflow unanswered questions</h3>
<p align="center">
	<a href="LICENSE">
        <img alt="license" src="https://img.shields.io/badge/license-MIT-informational">
    </a>
	<img alt="repo-size" src="https://img.shields.io/github/repo-size/MiguelMJ/Answerable">
	<img alt="python3.8" src="https://img.shields.io/badge/python-3.8-informational">
	<a href="https://github.com/MiguelMJ/Answerable/wiki">
        <img alt="documentation" src="https://img.shields.io/badge/documentation-wiki-success">
    </a>
	<a href="https://github.com/psf/black">
        <img alt="code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
</p>


Answerable is a Python program that learns from your answers in Stack Overflow and use them to recommend questions that you could answer.

**Preview**

<p align="center"><img src="doc/preview.png" alt="preview"></p>

**Table of contents**

<span id="toc"></span>

  - [Quick guide](#Quick-guide30)
  - [Contributors](#contributors)
  - [Contributing](#Contributing66)
  - [To do](#To-do77)
  - [License](#License99)

<h2 id="Quick-guide30">Quick guide</h2> 

[[TOC](#toc)]

- Clone the repository

    ```bash
    git clone https://github.com/MiguelMJ/Answerable.git
    ```

- Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

- Save the user (see [how to get your relevant user information](https://github.com/MiguelMJ/Answerable/wiki/Getting_user_info))

    ```bash
    python answerable.py save -u ID [-t FILE]
    ```

- Get information of your profile

    ```bash
    python answerable.py summary -u ID
    ```

- Get recommendations

  ```bash
  python answerable.py recommend -u ID
  ```

_To see a more complete guide, visit the [wiki](https://github.com/MiguelMJ/Answerable/wiki)._

<h2 id="contributors">Contributors</h2> 

[[TOC](#toc)]

Thanks to the people that have contributed to this project: ([emoji key](https://allcontributors.org/docs/en/emoji-key))

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://fxgit.work"><img src="https://avatars.githubusercontent.com/u/1080112?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Dennis Lee</b></sub></a><br /><a href="https://github.com/MiguelMJ/Answerable/issues?q=author%3Adennislwm" title="Bug reports">🐛</a> <a href="#blog-dennislwm" title="Blogposts">📝</a></td>
    <td align="center"><a href="https://github.com/danthe1st"><img src="https://avatars.githubusercontent.com/u/34687786?v=4?s=100" width="100px;" alt=""/><br /><sub><b>dan1st</b></sub></a><br /><a href="https://github.com/MiguelMJ/Answerable/commits?author=danthe1st" title="Documentation">📖</a></td>
  </tr>
</table>
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org/) specification.

<h2 id="Contributing66">Contributing</h2> 

[[TOC](#toc)]

- Find the contributing guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

- You can also contribute by testing the program yourself and reporting any issue [![](https://img.shields.io/github/issues/MiguelMJ/Answerable?style=social)](https://github.com/MiguelMJ/Answerable/issues).
- Give this project some visibility and feedback:
  - :star: Star this repository [![](https://img.shields.io/github/stars/MiguelMJ/Answerable?style=social)](https://github.com/MiguelMJ/Answerable/stargazers).
  - :arrow_up: Upvote it in [Stack Apps](https://stackapps.com/questions/8805/placeholder-answerable-a-recomendator-of-unanswered-questions) and comment your feedback there.

<h2 id="To-do77">To do</h2> 

[[TOC](#toc)]

- [x] Test all documented behaviour (argument usage).
- [x] Limit the number of answers retrieved from users with too many answers.
  - Too many answers reduce the recommendation quality.
  - Too many answers drastically increases the retrieval time.
- [ ] Allow said users to set which answers want to use.
  - Use X newest, X most popular or the whole activity history (maybe add a time estimation for this last option).
- [x] Implement statistics for `summary` command.
- [ ] For new users without answers, we could add the option to just select questions that they would like to have answered.

**Low priority**

- [ ] Include the rest of the Stack Exchange communitites.
- [ ] Make a GUI.
- [ ] Add flexible filters (Don't show questions with negative score e.g).
- [ ] Display statistics about the information taken into account to make the recommendations.
- [ ] Try out more learning models and integrate them.
- [ ] Adapt behaviour for users with authentication token.

<h2 id="License99">License</h2> 

[[TOC](#toc)]

Answerable uses the MIT license, a copy of which you can find [here](LICENSE), in the repo.

