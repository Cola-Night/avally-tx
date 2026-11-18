# cloudflared tunnel

Use `trycloudflare.com` for deploy.

```bash
# install cloudflare (on window)
winget install Cloudflare.cloudflared
```

```bash
# Run docker-containers
docker-compose up -d

# start tunnel
cloudflared tunnel --url http://localhost:8000
```

Note: cloudflared tunnel generate randomize url
```
URL-Pattern:
{RANDOM}.trycloudflare.com

Examples:
foo-bar-potato-banana.trycloudflare.com
ide-maiden-operational-exhibitions.trycloudflare.com
```