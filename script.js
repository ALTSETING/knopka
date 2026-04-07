document.addEventListener('DOMContentLoaded', () => {

    // 1. Навігація по вкладках
    const navLinks = document.querySelectorAll('.nav-links li');
    const tabPanes = document.querySelectorAll('.tab-pane');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Зняти active з усіх
            navLinks.forEach(l => l.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            // Додати active поточному
            link.classList.add('active');
            const targetTab = document.getElementById(link.getAttribute('data-tab'));
            targetTab.classList.add('active');
        });
    });

    // 2. Ініціалізація графіка (Chart.js)
    const ctx = document.getElementById('activityChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Пн', 'Вв', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'],
            datasets: [{
                label: 'Зароблено XP',
                data: [120, 190, 300, 250, 200, 400, 350],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#2a2a2a' }, ticks: { color: '#888' } },
                x: { grid: { display: false }, ticks: { color: '#888' } }
            }
        }
    });

    // 3. Логіка Pomodoro Таймера
    let timerInterval;
    let timeLeft = 25 * 60; // 25 хвилин
    const timerDisplay = document.getElementById('timer');
    const startBtn = document.getElementById('start-timer');
    const stopBtn = document.getElementById('stop-timer');

    function updateTimerDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    startBtn.addEventListener('click', () => {
        clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
                updateTimerDisplay();
            } else {
                clearInterval(timerInterval);
                alert("Час вийшов! Нараховано +50 XP");
                // Тут буде виклик бекенду для оновлення XP
                timeLeft = 25 * 60;
                updateTimerDisplay();
            }
        }, 1000);
    });

    stopBtn.addEventListener('click', () => {
        clearInterval(timerInterval);
    });

});

// 4. Логіка AI Чату (Симуляція для фронтенду)
function sendMessage() {
    const inputField = document.getElementById('ai-input');
    const chatBox = document.getElementById('chat-box');
    const message = inputField.value.trim();

    if (message) {
        // Повідомлення користувача
        const userMsgDiv = document.createElement('div');
        userMsgDiv.className = 'message user-message';
        userMsgDiv.textContent = message;
        chatBox.appendChild(userMsgDiv);
        inputField.value = '';

        // Автоскрол
        chatBox.scrollTop = chatBox.scrollHeight;

        // Симуляція відповіді AI (Сюди ти підключиш запит до OpenRouter/Llama-3)
        setTimeout(() => {
            const aiMsgDiv = document.createElement('div');
            aiMsgDiv.className = 'message ai-message';
            aiMsgDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Аналізую...';
            chatBox.appendChild(aiMsgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

            setTimeout(() => {
                aiMsgDiv.innerHTML = "Це чудова ціль! Давай розіб'ємо її на 3 дрібні кроки. Готовий?";
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 1000);
        }, 500);
    }
}

// Слухач на Enter у чаті
document.getElementById('ai-input')?.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
});

// Функція експорту (Заглушка)
function exportICS() {
    alert("Генерація .ics файлу... (Потребує підключення бекенду або бібліотеки ics.js)");
}
