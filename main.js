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
        sensorPoints.forEach(point => {
            // Remove any existing pulse elements
            const existingPulse = point.querySelector('.sensor-pulse');
            if (existingPulse) {
                point.removeChild(existingPulse);
            }

            // Add hover effects
            point.addEventListener('mouseenter', function() {
                this.classList.add('active');
            });

            point.addEventListener('mouseleave', function() {
                if (!this.classList.contains('selected')) {
                    this.classList.remove('active');
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
                });
            }
        });

        // Show info on click
        sensorPoints.forEach(point => {
            point.addEventListener('click', function() {
                const sensorType = this.getAttribute('data-sensor');
                const infoElement = document.getElementById(`${sensorType}-info`);

                if (infoElement) {
                    document.querySelectorAll('.sensor-info').forEach(info => {
                        if (info !== infoElement) {
                            info.classList.remove('active');
                        }
                    });

                    const wasSelected = this.classList.contains('selected');

                    document.querySelectorAll('.sensor-point').forEach(p => {
                        p.classList.remove('selected');
                    });

                    if (!wasSelected) {
                        this.classList.add('selected');
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
// This function creates the breaking text effect
function createBreakingTextEffect() {
    const textElement = document.querySelector('.hero-content .description');
    if (!textElement) return;
    
    const text = textElement.textContent;
    textElement.textContent = '';
    
    const words = text.split(' ');
    
    words.forEach(word => {
      const wordSpan = document.createElement('span');
      wordSpan.className = 'word';
      
      let letterCount = 0;
      Array.from(word).forEach(letter => {
        const letterSpan = document.createElement('span');
        letterSpan.className = 'letter';
        letterSpan.textContent = letter;
        letterSpan.style.setProperty('--index', letterCount);
        letterCount++;
        wordSpan.appendChild(letterSpan);
      });
      
      textElement.appendChild(wordSpan);
      textElement.appendChild(document.createTextNode(' '));
    });
  }
  
  // Run when the DOM is fully loaded
  document.addEventListener('DOMContentLoaded', function() {
    createBreakingTextEffect();
    
    // Add any other existing initialization code here
  });

  document.addEventListener("DOMContentLoaded", function () {
    const sliderWrapper = document.querySelector(".slider-wrapper");
    const slides = document.querySelectorAll(".slide");
    const dotsContainer = document.querySelector(".slider-dots");
    const prevButton = document.querySelector(".prev-slide");
    const nextButton = document.querySelector(".next-slide");
    const progressBar = document.querySelector(".progress-bar");
  
    let currentIndex = 0;
    let slideWidth = slides[0].clientWidth;
    let autoPlayInterval;
    let isDragging = false;
    let startPosition = 0;
    let currentTranslate = 0;
    let prevTranslate = 0;
  
    // Initialize slider
    function initSlider() {
      // Set initial slide width
      updateSlideWidth();
  
      // Create dots
      slides.forEach((_, index) => {
        const dot = document.createElement("div");
        dot.classList.add("dot");
        if (index === 0) dot.classList.add("active");
        dot.addEventListener("click", () => goToSlide(index));
        dotsContainer.appendChild(dot);
      });
  
      // Apply initial tech color
      updateTechColor();
  
      // Set up event listeners
      prevButton.addEventListener("click", prevSlide);
      nextButton.addEventListener("click", nextSlide);
  
      // Touch and mouse events
      sliderWrapper.addEventListener("mousedown", startDrag);
      sliderWrapper.addEventListener("touchstart", startDrag);
      sliderWrapper.addEventListener("mousemove", drag);
      sliderWrapper.addEventListener("touchmove", drag);
      sliderWrapper.addEventListener("mouseup", endDrag);
      sliderWrapper.addEventListener("touchend", endDrag);
      sliderWrapper.addEventListener("mouseleave", endDrag);
  
      // Window resize event
      window.addEventListener("resize", () => {
        updateSlideWidth();
        goToSlide(currentIndex);
      });
  
      // Start autoplay
      startAutoPlay();
    }
  
    // Update slide width on resize
    function updateSlideWidth() {
      slideWidth = sliderWrapper.clientWidth;
      slides.forEach((slide) => {
        slide.style.minWidth = `${slideWidth}px`;
      });
    }
  
    // Go to specific slide
    function goToSlide(index) {
      if (index < 0) index = slides.length - 1;
      if (index >= slides.length) index = 0;
  
      currentIndex = index;
      const position = -slideWidth * currentIndex;
  
      // Update slider position
      sliderWrapper.style.transform = `translateX(${position}px)`;
  
      // Update dots
      updateDots();
  
      // Update tech color
      updateTechColor();
  
      // Reset progress bar animation
      resetProgressBar();
    }
  
    // Previous slide
    function prevSlide() {
      goToSlide(currentIndex - 1);
      resetAutoPlay();
    }
  
    // Next slide
    function nextSlide() {
      goToSlide(currentIndex + 1);
      resetAutoPlay();
    }
  
    // Update dots
    function updateDots() {
      const dots = document.querySelectorAll(".dot");
      dots.forEach((dot, index) => {
        dot.classList.toggle("active", index === currentIndex);
      });
    }
  
    // Update tech color
    function updateTechColor() {
      document.documentElement.style.setProperty("--tech-color", "#870df1");
    }
  
    // Start autoplay
    function startAutoPlay() {
      resetProgressBar();
      autoPlayInterval = setInterval(() => {
        nextSlide();
      }, 5000);
    }
  
    // Reset autoplay
    function resetAutoPlay() {
      clearInterval(autoPlayInterval);
      startAutoPlay();
    }
  
    // Reset progress bar
    function resetProgressBar() {
      progressBar.style.width = "0%";
      setTimeout(() => {
        progressBar.style.transition = "width 5s linear";
        progressBar.style.width = "100%";
      }, 50);
    }
  
    // Start drag
    function startDrag(event) {
      isDragging = true;
      startPosition = getPositionX(event);
      prevTranslate = currentTranslate;
  
      // Pause transition during drag
      sliderWrapper.style.transition = "none";
  
      // Stop autoplay while dragging
      clearInterval(autoPlayInterval);
    }
  
    // Drag
    function drag(event) {
      if (isDragging) {
        const currentPosition = getPositionX(event);
        currentTranslate = prevTranslate + currentPosition - startPosition;
  
        // Limit drag to adjacent slides only
        const minTranslate = -slideWidth * (slides.length - 1) - slideWidth * 0.2;
        const maxTranslate = slideWidth * 0.2;
  
        if (currentTranslate < minTranslate) currentTranslate = minTranslate;
        if (currentTranslate > maxTranslate) currentTranslate = maxTranslate;
  
        sliderWrapper.style.transform = `translateX(${currentTranslate}px)`;
      }
    }
  
    // End drag
    function endDrag() {
      if (!isDragging) return;
      isDragging = false;
  
      // Restore transition
      sliderWrapper.style.transition = "transform 0.6s ease-in-out";
  
      // Calculate the moved distance
      const movedDistance = currentTranslate - prevTranslate;
  
      // Determine if we should change slides
      if (movedDistance < -slideWidth * 0.2) {
        nextSlide();
      } else if (movedDistance > slideWidth * 0.2) {
        prevSlide();
      } else {
        goToSlide(currentIndex);
      }
  
      // Restart autoplay after drag
      startAutoPlay();
    }
  
    // Get position X from event
    function getPositionX(event) {
      return event.type.includes("mouse")
        ? event.pageX
        : event.touches[0].clientX;
    }
  
    // Initialize
    initSlider();
  });

  document.addEventListener('DOMContentLoaded', function() {
    const gloveViewer = document.querySelector('.glove-viewer');
    const frontView = document.querySelector('.front-view');
    const backView = document.querySelector('.back-view');
    const viewLabel = document.querySelector('.view-label');
    
    let showingFront = true;
    
    gloveViewer.addEventListener('click', function() {
      // Toggle between front and back views
      if (showingFront) {
        frontView.classList.remove('active');
        backView.classList.add('active');
        viewLabel.textContent = 'Click to view front';
      } else {
        backView.classList.remove('active');
        frontView.classList.add('active');
        viewLabel.textContent = 'Click to view back';
      }
      
      showingFront = !showingFront;
      
      // Add animation effect
      gloveViewer.style.animation = 'flip 0.5s ease';
      setTimeout(() => {
        gloveViewer.style.animation = '';
      }, 500);
    });
  });
  
  // Add this to your CSS
  const style = document.createElement('style');
  style.textContent = `
    @keyframes flip {
      0% { transform: rotateY(0); }
      50% { transform: rotateY(90deg); }
      100% { transform: rotateY(0); }
    }
  `;
  document.head.appendChild(style);