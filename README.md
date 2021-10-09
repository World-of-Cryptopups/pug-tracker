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

### Hosting

- `web.py`
  Run this file if you are hosting on a free service such as http://repl.it

  ```sh
  python3 web.py
  ```

- `server.py`
  Run this file if you are hosting on a server, vps or your computer
  ```sh
  python3 server.py
  ```

##

&copy; 2021 | [**World of Cryptopups**](https://www.worldofcryptopups.cf/) | [License](./LICENSE)
