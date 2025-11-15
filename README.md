# Skraper Web - Full-Stack Social Media Analytics

A full-stack web application for social media data extraction and analysis, built with Supabase for real-time data and authentication.

## 🚀 Features

### Authentication & User Management
- ✅ **GitHub OAuth** integration
- ✅ **Magic Link** email authentication  
- ✅ **User profiles** with avatars
- ✅ **Secure session management**

### Real-time Todos
- ✅ **CRUD operations** with real-time sync
- ✅ **Row Level Security** (RLS) policies
- ✅ **Live updates** across multiple devices
- ✅ **User-specific data isolation**

### Social Media Scraping
- ✅ **18+ platform support** (Instagram, TikTok, Facebook, etc.)
- ✅ **Enhanced data analysis** for AI agents
- ✅ **Brand voice analysis**
- ✅ **Engagement pattern recognition**
- ✅ **Content theme identification**

### Modern UI/UX
- ✅ **Responsive design** with Tailwind CSS
- ✅ **Smooth animations** with Anime.js
- ✅ **Interactive particle background** with p5.js
- ✅ **Glass morphism** design elements

## 🛠 Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first styling
- **JavaScript ES6+** - Modern JavaScript
- **Anime.js** - Smooth animations
- **p5.js** - Particle background effects
- **Splitting.js** - Text animations
- **Typed.js** - Typewriter effects

### Backend & Database
- **Supabase** - Backend-as-a-Service
  - **PostgreSQL** - Primary database
  - **Authentication** - User management
  - **Real-time subscriptions** - Live updates
  - **Row Level Security** - Data protection

### Deployment
- **Netlify** - Static site hosting
- **CDN delivery** - Global performance
- **Environment variables** - Secure configuration

## 📁 Project Structure

```
/mnt/okcomputer/output/
├── index.html              # Main application page
├── app.js                  # Main application logic
├── supabase-schema.sql     # Database schema & RLS policies
├── netlify.toml           # Netlify configuration
├── README.md              # This file
└── resources/             # Static assets
    ├── app-icon.png       # Application icon
    ├── hero-bg.png        # Hero background
    └── json-visual.png    # JSON visualization
```

## 🚀 Quick Start

### 1. Set up Supabase

