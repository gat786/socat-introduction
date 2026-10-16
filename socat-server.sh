#!/usr/bin/env bash
# A bare-bones HTTP server: socat sends the raw bytes of response.http to every client.
# -v prints each raw request (>) and response (<) to this terminal.
cd "$(dirname "$0")"
socat -v TCP-LISTEN:"${1:-8080}",reuseaddr,fork SYSTEM:"cat response.http"
