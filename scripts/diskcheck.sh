#!/bin/bash

echo "=== Дата ==="
date
echo

echo "=== Аптайм ==="
uptime
echo

echo "=== Свободное место на диске ==="
df -h
echo

echo "=== Использование памяти ==="
free -h
echo

echo "=== Топ-5 процессов по памяти ==="
ps aux --sort=-%mem | head -n 6
