# Deployment Guide

## Option 1: Streamlit Cloud (Recommended for Beginners)

### Prerequisites
- GitHub account with your code pushed to a repo
- `requirements.txt` file in your repo listing Python packages

### Steps
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository, branch, and main file (e.g., `app.py`)
5. Click "Deploy"
6. Wait 2-5 minutes — your app will be live at `https://[your-app].streamlit.app`

### requirements.txt example
```
streamlit
pandas
plotly
```

### Troubleshooting
- **App crashes on deploy**: Check that all packages are in `requirements.txt`
- **Data not loading**: Use relative paths (`data.csv` not `/home/user/data.csv`)
- **Slow loading**: Consider reducing dataset size or adding `@st.cache_data`

## Option 2: Vercel (For JavaScript/Next.js Apps)

### Steps
1. Push your code to GitHub
2. Go to https://vercel.com/new
3. Import your GitHub repository
4. Vercel auto-detects your framework
5. Click "Deploy"
6. Live at `https://[your-project].vercel.app`

## Option 3: Netlify

### Steps
1. Push your code to GitHub
2. Go to https://app.netlify.com/start
3. Connect to GitHub and select your repo
4. Set build command and publish directory
5. Click "Deploy site"

## Option 4: Hugging Face Spaces

### Good for ML/data science apps
1. Go to https://huggingface.co/spaces
2. Create new Space
3. Choose Streamlit or Gradio
4. Upload your files or connect to GitHub
5. Space builds and deploys automatically

## Making Your App Shareable

Once deployed, you'll have a URL you can share with anyone. To make it more professional:

1. **Add a good title and description** in your app
2. **Include an "About" section** explaining the data source and methodology
3. **Add your name/attribution**
4. **Test on mobile** — many people will view on phones
5. **Share the link** — that's your portfolio piece!

## After the Workshop

Your app will stay deployed as long as:
- Your GitHub repo exists
- Your deployment platform account is active
- (Streamlit Cloud) The app gets at least one visit per month

To update your app later:
1. Edit your code locally or on GitHub
2. Push changes to the main branch
3. The deployment platform will automatically redeploy
