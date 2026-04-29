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
    });
// --- PART 2: CONTACT FORM LOGIC ---
const form = document.getElementById('contact-form');
const submitBtn = document.getElementById('contact-form-submit'); 

if (form) {
    submitBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        console.log('Form submission prevented');
        console.log('Form is being submitted');

        const btn = form.querySelector('button');
        
        // 1. CAPTURE original state BEFORE we change anything
        const originalText = btn.innerText;
        const originalGradient = window.getComputedStyle(btn).background;

        // 2. IMMEDIATE UI FEEDBACK
        btn.innerText = 'Initializing Transmission...';
        btn.disabled = true;

        const formData = {
            name: form.querySelector('input[type="text"]').value,
            email: form.querySelector('input[type="email"]').value,
            message: form.querySelector('textarea').value
        };
        

        try {
            const response = await fetch('https://portfolio-backend-zhwg.onrender.com', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                // 3. SUCCESS STATE
                btn.innerText = 'Transmission Successful';
                btn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
                console.log('Email sent successfully');
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
            // 4. ERROR STATE
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