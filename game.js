// Core game system
class LifeSimulator {
    constructor() {
        this.character = null;
        this.currentAge = 0;
        this.maxAge = 100;
        this.lifeEvents = [];
        this.isPaused = false;
        this.currentEvent = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.getElementById('start-btn').addEventListener('click', () => this.startNewLife());
        document.getElementById('next-year-btn').addEventListener('click', () => this.advanceYear());
        document.getElementById('pause-btn').addEventListener('click', () => this.togglePause());
        document.getElementById('restart-btn').addEventListener('click', () => this.restart());
        document.getElementById('restart-end-btn').addEventListener('click', () => this.restart());
    }

    // Generate random name
    generateName() {
        const firstNames = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn', 'Sage', 'Blake', 'Cameron', 'Dakota', 'Emery', 'Finley', 'Hayden'];
        const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas'];
        const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
        const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
        return firstName + ' ' + lastName;
    }

    // Generate MBTI personality type
    generateMBTI() {
        // MBTI has 4 dimensions, each with 2 options
        const extraversion = Math.random() > 0.5 ? 'E' : 'I'; // Extraversion vs Introversion
        const sensing = Math.random() > 0.5 ? 'S' : 'N'; // Sensing vs Intuition
        const thinking = Math.random() > 0.5 ? 'T' : 'F'; // Thinking vs Feeling
        const judging = Math.random() > 0.5 ? 'J' : 'P'; // Judging vs Perceiving
        
        const mbtiType = extraversion + sensing + thinking + judging;
        
        // MBTI type descriptions
        const mbtiDescriptions = {
            'INTJ': 'The Architect - Strategic, independent, and decisive',
            'INTP': 'The Thinker - Innovative, logical, and curious',
            'ENTJ': 'The Commander - Bold, imaginative, and strong-willed',
            'ENTP': 'The Debater - Smart, curious, and confident',
            'INFJ': 'The Advocate - Creative, insightful, and principled',
            'INFP': 'The Mediator - Poetic, kind, and altruistic',
            'ENFJ': 'The Protagonist - Charismatic, inspiring, and natural-born leaders',
            'ENFP': 'The Campaigner - Enthusiastic, creative, and sociable',
            'ISTJ': 'The Logistician - Practical, fact-minded, and reliable',
            'ISFJ': 'The Protector - Warm-hearted, dedicated, and meticulous',
            'ESTJ': 'The Executive - Organized, strong-willed, and direct',
            'ESFJ': 'The Consul - Extraordinarily caring, social, and popular',
            'ISTP': 'The Virtuoso - Bold, practical, and experimental',
            'ISFP': 'The Adventurer - Flexible, charming, and spontaneous',
            'ESTP': 'The Entrepreneur - Smart, energetic, and perceptive',
            'ESFP': 'The Entertainer - Spontaneous, enthusiastic, and people-focused'
        };

        return {
            type: mbtiType,
            description: mbtiDescriptions[mbtiType] || 'Unique personality type',
            dimensions: {
                extraversion: extraversion === 'E',
                sensing: sensing === 'S',
                thinking: thinking === 'T',
                judging: judging === 'J'
            }
        };
    }

    // Get MBTI-based choice modifier
    getMBTIModifier(choice, mbti) {
        let modifier = 1.0;
        
        // Extraversion affects social choices
        if (choice.social) {
            modifier *= mbti.dimensions.extraversion ? 1.2 : 0.9;
        }
        
        // Intuition affects creative/abstract choices
        if (choice.creative) {
            modifier *= mbti.dimensions.sensing ? 0.9 : 1.2;
        }
        
        // Thinking affects logical choices
        if (choice.logical) {
            modifier *= mbti.dimensions.thinking ? 1.2 : 0.9;
        }
        
        // Judging affects structured choices
        if (choice.structured) {
            modifier *= mbti.dimensions.judging ? 1.2 : 0.9;
        }
        
        return modifier;
    }

