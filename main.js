// Skraper Web App - Main JavaScript with Functional Backend Integration
class SkraperApp {
    constructor() {
        this.isProcessing = false;
        this.currentPlatform = null;
        this.apiBaseUrl = 'https://skraper-api.onrender.com/api'; // Cloud backend URL
        this.supportedPlatforms = {
            instagram: {
                pattern: /(?:instagram\.com|instagr\.am)\/(?:[\w\.]+)/,
                icon: '📷',
                color: '#E4405F'
            },
            tiktok: {
                pattern: /tiktok\.com\/@([\w\.]+)/,
                icon: '🎵',
                color: '#FF0050'
            },
            twitter: {
                pattern: /(?:twitter\.com|x\.com)\/([\w]+)/,
                icon: '🐦',
                color: '#1DA1F2'
            },
            youtube: {
                pattern: /(?:youtube\.com|youtu\.be)\/(?:channel\/|user\/|c\/)?([\w-]+)/,
                icon: '📺',
                color: '#FF0000'
            },
            facebook: {
                pattern: /facebook\.com\/(?:[\w\.]+)/,
                icon: '📘',
                color: '#1877F2'
            },
            reddit: {
                pattern: /reddit\.com\/(?:r\/|user\/)?([\w]+)/,
                icon: '🔴',
                color: '#FF4500'
            }
        };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeAnimations();
        this.setupParticleBackground();
        this.startTypedAnimation();
        this.checkBackendStatus();
    }

