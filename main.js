console.log("JS is alive and loaded!");
document.addEventListener('DOMContentLoaded', () => {
    
    // --- PART 1: REVEAL ANIMATIONS (Existing) ---
    const observerOptions = { threshold: 0.1 };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
            }
        });
    }, observerOptions);

    const cards = document.querySelectorAll('.project-card');
    cards.forEach(card => {
        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";
        card.style.transition = "all 0.8s ease-out";
        observer.observe(card);
    });// --- PART 2: CONTACT FORM LOGIC ---
const form = document.getElementById('contact-form');
const submitBtn = document.getElementById('contact-form-submit'); 

if (form) {
    submitBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        
        // --- ADDED THIS: Capture the data from the inputs ---
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            message: document.getElementById('message').value
        };

        const btn = form.querySelector('button');
        const originalText = btn.innerText;
        const originalGradient = window.getComputedStyle(btn).background;

        btn.innerText = 'sending...';
        btn.disabled = true;

        try {
            // Ensure this URL matches your Render URL + /send-email
            const response = await fetch('https://portfolio-backend-zhwg.onrender.com/send-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData) // Now formData actually exists!
            });

            if (response.ok) {
                btn.innerText = 'sent!';
                btn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
                form.reset();

                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.style.background = originalGradient;
                    btn.disabled = false;
                }, 4000);
            } else {
                throw new Error('Server Error');
            }
        } catch (error) {
            console.error("Backend connection failed:", error);
            btn.innerText = 'Connection Failed';
            btn.style.background = '#ef4444';

            setTimeout(() => {
                btn.innerText = originalText;
                btn.style.background = originalGradient;
                btn.disabled = false;
            }, 3000);
        }
    });
}
});