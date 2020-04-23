# meeoh
Slowed-And-Reverbed

## Usage
1. Fill in `.env.template` and rename to `.env`. Need reddit client id and secret, and giphy api key
2. `docker build -t sandr .`
3. `docker run -v $(pwd):/usr/src/app/ -t sandr` (assuming you're currently in the repo)
