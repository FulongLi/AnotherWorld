// Update value displays when sliders change
document.querySelectorAll('input[type="range"]').forEach(slider => {
    const valueDisplay = document.getElementById(slider.id + '_value');
    if (valueDisplay) {
        slider.addEventListener('input', () => {
            valueDisplay.textContent = parseFloat(slider.value).toFixed(1);
        });
    }
});

// Handle form submission
document.getElementById('simulationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = document.getElementById('simulateBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    
    // Show loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    
    // Collect form data
    const formData = {
        birth_year: parseInt(form.birth_year.value),
        region: form.region.value,
        family_class: parseFloat(form.family_class.value),
        parents_education: parseFloat(form.parents_education.value),
        family_stability: parseFloat(form.family_stability.value),
        genetic_health: parseFloat(form.genetic_health.value),
        cognitive_potential: parseFloat(form.cognitive_potential.value),
        openness: parseFloat(form.openness.value),
        conscientiousness: parseFloat(form.conscientiousness.value),
        risk_preference: parseFloat(form.risk_preference.value),
        social_drive: parseFloat(form.social_drive.value),
        resilience: parseFloat(form.resilience.value),
        country: form.country.value,
        city: form.city.value,
        max_age: parseInt(form.max_age.value)
    };
    
    try {
        // Call API
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result);
        } else {
            showError(result.error || '模拟失败，请重试');
        }
    } catch (error) {
        showError('网络错误: ' + error.message);
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
});

function displayResults(result) {
    // Show results panel
    document.getElementById('resultsPanel').style.display = 'block';
    
    // Scroll to results
    document.getElementById('resultsPanel').scrollIntoView({ behavior: 'smooth' });
    
    // Display summary
    const summaryText = document.getElementById('summaryText');
    if (result.summary && result.summary.summary) {
        summaryText.textContent = result.summary.summary;
    } else {
        summaryText.textContent = '模拟完成，但未生成总结。';
    }
    
    // Display stats
    const person = result.person;
    document.getElementById('finalAge').textContent = person.age + ' 岁';
    document.getElementById('finalWealth').textContent = formatCurrency(person.wealth);
    document.getElementById('finalIncome').textContent = formatCurrency(person.income);
    document.getElementById('finalEducation').textContent = (person.education_level * 100).toFixed(1) + '%';
    document.getElementById('finalHealth').textContent = (person.health * 100).toFixed(1) + '%';
    document.getElementById('finalStress').textContent = (person.stress * 100).toFixed(1) + '%';
    
    // Display events
    const eventsList = document.getElementById('eventsList');
    if (result.events && result.events.length > 0) {
        eventsList.innerHTML = result.events.map(event => `
            <div class="event-item">
                <div class="event-year">${event.year}年 (${event.age}岁)</div>
                <h4>${event.title || '人生事件'}</h4>
                <div class="event-description">${event.description || '无描述'}</div>
            </div>
        `).join('');
    } else {
        eventsList.innerHTML = '<p>本次模拟中未记录重大事件。</p>';
    }
    
    // Display context
    const contextInfo = document.getElementById('contextInfo');
    const contextItems = [];
    
    if (result.country) {
        contextItems.push(`<div class="context-item">
            <span class="context-label">国家:</span>${result.country.country || 'N/A'}
        </div>`);
        contextItems.push(`<div class="context-item">
            <span class="context-label">时代:</span>${result.country.era || 'N/A'}
        </div>`);
        contextItems.push(`<div class="context-item">
            <span class="context-label">社会流动性:</span>${(result.country.social_mobility * 100).toFixed(1)}%
        </div>`);
    }
    
    if (result.city) {
        contextItems.push(`<div class="context-item">
            <span class="context-label">城市:</span>${result.city.city_name || 'N/A'}
        </div>`);
        contextItems.push(`<div class="context-item">
            <span class="context-label">城市层级:</span>${result.city.tier || 'N/A'}
        </div>`);
    }
    
    if (result.base_world) {
        contextItems.push(`<div class="context-item">
            <span class="context-label">经济周期:</span>${(result.base_world.economic_cycle * 100).toFixed(1)}%
        </div>`);
        contextItems.push(`<div class="context-item">
            <span class="context-label">技术水平:</span>${(result.base_world.tech_level * 100).toFixed(1)}%
        </div>`);
    }
    
    contextInfo.innerHTML = contextItems.join('');
}

function formatCurrency(amount) {
    if (amount >= 0) {
        return '¥' + amount.toLocaleString('zh-CN', { maximumFractionDigits: 2 });
    } else {
        return '-¥' + Math.abs(amount).toLocaleString('zh-CN', { maximumFractionDigits: 2 });
    }
}

function showError(message) {
    const resultsPanel = document.getElementById('resultsPanel');
    resultsPanel.style.display = 'block';
    resultsPanel.innerHTML = `
        <div class="error">
            <h3>错误</h3>
            <p>${message}</p>
        </div>
    `;
    resultsPanel.scrollIntoView({ behavior: 'smooth' });
}

