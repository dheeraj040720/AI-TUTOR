# Security Policy

## Reporting a Security Vulnerability

If you discover a security vulnerability in the AI Learning Tutor project, please report it by emailing the project maintainer. Please do not create public GitHub issues for security vulnerabilities.

## Secure Setup Instructions

### Environment Variables

This project uses environment variables to protect sensitive API keys and credentials. **Never commit the `.env` file to version control.**

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Gemini API Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Supabase Configuration
# Get your credentials from: https://supabase.com/dashboard/project/_/settings/api
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### How to Obtain API Keys

#### Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

#### Supabase Credentials
1. Visit [Supabase Dashboard](https://supabase.com/dashboard)
2. Create a new project or select an existing one
3. Go to Settings → API
4. Copy the "Project URL" and "anon public" key
5. Add them to your `.env` file

### Frontend Configuration

The frontend uses Supabase credentials that are safe to expose in client-side code. These are stored in `frontend/config.js`. 

**Important:** Supabase anon keys are designed to be public. Security is enforced through Row Level Security (RLS) policies in your Supabase database.

### What to Do If Keys Are Exposed

If you accidentally commit API keys to GitHub:

1. **Immediately revoke the exposed keys:**
   - Gemini: Delete the API key in [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Supabase: Reset your project keys in the Supabase dashboard

2. **Generate new keys** and update your `.env` file

3. **Remove the keys from Git history:**
   ```bash
   # Use git filter-branch or BFG Repo-Cleaner
   # Or simply delete the repository and create a new one
   ```

4. **Verify `.gitignore` is working:**
   ```bash
   git status
   # .env should NOT appear in untracked files
   ```

## Security Features

### Backend Security

- **Environment Variables:** All sensitive credentials are stored in `.env` files
- **Security Headers:** HTTP security headers are automatically added to all responses:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Strict-Transport-Security: max-age=31536000`
- **CORS Configuration:** Configured to allow frontend access
- **Compression:** GZip compression for improved performance

### Frontend Security

- **Centralized Configuration:** All Supabase credentials are in `config.js`
- **Public Keys Only:** Only public anon keys are used (RLS enforces security)
- **No Sensitive Data:** No private keys or secrets in frontend code

## Best Practices

1. **Never commit `.env` files** to version control
2. **Use `.env.example`** to document required variables without exposing values
3. **Rotate API keys regularly** for enhanced security
4. **Enable Row Level Security (RLS)** in Supabase for all tables
5. **Monitor API usage** to detect unauthorized access
6. **Use HTTPS** in production deployments

## Deployment Security

When deploying to production:

1. Set environment variables in your hosting platform (Vercel, Heroku, etc.)
2. Never use development keys in production
3. Enable HTTPS/SSL certificates
4. Configure proper CORS origins (don't use `*` in production)
5. Set up monitoring and alerts for unusual API activity