    // Create new character
    createCharacter() {
        const familyWealth = Math.random() * 100; // Family wealth affects initial attributes
        const mbti = this.generateMBTI();
        
        // Adjust initial attributes based on MBTI
        let intelligence = 30 + Math.random() * 40 + (familyWealth > 50 ? 10 : 0);
        let charm = 30 + Math.random() * 40 + (familyWealth > 60 ? 10 : 0);
        
        // MBTI adjustments
        if (mbti.dimensions.extraversion) charm += 5;
        if (!mbti.dimensions.sensing) intelligence += 5; // Intuitive types tend to be more abstract thinkers
        
        return {
            name: this.generateName(),
            age: 0,
            intelligence: Math.min(100, intelligence),
            charm: Math.min(100, charm),
            health: 50 + Math.random() * 30 + (familyWealth > 70 ? 10 : 0),
            luck: 20 + Math.random() * 60, // 20-80
            wealth: familyWealth,
            education: 0, // Education level
            career: null,
            relationship: null,
            family: {
                wealth: familyWealth,
                education: Math.random() * 100
            },
            mbti: mbti
        };
    }

    // Start new life
    startNewLife() {
        this.character = this.createCharacter();
        this.currentAge = 0;
        this.lifeEvents = [];
        this.isPaused = false;
        
        document.getElementById('start-screen').classList.remove('active');
        document.getElementById('game-screen').classList.add('active');
        document.getElementById('end-screen').classList.remove('active');
        
        this.updateDisplay();
        this.triggerEvent();
    }

    // Update display
    updateDisplay() {
        if (!this.character) return;

        document.getElementById('character-name').textContent = this.character.name;
        document.getElementById('current-age').textContent = this.currentAge;
        document.getElementById('mbti-type').textContent = this.character.mbti.type;

        // Update attribute bars
        this.updateAttribute('intelligence', this.character.intelligence);
        this.updateAttribute('charm', this.character.charm);
        this.updateAttribute('health', this.character.health);
        this.updateAttribute('luck', this.character.luck);
        this.updateAttribute('wealth', Math.min(this.character.wealth, 100));
    }

    updateAttribute(name, value) {
        const clampedValue = Math.max(0, Math.min(100, value));
        document.getElementById(`attr-${name}`).style.width = clampedValue + '%';
        document.getElementById(`val-${name}`).textContent = Math.round(clampedValue);
    }

    // Advance to next year
    advanceYear() {
        if (this.isPaused || !this.character) return;
        
        this.currentAge++;
        this.character.age = this.currentAge;

        // Natural attribute changes
        this.naturalAging();

        // Check if life ended
        if (this.currentAge >= this.maxAge || this.character.health <= 0) {
            this.endLife();
            return;
        }

        // Trigger event
        this.triggerEvent();
        this.updateDisplay();
    }

    // Natural aging
    naturalAging() {
        // Health decreases with age
        if (this.currentAge > 40) {
            this.character.health -= (this.currentAge - 40) * 0.5;
        }
        if (this.currentAge > 60) {
            this.character.health -= 1;
        }

        // Intelligence may increase (experience) or decrease (aging)
        if (this.currentAge < 30) {
            this.character.intelligence += Math.random() * 2;
        } else if (this.currentAge > 70) {
            this.character.intelligence -= Math.random() * 1;
        }
    }

    // Trigger event
    triggerEvent() {
        const ageGroup = this.getAgeGroup();
        const events = this.getEventsForAge(ageGroup);
        
        if (events.length === 0) return;

        const event = events[Math.floor(Math.random() * events.length)];
        this.currentEvent = event;
        this.displayEvent(event);
    }

    // Get age group
    getAgeGroup() {
        if (this.currentAge <= 12) return 'childhood';
        if (this.currentAge <= 18) return 'teenage';
        if (this.currentAge <= 30) return 'youngAdult';
        if (this.currentAge <= 50) return 'middleAge';
        return 'elderly';
    }

