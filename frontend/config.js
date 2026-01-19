// Frontend Configuration
// Note: Supabase anon keys are safe to expose in frontend code
// Security is enforced through Row Level Security (RLS) policies in Supabase

const CONFIG = {
    SUPABASE_URL: 'https://envlmnomvlwmytrqelnz.supabase.co',
    SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVudmxtbm9tdmx3bXl0cnFlbG56Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc2OTA0NjUsImV4cCI6MjA4MzI2NjQ2NX0.lp7zWRwQGeDeKlkrD0q5ECFfkkC1fPMmrOvHSs-eCYs',
    API_BASE_URL: 'http://localhost:8000'
};

// For production (Vercel), use relative URLs since frontend and backend are on the same domain
if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    // Use empty string for same-origin requests on Vercel
    CONFIG.API_BASE_URL = '';
}
