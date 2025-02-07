# Multi-Client Socket Server

A Python server that handles multiple clients, supporting:

-   `count <words>` → Returns the number of words.
-   `translate <text>` → Converts text to Pig Latin.

## Usage

1. Configure PYTHONPATH:

    Navigate to `262-Design-Exercise-1` directory.

    ```bash
    export PYTHONPATH="$PWD"
    ```

2. Start the server:

    ```bash
    python server.py
    ```

3. Start a client:

    ```bash
    python client.py
    ```

4. Enter commands:

    ```bash
    > count hello world
    Server response: 2

    > translate hello world
    Server response: ellohay orldway
    ```

Type `exit` to close the client.