    // Get events for age group
    getEventsForAge(ageGroup) {
        const allEvents = {
            childhood: [
                {
                    title: 'First Day of Kindergarten',
                    description: 'Your first day away from home, entering kindergarten.',
                    choices: [
                        { text: 'Make friends actively', effect: { charm: 5, intelligence: 2 }, social: true },
                        { text: 'Observe quietly', effect: { intelligence: 5 }, logical: true },
                        { text: 'Cry and want to go home', effect: { health: -3 } }
                    ]
                },
                {
                    title: 'Discovering Interests',
                    description: 'You show special interest in a particular field.',
                    choices: [
                        { text: 'Learn music', effect: { charm: 8, intelligence: 3 }, creative: true },
                        { text: 'Learn art', effect: { charm: 5, intelligence: 5 }, creative: true },
                        { text: 'Learn sports', effect: { health: 10, charm: 3 } },
                        { text: 'Learn science', effect: { intelligence: 10 }, logical: true }
                    ]
                },
                {
                    title: 'Family Situation',
                    description: this.character.family.wealth > 50 
                        ? 'Your family is in good financial condition, providing you with a good growth environment.'
                        : 'Your family is facing some financial difficulties.',
                    choices: [
                        { text: 'Understand and study hard', effect: { intelligence: 5, wealth: this.character.family.wealth > 50 ? 5 : -5 }, structured: true },
                        { text: 'Help the family', effect: { charm: 3, wealth: -3 }, social: true }
                    ]
                }
            ],
            teenage: [
                {
                    title: 'Middle School Life',
                    description: 'You enter middle school, and academic pressure begins to increase.',
                    choices: [
                        { text: 'Study hard', effect: { intelligence: 8, education: 10, health: -2 }, structured: true },
                        { text: 'Balance study and fun', effect: { intelligence: 5, charm: 5, health: 2 } },
                        { text: 'Focus on socializing', effect: { charm: 8, intelligence: 2 }, social: true }
                    ]
                },
                {
                    title: 'Adolescent Troubles',
                    description: 'You start to care about your appearance and how others see you.',
                    choices: [
                        { text: 'Focus on inner growth', effect: { intelligence: 5, charm: 3 }, logical: true },
                        { text: 'Improve appearance', effect: { charm: 8, wealth: -5 }, social: true },
                        { text: 'Don\'t care', effect: { health: 3 } }
                    ]
                },
                {
                    title: 'College Entrance Exam',
                    description: 'An important exam that determines your future direction.',
                    choices: [
                        { text: 'Give it your all', effect: { intelligence: 10, education: 20, health: -5 }, structured: true },
                        { text: 'Perform normally', effect: { intelligence: 5, education: 10 } },
                        { text: 'Underperform', effect: { intelligence: -5, education: 5, health: -3 } }
                    ]
                }
            ],
            youngAdult: [
                {
                    title: 'College Choice',
                    description: 'You need to choose a major direction.',
                    choices: [
                        { text: 'Choose popular major', effect: { intelligence: 5, education: 15, wealth: 5 }, structured: true },
                        { text: 'Choose major of interest', effect: { intelligence: 8, education: 12, charm: 3 }, creative: true },
                        { text: 'Start working directly', effect: { wealth: 10, education: 5 } }
                    ]
                },
                {
                    title: 'First Job',
                    description: 'You found your first job in life.',
                    choices: [
                        { text: 'Choose high-paying job', effect: { wealth: 15, health: -3 }, structured: true },
                        { text: 'Choose job with growth potential', effect: { intelligence: 5, wealth: 8 }, logical: true },
                        { text: 'Choose easy job', effect: { health: 5, wealth: 5 } }
                    ]
                },
                {
                    title: 'Finding Love',
                    description: 'You meet someone special.',
                    choices: [
                        { text: 'Pursue bravely', effect: { charm: 10, health: 5 }, social: true },
                        { text: 'Stay friends', effect: { charm: 5 } },
                        { text: 'Focus on career', effect: { intelligence: 5, wealth: 5 }, structured: true }
                    ]
                },
                {
                    title: 'Entrepreneurship Opportunity',
                    description: 'You see an opportunity to start a business.',
                    choices: [
                        { text: 'Seize the opportunity', effect: { wealth: this.character.luck > 50 ? 30 : -10, intelligence: 5 }, creative: true },
                        { text: 'Continue stable job', effect: { wealth: 5, health: 3 }, structured: true },
                        { text: 'Observe more', effect: { intelligence: 3 }, logical: true }
                    ]
                }
            ],
            middleAge: [
                {
                    title: 'Career Development',
                    description: 'You face new choices on your career path.',
                    choices: [
                        { text: 'Pursue higher position', effect: { wealth: 15, health: -5, intelligence: 5 }, structured: true },
                        { text: 'Maintain status quo', effect: { health: 5, wealth: 5 } },
                        { text: 'Change career', effect: { wealth: -5, intelligence: 8, charm: 5 }, creative: true }
                    ]
                },
                {
                    title: 'Family Responsibilities',
                    description: 'You need to balance work and family.',
                    choices: [
                        { text: 'Prioritize work', effect: { wealth: 10, health: -5, charm: -3 }, structured: true },
                        { text: 'Balance both', effect: { health: 3, wealth: 5, charm: 5 } },
                        { text: 'Prioritize family', effect: { health: 8, charm: 10, wealth: -5 }, social: true }
                    ]
                },
                {
                    title: 'Health Warning',
                    description: 'Your body starts showing some health problems.',
                    choices: [
                        { text: 'Actively treat and exercise', effect: { health: 15, wealth: -10 }, structured: true },
                        { text: 'Take rest', effect: { health: 5, wealth: -3 } },
                        { text: 'Ignore the problem', effect: { health: -10 } }
                    ]
                }
            ],
            elderly: [
                {
                    title: 'Retirement Life',
                    description: 'You retire and begin to enjoy your later years.',
                    choices: [
                        { text: 'Cultivate new hobbies', effect: { charm: 5, health: 5 }, creative: true },
                        { text: 'Spend time with family', effect: { health: 8, charm: 8 }, social: true },
                        { text: 'Continue working', effect: { wealth: 10, health: -3 }, structured: true }
                    ]
                },
                {
                    title: 'Life Reflection',
                    description: 'You begin to reflect on your life.',
                    choices: [
                        { text: 'Feel satisfied', effect: { health: 5, charm: 5 } },
                        { text: 'Have some regrets', effect: { health: -3 } },
                        { text: 'Cherish the present', effect: { health: 8 } }
                    ]
                }
            ]
        };

        return allEvents[ageGroup] || [];
    }

