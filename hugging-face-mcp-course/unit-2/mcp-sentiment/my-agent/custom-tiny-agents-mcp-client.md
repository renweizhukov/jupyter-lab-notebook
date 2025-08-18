# Building Tiny Agents with MCP and the Hugging Face Hub

Based on the [Hugging Face MCP Course Unit 2](https://huggingface.co/learn/mcp-course/en/unit2/tiny-agents), we document the steps for building Tiny Agents with MCP and the Hugging Face Hub on a **Macbook**.

## Setup

1. Install nvm and node.js.

  ```bash
  # Download and install nvm.
  $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
  # Reload the nvm related environment variables added in .zshrc.
  $ source ~/.zshrc

  # Install node.js 20.
  $ nvm install 20
  $ nvm use 20

  # Verify the node.js and npm installation.
  $ node -v
  v20.19.4
  $ npm -v
  10.8.2
  ```

2. Install npx and the mcp-remote package.

  ```bash
  $ npm install -g npx
  $ npm i mcp-remote
  ```

## Run Tiny Agents

Assume that you have installed the `@huggingface/tiny-agents` package for Typescript or the `huggingface_hub[mcp]` package for Python.

1. Create a project with a basic Tiny Agent (see agent.json).

2. Log in Hugging Face Hub via `huggingface-cli login` with your access token.

3. Run the basic Tiny Agent.

  ```bash
  $ tiny-agents run agent.json
  ```

  If you see the following `SSLCertVerificationError`, you can manually tell Python to use `certifi` for root CAs, i.e.,
  `export SSL_CERT_FILE="$(python3 -m certifi)"`.

  ```
    Error during agent run: Cannot connect to host router.huggingface.co:443 ssl:True [SSLCertVerificationError: (1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify
    failed: unable to get local issuer certificate (_ssl.c:1010)')]
    Traceback (most recent call last):
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/aiohttp/connector.p
    y", line 1283, in _wrap_create_connection
        return await self._loop.create_connection(*args, **kwargs, sock=sock)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/usr/local/fbcode/platform010/Python3.12.framework/Versions/3.12/lib/python3.12/asyncio/base_events.py", line 1159, in create_connection
        transport, protocol = await self._create_connection_transport(
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/usr/local/fbcode/platform010/Python3.12.framework/Versions/3.12/lib/python3.12/asyncio/base_events.py", line 1192, in _create_connection_transport
        await waiter
    File "/usr/local/fbcode/platform010/Python3.12.framework/Versions/3.12/lib/python3.12/asyncio/sslproto.py", line 581, in _on_handshake_complete
        raise handshake_exc
    File "/usr/local/fbcode/platform010/Python3.12.framework/Versions/3.12/lib/python3.12/asyncio/sslproto.py", line 563, in _do_handshake
        self._sslobj.do_handshake()
    File "/usr/local/fbcode/platform010/Python3.12.framework/Versions/3.12/lib/python3.12/ssl.py", line 916, in do_handshake
        self._sslobj.do_handshake()
    ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1010)

    The above exception was the direct cause of the following exception:

    Traceback (most recent call last):
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/huggingface_hub/inf
    erence/_mcp/cli.py", line 178, in run_agent
        async for chunk in agent.run(user_input, abort_event=abort_event):
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/huggingface_hub/inf
    erence/_mcp/agent.py", line 84, in run
        async for item in self.process_single_turn_with_tools(
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/huggingface_hub/inf
    erence/_mcp/mcp_client.py", line 261, in process_single_turn_with_tools
        response = await self.client.chat.completions.create(
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/huggingface_hub/inf
    erence/_generated/_async_client.py", line 962, in chat_completion
        data = await self._inner_post(request_parameters, stream=stream)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/huggingface_hub/inf
    erence/_generated/_async_client.py", line 265, in _inner_post
        response = await session.post(
                ^^^^^^^^^^^^^^^^^^^
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/huggingface_hub/inf
    erence/_generated/_async_client.py", line 3377, in _request
        response = await session._wrapped_request(method, url, **kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/aiohttp/client.py",
    line 770, in _request
        resp = await handler(req)
            ^^^^^^^^^^^^^^^^^^
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/aiohttp/client.py",
    line 725, in _connect_and_send_request
        conn = await self._connector.connect(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/aiohttp/connector.p
    y", line 642, in connect
        proto = await self._create_connection(req, traces, timeout)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/aiohttp/connector.p
    y", line 1209, in _create_connection
        _, proto = await self._create_direct_connection(req, traces, timeout)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/aiohttp/connector.p
    y", line 1581, in _create_direct_connection
        raise last_exc
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/aiohttp/connector.p
    y", line 1550, in _create_direct_connection
        transp, proto = await self._wrap_create_connection(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File
    "/Users/wrn/workspace/github/renweizhukov/jupyter-lab-notebook/hugging-face-mcp-course/unit-2/mcp-sentiment/mcp-sentiment/lib/python3.12/site-packages/aiohttp/connector.p
    y", line 1285, in _wrap_create_connection
        raise ClientConnectorCertificateError(req.connection_key, exc) from exc
    aiohttp.client_exceptions.ClientConnectorCertificateError: Cannot connect to host router.huggingface.co:443 ssl:True [SSLCertVerificationError: (1, '[SSL:
    CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1010)')]
  ```
