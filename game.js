// Core game system - Integrates all modules
class LifeSimulator {
    constructor() {
        this.character = null;
        this.currentAge = 0;
        this.maxAge = 100;
        this.lifeEvents = [];
        this.isPaused = false;
        this.currentEvent = null;
        
        // Initialize modules
        this.worldEra = new WorldEraModule();
        this.lifeState = new LifeStateEngine();
        this.behaviorChoice = new BehaviorChoiceModule();
        this.narrative = new NarrativeGenerationModule();
        
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
        const extraversion = Math.random() > 0.5 ? 'E' : 'I';
        const sensing = Math.random() > 0.5 ? 'S' : 'N';
        const thinking = Math.random() > 0.5 ? 'T' : 'F';
        const judging = Math.random() > 0.5 ? 'J' : 'P';
        
        const mbtiType = extraversion + sensing + thinking + judging;
        
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

    // Create new character
    createCharacter() {
        const familyWealth = Math.random() * 100;
        const mbti = this.generateMBTI();
        
        let intelligence = 30 + Math.random() * 40 + (familyWealth > 50 ? 10 : 0);
        let charm = 30 + Math.random() * 40 + (familyWealth > 60 ? 10 : 0);
        
        if (mbti.dimensions.extraversion) charm += 5;
        if (!mbti.dimensions.sensing) intelligence += 5;
        
        return {
            name: this.generateName(),
            age: 0,
            intelligence: Math.min(100, intelligence),
            charm: Math.min(100, charm),
            health: 50 + Math.random() * 30 + (familyWealth > 70 ? 10 : 0),
            luck: 20 + Math.random() * 60,
            wealth: familyWealth,
            mbti: mbti,
            family: {
                wealth: familyWealth,
                education: Math.random() * 100
            }
        };
    }

    // Start new life
    startNewLife() {
        this.character = this.createCharacter();
        this.currentAge = 0;
        this.lifeEvents = [];
        this.isPaused = false;
        
        // Reset modules
        this.worldEra = new WorldEraModule();
        this.lifeState = new LifeStateEngine();
        this.behaviorChoice = new BehaviorChoiceModule();
        this.narrative = new NarrativeGenerationModule();
        
        document.getElementById('start-screen').classList.remove('active');
        document.getElementById('game-screen').classList.add('active');
        document.getElementById('end-screen').classList.remove('active');
        
        this.updateDisplay();
        this.triggerEvent();
    }

    // Update display
    updateDisplay() {
        if (!this.character) return;

        // Character info
        document.getElementById('character-name').textContent = this.character.name;
        document.getElementById('current-age').textContent = this.currentAge;
        document.getElementById('mbti-type').textContent = this.character.mbti.type;

        // Attributes
        this.updateAttribute('intelligence', this.character.intelligence);
        this.updateAttribute('charm', this.character.charm);
        this.updateAttribute('health', this.character.health);
        this.updateAttribute('luck', this.character.luck);
        this.updateAttribute('wealth', Math.min(this.character.wealth, 100));

        // World/Era info
        const eraInfo = this.worldEra.getEraDescription();
        document.getElementById('era-name').textContent = eraInfo.name;
        document.getElementById('world-economy').textContent = Math.round(eraInfo.state.economy);
        document.getElementById('world-tech').textContent = Math.round(eraInfo.state.technology);

        // Life states
        const state = this.lifeState.getStateSummary();
        document.getElementById('state-education').textContent = Math.round(state.individual.education);
        document.getElementById('state-career').textContent = Math.round(state.individual.careerLevel);
        document.getElementById('state-reputation').textContent = Math.round(state.social.reputation);
        
        let relationshipStatus = state.relationship.romantic.status;
        if (state.relationship.children.count > 0) {
            relationshipStatus += `, ${state.relationship.children.count} child(ren)`;
        }
        document.getElementById('state-relationship').textContent = relationshipStatus;
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

        // Update world state
        this.worldEra.updateWorldState(this.currentAge);

        // Natural aging
        this.naturalAging();

        // Update life states
        this.lifeState.updateIndividualState(this.character, this.currentAge);
        this.lifeState.updateSocialState(this.character, { social: false }, this.worldEra.worldState);
        this.lifeState.updateRelationshipState(this.currentAge, { social: false, romantic: false }, this.character);

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
        if (this.currentAge > 40) {
            this.character.health -= (this.currentAge - 40) * 0.5;
        }
        if (this.currentAge > 60) {
            this.character.health -= 1;
        }

        if (this.currentAge < 30) {
            this.character.intelligence += Math.random() * 2;
        } else if (this.currentAge > 70) {
            this.character.intelligence -= Math.random() * 1;
        }
    }

    // Trigger event
    triggerEvent() {
        // Get age-based events
        const ageGroup = this.getAgeGroup();
        const ageEvents = this.getEventsForAge(ageGroup);
        
        // Get behavior choices
        const context = {
            age: this.currentAge,
            state: this.lifeState.getStateSummary(),
            worldState: this.worldEra.worldState,
            mbti: this.character.mbti,
            attributes: this.character
        };
        const behaviorChoices = this.behaviorChoice.generateBehaviorChoices(context);
        
        // Combine and select event
        const allEvents = [...ageEvents];
        if (allEvents.length === 0) return;

        const event = allEvents[Math.floor(Math.random() * allEvents.length)];
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

    // Get events for age group (keeping original events)
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

        event.choices.forEach((choice) => {
            const button = document.createElement('button');
            button.className = 'choice-btn';
            button.textContent = choice.text;
            
            // Apply MBTI modifier
            const mbtiModifier = this.getMBTIModifier(choice, this.character.mbti);
            const worldModifier = this.worldEra.getWorldModifier(this.getEventType(choice));
            
            const modifiedChoice = { ...choice };
            const modifiedEffect = {};
            Object.keys(choice.effect).forEach(attr => {
                let value = choice.effect[attr];
                value *= mbtiModifier;
                if (attr === 'wealth' || attr === 'education') {
                    value *= worldModifier;
                }
                modifiedEffect[attr] = value;
            });
            modifiedChoice.effect = modifiedEffect;
            
            button.addEventListener('click', () => this.makeChoice(modifiedChoice));
            choicesContainer.appendChild(button);
        });
    }

    // Get MBTI modifier
    getMBTIModifier(choice, mbti) {
        let modifier = 1.0;
        if (choice.social) modifier *= mbti.dimensions.extraversion ? 1.2 : 0.9;
        if (choice.creative) modifier *= mbti.dimensions.sensing ? 0.9 : 1.2;
        if (choice.logical) modifier *= mbti.dimensions.thinking ? 1.2 : 0.9;
        if (choice.structured) modifier *= mbti.dimensions.judging ? 1.2 : 0.9;
        return modifier;
    }

    // Get event type for world modifier
    getEventType(choice) {
        if (choice.effect.education) return 'education';
        if (choice.effect.wealth) return 'economic';
        if (choice.effect.careerLevel) return 'career';
        return 'general';
    }

    // Make choice
    makeChoice(choice) {
        // Apply choice effects to character attributes
        Object.keys(choice.effect).forEach(attr => {
            if (this.character[attr] !== undefined) {
                this.character[attr] += choice.effect[attr];
                this.character[attr] = Math.max(0, Math.min(100, this.character[attr]));
            }
        });

        // Apply effects to life state
        this.lifeState.applyChoiceEffects(choice, this.character);

        // Record event
        this.lifeEvents.push({
            age: this.currentAge,
            event: this.currentEvent.title,
            choice: choice.text,
            type: choice.type || 'general'
        });

        // Record behavior
        if (choice.type) {
            this.behaviorChoice.recordBehavior(choice, this.currentAge);
        }

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

    // Generate life summary using narrative module
    generateLifeSummary() {
        const state = this.lifeState.getStateSummary();
        const summary = this.narrative.generateLifeSummary(
            this.character,
            state,
            { ...this.character, age: this.currentAge },
            this.lifeEvents,
            this.worldEra
        );

        let html = `
            <div class="summary-item">
                <strong>Name:</strong> ${summary.overview.name}
            </div>
            <div class="summary-item">
                <strong>Age at Death:</strong> ${summary.overview.age} years old
            </div>
            <div class="summary-item">
                <strong>MBTI Type:</strong> ${summary.overview.mbti} - ${this.character.mbti.description}
            </div>
            <div class="summary-item">
                <strong>Final Attributes:</strong><br>
                Intelligence: ${summary.overview.attributes.intelligence} | 
                Charm: ${summary.overview.attributes.charm} | 
                Health: ${summary.overview.attributes.health} | 
                Wealth: ${summary.overview.attributes.wealth}
            </div>
            <div class="summary-item">
                <strong>Era:</strong> ${summary.eraContext.primaryEra} - ${summary.eraContext.description}
            </div>
        `;

        if (summary.achievements.length > 0) {
            html += `
                <div class="summary-item">
                    <strong>Achievements:</strong><br>
                    ${summary.achievements.join(', ')}
                </div>
            `;
        }

        if (summary.keyMoments.length > 0) {
            html += `
                <div class="summary-item">
                    <strong>Key Life Moments:</strong><br>
                    ${summary.keyMoments.map(m => `Age ${m.age}: ${m.title}`).join('<br>')}
                </div>
            `;
        }

        html += `
            <div class="summary-item">
                <strong>Relationships:</strong><br>
                Romantic: ${summary.relationships.romantic.status} (Quality: ${summary.relationships.romantic.quality})<br>
                Children: ${summary.relationships.children.count}<br>
                Friends: ${summary.relationships.friendships.count} (Quality: ${summary.relationships.friendships.quality})
            </div>
            <div class="summary-item">
                <strong>Legacy:</strong><br>
                ${summary.legacy.join('<br>')}
            </div>
            <div class="summary-item">
                <strong>Life Evaluation:</strong> ${summary.overview.evaluation}
            </div>
        `;

        return html;
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

