FROM gcc:latest

COPY ./codeFiles/sample.cpp /home/oj/

WORKDIR /home/oj/

RUN g++ sample.cpp -o output

CMD [ "./output" ]