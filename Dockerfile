ARG GIT_TOKEN

FROM alpine:3.18 AS build_python
RUN apk add git build-base linux-headers python3-dev py3-pip

FROM build_python AS build_poschtar
ARG GIT_TOKEN
WORKDIR /app
RUN git clone --depth 1 https://$GIT_TOKEN@github.com/swissinnovationlab/poschtar
WORKDIR /app/poschtar 
RUN rm -Rf .git
RUN pip install -e ./

FROM build_python AS build_entrio2mail
WORKDIR /app
RUN git clone --depth 1 https://github.com/schef/entrio2mail
WORKDIR /app/entrio2mail
RUN rm -Rf .git
RUN pip install -e ./

FROM alpine:3.18 AS prod
RUN apk add --no-cache python3
COPY --from=build_poschtar /usr/lib/python3.11/site-packages /usr/lib/python3.11/site-packages
COPY --from=build_poschtar /app /app
COPY --from=build_entrio2mail /usr/lib/python3.11/site-packages /usr/lib/python3.11/site-packages
COPY --from=build_entrio2mail /app /app

CMD mkdir ~/.config/poschtar
CMD mkdir ~/.config/entrio2mail

CMD python /app/entrio2mail/entrio2mail/main.py
