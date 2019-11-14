# Генератор ключевых слов для Яндекс.Директа и Google Ads

Готовый контейнер для запуска в на сервере.
Предполагается установленный контейнер nginx со следующитми настройками docker-compose.yml:

```version: '3.7'

services:
  nginx:
    container_name: nginx
    image: nginx:latest
    networks:
      nginx_net:
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    ports:
      - 80:80

networks:
  nginx_net:
    name: nginx_net```

nginx.conf:

```server {
  server_name yourdomain.ltd;

  location / {
    resolver 127.0.0.11;
    set $project http://keygen_app:5000;
    
    proxy_pass $project;
  }
}```