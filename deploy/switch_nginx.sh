#!/bin/bash
# Usage: ./switch_nginx.sh <blue|green>
set -e

TARGET=$1
if [[ "$TARGET" != "blue" && "$TARGET" != "green" ]]; then
  echo "Usage: $0 <blue|green>"
  exit 1
fi

NGINX_CONF_PATH="$(dirname "$0")/../nginx/nginx.conf"

cat > "$NGINX_CONF_PATH" <<EOF
events {}
http {
    upstream flask_app {
        server flask_${TARGET}:5000;
    }
    server {
        listen 80;
        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

echo "Reloading nginx container..."
docker-compose restart nginx
