#!/bin/bash

pip freeze --exclude pytest | tee requirements.txt
