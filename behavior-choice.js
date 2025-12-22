// Behavior Choice Module - Manages learning, work, adventure, and other behaviors
class BehaviorChoiceModule {
    constructor() {
        this.behaviorCategories = {
            learning: ['Study', 'Research', 'Practice', 'Read', 'Attend classes'],
            work: ['Work hard', 'Network', 'Take on projects', 'Seek promotion', 'Change jobs'],
            adventure: ['Travel', 'Explore', 'Take risks', 'Try new things', 'Challenge yourself'],
            social: ['Socialize', 'Build relationships', 'Help others', 'Join groups', 'Attend events'],
            creative: ['Create art', 'Write', 'Innovate', 'Design', 'Express yourself'],
            health: ['Exercise', 'Eat well', 'Rest', 'Meditate', 'Seek treatment'],
            family: ['Spend time with family', 'Support family', 'Create traditions', 'Celebrate'],
            romantic: ['Date', 'Commit', 'Communicate', 'Show affection', 'Plan future']
        };
        
        this.behaviorHistory = [];
    }

    // Generate behavior choices based on context
    generateBehaviorChoices(context) {
        const { age, state, worldState, mbti } = context;
        const choices = [];
        
        // Learning behaviors
        if (age < 30 || state.individualState.education < 80) {
            choices.push({
                type: 'learning',
                text: 'Focus on learning and education',
                effect: { intelligence: 5, education: 10 },
                requirements: { age: [0, 50] },
                mbtiBonus: { N: 1.2, T: 1.1 }
            });
        }
        
        // Work behaviors
        if (age >= 18) {
            choices.push({
                type: 'work',
                text: 'Dedicate yourself to work',
                effect: { wealth: 8, careerLevel: 5, health: -2 },
                requirements: { age: [18, 70] },
                mbtiBonus: { J: 1.2, T: 1.1 }
            });
            
            choices.push({
                type: 'work',
                text: 'Balance work and life',
                effect: { wealth: 4, health: 3, lifeSatisfaction: 5 },
                requirements: { age: [18, 70] },
                mbtiBonus: { P: 1.1, F: 1.1 }
            });
        }
        
        // Adventure behaviors
        if (age < 60 && state.individualState.healthStatus !== 'poor') {
            choices.push({
                type: 'adventure',
                text: 'Go on an adventure',
                effect: { charm: 5, health: 3, wealth: -5, lifeSatisfaction: 8 },
                requirements: { health: 40 },
                mbtiBonus: { P: 1.2, E: 1.1 }
            });
        }
        
        // Social behaviors
        choices.push({
            type: 'social',
            text: 'Build social connections',
            effect: { charm: 6, network: 3, reputation: 4 },
            requirements: {},
            mbtiBonus: { E: 1.3, F: 1.1 }
        });
        
        // Creative behaviors
        choices.push({
            type: 'creative',
            text: 'Engage in creative activities',
            effect: { charm: 4, intelligence: 3, lifeSatisfaction: 5 },
            requirements: {},
            mbtiBonus: { N: 1.2, F: 1.1 }
        });
        
        // Health behaviors
        if (state.individualState.healthStatus !== 'good') {
            choices.push({
                type: 'health',
                text: 'Focus on health and wellness',
                effect: { health: 10, wealth: -5 },
                requirements: {},
                mbtiBonus: { J: 1.1 }
            });
        }
        
        // Family behaviors
        if (state.relationshipState.family.parents === 'alive' || state.relationshipState.children.count > 0) {
            choices.push({
                type: 'family',
                text: 'Spend quality time with family',
                effect: { familyRelationship: 5, lifeSatisfaction: 6, health: 2 },
                requirements: {},
                mbtiBonus: { F: 1.2 }
            });
        }
        
        // Romantic behaviors
        if (age >= 18 && state.relationshipState.romantic.status !== 'married') {
            choices.push({
                type: 'romantic',
                text: 'Focus on romantic relationships',
                effect: { charm: 5, romanticQuality: 8 },
                requirements: { age: [18, 50] },
                mbtiBonus: { F: 1.2, E: 1.1 }
            });
        }
        
        // Filter choices based on requirements
        return choices.filter(choice => this.checkRequirements(choice, context));
    }

    // Check if choice requirements are met
    checkRequirements(choice, context) {
        const { age, state, attributes } = context;
        
        if (choice.requirements.age) {
            const [min, max] = choice.requirements.age;
            if (age < min || age > max) return false;
        }
        
        if (choice.requirements.health && attributes.health < choice.requirements.health) {
            return false;
        }
        
        if (choice.requirements.wealth && attributes.wealth < choice.requirements.wealth) {
            return false;
        }
        
        return true;
    }

    // Apply MBTI bonuses to choice effects
    applyMBTIBonus(choice, mbti) {
        const bonus = choice.mbtiBonus || {};
        let modifier = 1.0;
        
        if (bonus.E && mbti.dimensions.extraversion) modifier *= bonus.E;
        if (bonus.I && !mbti.dimensions.extraversion) modifier *= bonus.I;
        if (bonus.S && mbti.dimensions.sensing) modifier *= bonus.S;
        if (bonus.N && !mbti.dimensions.sensing) modifier *= bonus.N;
        if (bonus.T && mbti.dimensions.thinking) modifier *= bonus.T;
        if (bonus.F && !mbti.dimensions.thinking) modifier *= bonus.F;
        if (bonus.J && mbti.dimensions.judging) modifier *= bonus.J;
        if (bonus.P && !mbti.dimensions.judging) modifier *= bonus.P;
        
        // Apply modifier to effects
        const modifiedEffect = {};
        Object.keys(choice.effect).forEach(key => {
            modifiedEffect[key] = choice.effect[key] * modifier;
        });
        
        return { ...choice, effect: modifiedEffect };
    }

    // Record behavior choice
    recordBehavior(choice, age) {
        this.behaviorHistory.push({
            age,
            type: choice.type,
            text: choice.text
        });
    }

    // Get behavior statistics
    getBehaviorStats() {
        const stats = {};
        Object.keys(this.behaviorCategories).forEach(category => {
            stats[category] = this.behaviorHistory.filter(b => b.type === category).length;
        });
        return stats;
    }
}

