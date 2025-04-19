// Fruit Battlegrounds Wiki - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Enable Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Active navigation link highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.includes(href))) {
            link.classList.add('active');
        }
    });

    // Fruit filtering on the fruits page
    const rarityFilter = document.getElementById('rarity-filter');
    if (rarityFilter) {
        rarityFilter.addEventListener('change', function() {
            const selectedRarity = this.value;
            const fruitCards = document.querySelectorAll('.fruit-card');
            
            fruitCards.forEach(card => {
                if (selectedRarity === 'all' || card.dataset.rarity === selectedRarity) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Search functionality enhancement
    const searchForm = document.querySelector('form[action="/search"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');
        searchInput.addEventListener('focus', function() {
            this.setAttribute('placeholder', 'Search for fruits, bosses, maps...');
        });
        
        searchInput.addEventListener('blur', function() {
            this.setAttribute('placeholder', 'Search');
        });
    }

    // Back to top button
    const backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.style.display = 'block';
            } else {
                backToTopBtn.style.display = 'none';
            }
        });
        
        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
    }

    // Add a back-to-top button if it doesn't exist
    if (!document.getElementById('back-to-top')) {
        const btn = document.createElement('button');
        btn.id = 'back-to-top';
        btn.className = 'btn btn-primary rounded-circle position-fixed';
        btn.innerHTML = '<i class="bi bi-arrow-up"></i>';
        btn.style.cssText = 'bottom: 20px; right: 20px; display: none; width: 50px; height: 50px; z-index: 1000;';
        
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
        
        document.body.appendChild(btn);
        
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                btn.style.display = 'block';
            } else {
                btn.style.display = 'none';
            }
        });
    }

    // Code copy functionality
    const codeCopyBtns = document.querySelectorAll('.code-copy-btn');
    codeCopyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const codeText = this.closest('.code-container').querySelector('.code-text').textContent;
            navigator.clipboard.writeText(codeText).then(() => {
                // Change button text temporarily
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            });
        });
    });

    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 50) {
                element.classList.add('fade-in');
            }
        });
    };
    
    if (document.querySelectorAll('.animate-on-scroll').length > 0) {
        window.addEventListener('scroll', animateOnScroll);
        // Initial check
        animateOnScroll();
    }

    // Dynamic year for copyright
    const yearSpan = document.getElementById('current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
}); 