FROM vulnfree.dev/public/python-alpine:latest

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

# vulnfree images commonly run as non-root; switch to root to install system packages.
USER root

# Tkinter on Alpine requires Tk/Tcl plus X11 libraries.
# Note: GUI apps in containers still need an X server on the host (or Xvfb for headless runs/tests).
RUN apk add --no-cache \
	  tcl \
	  tk \
	  fontconfig \
	  ttf-dejavu \
	  libx11 \
	  libxext \
	  libxrender \
	  libxrandr \
	  libxfixes \
	  libxi \
	  libxtst \
	  mesa-gl \
	  xvfb

# Provide a tiny xvfb-run helper (Alpine doesn't always ship the wrapper script).
# Use printf to guarantee LF line endings (avoids CRLF shebang issues on Windows hosts).
RUN printf '%s\n' \
	'#!/bin/sh' \
	'set -eu' \
	'' \
	'DISPLAY_NUM="${DISPLAY_NUM:-99}"' \
	'SCREEN="${XVFB_SCREEN:-0}"' \
	'RES="${XVFB_RESOLUTION:-1280x800x24}"' \
	'' \
	'Xvfb ":${DISPLAY_NUM}" -screen "${SCREEN}" "${RES}" -nolisten tcp >/dev/null 2>&1 &' \
	'XVFB_PID=$!' \
	'trap "kill ${XVFB_PID} >/dev/null 2>&1 || true" EXIT' \
	'' \
	'export DISPLAY=":${DISPLAY_NUM}"' \
	'exec "$@"' \
	> /usr/local/bin/xvfb-run \
	&& chmod +x /usr/local/bin/xvfb-run

# Create an unprivileged runtime user.
RUN addgroup -S app >/dev/null 2>&1 || true \
 && adduser -S -G app app >/dev/null 2>&1 || true \
 && mkdir -p /home/app /app \
 && chown -R app:app /home/app /app

# Copy sources as the unprivileged user so the app can create/save files under /app.
COPY --chown=app:app . /app

ENV HOME=/home/app

USER app

# Default: run the app (requires a display server to actually show the window)
CMD ["python", "execute.py"]