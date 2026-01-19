// Supabase Client Configuration
// This file is kept for compatibility but config.js is the primary configuration source
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.38.4/+esm';

// Import configuration (ensure config.js is loaded first)
const SUPABASE_URL = window.CONFIG?.SUPABASE_URL || 'https://envlmnomvlwmytrqelnz.supabase.co';
const SUPABASE_ANON_KEY = window.CONFIG?.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVudmxtbm9tdmx3bXl0cnFlbG56Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc2OTA0NjUsImV4cCI6MjA4MzI2NjQ2NX0.lp7zWRwQGeDeKlkrD0q5ECFfkkC1fPMmrOvHSs-eCYs';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

export { supabase };
