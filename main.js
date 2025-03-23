/**
 * E-S.H.A.R.A. Website JavaScript
 * Electronic Sign-language Hand Augmented Recognition Assistant (إشارة)
 * 
 * This file combines all interactive functionality for the E-S.H.A.R.A. project website
 * including animations, navigation, sensor point interaction, and visual effects.
 */

document.addEventListener('DOMContentLoaded', function() {
    // ===== Core Functionality =====
    initNavigation();
    initHeroSection();
    initTechnicalSection();
    initAnimations();
    initScrollEffects();
    initTeamSection();
    
    // Add loaded class when everything is ready
    window.addEventListener('load', function() {
        document.body.classList.add('loaded');
    });
});

/**
 * Initialize Navigation Components
 */
function initNavigation() {
    // Mobile Navigation Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const nav = document.querySelector('nav');
    
    if (mobileToggle && nav) {
        mobileToggle.addEventListener('click', function() {
            nav.classList.toggle('active');
            // Toggle between hamburger and close icons
            const icon = this.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
    
    // Smooth Scrolling for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Close mobile menu if open
            if (nav && nav.classList.contains('active')) {
                nav.classList.remove('active');
                if (mobileToggle) {
                    const icon = mobileToggle.querySelector('i');
                    if (icon) {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                }
            }
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80, // Adjusted for header height
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Header Scroll Effect
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Add shadow and background opacity based on scroll position
            if (scrollTop > 50) {
                header.style.backgroundColor = 'rgba(29, 14, 64, 0.95)';
                header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
            } else {
                header.style.backgroundColor = 'rgba(29, 14, 64, 0.8)';
                header.style.boxShadow = '0 2px 15px rgba(0, 0, 0, 0.3)';
            }
            
            // Active menu item based on scroll position
            const sections = document.querySelectorAll('section[id]');
            sections.forEach(section => {
                const sectionTop = section.offsetTop - 100;
                const sectionHeight = section.offsetHeight;
                const sectionId = section.getAttribute('id');
                
                if (scrollTop >= sectionTop && scrollTop < sectionTop + sectionHeight) {
                    document.querySelector(`nav ul li a[href="#${sectionId}"]`)?.classList.add('active');
                } else {
                    document.querySelector(`nav ul li a[href="#${sectionId}"]`)?.classList.remove('active');
                }
            });
        });
    }
}

/**
 * Initialize Hero Section Components
 */
function initHeroSection() {
    // Create and animate background particles
    createParticles();
    
    // Add typing effect to hero tagline
    typeWriterEffect();
    
    // Initialize scroll indicator
    initScrollIndicator();
    
    // Add parallax effect to hero elements
    document.addEventListener('mousemove', function(e) {
        const heroContent = document.querySelector('.hero-content');
        if (!heroContent) return;
        
        const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
        const yAxis = (window.innerHeight / 2 - e.pageY) / 25;
        
        const gloveImage = document.querySelector('.glove-main-image');
        if (gloveImage) {
            gloveImage.style.transform = `translateX(${xAxis}px) translateY(${yAxis}px)`;
        }
        
        const waveAnimation = document.querySelector('.wave-animation');
        if (waveAnimation) {
            waveAnimation.style.transform = `translateX(${xAxis * 2}px) translateY(${yAxis * 2}px) scale(1.2)`;
        }
    });
    
    // Arabic logo animation
    const arabicLogo = document.querySelector('.arabic-logo');
    if (arabicLogo) {
        // Add a subtle animation to the Arabic logo
        arabicLogo.classList.add('animated');
        
        // Change the gradient angle periodically
        let gradientAngle = 90;
        setInterval(() => {
            gradientAngle = (gradientAngle + 5) % 360;
            arabicLogo.style.background = `linear-gradient(${gradientAngle}deg, var(--text-light), var(--accent-purple-light))`;
            arabicLogo.style.webkitBackgroundClip = 'text';
            arabicLogo.style.backgroundClip = 'text';
        }, 3000);
    }
}

/**
 * Creates animated particles in the background
 */
function createParticles() {
    const particlesContainer = document.querySelector('.tech-particles');
    if (!particlesContainer) return;
    
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random position
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        
        // Random size
        const size = Math.random() * 5 + 2;
        
        // Random opacity
        const opacity = Math.random() * 0.5 + 0.1;
        
        // Random animation delay
        const delay = Math.random() * 5;
        
        // Random animation duration
        const duration = Math.random() * 15 + 10;
        
        // Apply styles
        particle.style.cssText = `
            position: absolute;
            top: ${posY}%;
            left: ${posX}%;
            width: ${size}px;
            height: ${size}px;
            border-radius: 50%;
            background-color: rgba(157, 78, 221, ${opacity});
            pointer-events: none;
            animation: float-particle ${duration}s ease-in-out infinite;
            animation-delay: ${delay}s;
        `;
        
        particlesContainer.appendChild(particle);
    }
    
    // Add animation keyframes
    const styleSheet = document.createElement('style');
    styleSheet.innerHTML = `
        @keyframes float-particle {
            0% { transform: translate(0, 0); }
            25% { transform: translate(${Math.random() * 50 - 25}px, ${Math.random() * 50 - 25}px); }
            50% { transform: translate(${Math.random() * 50 - 25}px, ${Math.random() * 50 - 25}px); }
            75% { transform: translate(${Math.random() * 50 - 25}px, ${Math.random() * 50 - 25}px); }
            100% { transform: translate(0, 0); }
        }
    `;
    document.head.appendChild(styleSheet);
}

