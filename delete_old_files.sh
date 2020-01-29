#!/bin/bash

directory=("/home/donald/Desktop/testfiles" "/home/donald/Desktop/testfiles1")
for i in "${directory[@]}"
do
	find $i -mindepth 1 -mtime +30 -delete
done
