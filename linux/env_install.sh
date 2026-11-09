#!/bin/bash

pretty_print() {
    printf "\n%s\n\n" "$1"
}

if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    pretty_print "OS not supported: $OSTYPE"
    exit 1
fi
pretty_print "OS: $OS"

if command -v python3 > /dev/null; then
    pretty_print "python ok: $(python3 --version)"
else
    pretty_print "python3 not found, installing..."
    if [ "$OS" = "mac" ]; then
        brew install python
    else
        sudo apt update
        sudo apt install -y python3 python3-pip
    fi
fi

pretty_print "pip: $(python3 -m pip --version)"

if [ "$OS" = "mac" ]; then
    brew install jupyterlab
else
    python3 -m pip install --user notebook
fi
pretty_print "jupyter installed"

if [ "$OS" = "mac" ]; then
    brew doctor
fi

pretty_print "done"
