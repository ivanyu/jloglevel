FROM openjdk:8u162-jdk

COPY jloglevel-test-app/pom.xml /jloglevel-test-app/pom.xml
COPY jloglevel-test-app/src/ /jloglevel-test-app/src/
COPY run.sh /run.sh

RUN wget http://search.maven.org/remotecontent?filepath=org/jolokia/jolokia-jvm/1.5.0/jolokia-jvm-1.5.0-agent.jar \
  -O /jolokia.jar

ENV MAVEN_VERSION 3.5.2
ENV MAVEN_HOME /usr/lib/mvn
ENV PATH $MAVEN_HOME/bin:$PATH

RUN wget http://archive.apache.org/dist/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.tar.gz && \
  tar -zxvf apache-maven-$MAVEN_VERSION-bin.tar.gz && \
  rm apache-maven-$MAVEN_VERSION-bin.tar.gz && \
  mv apache-maven-$MAVEN_VERSION /usr/lib/mvn

#WORKDIR /jloglevel-test-app/

RUN mvn -f /jloglevel-test-app/pom.xml package
RUN mv /jloglevel-test-app/target/jloglevel-test-app-1.0-jar-with-dependencies.jar /jloglevel-test-app.jar

CMD /run.sh
