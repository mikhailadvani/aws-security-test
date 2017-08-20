#!/usr/bin/env bash
set -e
clean() {
    rm -rf build dist aws_security_test.egg-info
}

build() {
    clean
    python setup.py sdist
    python setup.py bdist_wheel
}

uninstall() {
    pip uninstall -y aws_security_test
}

publishToTestPyPi() {
    python setup.py register -r https://testpypi.python.org/pypi
    twine upload dist/* -r testpypi
    uninstall
    pip install -i https://testpypi.python.org/pypi aws_security_test
}

publishToPyPi() {
    python setup.py register -r https://pypi.python.org/pypi
    twine upload dist/*
    uninstall
    pip install aws_security_test
}

if [ "$1" = 'publish' ]; then
    if [ "$2" = 'test' ]; then
        publishToTestPyPi
    elif [ "$2" = 'prod' ]; then
        publishToPyPi
    else
        echo "No publish target defined"
        exit 1
    fi
elif [ "$1" = 'clean' ]; then
    clean
elif [ "$1" = 'build' ]; then
    build
else
    echo "No task defined"
    exit 1
fi

