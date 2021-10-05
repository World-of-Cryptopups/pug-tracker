# pug-tracker

A crypto market quote price tracker.

This bot uses the CoinMarketCap API so you need to signup for their api (https://coinmarketcap.com/api/).

## Development

- Setup your `.env` file.

  ```
  TOKEN={your discord bot token}
  API_KEY={your coinmarketcap apikey}
  ```

- Install all required dependencies

  ```sh
  pip3 install -r requirements.txt
  ```

- `web.py`
  - This file is meant for usage on hosting your bot on some sites such as https://repl.it/

### Hosting

- Running the main file
  ```sh
  python3 main.py
  ```
  Note: You can comment the following function to prevent running a local flask web server, if you are using a server.
  ```py
  # run webapp
  keep_alive()
  ```

##

&copy; 2021 | [**World of Cryptopups**](https://www.worldofcryptopups.cf/) | [License](./LICENSE)
