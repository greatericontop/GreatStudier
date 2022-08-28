# GreatStudier

A free and open source studying software. 

- [Requirements](#requirements)
- [Usage](#usage)
  - [Sets](#sets)
  - [Learn](#learn)
  - [Review](#review)
- [Sharing](#sharing)
- [License](#license)

---

## Requirements

- Python 3.9 (or higher), although 3.6 will probably work.
- `Levenshtein` module: Install using `pip install Levenshtein` or the equivalent (`python3 -m pip`, `pip3`, etc.) for your system.
- `Requests` module: Install using `pip install requests` or the equivalent (`python3 -m pip`, `pip3`, etc.) for your system.

---

## Usage

Run `main.py` in the root directory of the project.

Default directory for sets is `~/GreatStudier/`. You can change this in the configurations. **NOTE MAKE SURE TO TYPE TO FULL PATH TO THE DIRECTORY OR IT MIGHT BREAK.**

It is suggested to edit the options file though the CLI.

### Sets

Study sets are stored in a file with the header of `## * greatstudier *`. 

### Learn

Learn mode is a mode where you type out the term shown on screen. After typing all of the terms in the set, there will be a quiz.

### Review

Review mode is used for long term memory, you will be quizzed over the materials in the set after a certain amount of time.

---

## Sharing

GreatStudier uses [`paste.gg`](https://paste.gg) and its API for uploading and downloading sets.

You can set a custom API key in the config (go to `settings`, then `API keys`) to link any GreatStudier uploads to your account.

---

## License

This project is Licenced under the GNU General Public Licence v3, or at your option, any later version.