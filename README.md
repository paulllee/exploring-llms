# llm-exploration

senior design group exploring LLMs with LangChain

this is simply a monorepo of aggregated individual-led explorations

# prerequisites

supporting `python<3.12.0`
- `python>=3.12.0` is incompatible with `aiohttp` which is a build dependency to one of our requirements

while in this project directory, please install all the requirements via `pip install -r requirements.txt`

# alternative setup through vscode devcontainers

if you use vcsode and docker, i provided a `.devcontainer` where it will setup everything for you in a devcontainer

all you need is to install this extension `ms-vscode-remote.remote-containers` as well as having docker installed

go to the command palette and search `Rebuild Container` to build the container from this directory and vscode will relaunch with everything necessary

# contribution

please add to `requirements.txt` if you installed a new external python library
