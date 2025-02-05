# Multi-Client Socket Server

A Python server that handles multiple clients, supporting:

-   `count <words>` → Returns the number of words.
-   `translate <text>` → Converts text to Pig Latin.

## Usage

1. Start the server:

    ```bash
    python server.py
    ```

2. Start a client:

    ```bash
    python client.py
    ```

3. Enter commands:

    ```bash
    > count hello world
    Server response: 2

    > translate hello world
    Server response: ellohay orldway
    ```

Type `exit` to close the client.
