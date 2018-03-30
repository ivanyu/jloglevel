FROM openjdk:8u162-jdk

RUN wget http://search.maven.org/remotecontent?filepath=org/jolokia/jolokia-jvm/1.5.0/jolokia-jvm-1.5.0-agent.jar -O /jolokia.jar
COPY jloglevel-test-app/ /jloglevel-test-app/

RUN javac
