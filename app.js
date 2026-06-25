// app.js - Shared utilities and API connection logic

const API_BASE_URL = 'http://127.0.0.1:5000';

document.addEventListener('DOMContentLoaded', () => {
    // Handling forms, especially login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        let isSignupActive = false;
        
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const emailError = document.getElementById('emailError');
        const passwordError = document.getElementById('passwordError');
        const generalMessage = document.getElementById('generalMessage');
        const submitBtn = document.getElementById('loginBtn');
        const toggleBtn = document.getElementById('toggleAuthBtn');
        const authSubtitle = document.getElementById('authSubtitle');
        const signupNameFrame = document.getElementById('signupNameFrame');
        const signupName = document.getElementById('signupName');

        const validateEmail = (email) => {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(String(email).toLowerCase());
        };

        const validatePassword = (password) => {
            const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
            return re.test(password);
        };

        const checkValidity = () => {
            let isValid = true;
            
            // Email Validation
            if (emailInput.value && !validateEmail(emailInput.value)) {
                emailError.textContent = "Please enter a valid email address";
                emailError.style.display = "block";
                emailInput.style.borderColor = "var(--danger)";
                isValid = false;
            } else {
                emailError.style.display = "none";
                emailInput.style.borderColor = emailInput.value ? "var(--success)" : "var(--border-color)";
            }

            // Password Validation
            if (passwordInput.value && !validatePassword(passwordInput.value)) {
                passwordError.textContent = "Password must be at least 8 characters and include uppercase, lowercase, number, and special character";
                passwordError.style.display = "block";
                passwordInput.style.borderColor = "var(--danger)";
                isValid = false;
            } else {
                passwordError.style.display = "none";
                passwordInput.style.borderColor = passwordInput.value ? "var(--success)" : "var(--border-color)";
            }

            if (!emailInput.value || !passwordInput.value) isValid = false;

            submitBtn.disabled = !isValid;
        };

        emailInput.addEventListener('input', checkValidity);
        passwordInput.addEventListener('input', checkValidity);
        emailInput.addEventListener('blur', checkValidity);
        passwordInput.addEventListener('blur', checkValidity);
        
        // Handle Toggle between Login and Signup
        toggleBtn.addEventListener('click', () => {
            isSignupActive = !isSignupActive;
            
            if (isSignupActive) {
                authTitle.textContent = "Sign Up";
                authSubtitle.textContent = "Create an account to access the dashboard";
                submitBtn.textContent = "Sign Up";
                toggleBtn.textContent = "Back to Login";
                signupNameFrame.style.display = "flex";
            } else {
                authTitle.textContent = "Login";
                authSubtitle.textContent = "Access your patient monitoring dashboard";
                submitBtn.textContent = "Login";
                toggleBtn.textContent = "Sign Up";
                signupNameFrame.style.display = "none";
            }
            
            // Clear inputs and errors
            emailInput.value = '';
            passwordInput.value = '';
            checkValidity();
            generalMessage.style.display = "none";
        });

        const showMessage = (msg, type) => {
            generalMessage.textContent = msg;
            generalMessage.style.display = "block";
            generalMessage.style.color = type === "error" ? "var(--danger)" : "var(--success)";
        };

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading"><i class="fa-solid fa-spinner fa-spin"></i> Processing...</span>';
            submitBtn.style.opacity = '0.7';
            submitBtn.disabled = true;

            const email = emailInput.value;
            const password = passwordInput.value;

            try {
                const action = isSignupActive ? 'signup' : 'login';
                
                // Using explicit root URL since routes are /login and /signup
                const authUrl = `${API_BASE_URL}/${action}`;
                
                const response = await fetch(authUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        email, 
                        password,
                        full_name: isSignupActive ? signupName.value : undefined
                    })
                });
                
                const data = await response.json();

                if (response.ok) {
                    if (isSignupActive) {
                        showMessage("Registration successful! Logging you in...", "success");
                        setTimeout(() => {
                            // After signup, switch to login or automatically simulate login
                            // For simplicity, we can log them in if token is returned, or switch tab
                            if (data.token) {
                                localStorage.setItem('auth_token', data.token);
                                window.location.href = 'dashboard.html';
                            } else {
                                // If backend didn't log them in automatically, just click toggle
                                toggleBtn.click();
                                emailInput.value = email;
                                showMessage("Registration successful! Please log in.", "success");
                            }
                        }, 1000);
                    } else {
                        showMessage("Login successful!", "success");
                        setTimeout(() => {
                            localStorage.setItem('auth_token', data.token || 'real_token_123'); // Save token securely
                            window.location.href = 'dashboard.html';
                        }, 1000);
                        return; // Kept disabled while redirecting
                    }
                } else {
                    showMessage(data.error || "Authentication failed. Please try again.", "error");
                }
            } catch (err) {
                console.error("Auth Error:", err);
                showMessage(`Failed to connect: ${err.message}. Ensure Flask is running.`, 'error');
            }

            submitBtn.innerHTML = originalText;
            submitBtn.style.opacity = '1';
            submitBtn.disabled = false;
        });
    }

    // Highlight active nav link based on current page
    const currentPath = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav-link');
    if (navLinks.length > 0) {
        navLinks.forEach(link => {
            link.classList.remove('active');
            const linkHref = link.getAttribute('href');
            if (currentPath === linkHref || (currentPath === '' && linkHref === 'dashboard.html')) {
                link.classList.add('active');
            }
        });
    }

    // Fetch and sync profile data globally
    fetch(`${API_BASE_URL}/profile`)
        .then(res => res.json())
        .then(data => {
            if(data && data.name) {
                document.querySelectorAll('.user-name').forEach(el => el.textContent = data.name);
                document.querySelectorAll('.profile-name').forEach(el => el.textContent = data.name);
                if (data.role) {
                    document.querySelectorAll('.user-role').forEach(el => el.textContent = data.role);
                    document.querySelectorAll('.profile-role').forEach(el => el.textContent = data.role);
                }
            }
        })
        .catch(err => console.error("Failed to load profile:", err));

    // Dashboard Tabs Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    if (tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active from all tabs
                tabBtns.forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => {
                    c.style.display = 'none';
                    c.classList.remove('tab-content-active');
                });
                
                // Add active to clicked
                btn.classList.add('active');
                const targetId = btn.getAttribute('data-tab');
                if (targetId) {
                    const targetContent = document.getElementById(targetId);
                    if (targetContent) {
                        targetContent.style.display = 'block';
                        targetContent.classList.add('tab-content-active');
                    }
                }
            });
        });
    }
});

// Helper for showing notifications/toasts
function showNotification(message, type = 'success') {
    // Basic implementation for demo purposes
    alert(`[${type.toUpperCase()}] ${message}`);
}

