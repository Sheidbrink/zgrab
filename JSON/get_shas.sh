#!/bin/bash

~/pv 2016-07-13.json | sha256sum | tee sha_2016-07-13.out
~/pv 2016-07-14.json | sha256sum | tee sha_2016-07-14.out
~/pv 2016-07-18.json | sha256sum | tee sha_2016-07-18.out
~/pv 2016-07-20.json | sha256sum | tee sha_2016-07-20.out
~/pv 2016-07-22.json | sha256sum | tee sha_2016-07-22.out
~/pv 2016-07-24.json | sha256sum | tee sha_2016-07-24.out
