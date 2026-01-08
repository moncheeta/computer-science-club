# Computer Science Club Website

A website for Computer Science Club made during a mini-hackathon.

![home page](./assets/home.png)

## Setup

### Environment Variables

The following environment variables are required:

| Variable | Description |
|----------|-------------|
| `DOMAIN` | The URL where this app is hosted |
| `GROUP_ID` | Schoology group ID (found in the URL after `/group/`) |
| `SCHOOLOGY_DOMAIN` | Your Schoology instance domain (e.g., `schoology.example.com`) |
| `SCHOOLOGY_API_KEY` | Schoology API key |
| `SCHOOLOGY_API_SECRET` | Schoology API secret |

### Schoology

To get a Schoology API key and secret, go to `https://<your-schoology-domain>/api`. There you can manage your API credentials.

### Google OAuth

To setup Google OAuth2, follow [these instructions](https://developers.google.com/identity/oauth2/web/guides/get-google-api-clientid). Copy the credentials JSON into a file called `google_auth.json` in the root of the project. Make sure your domain is added as an "Authorized redirect URI."

## Running

### Docker (Recommended)

```sh
docker build -t cs-club .
docker run -p 80:80 \
  -e DOMAIN="https://example.com" \
  -e GROUP_ID="123456" \
  -e SCHOOLOGY_DOMAIN="schoology.example.com" \
  -e SCHOOLOGY_API_KEY="your-key" \
  -e SCHOOLOGY_API_SECRET="your-secret" \
  cs-club
```

### Local Development

```sh
python -m venv venv
source venv/bin/activate
pip install flask schoolopy schedule cachecontrol google-auth google_auth_oauthlib
flask --app main run
```
