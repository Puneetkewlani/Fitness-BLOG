/**
 * FitLife AI Chatbot Widget
 * Premium, glassmorphic floating assistant with automatic API connection & offline fallback.
 * Session state is stored in sessionStorage to survive page navigation!
 */

(function() {
  // Direct access to backend host
  const BACKEND_URL = window.location.origin;
  
  // Local Expert Fallback Engine (JS side for absolute double-safety if backend is completely down)
  const LOCAL_RESPONSES = {
    greetings: `
      <p>👋 <strong>Hello! I'm your FitLife AI Coach.</strong></p>
      <p>I'm here to help you guide through your health, exercise, and diet journey! What can I help you with today?</p>
      <p>Try asking me:</p>
      <ul>
        <li><em>"How do I lose weight safely?"</em></li>
        <li><em>"Give me a simple balanced meal plan."</em></li>
        <li><em>"What are the best exercises for strength?"</em></li>
        <li><em>"How can I calculate my BMI?"</em></li>
      </ul>
    `,
    diet: `
      <p>🥗 <strong>Nutrition & Diet Tips</strong></p>
      <p>A balanced diet is the cornerstone of sustainable health. Focus on whole foods and high-quality macronutrients:</p>
      <ul>
        <li><strong>Proteins:</strong> Vital for muscle repair. Include eggs, chicken, paneer, tofu, and legumes.</li>
        <li><strong>Carbohydrates:</strong> Your main energy source. Choose complex carbs like oats, brown rice, and sweet potatoes.</li>
        <li><strong>Fats:</strong> Essential for hormones. Opt for nuts, olive oil, and avocados.</li>
      </ul>
      <p>Check out our detailed <a href="diet.html" style="color: #6366f1; text-decoration: underline;">Diet Plans</a> page for sample macronutrient distributions, or fill out the <strong>Fitness Assessment</strong> on our home page to receive a fully customized plan in your inbox!</p>
    `,
    exercise: `
      <p>💪 <strong>Exercise & Training Guide</strong></p>
      <p>To see continuous progress, your routine should incorporate a mix of strength and cardiovascular training:</p>
      <ul>
        <li><strong>Strength Training:</strong> Builds calorie-burning muscle tissue and increases density. Try compound lifts like squats, deadlifts, and push-ups.</li>
        <li><strong>Cardiovascular Exercise:</strong> Improves heart health and boosts fat loss. Aim for 150 minutes of moderate activity (like brisk walking) per week.</li>
        <li><strong>Flexibility & Recovery:</strong> Never skip stretching. It prevents injuries and increases your range of motion.</li>
      </ul>
      <p>Explore full instructional guides on our <a href="exercise.html" style="color: #6366f1; text-decoration: underline;">Exercise Catalog</a>!</p>
    `,
    bmi: `
      <p>📏 <strong>Body Mass Index (BMI)</strong></p>
      <p>BMI is a useful standard measure to categorize individuals into weight classifications (Underweight, Normal, Overweight, Obese):</p>
      <ul>
        <li><strong>Underweight:</strong> Below 18.5</li>
        <li><strong>Normal weight:</strong> 18.5 to 24.9</li>
        <li><strong>Overweight:</strong> 25.0 to 29.9</li>
        <li><strong>Obese:</strong> 30.0 and above</li>
      </ul>
      <p>We have a fully interactive calculator waiting for you! Scroll down on the <a href="diet.html#bmiResult" style="color: #6366f1; text-decoration: underline;">Diet Plans</a> page to enter your measurements and get instant feedback with local database saving.</p>
    `,
    weightloss: `
      <p>🔥 <strong>Sustainable Fat Loss</strong></p>
      <p>The golden rule of fat loss is simple: you must create a <strong>calorie deficit</strong> (burning more calories than you consume). Here's a safe strategy:</p>
      <ol>
        <li><strong>Target Deficit:</strong> Aim for a mild deficit of 300 to 500 kcal below your daily maintenance level. This achieves about 0.5kg of healthy fat loss per week.</li>
        <li><strong>High Protein:</strong> Crucial to prevent muscle loss while losing weight. Make sure protein represents at least 30% of your daily intake.</li>
        <li><strong>NEAT (Activity):</strong> Walk more! Aiming for 8,000–10,000 steps daily is a massive contributor to fat loss.</li>
      </ol>
      <p><em>Note: Always consult a doctor before making any aggressive dietary modifications.</em></p>
    `,
    muscle: `
      <p>🏋️ <strong>Muscle Hypertrophy & Gain</strong></p>
      <p>To build clean muscle tissue, your body requires two main stimuli: a calorie surplus and progressive strength overload.</p>
      <ul>
        <li><strong>Calorie Surplus:</strong> Consume 200–400 calories *above* your maintenance level to provide building blocks.</li>
        <li><strong>Protein intake:</strong> Consume 1.6 to 2.2 grams of protein per kilogram of body weight.</li>
        <li><strong>Progressive Overload:</strong> Gradually increase the resistance (weights or reps) in your exercises over time to force adaptation.</li>
        <li><strong>Rest:</strong> Muscles grow when you rest, not when you lift. Get 7-8 hours of sleep.</li>
      </ul>
    `,
    sleep: `
      <p>😴 <strong>Sleep & Recovery Protocol</strong></p>
      <p>Recovery is where the transformation happens. Without adequate rest, your body cannot heal and build muscle tissues efficiently:</p>
      <ul>
        <li><strong>Aim for 7-9 Hours:</strong> Consistent sleep cycles regulate critical fat-burning and growth hormones.</li>
        <li><strong>Sleep Hygiene:</strong> Discontinue phone/screen usage at least 45 minutes before bed. Keep your room dark, cool, and quiet.</li>
        <li><strong>Active Recovery:</strong> On rest days, do light walking or yoga to promote blood flow and alleviate soreness.</li>
      </ul>
    `,
    injury: `
      <p>⚠️ <strong>Injury Care & Safety First</strong></p>
      <p>Your safety is the highest priority! If you feel sharp pain (distinguished from normal muscle soreness):</p>
      <ul>
        <li><strong>STOP immediately:</strong> Never 'push through' acute joint or tendon pain.</li>
        <li><strong>Use R.I.C.E.:</strong> Rest, Ice, Compression, and Elevation for minor strains.</li>
        <li><strong>Consult a professional:</strong> For any persistent joint pain, visit a licensed physician or physical therapist.</li>
      </ul>
    `,
    default: `
      <p>💡 <strong>Thanks for your question!</strong></p>
      <p>As your FitLife Coach, I want to make sure you get the most accurate support. To give you custom diet and training recommendations tailored precisely to your metrics, please complete our <a href="index.html#assessment" style="color: #6366f1; text-decoration: underline;">Personalized Fitness Assessment</a>!</p>
      <p>You can also ask me about topics like: <strong>dieting, muscle gain, burning fat, sleep, exercise guides, and BMI calculations.</strong></p>
    `
  };

  function getFallbackResponse(msg) {
    msg = msg.toLowerCase();
    if (msg.match(/(hello|hi|hey|greetings|yo)/)) return LOCAL_RESPONSES.greetings;
    if (msg.match(/(diet|food|eat|meal|nutrition|recipe|breakfast|lunch|dinner)/)) return LOCAL_RESPONSES.diet;
    if (msg.match(/(workout|exercise|routine|gym|training|cardio|strength|stretch)/)) return LOCAL_RESPONSES.exercise;
    if (msg.match(/(bmi|body mass index|calculate weight)/)) return LOCAL_RESPONSES.bmi;
    if (msg.match(/(lose weight|weight loss|burn fat|slim down|calories|deficit)/)) return LOCAL_RESPONSES.weightloss;
    if (msg.match(/(gain muscle|build muscle|bulk|hypertrophy|size)/)) return LOCAL_RESPONSES.muscle;
    if (msg.match(/(sleep|rest|recovery|insomnia|hours)/)) return LOCAL_RESPONSES.sleep;
    if (msg.match(/(injury|pain|hurt|sore|knees|back)/)) return LOCAL_RESPONSES.injury;
    return LOCAL_RESPONSES.default;
  }

  // Initialize Chatbot UI
  function initChatbot() {
    // Create elements
    const launcher = document.createElement('div');
    launcher.className = 'chatbot-launcher';
    launcher.id = 'chatbotLauncher';
    launcher.innerHTML = `
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-message-circle"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
      <div class="chatbot-launcher-pulse"></div>
      <div class="chatbot-launcher-badge" id="chatbotBadge" style="display: none;">1</div>
    `;

    const container = document.createElement('div');
    container.className = 'chatbot-container';
    container.id = 'chatbotContainer';
    container.innerHTML = `
      <div class="chatbot-header">
        <div class="chatbot-profile">
          <div class="chatbot-avatar">
            🤖
            <div class="chatbot-status-dot"></div>
          </div>
          <div class="chatbot-info">
            <h4>FitLife Coach</h4>
            <p><span style="width:6px;height:6px;background:#10b981;border-radius:50%;display:inline-block;"></span> Active & Online</p>
          </div>
        </div>
        <button class="chatbot-close-btn" id="chatbotClose">&times;</button>
      </div>
      <div class="chatbot-messages" id="chatbotMessages">
        <!-- Messages loaded dynamically -->
      </div>
      <div class="chatbot-input-container">
        <div class="chatbot-input-wrapper">
          <input type="text" class="chatbot-input" id="chatbotInput" placeholder="Ask your FitLife coach...">
        </div>
        <button class="chatbot-send-btn" id="chatbotSend" disabled>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="transform: rotate(45deg); margin-left: -2px; margin-top: 2px;"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
        </button>
      </div>
    `;

    document.body.appendChild(launcher);
    document.body.appendChild(container);

    // Event Bindings
    const launcherBtn = document.getElementById('chatbotLauncher');
    const closeBtn = document.getElementById('chatbotClose');
    const sendBtn = document.getElementById('chatbotSend');
    const inputField = document.getElementById('chatbotInput');
    const messagesBox = document.getElementById('chatbotMessages');
    const badge = document.getElementById('chatbotBadge');

    // Toggle panel
    launcherBtn.addEventListener('click', () => {
      container.classList.toggle('active');
      if (container.classList.contains('active')) {
        badge.style.display = 'none';
        sessionStorage.setItem('fitlife_chat_badge', 'read');
        setTimeout(() => inputField.focus(), 150);
        sessionStorage.setItem('fitlife_chat_open', 'true');
      } else {
        sessionStorage.setItem('fitlife_chat_open', 'false');
      }
    });

    closeBtn.addEventListener('click', () => {
      container.classList.remove('active');
      sessionStorage.setItem('fitlife_chat_open', 'false');
    });

    // Toggle Send Button on input
    inputField.addEventListener('input', () => {
      sendBtn.disabled = inputField.value.trim() === '';
    });

    // Keyboard enter submit
    inputField.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && inputField.value.trim() !== '') {
        submitMessage(inputField.value.trim());
      }
    });

    sendBtn.addEventListener('click', () => {
      if (inputField.value.trim() !== '') {
        submitMessage(inputField.value.trim());
      }
    });

    // Populate Initial Welcoming or History
    loadChatSession();
  }

  // Load chat session from sessionStorage
  function loadChatSession() {
    const messagesBox = document.getElementById('chatbotMessages');
    const badge = document.getElementById('chatbotBadge');
    
    // Check if we have unread badge status
    const badgeStatus = sessionStorage.getItem('fitlife_chat_badge');
    if (!badgeStatus) {
      // First visit, show badge to attract clicking
      badge.style.display = 'flex';
    }

    const savedHistory = sessionStorage.getItem('fitlife_chat_history');
    if (savedHistory) {
      const history = JSON.parse(savedHistory);
      history.forEach(item => {
        appendMessageBubble(item.role, item.content);
      });
    } else {
      // Initial introduction
      const greetingText = `
        <p>👋 <strong>Welcome to FitLife! I'm your virtual Fitness & Nutrition Coach.</strong></p>
        <p>I am powered by Gemini AI and can suggest workout splits, design custom healthy diet plans, analyze macro goals, explain exercises, or calculate BMI parameters!</p>
        <p>Select a quick topic to start:</p>
      `;
      appendMessageBubble('bot', greetingText);
      appendSuggestionsChips();
      saveToSession('bot', greetingText);
    }

    // Check if chat container should be open
    const isOpen = sessionStorage.getItem('fitlife_chat_open') === 'true';
    if (isOpen) {
      document.getElementById('chatbotContainer').classList.add('active');
      badge.style.display = 'none';
    }
  }

  // Append a message bubble to container
  function appendMessageBubble(role, content) {
    const messagesBox = document.getElementById('chatbotMessages');
    const bubble = document.createElement('div');
    bubble.className = `chatbot-msg-bubble ${role}`;
    
    // Calculate readable timestamp
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    bubble.innerHTML = `
      <div class="chatbot-msg-text">${content}</div>
      <span class="chatbot-msg-time">${timeStr}</span>
    `;
    
    messagesBox.appendChild(bubble);
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }

  // Append suggestion chips
  function appendSuggestionsChips() {
    const messagesBox = document.getElementById('chatbotMessages');
    const chipsWrapper = document.createElement('div');
    chipsWrapper.className = 'chatbot-chips';
    
    const suggestions = [
      { text: '🥗 Plan fat loss diet', label: 'Fat Loss Diet' },
      { text: '💪 Build muscle routine', label: 'Gain Muscle' },
      { text: '📏 Calculate my BMI', label: 'BMI Info' },
      { text: '😴 Improve sleeping habits', label: 'Better Sleep' }
    ];

    suggestions.forEach(item => {
      const chip = document.createElement('button');
      chip.className = 'chatbot-chip';
      chip.textContent = item.text;
      chip.addEventListener('click', () => {
        submitMessage(item.text);
        chipsWrapper.remove(); // Clean up current chips after clicking
      });
      chipsWrapper.appendChild(chip);
    });

    messagesBox.appendChild(chipsWrapper);
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }

  // Save chat bubble to history session
  function saveToSession(role, content) {
    let history = [];
    const saved = sessionStorage.getItem('fitlife_chat_history');
    if (saved) {
      history = JSON.parse(saved);
    }
    history.push({ role, content });
    sessionStorage.setItem('fitlife_chat_history', JSON.stringify(history));
  }

  // Add thinking loading state
  function toggleTypingIndicator(show) {
    const messagesBox = document.getElementById('chatbotMessages');
    const indicatorId = 'chatbotTypingIndicator';
    
    if (show) {
      const bubble = document.createElement('div');
      bubble.className = 'chatbot-msg-bubble bot chatbot-typing-bubble';
      bubble.id = indicatorId;
      bubble.innerHTML = `
        <div class="chatbot-typing-dot"></div>
        <div class="chatbot-typing-dot"></div>
        <div class="chatbot-typing-dot"></div>
      `;
      messagesBox.appendChild(bubble);
      messagesBox.scrollTop = messagesBox.scrollHeight;
    } else {
      const el = document.getElementById(indicatorId);
      if (el) el.remove();
    }
  }

  // Submit message process
  async function submitMessage(message) {
    const inputField = document.getElementById('chatbotInput');
    const sendBtn = document.getElementById('chatbotSend');
    
    // UI updates
    appendMessageBubble('user', message);
    saveToSession('user', message);
    
    inputField.value = '';
    sendBtn.disabled = true;
    
    toggleTypingIndicator(true);
    inputField.disabled = true;

    try {
      // Call Flask Backend route
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
      });

      const data = await response.json();
      toggleTypingIndicator(false);

      if (data && data.status === 'success') {
        appendMessageBubble('bot', data.response);
        saveToSession('bot', data.response);
      } else {
        // Safe backend response fallback
        const fallbackText = getFallbackResponse(message);
        appendMessageBubble('bot', fallbackText);
        saveToSession('bot', fallbackText);
      }
    } catch (error) {
      console.log("FitLife Chat: API offline/unreachable. Activating local coach fallback engine.");
      toggleTypingIndicator(false);
      
      // Standalone browser client response fallback
      const fallbackText = getFallbackResponse(message);
      appendMessageBubble('bot', fallbackText);
      saveToSession('bot', fallbackText);
    } finally {
      inputField.disabled = false;
      inputField.focus();
    }
  }

  // Execute initialization once page is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChatbot);
  } else {
    initChatbot();
  }
})();
