# Tiny Agents Clients

Based on the [Hugging Face MCP Course](https://huggingface.co/learn/mcp-course/en/unit1/mcp-clients#tiny-agents-clients), we document the steps for using tiny agents as MCP Clients to control a browser with Playwright on a **Windows** laptop. Note that we run all the commands in PowerShell.

## Setup

1. Download and install the Windows Node version manager `nvm-windows` by following the link given in https://docs.npmjs.com/downloading-and-installing-node-js-and-npm#windows-node-version-managers. Note that DO NOT install `nodist` since it is no longer actively maintained.
  
    1. Download the latest installer from https://github.com/coreybutler/nvm-windows/releases and follow the prompts.

    1. Install a clean Node version with matching npm.

        ```
        > nvm install 20.11.1
        > nvm use 20.11.1

        # Verify:
        > node -v
        > npm -v
        ```   

1. Install the playwight tool.

    ```
    > npm install -g @playwright/mcp
    > npx playwright install
    ```

1. Find out where global modules are installed and add the path to the environment variable `PATH`.

    ```
    > npm config get prefix
    C:\nvm4w\nodejs
    
    > $env:PATH += "C:\nvm4w\nodejs"

    # Verify the environment variable PATH.
    > $env:PATH -split ';'
    ```

1. Create a Python virtual environment and install the `huggingface_hub` package with the MCP support. Assume that we already have python3 installed.

    ```
    > python -m venv mcp

    # If you get a script execution error, use:
    # Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    > .\mcp\Scripts\Activate.ps1

    > pip install "huggingface_hub[mcp]>=0.32.0"
    ```

## Run the agent to connect to MCP servers

1. Create an agent configuration file agent-nebius-qwen.json as given in the same folder. For all the supported inference providers and models, please refer to Hugging Face [Inference Providers / Models Support Matrix](https://huggingface.co/inference/models).

1. Log in to the Hugging Face Hub to access the Qwen model provided by nebius.

    ```
    > huggingface-cli login
    ```

1. Run the agent.

    ```
    > tiny-agents run agent-nebius-qwen.json

    # Try the following prompt:
    >> do a Web Search for HF inference providers on Brave Search and open the first result and then give me the list of the inference providers supported on Hugging Face
    ```