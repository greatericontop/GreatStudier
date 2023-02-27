# GreatStudier

A free and open source studying software. 

[**Get the releases here!**](https://github.com/greatericontop/GreatStudier/releases)

---

## Requirements

- Python 3.9 (or higher), although 3.6 will probably work.
- `requests` module: Install using `pip install requests` or the equivalent (`python3 -m pip`, `pip3`, etc.) for your system.
- `bs4` module: Install using `pip install bs4` or the equivalent (`python3 -m pip`, `pip3`, etc.) for your system.

Some pre-built binaries are available, but they won't work for every system. Use the source code if possible.

---

## Usage

Run `main.py`.

Default directory for sets is `~/GreatStudier/`. You can change this in the configurations. You will need to enter the full path, but the home folder `~` is supported.

It is suggested to edit the options file though the CLI, but if you're feeling brave, go ahead and edit it raw.

Leave fields blank to exit.

### Sets

Study sets are stored in a file with the header of `## * greatstudier *`. 

### Learn

Learn mode is a mode where you type out the term shown on screen. After typing all of the terms in the set, there will be a quiz.

### Review

Review mode is used for long term memory, you will be quizzed over the materials in the set after a certain amount of time.

To overwrite an answer that was automatically graded incorrectly, type `*`.

### Study

Study mode is used for short term memory. Use this mode if you need to remember something before a test.

To overwrite an answer that was automatically graded incorrectly, type `*`.

---

## Sharing

GreatStudier uses [`paste.gg`](https://paste.gg) and its API for uploading and downloading sets.

You can set a custom API key in the config (go to `options`, then `API keys`) to link any GreatStudier uploads to your account, so they're easier to find and manage.

---

## Quizlet Convert

Quizlet sets can convert to GreatStudier using the `Quizlet Convert` Option in the menu. The Quizlet set must be public to be able to be converted. **NOTE: you may have to run this multiple times to download the set completely** 

---

## Options

`set_directory` >> The directory that the sets are stored in. Defaults to `~/GreatStudier`.

`paste_api_key` >> API key used to upload sets. Use it to link your uploads to an account. Also necessary to edit uploaded sets.

`paste_username` >> Due to an API limitation the username is needed to edit sets.

`remove_language_accents` >> Changes most accented letters to non-accented letters in answers for languages. Currently supports Spanish, French, German, Chinese.

`upload_set_permissions` >> Permissions used for the paste link. Valid values are `public`, `unlisted`, `private`. You need a key to use the `private` option.

`alpha_only` >> Removes any non-alphanumeric characters (punctuation, unicode, etc.) from answers.

---

## License

GreatStudier is Free Software!

This project is licensed under the GNU General Public License v3 or later.
