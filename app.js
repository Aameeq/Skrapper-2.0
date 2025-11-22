// Skraper Web Full-Stack App - Supabase Integration
// Main application logic for authentication and real-time todos

class SkraperWebApp {
    constructor() {
        // Initialize Supabase client
        this.supabase = null;
        this.currentUser = null;
        this.todos = [];
        this.isLoading = false;
        
        this.init();
    }

    async init() {
        try {
            // Get Supabase credentials from environment variables
            const supabaseUrl = 'https://pmloahcuayyyizyfpoycs.supabase.co';
            const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtbG9haGN1YXl5aXp5ZnBveWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MzE0ODAsImV4cCI6MjA3ODAwNzQ4MH0.ETj1GRraw5ek4qNwC7QSAhUIhN935f1qledd5cbfp34';
            
            // Initialize Supabase client
            this.supabase = supabase.createClient(supabaseUrl, supabaseAnonKey);
            
            // Check for existing session
            // await this.checkUserSession(); // REMOVED AUTH CHECK - Simulating user session
            
            // *** SIMULATE USER SESSION ***
            this.currentUser = {
                id: 'simulated_user',
                email: 'guest@example.com',
                user_metadata: {}
            };
            // Load profile (might be skipped if not needed, or simulated)
            // await this.loadUserProfile(); // Optionally call if profile loading is needed for UI
            // Show main UI directly
            this.showMainUI();
            // Optionally load todos if the main UI includes them (using simulated user ID)
            // await this.loadTodos(); // Requires modification to use simulated user ID
            // this.subscribeToTodos(); // Requires modification to use simulated user ID
            console.log('✅ Simulated user session active, main UI displayed');
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Initialize UI
            this.initializeUI();
            
            console.log('âœ… Skraper Web App initialized successfully');
            
        } catch (error) {
            console.error('âŒ Failed to initialize app:', error);
            this.showError('Failed to connect to backend. Please refresh the page.');
        }
    }

    // async checkUserSession() {
    //     try {
    //         const { data: { user }, error } = await this.supabase.auth.getUser();
    //         
    //         if (error) {
    //             console.log('No active session:', error.message);
    //             this.showAuthUI();
    //             return;
    //         }
    //         
    //         if (user) {
    //             this.currentUser = user;
    //             await this.loadUserProfile();
    //             this.showMainUI();
    //             await this.loadTodos();
    //             this.subscribeToTodos();
    //         } else {
    //             this.showAuthUI();
    //         }
    //         
    //     } catch (error) {
    //         console.error('Error checking session:', error);
    //         this.showAuthUI();
    //     }
    // }

    async loadUserProfile() {
        if (!this.currentUser) return;
        
        try {
            const { data, error } = await this.supabase
                .from('profiles')
                .select('*')
                .eq('id', this.currentUser.id)
                .single();
            
            if (error) {
                console.log('Profile not found, creating...');
                await this.createUserProfile();
            } else {
                this.userProfile = data;
                this.updateUserUI();
            }
            
        } catch (error) {
            console.error('Error loading profile:', error);
        }
    }

    async createUserProfile() {
        if (!this.currentUser) return;
        
        try {
            const { data, error } = await this.supabase
                .from('profiles')
                .insert([{
                    id: this.currentUser.id,
                    username: this.currentUser.email?.split('@')[0] || 'user',
                    avatar_url: `https://ui-avatars.com/api/?name=${encodeURIComponent(this.currentUser.email || 'User')}&background=random`
                }]);
            
            if (error) throw error;
            
            console.log('âœ… User profile created');
            await this.loadUserProfile();
            
        } catch (error) {
            console.error('Error creating profile:', error);
        }
    }

    updateUserUI() {
        if (!this.userProfile) return;
        
        const userAvatar = document.getElementById('userAvatar');
        const userName = document.getElementById('userName');
        
        if (userAvatar && this.userProfile.avatar_url) {
            userAvatar.src = this.userProfile.avatar_url;
        }
        
        if (userName && this.userProfile.username) {
            userName.textContent = this.userProfile.username;
        }
    }

