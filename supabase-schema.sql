-- Supabase Schema for Skraper Web Full-Stack App
-- Enable UUID extension for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create profiles table to store user information
-- This table references auth.users to maintain connection with Supabase auth
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create todos table for user tasks
-- Uses UUID primary key with default generation
-- References profiles for user ownership
CREATE TABLE IF NOT EXISTS public.todos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    task TEXT NOT NULL,
    is_complete BOOLEAN DEFAULT false,
    inserted_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (RLS) on both tables
-- This ensures users can only access their own data
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.todos ENABLE ROW LEVEL SECURITY;

-- Create updated_at trigger function
-- This automatically updates the updated_at timestamp on any changes
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add updated_at triggers to both tables
CREATE TRIGGER handle_profiles_updated_at BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER handle_todos_updated_at BEFORE UPDATE ON public.todos
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- PROFILES TABLE RLS POLICIES
-- Users can only see their own profile
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);

-- Users can insert their own profile (happens on signup)
CREATE POLY "Users can insert own profile" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- Users can delete their own profile
CREATE POLICY "Users can delete own profile" ON public.profiles
    FOR DELETE USING (auth.uid() = id);

-- TODOS TABLE RLS POLICIES
-- Users can only see their own todos
CREATE POLICY "Users can view own todos" ON public.todos
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert todos for themselves
CREATE POLICY "Users can insert own todos" ON public.todos
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own todos
CREATE POLICY "Users can update own todos" ON public.todos
    FOR UPDATE USING (auth.uid() = user_id);

-- Users can delete their own todos
CREATE POLICY "Users can delete own todos" ON public.todos
    FOR DELETE USING (auth.uid() = user_id);

-- Create function to handle new user signup
-- This automatically creates a profile when a user signs up
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, username, avatar_url)
    VALUES (NEW.id, NEW.raw_user_meta_data->>'username', NEW.raw_user_meta_data->>'avatar_url');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Create indexes for better performance
CREATE INDEX idx_todos_user_id ON public.todos(user_id);
CREATE INDEX idx_todos_is_complete ON public.todos(is_complete);
CREATE INDEX idx_todos_inserted_at ON public.todos(inserted_at);

-- Insert sample data for testing (optional)
-- This creates a sample profile and todos for the demo
INSERT INTO public.profiles (id, username, avatar_url) VALUES 
('00000000-0000-0000-0000-000000000000', 'demo_user', 'https://via.placeholder.com/150');

INSERT INTO public.todos (user_id, task, is_complete) VALUES 
('00000000-0000-0000-0000-000000000000', 'Complete Skraper Web integration', true),
('00000000-0000-0000-0000-000000000000', 'Test authentication flow', false),
('00000000-0000-0000-0000-000000000000', 'Deploy to Netlify', false),
('00000000-0000-0000-0000-000000000000', 'Add real-time subscriptions', false),
('00000000-0000-0000-0000-000000000000', 'Create AI agent integration', false);

-- Grant necessary permissions
GRANT ALL ON public.profiles TO anon;
GRANT ALL ON public.profiles TO authenticated;
GRANT ALL ON public.todos TO anon;
GRANT ALL ON public.todos TO authenticated;
GRANT ALL ON public.handle_updated_at TO anon;
GRANT ALL ON public.handle_updated_at TO authenticated;
GRANT ALL ON public.handle_new_user TO anon;
GRANT ALL ON public.handle_new_user TO authenticated;

-- Success message
SELECT 'Supabase schema created successfully! 🎉' as status;