    // Display event
    displayEvent(event) {
        document.getElementById('event-title').textContent = event.title;
        document.getElementById('event-description').textContent = event.description;

        const choicesContainer = document.getElementById('event-choices');
        choicesContainer.innerHTML = '';

        event.choices.forEach((choice, index) => {
            const button = document.createElement('button');
            button.className = 'choice-btn';
            button.textContent = choice.text;
            
            // Apply MBTI modifier to choice effects
            const modifiedChoice = { ...choice };
            if (this.character && this.character.mbti) {
                const modifier = this.getMBTIModifier(choice, this.character.mbti);
                const modifiedEffect = {};
                Object.keys(choice.effect).forEach(attr => {
                    modifiedEffect[attr] = Math.round(choice.effect[attr] * modifier);
                });
                modifiedChoice.effect = modifiedEffect;
            }
            
            button.addEventListener('click', () => this.makeChoice(modifiedChoice));
            choicesContainer.appendChild(button);
        });
    }

    // Make choice
    makeChoice(choice) {
        // Apply choice effects
        Object.keys(choice.effect).forEach(attr => {
            if (this.character[attr] !== undefined) {
                this.character[attr] += choice.effect[attr];
                this.character[attr] = Math.max(0, Math.min(100, this.character[attr]));
            }
        });

        // Record event
        this.lifeEvents.push({
            age: this.currentAge,
            event: this.currentEvent.title,
            choice: choice.text
        });

        this.addTimelineItem(this.currentAge, this.currentEvent.title, choice.text);
        this.updateDisplay();

        // Clear current event
        this.currentEvent = null;
        document.getElementById('event-title').textContent = 'Waiting for next year...';
        document.getElementById('event-description').textContent = 'Click "Next Year" to continue your life.';
        document.getElementById('event-choices').innerHTML = '';
    }

