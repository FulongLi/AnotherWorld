// Life State Engine - Manages individual, social, and relationship states
class LifeStateEngine {
    constructor() {
        this.individualState = {
            education: 0,        // 0-100: Education level
            career: null,         // Current career
            careerLevel: 0,       // 0-100: Career advancement
            skills: {},          // Skill set
            healthStatus: 'good', // good, fair, poor, critical
            mentalHealth: 50,     // 0-100: Mental well-being
            lifeSatisfaction: 50  // 0-100: Overall satisfaction
        };
        
        this.socialState = {
            reputation: 50,       // 0-100: Social reputation
            network: 0,           // Number of connections
            socialStatus: 'average', // low, average, high, elite
            community: 'local',   // local, regional, national, global
            influence: 0          // 0-100: Social influence
        };
        
        this.relationshipState = {
            family: {
                parents: 'alive',    // alive, distant, deceased
                siblings: 0,         // Number of siblings
                relationship: 50     // 0-100: Family relationship quality
            },
            romantic: {
                status: 'single',    // single, dating, engaged, married, divorced, widowed
                partner: null,
                quality: 0           // 0-100: Relationship quality
            },
            friendships: {
                count: 0,           // Number of close friends
                quality: 50,        // 0-100: Average friendship quality
                bestFriend: null
            },
            children: {
                count: 0,
                relationship: 0     // 0-100: Relationship with children
            }
        };
        
        this.milestones = [];
    }

    // Update individual state
    updateIndividualState(attributes, age) {
        // Update education based on age and choices
        if (age < 25 && this.individualState.education < 100) {
            // Natural education progression
            this.individualState.education += Math.random() * 2;
        }
        
        // Update health status based on health attribute
        if (attributes.health > 70) {
            this.individualState.healthStatus = 'good';
        } else if (attributes.health > 40) {
            this.individualState.healthStatus = 'fair';
        } else if (attributes.health > 20) {
            this.individualState.healthStatus = 'poor';
        } else {
            this.individualState.healthStatus = 'critical';
        }
        
        // Update mental health based on various factors
        const baseMentalHealth = (attributes.charm + attributes.intelligence) / 2;
        const socialFactor = this.socialState.reputation / 2;
        const relationshipFactor = this.relationshipState.romantic.quality / 2;
        this.individualState.mentalHealth = Math.min(100, (baseMentalHealth + socialFactor + relationshipFactor) / 2);
        
        // Update life satisfaction
        const satisfactionFactors = [
            attributes.wealth / 2,
            this.individualState.careerLevel,
            this.relationshipState.romantic.quality,
            this.socialState.reputation / 2
        ];
        this.individualState.lifeSatisfaction = satisfactionFactors.reduce((a, b) => a + b, 0) / satisfactionFactors.length;
    }

    // Update social state
    updateSocialState(attributes, choices, worldState) {
        // Reputation based on charm and actions
        this.socialState.reputation += (attributes.charm - 50) * 0.1;
        
        // Network grows with social choices
        if (choices.social) {
            this.socialState.network += Math.random() * 2;
        }
        
        // Social status based on wealth and reputation
        const statusScore = (attributes.wealth + this.socialState.reputation) / 2;
        if (statusScore > 80) {
            this.socialState.socialStatus = 'elite';
        } else if (statusScore > 60) {
            this.socialState.socialStatus = 'high';
        } else if (statusScore > 40) {
            this.socialState.socialStatus = 'average';
        } else {
            this.socialState.socialStatus = 'low';
        }
        
        // Influence based on career, reputation, and network
        this.socialState.influence = (
            this.individualState.careerLevel * 0.4 +
            this.socialState.reputation * 0.3 +
            Math.min(this.socialState.network / 10, 30)
        );
    }

    // Update relationship state
    updateRelationshipState(age, choices, attributes) {
        // Family relationships
        if (age > 30 && Math.random() > 0.95) {
            // Parents may pass away
            if (this.relationshipState.family.parents === 'alive') {
                this.relationshipState.family.parents = 'deceased';
                this.addMilestone('Lost a parent', age);
            }
        }
        
        // Romantic relationships
        if (age >= 18 && this.relationshipState.romantic.status === 'single') {
            // Chance to meet someone
            if (Math.random() > 0.7 && attributes.charm > 40) {
                this.relationshipState.romantic.status = 'dating';
                this.relationshipState.romantic.quality = 50 + Math.random() * 30;
                this.addMilestone('Started dating', age);
            }
        }
        
        if (this.relationshipState.romantic.status === 'dating' && age >= 22) {
            // Chance to get married
            if (Math.random() > 0.6 && this.relationshipState.romantic.quality > 60) {
                this.relationshipState.romantic.status = 'married';
                this.addMilestone('Got married', age);
            }
        }
        
        if (this.relationshipState.romantic.status === 'married' && age >= 25 && age <= 40) {
            // Chance to have children
            if (this.relationshipState.children.count === 0 && Math.random() > 0.8) {
                this.relationshipState.children.count = 1;
                this.addMilestone('Had first child', age);
            } else if (this.relationshipState.children.count > 0 && this.relationshipState.children.count < 3 && Math.random() > 0.85) {
                this.relationshipState.children.count++;
                this.addMilestone(`Had ${this.relationshipState.children.count === 2 ? 'second' : 'third'} child`, age);
            }
        }
        
        // Maintain relationship quality
        if (this.relationshipState.romantic.status !== 'single') {
            if (choices.social && choices.romantic) {
                this.relationshipState.romantic.quality += Math.random() * 2;
            } else {
                this.relationshipState.romantic.quality -= Math.random() * 1;
            }
            this.relationshipState.romantic.quality = Math.max(0, Math.min(100, this.relationshipState.romantic.quality));
        }
        
        // Friendships
        if (choices.social) {
            this.relationshipState.friendships.count += Math.random() * 0.5;
            this.relationshipState.friendships.quality += Math.random() * 1;
        }
        this.relationshipState.friendships.quality = Math.max(0, Math.min(100, this.relationshipState.friendships.quality));
    }

    // Add milestone
    addMilestone(milestone, age) {
        this.milestones.push({ milestone, age });
    }

    // Get state summary
    getStateSummary() {
        return {
            individual: { ...this.individualState },
            social: { ...this.socialState },
            relationship: { ...this.relationshipState },
            milestones: [...this.milestones]
        };
    }

    // Apply choice effects to states
    applyChoiceEffects(choice, attributes) {
        // Update career if choice affects it
        if (choice.career) {
            this.individualState.careerLevel += choice.effect.careerLevel || 0;
            this.individualState.careerLevel = Math.max(0, Math.min(100, this.individualState.careerLevel));
        }
        
        // Update education
        if (choice.effect.education) {
            this.individualState.education += choice.effect.education;
            this.individualState.education = Math.max(0, Math.min(100, this.individualState.education));
        }
    }
}

