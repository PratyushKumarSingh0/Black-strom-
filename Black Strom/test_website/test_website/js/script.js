document.addEventListener('DOMContentLoaded', function() {
    // ==================== Original Functionality ====================
    // Mode Toggle Functionality
    const modeToggle = document.getElementById('modeToggle');
    const mainModeToggle = document.getElementById('mainModeToggle');
    
    const toggleButtons = [];
    if (modeToggle) toggleButtons.push(modeToggle);
    if (mainModeToggle) toggleButtons.push(mainModeToggle);
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            document.body.classList.toggle('day-mode');
            document.body.classList.toggle('night-mode');
            
            // Update button text
            const isNightMode = document.body.classList.contains('night-mode');
            toggleButtons.forEach(btn => {
                btn.textContent = isNightMode ? 'Day Mode' : 'Night Mode';
            });
            
            // Save preference to localStorage
            localStorage.setItem('colorMode', isNightMode ? 'night' : 'day');
        });
    });
    
    // Check for saved mode preference
    const savedMode = localStorage.getItem('colorMode');
    if (savedMode === 'night') {
        document.body.classList.remove('day-mode');
        document.body.classList.add('night-mode');
        toggleButtons.forEach(btn => {
            if (btn) btn.textContent = 'Day Mode';
        });
    }
    
    // Navigation between sections
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.content-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the target section
            const targetSection = this.getAttribute('data-section');
            
            // Update active nav link
            navLinks.forEach(navLink => navLink.classList.remove('active'));
            this.classList.add('active');
            
            // Animate section transition
            sections.forEach(section => {
                if (section.classList.contains('active-section')) {
                    section.classList.remove('active-section');
                    section.classList.add('slide-out');
                    
                    // After animation completes, hide the section and show the new one
                    setTimeout(() => {
                        section.classList.remove('slide-out');
                        section.style.display = 'none';
                        
                        const newSection = document.getElementById(targetSection);
                        newSection.style.display = 'block';
                        setTimeout(() => {
                            newSection.classList.add('active-section');
                            newSection.classList.add('slide-in');
                            
                            // Remove slide-in class after animation completes
                            setTimeout(() => {
                                newSection.classList.remove('slide-in');
                            }, 500);
                        }, 10);
                    }, 500);
                }
            });
        });
    });
    
    // Stats counter animation
    const statNumbers = document.querySelectorAll('.stat-number');
    
    function animateStats() {
        statNumbers.forEach(stat => {
            const target = +stat.getAttribute('data-target');
            const increment = target / 50;
            let current = 0;
            
            const timer = setInterval(() => {
                current += increment;
                stat.textContent = Math.floor(current);
                
                if (current >= target) {
                    stat.textContent = target;
                    clearInterval(timer);
                }
            }, 20);
        });
    }
    
    // Testimonial slider
    const testimonials = document.querySelectorAll('.testimonial');
    let currentTestimonial = 0;
    
    function showTestimonial(index) {
        testimonials.forEach(testimonial => testimonial.classList.remove('active'));
        testimonials[index].classList.add('active');
    }
    
    if (testimonials.length > 0) {
        showTestimonial(0);
        
        setInterval(() => {
            currentTestimonial = (currentTestimonial + 1) % testimonials.length;
            showTestimonial(currentTestimonial);
        }, 5000);
    }
    
    // Initialize animations when elements come into view
    const observerOptions = {
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (entry.target.classList.contains('stats-grid')) {
                    animateStats();
                }
            }
        });
    }, observerOptions);
    
    // Observe elements that need animations
    const animatedElements = document.querySelectorAll('.stats-grid, .approach-steps, .differentiator-cards');
    animatedElements.forEach(el => observer.observe(el));

    // ==================== Payment & Download Functionality ====================
    // Modal handling
    const getStartedBtns = document.querySelectorAll('.get-started');
    const paymentModals = document.querySelectorAll('.payment-modal');
    const downloadModal = document.getElementById('download-modal');
    const closeModalBtns = document.querySelectorAll('.close-modal');
    
    // Open payment modal when Get Started is clicked
    getStartedBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const plan = this.getAttribute('data-plan');
            const modal = document.getElementById(`${plan}-modal`);
            modal.style.display = 'flex';
        });
    });
    
    // Close modals
    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.payment-modal, .download-modal').style.display = 'none';
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('payment-modal') || e.target.classList.contains('download-modal')) {
            e.target.style.display = 'none';
        }
    });
    
    // Form submission handling
    const paymentForms = document.querySelectorAll('.payment-form');
    
    paymentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.classList.add('processing');
            submitBtn.disabled = true;
            
            // Simulate payment processing
            setTimeout(() => {
                submitBtn.classList.remove('processing');
                submitBtn.disabled = false;
                
                // Hide payment modal
                this.closest('.payment-modal').style.display = 'none';
                
                // Show download modal
                const planName = this.closest('.payment-modal').querySelector('h3').textContent;
                document.getElementById('plan-name').textContent = planName;
                downloadModal.style.display = 'flex';
                
                // Set Windows EXE download
                const windowsBtn = document.querySelector('.download-btn.windows');
                windowsBtn.setAttribute('href', '../downloads/dummy.exe');
                windowsBtn.setAttribute('download', 'dummy.exe');
                
                // Set other platform download links (placeholders)
                document.querySelector('.download-btn.mac').setAttribute('href', '#');
                document.querySelector('.download-btn.linux').setAttribute('href', '#');
                document.querySelector('.download-btn.android').setAttribute('href', '#');
                document.querySelector('.download-btn.ios').setAttribute('href', '#');
                
                // Generate license key
                const licenseKey = generateLicenseKey();
                const licenseDisplay = document.createElement('div');
                licenseDisplay.className = 'license-key';
                licenseDisplay.innerHTML = `
                    <h4>Your License Key:</h4>
                    <div class="key-box">${licenseKey}</div>
                    <p class="key-instructions">Use this key during installation</p>
                `;
                
                // Add license to modal
                const downloadContent = document.querySelector('.download-content');
                const existingLicense = downloadContent.querySelector('.license-key');
                if (existingLicense) existingLicense.remove();
                downloadContent.insertBefore(licenseDisplay, downloadContent.querySelector('.download-options'));
            }, 2000);
            
        });
    });
    
    // Generate a random license key
    function generateLicenseKey() {
        const segments = [];
        const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
        
        for (let i = 0; i < 4; i++) {
            let segment = '';
            for (let j = 0; j < 4; j++) {
                segment += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            segments.push(segment);
        }
        
        return segments.join('-');
    }
    
    // Credit card formatting
    const cardInputs = document.querySelectorAll('input[placeholder*="1234 5678"]');
    cardInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = this.value.replace(/\s+/g, '');
            if (value.length > 0) {
                value = value.match(new RegExp('.{1,4}', 'g')).join(' ');
            }
            this.value = value;
        });
    });
    
    // Expiry date formatting
    const expiryInputs = document.querySelectorAll('input[placeholder*="MM/YY"]');
    expiryInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 2) {
                value = value.substring(0, 2) + '/' + value.substring(2, 4);
            }
            this.value = value;
        });
    });

    // Form validation
    paymentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = this.querySelectorAll('input[required], select[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.style.borderColor = 'red';
                    isValid = false;
                } else {
                    input.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill all required fields');
            }
        });
    });
});