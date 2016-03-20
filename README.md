# Messenger Colors

A Python script which allows you to set the color of a Facebook Messenger thread from the command line.

The script requires some setup. Create a new file called `config.py` in the script directory with the following variables:

- `user` - the default username or numerical ID used to set the color
- `cookie` - the cookie header sent with requests on [messenger.com](https://messenger.com)

**Usage:**

    python3 messenger-colors.py --color="#003A69" thread_username_or_id

For a full list of options, run the script with the `--help` argument
