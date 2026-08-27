# --- builder: compile deps into a venv ---
FROM python:3.11-slim AS builder

WORKDIR /usr/src/app/ga4-report

# gcc/libc-dev needed to build uWSGI's C extension; nothing else in requirements.txt compiles native code
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv venv

COPY requirements.txt .
RUN venv/bin/pip install --upgrade pip \
    && venv/bin/pip install -r requirements.txt

# --- runtime: just the venv + app code, no compiler toolchain ---
FROM python:3.11-slim

RUN addgroup --system user && adduser --system --home /home/user --shell /bin/sh --ingroup user user

RUN apt-get update \
    && apt-get install -y --no-install-recommends locales \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen

WORKDIR /usr/src/app/ga4-report

COPY --from=builder /usr/src/app/ga4-report/venv ./venv
COPY . .

RUN chown -R user:user /usr/src/app/ga4-report
USER user

ENV LC_ALL="en_US.utf8"

EXPOSE 8080
CMD ["./venv/bin/uwsgi", "--ini", "server.ini"]
