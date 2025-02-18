ARG GIT_TOKEN

FROM archlinux AS build_python
RUN pacman -Syu --noconfirm python python-pip git

FROM build_python AS build_poschtar
ARG GIT_TOKEN
WORKDIR /app
RUN git clone --depth 1 https://$GIT_TOKEN@github.com/swissinnovationlab/poschtar
WORKDIR /app/poschtar 
RUN rm -Rf .git
RUN pip install -e ./ --break-system-packages

FROM build_python AS build_entrio2mail
WORKDIR /app
RUN git clone --depth 1 https://github.com/schef/entrio2mail
WORKDIR /app/entrio2mail
RUN rm -Rf .git
RUN pip install -e ./ --break-system-packages

FROM archlinux AS prod
RUN pacman -Syu --noconfirm python chromium
COPY --from=build_poschtar /usr/lib/python3.13/site-packages /usr/lib/python3.13/site-packages
COPY --from=build_poschtar /app /app
COPY --from=build_entrio2mail /usr/lib/python3.13/site-packages /usr/lib/python3.13/site-packages
COPY --from=build_entrio2mail /app /app
COPY --from=build_entrio2mail /usr/bin/playwright /usr/bin

RUN playwright install chromium

RUN mkdir -p /root/.config/poschtar
RUN mkdir -p /root/.config/entrio2mail

CMD python /app/entrio2mail/entrio2mail/main.py