/**
 * Add typing effect to hero tagline
 */
function typeWriterEffect() {
    // Main tagline typing effect
    const tagline = document.querySelector('.hero-tagline');
    if (tagline) {
        const originalText = tagline.textContent;
        tagline.textContent = '';
        tagline.style.borderRight = '3px solid #9D4EDD';
        
        let charIndex = 0;
        const typingSpeed = 50; // milliseconds per character
        
        function typeWriter() {
            if (charIndex < originalText.length) {
                tagline.textContent += originalText.charAt(charIndex);
                charIndex++;
                setTimeout(typeWriter, typingSpeed);
            } else {
                // Remove cursor after typing is complete
                setTimeout(() => {
                    tagline.style.borderRight = 'none';
                }, 1000);
            }
        }
        
        // Start typing effect after a short delay
        setTimeout(typeWriter, 800);
    }
    
    // Subtitle typing effect on page load
    window.addEventListener('load', function() {
        const heroSubtitle = document.querySelector('.hero p:not(.hero-tagline)');
        if (heroSubtitle) {
            const originalText = heroSubtitle.textContent;
            heroSubtitle.textContent = '';
            let charIndex = 0;
            
            const typingInterval = setInterval(() => {
                if (charIndex < originalText.length) {
                    heroSubtitle.textContent += originalText.charAt(charIndex);
                    charIndex++;
                } else {
                    clearInterval(typingInterval);
                }
            }, 30);
        }
    });
}

/**
 * Initialize scroll indicator functionality
 */
function initScrollIndicator() {
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (!scrollIndicator) return;
    
    scrollIndicator.addEventListener('click', function() {
        const aboutSection = document.querySelector('#our-story') || document.querySelector('#about');
        if (aboutSection) {
            window.scrollTo({
                top: aboutSection.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
    
    // Hide scroll indicator when scrolling down
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            scrollIndicator.style.opacity = '0';
        } else {
            scrollIndicator.style.opacity = '1';
        }
    });
}

/**
 * Initialize Technical Section Components
 */
function initTechnicalSection() {
    // Initialize interactive sensor points
    initSensorPoints();
    
    // Tabs Handler for Technical Specifications
    const tabButtons = document.querySelectorAll('.tab-button');
    
    if (tabButtons.length > 0) {
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons and content
                tabButtons.forEach(btn => btn.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                
                // Add active class to clicked button and corresponding content
                this.classList.add('active');
                const tabId = this.getAttribute('data-tab');
                document.getElementById(tabId)?.classList.add('active');
            });
        });
    }
    
    // Video Player Placeholder Click Handler
    const videoPlaceholder = document.querySelector('.video-placeholder');
    
    if (videoPlaceholder) {
        videoPlaceholder.addEventListener('click', function() {
            // Replace placeholder with actual video
            const videoContainer = this.parentElement;
            const iframe = document.createElement('iframe');
            
            // Use data attribute to get the video ID or use a default
            const videoId = this.getAttribute('data-video-id') || 'YOUR_VIDEO_ID';
            
            iframe.setAttribute('src', `https://www.youtube.com/embed/${videoId}?autoplay=1`);
            iframe.setAttribute('frameborder', '0');
            iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
            iframe.setAttribute('allowfullscreen', '');
            iframe.style.position = 'absolute';
            iframe.style.top = '0';
            iframe.style.left = '0';
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            
            videoContainer.innerHTML = '';
            videoContainer.appendChild(iframe);
        });
    }
}

