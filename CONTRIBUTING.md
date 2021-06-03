# Contributing to Answerable

Thank you for thinking about contributing to this project! I hope you find Answerable useful and have some ideas to make it better.

In the [README.md](README.md) you will find the list of tasks I'm currently working on, in case you want to open a related issue or PR.

# How to contribute

1. Fork the repository [![](https://img.shields.io/github/forks/MiguelMJ/Answerable?style=social)](https://github.com/MiguelMJ/Answerable/network/members).
2. Create a new branch from the latest `dev` branch.
3. Make your changes there.
4. Commit and push to the new branch.
5. Make a pull request.

Consider running Black, Pyflakes and/or other code formatters and analyzers before submitting your changes.

## Almost directly acceptable contributions

- Making grammar corrections anywhere in [the documentation](https://github.com/MiguelMJ/Answerable/wiki) or the comments in the code (don't spam these).
- Fixing a bug. If you don't want or know how to fix it, you can still **open an issue** [![](https://img.shields.io/github/issues/MiguelMJ/Answerable?logo=GitHub&style=social)](https://github.com/MiguelMJ/Answerable/issues).
- Improving a piece of code without importing a new library. The less dependencies, the better.

## Contributions subject to review

- Modifying or extending the displayed statistics.
- Modifying or extending the recommendation algorithm.
- Extending the documentation.
- Solving any of the tasks listed in the To Do list in the [README.md](README.md).
  - Notice that most of them require the use of the [Stack Exchange API](https://api.stackexchange.com/).

## Contributions that require a heavy justification

- Replacing a working piece of code by an new import.
- Changes in the way data is displayed.

## Contributing with a new model

I invite you to make your own model and share it, but I will only accept a model in the central repository if:

- It makes an obvious and noticeable improvement on an existing model.
- It takes into account different/more information than other models.
- It uses a new approach that no other present model has.

Don't forget do document any new model in [models/README.md](models/README.md).

# Give feedback and visibility

:star: Star this repository [![](https://img.shields.io/github/stars/MiguelMJ/Answerable?style=social)](https://github.com/MiguelMJ/Answerable/stargazers).
:arrow_up: Upvote it on [Stack Apps](https://stackapps.com/questions/8805/placeholder-answerable-a-recomendator-of-unanswered-questions) and comment your feedback.
