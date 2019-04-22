#!/bin/bash

cd $(dirname $0);
jupyter nbconvert --to html *.ipynb --template=interactive.tpl;
