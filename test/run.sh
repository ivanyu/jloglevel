#!/bin/bash

java \
-javaagent:/jolokia.jar=port=8778,host=0.0.0.0 \
-server \
-jar /jloglevel-test-app.jar
