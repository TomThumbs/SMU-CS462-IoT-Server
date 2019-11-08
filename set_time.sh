#!/bin/bash
while ! ping -c 1 -W 1 google.com; do
    echo "Waiting for google.com - network interface might be down..."
    sleep 1
done

sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"