/**
 * Initialize sensor points interactivity with actual sensor icons
 */
function initSensorPoints() {
    const sensorPoints = document.querySelectorAll('.sensor-point');
    
    if (sensorPoints.length > 0) {
        // Create sensor icons based on sensor type
        sensorPoints.forEach(point => {
            const sensorType = point.getAttribute('data-sensor');
            // Remove any existing pulse elements
            const existingPulse = point.querySelector('.sensor-pulse');
            if (existingPulse) {
                point.removeChild(existingPulse);
            }
            
            // Create sensor icon based on type
            const sensorIcon = document.createElement('div');
            sensorIcon.className = 'sensor-icon';
            
            // Add appropriate sensor icon/visualization based on sensor type
            switch(sensorType) {
                case 'flex':
                    sensorIcon.innerHTML = `
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M7 14.5C7 14.5 7 12.5 7 11C7 9.5 8.5 9 9.5 9C10.5 9 11 9.5 11 11C11 12.5 11 19 11 19" stroke="#9D4EDD" stroke-width="2" stroke-linecap="round"/>
                            <path d="M11 12C11 12 11 10 11 9C11 7.5 12.5 7 13.5 7C14.5 7 15 7.5 15 9C15 10.5 15 19 15 19" stroke="#9D4EDD" stroke-width="2" stroke-linecap="round"/>
                            <path d="M15 10C15 10 15 8 15 7C15 5.5 16.5 5 17.5 5C18.5 5 19 5.5 19 7C19 8.5 19 19 19 19" stroke="#9D4EDD" stroke-width="2" stroke-linecap="round"/>
                            <path d="M5 19H19" stroke="#9D4EDD" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                        <span class="sensor-label">Flex</span>
                    `;
                    break;
                case 'fsr':
                    sensorIcon.innerHTML = `
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="6" stroke="#9D4EDD" stroke-width="2"/>
                            <path d="M12 6V18" stroke="#9D4EDD" stroke-width="2"/>
                            <path d="M16 8L8 16" stroke="#9D4EDD" stroke-width="2"/>
                            <path d="M8 8L16 16" stroke="#9D4EDD" stroke-width="2"/>
                        </svg>
                        <span class="sensor-label">Force</span>
                    `;
                    break;
                case 'mpu':
                    sensorIcon.innerHTML = `
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <rect x="4" y="4" width="16" height="16" rx="2" stroke="#9D4EDD" stroke-width="2"/>
                            <path d="M12 8V16" stroke="#9D4EDD" stroke-width="2"/>
                            <path d="M8 12H16" stroke="#9D4EDD" stroke-width="2"/>
                            <circle cx="12" cy="12" r="2" fill="#9D4EDD"/>
                        </svg>
                        <span class="sensor-label">IMU</span>
                    `;
                    break;
                default:
                    sensorIcon.innerHTML = `
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="8" stroke="#9D4EDD" stroke-width="2"/>
                            <circle cx="12" cy="12" r="3" fill="#9D4EDD"/>
                        </svg>
                        <span class="sensor-label">Sensor</span>
                    `;
            }
            
            // Append the sensor icon to the sensor point
            point.appendChild(sensorIcon);
            
            // Add hover effects
            point.addEventListener('mouseenter', function() {
                // Add highlight effect
                const icon = this.querySelector('.sensor-icon');
                if (icon) {
                    icon.style.transform = 'scale(1.2)';
                    icon.style.boxShadow = '0 0 15px rgba(157, 78, 221, 0.8)';
                    icon.classList.add('active');
                }
            });
            
            point.addEventListener('mouseleave', function() {
                // Remove highlight effect
                const icon = this.querySelector('.sensor-icon');
                if (icon && !this.classList.contains('selected')) {
                    icon.style.transform = '';
                    icon.style.boxShadow = '';
                    icon.classList.remove('active');
                }
            });
        });
        
        // Hide all info panels when clicking elsewhere
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.sensor-point') && !e.target.closest('.sensor-info')) {
                document.querySelectorAll('.sensor-info').forEach(info => {
                    info.classList.remove('active');
                });
                document.querySelectorAll('.sensor-point').forEach(point => {
                    point.classList.remove('selected');
                    const icon = point.querySelector('.sensor-icon');
                    if (icon) {
                        icon.style.transform = '';
                        icon.style.boxShadow = '';
                        icon.classList.remove('active');
                    }
                });
            }
        });
        
        // Show info on click
        sensorPoints.forEach(point => {
            point.addEventListener('click', function() {
                const sensorType = this.getAttribute('data-sensor');
                const infoElement = document.getElementById(`${sensorType}-info`);
                
                if (infoElement) {
                    // Toggle info visibility
                    document.querySelectorAll('.sensor-info').forEach(info => {
                        if (info !== infoElement) {
                            info.classList.remove('active');
                        }
                    });
                    
                    // Toggle selected state of the current point
                    const wasSelected = this.classList.contains('selected');
                    
                    // Reset all points
                    document.querySelectorAll('.sensor-point').forEach(p => {
                        p.classList.remove('selected');
                        const icon = p.querySelector('.sensor-icon');
                        if (icon) {
                            icon.style.transform = '';
                            icon.style.boxShadow = '';
                            icon.classList.remove('active');
                        }
                    });
                    
                    // If it wasn't selected before, select it now
                    if (!wasSelected) {
                        this.classList.add('selected');
                        const icon = this.querySelector('.sensor-icon');
                        if (icon) {
                            icon.style.transform = 'scale(1.2)';
                            icon.style.boxShadow = '0 0 15px rgba(157, 78, 221, 0.8)';
                            icon.classList.add('active');
                        }
                        infoElement.classList.add('active');
                    } else {
                        infoElement.classList.remove('active');
                    }
                }
            });
        });
    }
}

