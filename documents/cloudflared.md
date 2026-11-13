# cloudflared

## cloudflared tunnel

trycloudflare.com

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
Pattern:
{RANDOM}.trycloudflare.com

Example:
foo-bar-potato-banana.trycloudflare.com
ide-maiden-operational-exhibitions.trycloudflare.com
```