    setupEventListeners() {
        // Authentication buttons
        const signInBtn = document.getElementById('signInBtn');
        const signUpBtn = document.getElementById('signUpBtn');
        const signOutBtn = document.getElementById('signOutBtn');
        
        if (signInBtn) {
            signInBtn.addEventListener('click', () => this.handleSignIn());
        }
        
        if (signUpBtn) {
            signUpBtn.addEventListener('click', () => this.handleSignUp());
        }
        
        if (signOutBtn) {
            signOutBtn.addEventListener('click', () => this.handleSignOut());
        }

        // Todo form
        const todoForm = document.getElementById('todoForm');
        if (todoForm) {
            todoForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleAddTodo();
            });
        }

        // URL input for scraping
        const urlInput = document.getElementById('urlInput');
        if (urlInput) {
            urlInput.addEventListener('input', (e) => {
                this.handleUrlInput(e.target.value);
            });
        }

        // Scrape button
        const scrapeButton = document.getElementById('scrapeButton');
        if (scrapeButton) {
            scrapeButton.addEventListener('click', () => this.startScraping());
        }
    }

    initializeUI() {
        // Initialize animations and effects
        this.initializeAnimations();
        this.setupParticleBackground();
        this.startTypedAnimation();
    }

    showAuthUI() {
        const authSection = document.getElementById('authSection');
        const mainSection = document.getElementById('mainSection');
        
        if (authSection) {
            authSection.classList.remove('hidden');
        }
        
        if (mainSection) {
            mainSection.classList.add('hidden');
        }
    }

    showMainUI() {
        const authSection = document.getElementById('authSection');
        const mainSection = document.getElementById('mainSection');
        
        if (authSection) {
            authSection.classList.add('hidden');
        }
        
        if (mainSection) {
            mainSection.classList.remove('hidden');
        }
        
        // Animate main UI appearance
        anime({
            targets: '#mainSection',
            opacity: [0, 1],
            translateY: [50, 0],
            duration: 800,
            easing: 'easeOutExpo'
        });
    }

    async handleSignIn() {
        try {
            this.showLoading(true);
            
            const { data, error } = await this.supabase.auth.signInWithOAuth({
                provider: 'github',
                options: {
                    redirectTo: window.location.origin
                }
            });
            
            if (error) throw error;
            
            console.log('âœ… Sign in initiated');
            
        } catch (error) {
            console.error('âŒ Sign in failed:', error);
            this.showError('Failed to sign in. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    async handleSignUp() {
        const email = prompt('Enter your email address for magic link signup:');
        
        if (!email) return;
        
        try {
            this.showLoading(true);
            
            const { data, error } = await this.supabase.auth.signInWithOtp({
                email: email,
                options: {
                    emailRedirectTo: window.location.origin
                }
            });
            
            if (error) throw error;
            
            alert('Magic link sent! Check your email to complete signup.');
            console.log('âœ… Magic link sent');
            
        } catch (error) {
            console.error('âŒ Sign up failed:', error);
            this.showError('Failed to send magic link. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    async handleSignOut() {
        try {
            const { error } = await this.supabase.auth.signOut();
            
            if (error) throw error;
            
            this.currentUser = null;
            this.userProfile = null;
            this.todos = [];
            
            this.showAuthUI();
            
            console.log('âœ… Signed out successfully');
            
        } catch (error) {
            console.error('âŒ Sign out failed:', error);
            this.showError('Failed to sign out. Please try again.');
        }
    }

    async loadTodos() {
        if (!this.currentUser) return;
        
        try {
            const { data, error } = await this.supabase
                .from('todos')
                .select('*')
                .eq('user_id', this.currentUser.id)
                .order('inserted_at', { ascending: false });
            
            if (error) throw error;
            
            this.todos = data || [];
            this.renderTodos();
            
            console.log(`âœ… Loaded ${this.todos.length} todos`);
            
        } catch (error) {
            console.error('âŒ Failed to load todos:', error);
            this.showError('Failed to load todos.');
        }
    }

    async handleAddTodo() {
        const todoInput = document.getElementById('todoInput');
        const task = todoInput?.value.trim();
        
        if (!task || !this.currentUser) return;
        
        try {
            const { data, error } = await this.supabase
                .from('todos')
                .insert([{
                    user_id: this.currentUser.id,
                    task: task
                }]);
            
            if (error) throw error;
            
            todoInput.value = '';
            console.log('âœ… Todo added successfully');
            
        } catch (error) {
            console.error('âŒ Failed to add todo:', error);
            this.showError('Failed to add todo.');
        }
    }

    async toggleTodo(todoId, currentStatus) {
        if (!this.currentUser) return;
        
        try {
            const { data, error } = await this.supabase
                .from('todos')
                .update({ is_complete: !currentStatus })
                .eq('id', todoId)
                .eq('user_id', this.currentUser.id);
            
            if (error) throw error;
            
            console.log('âœ… Todo updated successfully');
            
        } catch (error) {
            console.error('âŒ Failed to update todo:', error);
            this.showError('Failed to update todo.');
        }
    }

    async deleteTodo(todoId) {
        if (!this.currentUser) return;
        
        try {
            const { data, error } = await this.supabase
                .from('todos')
                .delete()
                .eq('id', todoId)
                .eq('user_id', this.currentUser.id);
            
            if (error) throw error;
            
            console.log('âœ… Todo deleted successfully');
            
        } catch (error) {
            console.error('âŒ Failed to delete todo:', error);
            this.showError('Failed to delete todo.');
        }
    }

    subscribeToTodos() {
        if (!this.currentUser) return;
        
        const channel = this.supabase
            .channel('todos_changes')
            .on(
                'postgres_changes',
                {
                    event: '*',
                    schema: 'public',
                    table: 'todos',
                    filter: `user_id=eq.${this.currentUser.id}`
                },
                (payload) => {
                    console.log('ðŸ”„ Real-time update received:', payload.eventType);
                    this.handleRealtimeUpdate(payload);
                }
            )
            .subscribe();
        
        console.log('âœ… Subscribed to real-time todo updates');
    }

    handleRealtimeUpdate(payload) {
        const { eventType, new: newRecord, old: oldRecord } = payload;
        
        switch (eventType) {
            case 'INSERT':
                this.todos.unshift(newRecord);
                break;
            case 'UPDATE':
                const updateIndex = this.todos.findIndex(todo => todo.id === newRecord.id);
                if (updateIndex !== -1) {
                    this.todos[updateIndex] = newRecord;
                }
                break;
            case 'DELETE':
                this.todos = this.todos.filter(todo => todo.id !== oldRecord.id);
                break;
        }
        
        this.renderTodos();
    }

    renderTodos() {
        const todoList = document.getElementById('todoList');
        if (!todoList) return;
        
        if (this.todos.length === 0) {
            todoList.innerHTML = `
                <div class="text-center py-8 text-gray-400">
                    <p>No todos yet. Add one above!</p>
                </div>
            `;
            return;
        }
        
        todoList.innerHTML = this.todos.map(todo => `
            <div class="flex items-center p-4 bg-gray-800 rounded-lg mb-3 hover:bg-gray-700 transition-colors">
                <input 
                    type="checkbox" 
                    ${todo.is_complete ? 'checked' : ''} 
                    class="mr-3 w-5 h-5 text-cyan-500 rounded focus:ring-cyan-500"
                    onchange="app.toggleTodo('${todo.id}', ${todo.is_complete})"
                >
                <span class="flex-1 ${todo.is_complete ? 'line-through text-gray-500' : 'text-white'}">
                    ${this.escapeHtml(todo.task)}
                </span>
                <button 
                    onclick="app.deleteTodo('${todo.id}')"
                    class="ml-3 text-red-400 hover:text-red-300 transition-colors"
                    title="Delete todo"
                >
                    ðŸ—‘ï¸
                </button>
            </div>
        `).join('');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showLoading(show) {
        const loadingElements = document.querySelectorAll('.loading');
        loadingElements.forEach(el => {
            el.style.display = show ? 'block' : 'none';
        });
    }

    showError(message) {
        // Create or update error message
        let errorDiv = document.getElementById('errorMessage');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'errorMessage';
            errorDiv.className = 'fixed top-20 left-1/2 transform -translate-x-1/2 bg-red-600 text-white px-6 py-3 rounded-lg z-50';
            document.body.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    // Original Skraper functionality (for backward compatibility)
    handleUrlInput(url) {
        // This would integrate with the original scraping functionality
        // For now, it's a placeholder for the existing features
        console.log('URL input:', url);
    }

    startScraping() {
        // This would integrate with the original scraping functionality
        console.log('Starting scrape...');
    }

    // Animation and UI enhancements
    initializeAnimations() {
        // Animate stats cards on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateStatsCards();
                }
            });
        }, observerOptions);

        const statsSection = document.querySelector('.stats-card');
        if (statsSection) {
            observer.observe(statsSection);
        }

        // Animate glass cards on load
        anime({
            targets: '.glass-card',
            opacity: [0, 1],
            translateY: [50, 0],
            delay: anime.stagger(200),
            duration: 800,
            easing: 'easeOutExpo'
        });
    }

    setupParticleBackground() {
        // P5.js particle system
        new p5((p) => {
            let particles = [];
            const numParticles = 50;

            p.setup = () => {
                const canvas = p.createCanvas(p.windowWidth, p.windowHeight);
                canvas.id('p5-canvas');
                canvas.parent(document.getElementById('p5-canvas'));
                
                // Initialize particles
                for (let i = 0; i < numParticles; i++) {
                    particles.push({
                        x: p.random(p.width),
                        y: p.random(p.height),
                        vx: p.random(-0.5, 0.5),
                        vy: p.random(-0.5, 0.5),
                        size: p.random(2, 6),
                        opacity: p.random(0.3, 0.8)
                    });
                }
            };

            p.draw = () => {
                p.clear();
                
                // Update and draw particles
                particles.forEach(particle => {
                    // Update position
                    particle.x += particle.vx;
                    particle.y += particle.vy;
                    
                    // Wrap around edges
                    if (particle.x < 0) particle.x = p.width;
                    if (particle.x > p.width) particle.x = 0;
                    if (particle.y < 0) particle.y = p.height;
                    if (particle.y > p.height) particle.y = 0;
                    
                    // Draw particle
                    p.fill(0, 212, 255, particle.opacity * 255);
                    p.noStroke();
                    p.circle(particle.x, particle.y, particle.size);
                    
                    // Draw connections
                    particles.forEach(other => {
                        const distance = p.dist(particle.x, particle.y, other.x, other.y);
                        if (distance < 100) {
                            p.stroke(0, 212, 255, (1 - distance / 100) * 50);
                            p.strokeWeight(1);
                            p.line(particle.x, particle.y, other.x, other.y);
                        }
                    });
                });
            };

            p.windowResized = () => {
                p.resizeCanvas(p.windowWidth, p.windowHeight);
            };
        });
    }

    startTypedAnimation() {
        const typedElement = document.getElementById('typed-text');
        if (typedElement) {
            new Typed('#typed-text', {
                strings: [
                    'Extract Social Data',
                    'Scrape Media Content',
                    'Analyze Engagement',
                    'Get JSON Results'
                ],
                typeSpeed: 80,
                backSpeed: 50,
                backDelay: 2000,
                loop: true,
                showCursor: true,
                cursorChar: '|'
            });
        }
    }

    animateStatsCards() {
        anime({
            targets: '.stats-card',
            scale: [0.8, 1],
            opacity: [0, 1],
            delay: anime.stagger(100),
            duration: 600,
            easing: 'easeOutElastic(1, .8)'
        });
    }
}

// Initialize the app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new SkraperWebApp();
    
    // Make app globally available for onclick handlers
    window.app = app;
});

// Handle authentication redirect
// if (window.location.hash) {
//     // This handles OAuth redirects from GitHub
//     window.addEventListener('load', async () => {
//         const supabaseUrl = 'https://pmloahcuayyyizyfpoycs.supabase.co';
//         const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtbG9haGN1YXl5aXp5ZnBveWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MzE0ODAsImV4cCI6MjA3ODAwNzQ4MH0.ETj1GRraw5ek4qNwC7QSAhUIhN935f1qledd5cbfp34';
//         const supabase = supabase.createClient(supabaseUrl, supabaseAnonKey);
//         
//         try {
//             await supabase.auth.getUser();
//             window.location.hash = '';
//         } catch (error) {
//             console.log('No session found');
//         }
//     });
// }