/**
 * Initialize Animation Effects
 */
function initAnimations() {
    // Intersection Observer for Fade-In Elements
    const fadeElements = document.querySelectorAll('.fade-in');
    
    if (fadeElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    // Unobserve after animation to improve performance
                    observer.unobserve(entry.target);
                }
            });
        }, {
            root: null,
            rootMargin: '0px',
            threshold: 0.2
        });
        
        fadeElements.forEach(element => {
            observer.observe(element);
        });
    }
    
    // Timeline items animation
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    if (timelineItems.length > 0) {
        const timelineObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    timelineObserver.unobserve(entry.target);
                }
            });
        }, {
            root: null,
            rootMargin: '0px',
            threshold: 0.2
        });
        
        timelineItems.forEach((item, index) => {
            item.style.transitionDelay = `${index * 0.2}s`;
            timelineObserver.observe(item);
        });
    }
}

/**
 * Initialize Scroll-based Effects
 */
function initScrollEffects() {
    // Parallax effect for design section images
    const designImages = document.querySelectorAll('.design-image');
    
    if (designImages.length > 0) {
        window.addEventListener('scroll', function() {
            designImages.forEach(image => {
                const rect = image.getBoundingClientRect();
                if (rect.top < window.innerHeight && rect.bottom > 0) {
                    const scrollPosition = window.scrollY;
                    const parallaxValue = scrollPosition * 0.05;
                    image.style.transform = `translateY(${parallaxValue}px)`;
                }
            });
        });
    }
}

/**
 * Initialize Team Section Components
 */
function initTeamSection() {
    // Team member hover effects
    const teamMembers = document.querySelectorAll('.team-member');
    
    if (teamMembers.length > 0) {
        teamMembers.forEach(member => {
            member.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.05)';
                this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.2)';
            });
            
            member.addEventListener('mouseleave', function() {
                this.style.transform = '';
                this.style.boxShadow = '';
            });
        });
    }
}