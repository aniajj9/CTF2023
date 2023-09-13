FROM maven:3-amazoncorretto-19

WORKDIR /code

# Prepare by downloading dependencies
ADD pom.xml /code/pom.xml
RUN ["mvn", "dependency:resolve"]
RUN ["mvn", "verify"]

# Adding source, compile and package into a fat jar
ADD . /code/src
RUN ["mvn", "package"]

EXPOSE 4567

CMD ["java", "-cp", "target/calculator-1.0.0.jar", "com.kalmarunionen.calculator.MainController"]
#CMD tail -f /dev/null
#java -cp target/calculator-1.0.0.jar com.kalmarunionen.calculator.MainController