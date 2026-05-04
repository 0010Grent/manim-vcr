FROM python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git pkg-config build-essential \
    libcairo2-dev libpango1.0-dev \
    libgl1 libglx-mesa0 libgl1-mesa-dri \
    libegl1 libegl-mesa0 libgles2 \
    xvfb \
    ffmpeg \
    texlive-full \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
CMD ["bash"]