1. **Create Supabase project** at [supabase.com](https://supabase.com)
2. **Copy the SQL schema** from `supabase-schema.sql`
3. **Paste into Supabase SQL Editor** and run
4. **Note your project URL and anon key**

### 2. Deploy to Netlify

1. **Create Netlify account** at [netlify.com](https://netlify.com)
2. **Connect your GitHub repository**
3. **Add environment variables** in Netlify dashboard:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   ```
4. **Deploy the site**

### 3. Configure Authentication

1. **Enable GitHub OAuth** in Supabase dashboard
2. **Add redirect URL**: `https://your-site.netlify.app`
3. **Test authentication flow**

## 📋 Environment Variables

Add these to your Netlify dashboard → Site settings → Environment variables:

```bash
# Supabase Configuration
SUPABASE_URL=https://pmloahcuayyyizyfpoycs.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtbG9haGN1YXl5aXp5ZnBveWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MzE0ODAsImV4cCI6MjA3ODAwNzQ4MH0.ETj1GRraw5ek4qNwC7QSAhUIhN935f1qledd5cbfp34
```

## 🎯 Usage

### Authentication
1. **Sign in with GitHub** - One-click OAuth
2. **Sign up with Magic Link** - Email-based authentication
3. **Automatic profile creation** - Avatars and usernames

### Todo Management
1. **Add tasks** - Type and press Enter
2. **Complete tasks** - Click checkbox
3. **Delete tasks** - Click trash icon
4. **Real-time updates** - Changes sync instantly

### Social Media Scraping
1. **Enter URL** - Supports 18+ platforms
2. **Configure options** - Content type, format, limits
3. **Start scraping** - Real-time progress tracking
4. **View results** - Enhanced JSON with AI analysis

## 🔧 Configuration

### Supabase Schema
The database includes:
- **profiles table** - User information
- **todos table** - Task management
- **RLS policies** - Row-level security
- **Real-time subscriptions** - Live updates

### Netlify Configuration
- **SPA routing** - All routes to index.html
- **Security headers** - Production-ready
- **Asset caching** - Performance optimization
- **Environment variables** - Secure configuration

## 🎨 Customization

### Colors
Update CSS variables in `<style>` section:
```css
:root {
    --primary: #1a365d;      /* Main color */
    --secondary: #00d4ff;    /* Accent color */
    --accent: #ff6b35;       /* Highlight color */
    --success: #10b981;      /* Success color */
    --error: #ef4444;        /* Error color */
}
```

### Animations
Modify animation parameters in `app.js`:
```javascript
// Animation timing and easing
anime({
    duration: 800,
    easing: 'easeOutExpo',
    delay: anime.stagger(200)
});
```

### Particles
Adjust particle system in `setupParticleBackground()`:
```javascript
const numParticles = 50;        // Number of particles
const particleSpeed = 0.5;      // Movement speed
const connectionDistance = 100; // Connection threshold
```

## 🔒 Security

### Authentication Security
- **PKCE flow** for OAuth
- **Secure session management**
- **Automatic token refresh**
- **CSRF protection**

### Database Security
- **Row Level Security** (RLS) policies
- **User isolation** - Users can only access their data
- **Input validation** - SQL injection prevention
- **Rate limiting** - Abuse prevention

### Application Security
- **HTTPS only** - Encrypted connections
- **Security headers** - XSS, CSRF protection
- **Input sanitization** - XSS prevention
- **No secrets in code** - Environment variables

## 📊 Database Schema

### Profiles Table
```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    username TEXT UNIQUE,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Todos Table
```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id),
    task TEXT NOT NULL,
    is_complete BOOLEAN DEFAULT false,
    inserted_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### RLS Policies
```sql
-- Users can only see their own data
CREATE POLICY "Users can view own todos" ON todos
    FOR SELECT USING (auth.uid() = user_id);

-- Users can only modify their own data
CREATE POLICY "Users can update own todos" ON todos
    FOR UPDATE USING (auth.uid() = user_id);
```

## 🚀 Performance

### Optimization Features
- **CDN delivery** - Global asset distribution
- **Lazy loading** - On-demand resource loading
- **Debounced inputs** - Reduced API calls
- **Efficient rendering** - Minimal DOM updates
- **Compressed assets** - Smaller file sizes

### Monitoring
- **Real-time subscriptions** - Live data updates
- **Error boundaries** - Graceful error handling
- **Performance metrics** - Loading states
- **User feedback** - Success/error messages

## 🐛 Troubleshooting

### Common Issues

**"Failed to connect to Supabase"**
- Check environment variables in Netlify
- Verify Supabase project is active
- Check network connectivity

**"Authentication not working"**
- Verify OAuth credentials in Supabase
- Check redirect URLs configuration
- Ensure magic link provider is enabled

**"Real-time updates not working"**
- Verify RLS policies are enabled
- Check subscription filters
- Ensure user is authenticated

### Debug Mode
Enable debug logging in `app.js`:
```javascript
// Add to constructor
this.debugMode = true;

// Use throughout app
if (this.debugMode) {
    console.log('Debug:', data);
}
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- **Supabase** - Backend-as-a-Service platform
- **Netlify** - Static site hosting
- **Tailwind CSS** - Utility-first CSS framework
- **Anime.js** - Animation library
- **p5.js** - Creative coding library

---

## 🎉 Deployment Checklist

Before deploying, ensure:

- [ ] Supabase project created
- [ ] SQL schema executed
- [ ] Authentication providers configured
- [ ] Environment variables added to Netlify
- [ ] GitHub repository connected
- [ ] Netlify deployment successful
- [ ] Authentication flow tested
- [ ] Real-time todos working
- [ ] Social media scraping functional

**Need help?** Check the troubleshooting section or create an issue.

---

**Built with ❤️ using Supabase and Netlify**