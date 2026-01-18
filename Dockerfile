FROM apache/airflow:2.6.3

USER root

# Dépendances système nécessaires à Playwright
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    libwayland-client0 \
    libwayland-egl1 \
    libwayland-cursor0 \
    fonts-liberation \
    xdg-utils \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ⬅️ TRÈS IMPORTANT : on repasse en user airflow
USER airflow

# Librairies Python
RUN pip install --no-cache-dir pymysql playwright

# Installation du navigateur Playwright
RUN python -m playwright install chromium