    // Add timeline item
    addTimelineItem(age, event, choice) {
        const timeline = document.getElementById('timeline');
        const item = document.createElement('div');
        item.className = 'timeline-item';
        item.innerHTML = `<span class="timeline-age">Age ${age}:</span> ${event} - You chose: ${choice}`;
        timeline.appendChild(item);
        timeline.scrollTop = timeline.scrollHeight;
    }

    // Toggle pause
    togglePause() {
        this.isPaused = !this.isPaused;
        document.getElementById('pause-btn').textContent = this.isPaused ? 'Resume' : 'Pause';
    }

    // End life
    endLife() {
        document.getElementById('game-screen').classList.remove('active');
        document.getElementById('end-screen').classList.add('active');

        const summary = this.generateLifeSummary();
        document.getElementById('life-summary').innerHTML = summary;
    }

    // Generate life summary
    generateLifeSummary() {
        const finalWealth = Math.round(this.character.wealth);
        const finalIntelligence = Math.round(this.character.intelligence);
        const finalCharm = Math.round(this.character.charm);
        const finalHealth = Math.round(this.character.health);

        let summary = `
            <div class="summary-item">
                <strong>Name:</strong> ${this.character.name}
            </div>
            <div class="summary-item">
                <strong>Age at Death:</strong> ${this.currentAge} years old
            </div>
            <div class="summary-item">
                <strong>MBTI Type:</strong> ${this.character.mbti.type} - ${this.character.mbti.description}
            </div>
            <div class="summary-item">
                <strong>Final Attributes:</strong><br>
                Intelligence: ${finalIntelligence} | Charm: ${finalCharm} | Health: ${finalHealth} | Wealth: ${finalWealth}
            </div>
            <div class="summary-item">
                <strong>Life Events:</strong><br>
                ${this.lifeEvents.slice(0, 10).map(e => `Age ${e.age}: ${e.event}`).join('<br>')}
            </div>
        `;

        // Evaluation
        let evaluation = '';
        if (finalWealth > 80 && finalIntelligence > 70) {
            evaluation = 'You lived a successful and wealthy life!';
        } else if (finalHealth > 80 && finalCharm > 70) {
            evaluation = 'You lived a healthy and happy life!';
        } else if (finalIntelligence > 80) {
            evaluation = 'You lived a wise and intellectual life!';
        } else if (this.currentAge > 80) {
            evaluation = 'You lived a long life!';
        } else {
            evaluation = 'You lived an ordinary but authentic life.';
        }

        summary += `<div class="summary-item"><strong>Life Evaluation:</strong> ${evaluation}</div>`;

        return summary;
    }

    // Restart
    restart() {
        document.getElementById('start-screen').classList.add('active');
        document.getElementById('game-screen').classList.remove('active');
        document.getElementById('end-screen').classList.remove('active');
        document.getElementById('timeline').innerHTML = '';
    }
}

// Initialize game
let game;
window.addEventListener('DOMContentLoaded', () => {
    game = new LifeSimulator();
});