    async checkBackendStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/scrape/status`);
            const data = await response.json();
            
            if (data.skraper_available || data.enhanced_features) {
                console.log('✅ Backend connected and functional');
                this.showBackendStatus(true);
            } else {
                console.log('⚠️  Backend connected but limited functionality');
                this.showBackendStatus(true, 'Limited functionality');
            }
        } catch (error) {
            console.log('❌ Backend not connected:', error.message);
            this.showBackendStatus(false, 'Backend not connected');
            this.enableMockMode();
        }
    }

    showBackendStatus(available, message = null) {
        const statusIndicator = document.createElement('div');
        statusIndicator.id = 'backendStatus';
        statusIndicator.className = `fixed top-20 right-6 z-50 px-4 py-2 rounded-lg text-sm font-medium ${
            available ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
        }`;
        statusIndicator.textContent = available ? '✅ API Connected' : `❌ ${message || 'API Disconnected'}`;
        
        document.body.appendChild(statusIndicator);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (statusIndicator.parentNode) {
                statusIndicator.parentNode.removeChild(statusIndicator);
            }
        }, 5000);
    }

    enableMockMode() {
        console.log('🔄 Enabling mock mode for demonstration');
        // In a real deployment, this would be removed
        this.mockMode = true;
    }

    setupEventListeners() {
        const urlInput = document.getElementById('urlInput');
        const scrapeButton = document.getElementById('scrapeButton');
        const postLimit = document.getElementById('postLimit');
        const limitValue = document.getElementById('limitValue');
        const cancelButton = document.getElementById('cancelButton');

        // URL input validation and platform detection
        urlInput.addEventListener('input', (e) => {
            this.handleUrlInput(e.target.value);
        });

        // Scrape button click
        scrapeButton.addEventListener('click', () => {
            this.startScraping();
        });

        // Post limit slider
        postLimit.addEventListener('input', (e) => {
            limitValue.textContent = e.target.value;
        });

        // Cancel button
        if (cancelButton) {
            cancelButton.addEventListener('click', () => {
                this.cancelScraping();
            });
        }

        // Platform icon hover effects
        document.querySelectorAll('.platform-icon').forEach(icon => {
            icon.addEventListener('mouseenter', () => {
                anime({
                    targets: icon,
                    scale: 1.2,
                    rotate: '5deg',
                    duration: 300,
                    easing: 'easeOutElastic(1, .8)'
                });
            });

            icon.addEventListener('mouseleave', () => {
                anime({
                    targets: icon,
                    scale: 1,
                    rotate: '0deg',
                    duration: 300,
                    easing: 'easeOutElastic(1, .8)'
                });
            });
        });
    }

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

    handleUrlInput(url) {
        const validationDiv = document.getElementById('urlValidation');
        const platformIndicator = document.getElementById('platformIndicator');
        const scrapeButton = document.getElementById('scrapeButton');
        
        if (!url) {
            this.clearPlatformDetection();
            return;
        }

        // Detect platform
        const detectedPlatform = this.detectPlatform(url);
        
        if (detectedPlatform) {
            this.showPlatformDetected(detectedPlatform);
            validationDiv.innerHTML = `<span class="text-green-400">✓ ${detectedPlatform.charAt(0).toUpperCase() + detectedPlatform.slice(1)} URL detected</span>`;
            scrapeButton.disabled = false;
            scrapeButton.classList.add('pulse-glow');
        } else {
            this.clearPlatformDetection();
            if (url.length > 10) {
                validationDiv.innerHTML = '<span class="text-yellow-400">⚠ Unsupported platform or invalid URL format</span>';
            } else {
                validationDiv.innerHTML = '';
            }
            scrapeButton.disabled = true;
            scrapeButton.classList.remove('pulse-glow');
        }
    }

    detectPlatform(url) {
        for (const [platform, config] of Object.entries(this.supportedPlatforms)) {
            if (config.pattern.test(url)) {
                this.currentPlatform = platform;
                return platform;
            }
        }
        this.currentPlatform = null;
        return null;
    }

    showPlatformDetected(platform) {
        const platformIndicator = document.getElementById('platformIndicator');
        const config = this.supportedPlatforms[platform];
        
        platformIndicator.innerHTML = `
            <div class="flex items-center space-x-2 bg-gray-800 rounded-lg px-3 py-1">
                <span class="text-xl">${config.icon}</span>
                <span class="text-sm font-medium">${platform.charAt(0).toUpperCase() + platform.slice(1)}</span>
            </div>
        `;

        // Highlight platform icon
        document.querySelectorAll('.platform-icon').forEach(icon => {
            icon.classList.remove('active');
            if (icon.dataset.platform === platform) {
                icon.classList.add('active');
                icon.style.color = config.color;
            }
        });

        // Animate platform indicator
        anime({
            targets: platformIndicator,
            scale: [0, 1],
            opacity: [0, 1],
            duration: 500,
            easing: 'easeOutElastic(1, .8)'
        });
    }

    clearPlatformDetection() {
        const platformIndicator = document.getElementById('platformIndicator');
        
        platformIndicator.innerHTML = '';
        
        document.querySelectorAll('.platform-icon').forEach(icon => {
            icon.classList.remove('active');
            icon.style.color = '';
        });
    }

    async startScraping() {
        if (this.isProcessing) return;
        
        this.isProcessing = true;
        const scrapeButton = document.getElementById('scrapeButton');
        const buttonText = document.getElementById('buttonText');
        const loadingSpinner = document.getElementById('loadingSpinner');
        const progressSection = document.getElementById('progressSection');
        
        // Update button state
        scrapeButton.disabled = true;
        scrapeButton.classList.remove('pulse-glow');
        buttonText.textContent = 'Processing...';
        loadingSpinner.classList.remove('hidden');
        
        // Show progress section
        progressSection.classList.remove('hidden');
        
        // Animate progress section appearance
        anime({
            targets: progressSection,
            opacity: [0, 1],
            translateY: [50, 0],
            duration: 500,
            easing: 'easeOutExpo'
        });
        
        // Scroll to progress section
        progressSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        try {
            // Call the backend API
            await this.callScrapingAPI();
        } catch (error) {
            console.error('Scraping failed:', error);
            this.showError('Scraping failed: ' + error.message);
            this.resetScrapingState();
        }
    }

    async callScrapingAPI() {
        const url = document.getElementById('urlInput').value;
        const contentType = document.getElementById('contentType').value;
        const limit = parseInt(document.getElementById('postLimit').value);
        const outputFormat = document.getElementById('outputFormat').value;
        
        // Update progress status
        const progressStatus = document.getElementById('progressStatus');
        progressStatus.textContent = 'Sending request to backend...';
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/scrape/enhanced`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    content_type: contentType,
                    limit: limit,
                    output_format: outputFormat
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Store results and redirect
            localStorage.setItem('scrapingResults', JSON.stringify(data));
            this.completeScraping();
            
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    }

    completeScraping() {
        const progressStatus = document.getElementById('progressStatus');
        const buttonText = document.getElementById('buttonText');
        const loadingSpinner = document.getElementById('loadingSpinner');
        
        progressStatus.textContent = 'Scraping completed successfully!';
        progressStatus.className = 'text-green-400';
        
        // Update button
        buttonText.textContent = 'View Results';
        loadingSpinner.classList.add('hidden');
        
        // Change button to redirect to results
        const scrapeButton = document.getElementById('scrapeButton');
        scrapeButton.onclick = () => {
            window.location.href = 'results.html';
        };
        scrapeButton.disabled = false;
        
        // Show completion animation
        anime({
            targets: '.glass-card',
            scale: [1, 1.02, 1],
            duration: 600,
            easing: 'easeOutElastic(1, .8)'
        });
        
        this.isProcessing = false;
    }

    resetScrapingState() {
        this.isProcessing = false;
        const scrapeButton = document.getElementById('scrapeButton');
        const buttonText = document.getElementById('buttonText');
        const loadingSpinner = document.getElementById('loadingSpinner');
        
        // Reset button
        scrapeButton.disabled = false;
        buttonText.textContent = 'Start Scraping';
        loadingSpinner.classList.add('hidden');
    }

    showError(message) {
        const progressStatus = document.getElementById('progressStatus');
        progressStatus.textContent = message;
        progressStatus.className = 'text-red-400';
        
        // Show error animation
        anime({
            targets: progressStatus,
            scale: [1, 1.1, 1],
            duration: 500,
            easing: 'easeOutElastic(1, .8)'
        });
    }

    cancelScraping() {
        if (!this.isProcessing) return;
        
        this.isProcessing = false;
        const scrapeButton = document.getElementById('scrapeButton');
        const buttonText = document.getElementById('buttonText');
        const loadingSpinner = document.getElementById('loadingSpinner');
        const progressSection = document.getElementById('progressSection');
        
        // Reset button
        scrapeButton.disabled = false;
        buttonText.textContent = 'Start Scraping';
        loadingSpinner.classList.add('hidden');
        
        // Hide progress
        anime({
            targets: progressSection,
            opacity: [1, 0],
            translateY: [0, -50],
            duration: 500,
            easing: 'easeOutExpo',
            complete: () => {
                progressSection.classList.add('hidden');
            }
        });
        
        // Reset progress bar
        const progressBar = document.getElementById('progressBar');
        const progressPercent = document.getElementById('progressPercent');
        const progressStatus = document.getElementById('progressStatus');
        
        progressBar.style.width = '0%';
        progressPercent.textContent = '0%';
        progressStatus.textContent = 'Initializing...';
        progressStatus.className = '';
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

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SkraperApp();
});

// Add smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add hover effects to buttons
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.btn-primary, .glass-card');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            anime({
                targets: button,
                scale: 1.02,
                duration: 200,
                easing: 'easeOutQuad'
            });
        });
        
        button.addEventListener('mouseleave', () => {
            anime({
                targets: button,
                scale: 1,
                duration: 200,
                easing: 'easeOutQuad'
            });
        });
    });
});

// Add URL input focus effects
document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    
    urlInput.addEventListener('focus', () => {
        anime({
            targets: urlInput,
            scale: [1, 1.02],
            duration: 300,
            easing: 'easeOutQuad'
        });
    });
    
    urlInput.addEventListener('blur', () => {
        anime({
            targets: urlInput,
            scale: [1.02, 1],
            duration: 300,
            easing: 'easeOutQuad'
        });
    });
});