#!/bin/bash

time python store.py 2016-07-13.json
echo 2016-07-13.json >> store.done
mv 2016-07-13.json ~/DONE_store
time python store.py 2016-07-14.json
echo 2016-07-14.json >> store.done
mv 2016-07-14.json ~/DONE_store
time python store.py 2016-07-18.json
echo 2016-07-18.json >> store.done
mv 2016-07-18.json ~/DONE_store
time python store.py 2016-07-20.json
echo 2016-07-20.json >> store.done
mv 2016-07-20.json ~/DONE_store
time python store.py 2016-07-22.json
echo 2016-07-22.json >> store.done
mv 2016-07-22.json ~/DONE_store
time python store.py 2016-07-24.json
echo 2016-07-24.json >> store.done
mv 2016-07-24.json ~/DONE_store
