// World/Era Module - Manages global world state (Economy, Technology, War, Institutions)
class WorldEraModule {
    constructor() {
        this.currentEra = null;
        this.worldState = {
            economy: 50,      // 0-100: Economic prosperity
            technology: 50,  // 0-100: Technological advancement
            war: 0,          // 0-100: War intensity
            institutions: 50 // 0-100: Institutional stability
        };
        this.eraHistory = [];
        this.init();
    }

    init() {
        this.generateStartingEra();
    }

    // Generate starting era based on birth year
    generateStartingEra() {
        const eras = [
            {
                name: 'Post-War Era',
                startYear: 1950,
                endYear: 1970,
                economy: 40,
                technology: 30,
                war: 10,
                institutions: 60,
                description: 'A period of reconstruction and growth'
            },
            {
                name: 'Modern Era',
                startYear: 1970,
                endYear: 1990,
                economy: 60,
                technology: 50,
                war: 5,
                institutions: 70,
                description: 'Technological advancement and economic expansion'
            },
            {
                name: 'Information Age',
                startYear: 1990,
                endYear: 2010,
                economy: 70,
                technology: 75,
                war: 15,
                institutions: 65,
                description: 'Digital revolution and globalization'
            },
            {
                name: 'Contemporary Era',
                startYear: 2010,
                endYear: 2030,
                economy: 65,
                technology: 85,
                war: 20,
                institutions: 60,
                description: 'AI, climate change, and social transformation'
            },
            {
                name: 'Future Era',
                startYear: 2030,
                endYear: 2050,
                economy: 75,
                technology: 95,
                war: 25,
                institutions: 55,
                description: 'Advanced technology and new challenges'
            }
        ];

        // Randomly select starting era
        this.currentEra = eras[Math.floor(Math.random() * eras.length)];
        this.worldState = {
            economy: this.currentEra.economy + (Math.random() * 20 - 10),
            technology: this.currentEra.technology + (Math.random() * 20 - 10),
            war: this.currentEra.war + (Math.random() * 10),
            institutions: this.currentEra.institutions + (Math.random() * 20 - 10)
        };

        // Clamp values
        Object.keys(this.worldState).forEach(key => {
            this.worldState[key] = Math.max(0, Math.min(100, this.worldState[key]));
        });
    }

    // Update world state based on age and random events
    updateWorldState(age) {
        // Economic cycles
        this.worldState.economy += (Math.random() * 4 - 2);
        
        // Technology generally increases over time
        if (Math.random() > 0.3) {
            this.worldState.technology += Math.random() * 2;
        }
        
        // War can break out or end
        if (Math.random() > 0.9) {
            this.worldState.war += Math.random() * 20 - 10;
        } else if (this.worldState.war > 0) {
            this.worldState.war -= Math.random() * 2;
        }
        
        // Institutions fluctuate
        this.worldState.institutions += (Math.random() * 3 - 1.5);

        // Clamp values
        Object.keys(this.worldState).forEach(key => {
            this.worldState[key] = Math.max(0, Math.min(100, this.worldState[key]));
        });

        // Check for era transitions
        this.checkEraTransition(age);
    }

    // Check if era should transition
    checkEraTransition(age) {
        const currentYear = this.currentEra.startYear + age;
        if (currentYear >= this.currentEra.endYear) {
            this.transitionToNewEra(age);
        }
    }

    // Transition to new era
    transitionToNewEra(age) {
        const nextEras = {
            'Post-War Era': { name: 'Modern Era', economy: 60, technology: 50, war: 5, institutions: 70 },
            'Modern Era': { name: 'Information Age', economy: 70, technology: 75, war: 15, institutions: 65 },
            'Information Age': { name: 'Contemporary Era', economy: 65, technology: 85, war: 20, institutions: 60 },
            'Contemporary Era': { name: 'Future Era', economy: 75, technology: 95, war: 25, institutions: 55 },
            'Future Era': { name: 'Future Era', economy: 80, technology: 100, war: 30, institutions: 50 }
        };

        const nextEra = nextEras[this.currentEra.name] || nextEras['Future Era'];
        this.eraHistory.push({
            era: this.currentEra.name,
            endAge: age
        });
        
        this.currentEra = {
            ...this.currentEra,
            name: nextEra.name,
            startYear: this.currentEra.endYear,
            endYear: this.currentEra.endYear + 20
        };

        // Gradually transition world state
        this.worldState.economy = (this.worldState.economy + nextEra.economy) / 2;
        this.worldState.technology = (this.worldState.technology + nextEra.technology) / 2;
        this.worldState.war = (this.worldState.war + nextEra.war) / 2;
        this.worldState.institutions = (this.worldState.institutions + nextEra.institutions) / 2;
    }

    // Get world state modifier for events
    getWorldModifier(eventType) {
        let modifier = 1.0;
        
        switch(eventType) {
            case 'economic':
                modifier = 0.5 + (this.worldState.economy / 100);
                break;
            case 'technological':
                modifier = 0.5 + (this.worldState.technology / 100);
                break;
            case 'war':
                modifier = 1.0 + (this.worldState.war / 100);
                break;
            case 'education':
                modifier = 0.7 + (this.worldState.institutions / 100);
                break;
            case 'career':
                modifier = 0.6 + (this.worldState.economy / 100);
                break;
            default:
                modifier = 1.0;
        }
        
        return modifier;
    }

    // Get world events based on current state
    getWorldEvents() {
        const events = [];
        
        if (this.worldState.war > 50) {
            events.push({
                type: 'war',
                severity: this.worldState.war,
                description: 'Major conflict affects daily life'
            });
        }
        
        if (this.worldState.economy < 30) {
            events.push({
                type: 'recession',
                severity: 100 - this.worldState.economy,
                description: 'Economic downturn impacts opportunities'
            });
        } else if (this.worldState.economy > 70) {
            events.push({
                type: 'prosperity',
                severity: this.worldState.economy,
                description: 'Economic boom creates opportunities'
            });
        }
        
        if (this.worldState.technology > 80) {
            events.push({
                type: 'tech_boom',
                severity: this.worldState.technology,
                description: 'Rapid technological advancement'
            });
        }
        
        return events;
    }

    // Get era description
    getEraDescription() {
        return {
            name: this.currentEra.name,
            description: this.currentEra.description,
            state: { ...this.worldState }
        };
    }
}

