# 🔐 Supabase Authentication Setup Guide

## Quick Start - Get Your Supabase Credentials

### 1️⃣ Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and sign in
2. Click "New Project"
3. Fill in:
   - **Project name**: `vibez-ai-charts`
   - **Database password**: Create a strong password
   - **Region**: Choose closest to you
4. Click "Create new project" (takes ~2 minutes)

### 2️⃣ Get API Credentials
Once your project is ready:
1. Go to **Project Settings** (gear icon in sidebar)
2. Click **API** in the left menu
3. Copy these two values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJ...`)

### 3️⃣ Configure Frontend
1. Copy `frontend/.env.example` to `frontend/.env`:
   ```bash
   cp frontend/.env.example frontend/.env
   ```

2. Edit `frontend/.env` and paste your credentials:
   ```env
   VITE_SUPABASE_URL=https://your-project.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   VITE_API_URL=http://localhost:8000
   ```

### 4️⃣ Enable Google OAuth (Optional)
To enable "Sign in with Google":

1. In Supabase dashboard → **Authentication** → **Providers**
2. Find **Google** and click to expand
3. Toggle **Enable Sign in with Google**
4. Add your Google OAuth credentials:
   - Get these from [Google Cloud Console](https://console.cloud.google.com/)
   - Create OAuth 2.0 Client ID
   - Add authorized redirect URI: `https://your-project.supabase.co/auth/v1/callback`
5. Paste **Client ID** and **Client Secret** into Supabase
6. Click **Save**

### 5️⃣ Configure Email Templates (Optional)
Customize confirmation emails:
1. **Authentication** → **Email Templates**
2. Edit templates for:
   - Confirm signup
   - Reset password
   - Magic link

### 6️⃣ Test Authentication
1. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

2. Navigate to `http://localhost:5173/signup`
3. Create a test account
4. Check your email for confirmation link
5. Try logging in at `http://localhost:5173/login`

---

## 🚀 Features Included

✅ **Email/Password Authentication**
- Sign up with email verification
- Login with credentials
- Password reset flow

✅ **Google OAuth** (when configured)
- One-click sign in with Google
- Auto-create account from Google profile

✅ **Protected Routes**
- Main app accessible only when logged in
- Automatic redirect to login for unauthenticated users

✅ **User Profile**
- View account details
- See sign-in method
- Email verification status
- Sign out functionality

---

## 📱 Pages Created

| Route | Description | Access |
|-------|-------------|--------|
| `/login` | Email/password + Google sign in | Public |
| `/signup` | Create new account | Public |
| `/` | Main chart creation app | Protected |
| `/profile` | User profile & settings | Protected |

---

## 🔒 Security Notes

- ✅ Environment variables (`.env`) are gitignored
- ✅ Never commit Supabase keys to GitHub
- ✅ Use `.env.example` as template only
- ✅ For production, set environment variables in Render/Vercel dashboard
- ✅ Anon key is safe for frontend (has Row Level Security)

---

## 🐛 Troubleshooting

### "Supabase environment variables are not set"
- Check that `frontend/.env` exists
- Verify `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` are set
- Restart dev server after changing `.env`

### Email confirmation not working
- Check Supabase logs: **Authentication** → **Logs**
- Verify email templates are enabled
- For development, you can disable email confirmation:
  - **Authentication** → **Providers** → **Email**
  - Toggle off "Confirm email"

### Google OAuth not working
- Verify redirect URI matches exactly
- Check Google Cloud Console credentials are correct
- Ensure Google provider is enabled in Supabase

### User can't access main app
- Verify email is confirmed (check Supabase dashboard)
- Clear browser cache and cookies
- Check browser console for errors

---

## 📊 Supabase Dashboard Shortcuts

- **Users**: `Authentication` → `Users`
- **API Keys**: `Project Settings` → `API`
- **Logs**: `Authentication` → `Logs`
- **Email Templates**: `Authentication` → `Email Templates`
- **Providers**: `Authentication` → `Providers`

---

## 🎯 Next Steps

After authentication is working:
1. ✅ Test all auth flows (signup, login, logout)
2. ✅ Customize email templates
3. ✅ Set up Google OAuth (optional)
4. ✅ Deploy to production and update environment variables
5. ✅ Consider adding password reset flow
6. ✅ Add user metadata (profile pictures, preferences)

---

**Need Help?**
- Supabase Docs: https://supabase.com/docs/guides/auth
- Discord: https://discord.supabase.com
